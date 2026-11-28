"""Role siglas for printed tables (from the glossary in context/managers_tactics.md)."""
import re
from functools import lru_cache
from pathlib import Path

# Display order: GK, then each line right to left.
POSITION_ORDER = ['GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL', 'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'ST']


def pos_rank(pos):
    return POSITION_ORDER.index(pos) if pos in POSITION_ORDER else len(POSITION_ORDER)


def norm_role(name):
    name = re.sub(r'[_\s]+OOP$', '', str(name).strip())
    return re.sub(r'[^a-z0-9]', '', name.lower())


@lru_cache(maxsize=None)
def role_abbreviations(repo: Path):
    """{'ip'|'oop': {normalized role name: sigla}} from the glossary (section 6) of managers_tactics.md."""
    out = {'ip': {}, 'oop': {}}
    path = repo / 'context' / 'managers_tactics.md'
    if not path.exists():
        return out
    kind = None
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('### 6.1'):
            kind = 'ip'
        elif line.startswith('### 6.2'):
            kind = 'oop'
        elif line.startswith('## ') or (line.startswith('### ') and kind and not line.startswith('### 6.')):
            kind = None
        elif kind:
            m = re.match(r'\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|', line)
            if m:
                out[kind][norm_role(m.group(2))] = m.group(1)
    return out


def abbr(table, role, kind):
    """Sigla for a role name ('Ball_Playing_Centre_Back' -> 'BPCB'); initials if not in the glossary."""
    if not role:
        return ''
    key = norm_role(role)
    if key in table.get(kind, {}):
        return table[kind][key]
    words = re.sub(r'[_\s]+OOP$', '', str(role)).replace('_', ' ').replace('-', ' ').split()
    return ''.join(w[0].upper() for w in words)


def slot_siglas(repo: Path, role, role_oop):
    """'IW/TWM' for a slot's in- and out-of-possession roles."""
    table = role_abbreviations(Path(repo))
    return abbr(table, role, 'ip') + (f"/{abbr(table, role_oop, 'oop')}" if role_oop else '')


def role_sigla(repo: Path, role, kind):
    """Sigla of one role; kind is 'ip' or 'oop'."""
    return abbr(role_abbreviations(Path(repo)), role, kind)
