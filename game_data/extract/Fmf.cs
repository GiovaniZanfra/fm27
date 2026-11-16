// Reader for Football Manager 27 .fmf containers and the .jsb binary trees inside them.
// Compiled at runtime by fmf.ps1 (C# 5, .NET Framework) and calls libzstd.dll.
//
// .fmf layout:   "\x02\x01fmf." header (26 bytes), then one zstd frame per file;
//                the last frame is the index: folder name, then per file
//                name, extension, u64 offset (from byte 26), u64 compressed size,
//                u64 uncompressed size, u64 time, u64 time.
// .jsb layout:   tagged tree. Every value starts with one tag byte:
//                low nibble = type, high nibble = inline size/value (0 = a u32 follows).
//                0x0 null
//                0x1 bool    (high nibble 1 = true)
//                0x2 int     (inline: nibble - 8, else int32)
//                0x4 uint32, 0x5 uint64 (role bitmasks)
//                0x7 double  (inline: (nibble - 1) * 0.5, else 8 bytes). Inline values seen: 0, 0.5, 1;
//                checked against weight groups that must sum to 1.
//                0x8 string  (inline length: nibble - 1, else u32 length)
//                0x9 array   (inline count: nibble - 1, else u32 count)
//                0xA object  (same count rule; each member = u8 key length, key, value)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

public static class Fmf
{
    [StructLayout(LayoutKind.Sequential)] struct InBuf { public IntPtr src; public UIntPtr size; public UIntPtr pos; }
    [StructLayout(LayoutKind.Sequential)] struct OutBuf { public IntPtr dst; public UIntPtr size; public UIntPtr pos; }
    [DllImport("libzstd.dll", CallingConvention = CallingConvention.Cdecl)] static extern IntPtr ZSTD_createDStream();
    [DllImport("libzstd.dll", CallingConvention = CallingConvention.Cdecl)] static extern UIntPtr ZSTD_freeDStream(IntPtr d);
    [DllImport("libzstd.dll", CallingConvention = CallingConvention.Cdecl)] static extern UIntPtr ZSTD_initDStream(IntPtr d);
    [DllImport("libzstd.dll", CallingConvention = CallingConvention.Cdecl)] static extern UIntPtr ZSTD_decompressStream(IntPtr d, ref OutBuf o, ref InBuf i);
    [DllImport("libzstd.dll", CallingConvention = CallingConvention.Cdecl)] static extern UIntPtr ZSTD_findFrameCompressedSize(IntPtr src, UIntPtr size);
    [DllImport("libzstd.dll", CallingConvention = CallingConvention.Cdecl)] static extern uint ZSTD_isError(UIntPtr c);

    const int DataStart = 26;
    const uint Magic = 0xFD2FB528;

    public class Entry
    {
        public string Folder, Name, Ext;
        public long Offset, Compressed, Size;
        public string FileName { get { return Name + Ext; } }
        public string Path { get { return Folder.Length > 0 ? Folder + "/" + Name + Ext : Name + Ext; } }
    }

    static byte[] Decompress(byte[] data, long start, long length)
    {
        var ms = new MemoryStream();
        IntPtr d = ZSTD_createDStream();
        ZSTD_initDStream(d);
        var hin = GCHandle.Alloc(data, GCHandleType.Pinned);
        byte[] ob = new byte[1 << 20];
        var hout = GCHandle.Alloc(ob, GCHandleType.Pinned);
        try
        {
            var ib = new InBuf { src = new IntPtr(hin.AddrOfPinnedObject().ToInt64() + start), size = (UIntPtr)(ulong)length, pos = UIntPtr.Zero };
            while (true)
            {
                var o = new OutBuf { dst = hout.AddrOfPinnedObject(), size = (UIntPtr)ob.Length, pos = UIntPtr.Zero };
                var r = ZSTD_decompressStream(d, ref o, ref ib);
                if (ZSTD_isError(r) != 0) throw new InvalidDataException("zstd error at " + start);
                ms.Write(ob, 0, (int)(ulong)o.pos);
                if ((ulong)ib.pos >= (ulong)ib.size && (ulong)o.pos < (ulong)o.size) break;
            }
        }
        finally { hin.Free(); hout.Free(); ZSTD_freeDStream(d); }
        return ms.ToArray();
    }

    static long LastFrameStart(byte[] data)
    {
        // Walk the frames from the start; the index is the last one.
        var h = GCHandle.Alloc(data, GCHandleType.Pinned);
        try
        {
            long p = DataStart, last = -1;
            while (p < data.Length - 4)
            {
                if (BitConverter.ToUInt32(data, (int)p) == Magic)
                {
                    var c = ZSTD_findFrameCompressedSize(new IntPtr(h.AddrOfPinnedObject().ToInt64() + p), (UIntPtr)(ulong)(data.Length - p));
                    if (ZSTD_isError(c) == 0 && p + (long)(ulong)c <= data.Length) { last = p; p += (long)(ulong)c; continue; }
                }
                p++;
            }
            return last;
        }
        finally { h.Free(); }
    }

    public static List<Entry> ReadIndex(byte[] data)
    {
        long last = LastFrameStart(data);
        if (last < 0) throw new InvalidDataException("no zstd frames");
        byte[] idx = Decompress(data, last, data.Length - last);
        var list = new List<Entry>();
        int p = 0;
        ReadFolder(idx, ref p, "", list, true);
        return list;
    }

    // Folder := name, u32 file count, files, u32 subfolder count, subfolders.
    // File   := name, extension, u64 offset, u64 compressed, u64 size, u64 time, u64 time.
    static void ReadFolder(byte[] idx, ref int p, string parent, List<Entry> list, bool isRoot)
    {
        string name = ReadLenString(idx, ref p);
        if (name == null) throw new InvalidDataException("bad index at " + p);
        string path = isRoot ? "" : (parent.Length > 0 ? parent + "/" + name : name);
        int files = BitConverter.ToInt32(idx, p); p += 4;
        for (int i = 0; i < files; i++)
        {
            var e = new Entry { Folder = path };
            e.Name = ReadLenString(idx, ref p);
            e.Ext = ReadLenString(idx, ref p);
            if (e.Name == null || e.Ext == null) throw new InvalidDataException("bad file entry at " + p);
            e.Offset = BitConverter.ToInt64(idx, p); e.Compressed = BitConverter.ToInt64(idx, p + 8); e.Size = BitConverter.ToInt64(idx, p + 16);
            p += 40;
            list.Add(e);
        }
        if (p + 4 > idx.Length) return;
        int subs = BitConverter.ToInt32(idx, p); p += 4;
        for (int i = 0; i < subs; i++) ReadFolder(idx, ref p, path, list, false);
    }

    static string ReadLenString(byte[] b, ref int p)
    {
        if (p + 4 > b.Length) return null;
        int n = BitConverter.ToInt32(b, p);
        if (n <= 0 || n > 512 || p + 4 + n > b.Length) return null;
        for (int i = 0; i < n; i++) { byte c = b[p + 4 + i]; if (c < 0x20 || c > 0x7e) return null; }
        string s = Encoding.ASCII.GetString(b, p + 4, n);
        p += 4 + n;
        return s;
    }

    public static byte[] ReadEntry(byte[] data, Entry e)
    {
        return Decompress(data, DataStart + e.Offset, e.Compressed);
    }

    // ---------------- .jsb -> JSON ----------------

    public static string JsbToJson(byte[] b)
    {
        var sb = new StringBuilder();
        int p = 0;
        WriteValue(b, ref p, sb, 0);
        return sb.ToString();
    }

    static int Count(byte[] b, ref int p, int hi)
    {
        if (hi != 0) return hi - 1;
        int n = BitConverter.ToInt32(b, p); p += 4; return n;
    }

    static void Indent(StringBuilder sb, int depth) { sb.Append('\n').Append(' ', depth * 2); }

    static void WriteValue(byte[] b, ref int p, StringBuilder sb, int depth)
    {
        int tag = b[p++];
        int type = tag & 0x0F, hi = tag >> 4;
        switch (type)
        {
            case 0x0:
                if (hi != 0) goto default;
                sb.Append("null");
                break;
            case 0x1:
                sb.Append(hi != 0 ? "true" : "false");
                break;
            case 0x2:
                if (hi != 0) sb.Append((hi - 8).ToString(CultureInfo.InvariantCulture));
                else { sb.Append(BitConverter.ToInt32(b, p).ToString(CultureInfo.InvariantCulture)); p += 4; }
                break;
            case 0x4:
                if (hi != 0) goto default;
                sb.Append(BitConverter.ToUInt32(b, p).ToString(CultureInfo.InvariantCulture)); p += 4;
                break;
            case 0x5:
                if (hi != 0) goto default;
                sb.Append(BitConverter.ToUInt64(b, p).ToString(CultureInfo.InvariantCulture)); p += 8;
                break;
            case 0x7:
                if (hi != 0) { sb.Append(((hi - 1) * 0.5).ToString("R", CultureInfo.InvariantCulture)); break; }
                {
                    double v = BitConverter.ToDouble(b, p); p += 8;
                    sb.Append(double.IsNaN(v) || double.IsInfinity(v) ? "null" : v.ToString("R", CultureInfo.InvariantCulture));
                }
                break;
            case 0x8:
                {
                    int n = Count(b, ref p, hi);
                    WriteString(sb, Encoding.UTF8.GetString(b, p, n)); p += n;
                    break;
                }
            case 0x9:
                {
                    int n = Count(b, ref p, hi);
                    sb.Append('[');
                    for (int i = 0; i < n; i++)
                    {
                        if (i > 0) sb.Append(',');
                        Indent(sb, depth + 1);
                        WriteValue(b, ref p, sb, depth + 1);
                    }
                    if (n > 0) Indent(sb, depth);
                    sb.Append(']');
                    break;
                }
            case 0xA:
                {
                    int n = Count(b, ref p, hi);
                    sb.Append('{');
                    for (int i = 0; i < n; i++)
                    {
                        if (i > 0) sb.Append(',');
                        Indent(sb, depth + 1);
                        int kl = b[p++];
                        WriteString(sb, Encoding.UTF8.GetString(b, p, kl)); p += kl;
                        sb.Append(": ");
                        WriteValue(b, ref p, sb, depth + 1);
                    }
                    if (n > 0) Indent(sb, depth);
                    sb.Append('}');
                    break;
                }
            default:
                throw new InvalidDataException(String.Format("unknown jsb tag 0x{0:X2} at byte {1}", tag, p - 1));
        }
    }

    static void WriteString(StringBuilder sb, string s)
    {
        sb.Append('"');
        foreach (char c in s)
        {
            switch (c)
            {
                case '"': sb.Append("\\\""); break;
                case '\\': sb.Append("\\\\"); break;
                case '\n': sb.Append("\\n"); break;
                case '\r': sb.Append("\\r"); break;
                case '\t': sb.Append("\\t"); break;
                default:
                    if (c < 0x20) sb.AppendFormat("\\u{0:x4}", (int)c); else sb.Append(c);
                    break;
            }
        }
        sb.Append('"');
    }
}
