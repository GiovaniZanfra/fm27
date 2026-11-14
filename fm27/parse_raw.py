import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def parse_positions(position_str: str) -> set:
    """Parse position string into set of standardized positions.
    
    Args:
        position_str: Position string from FM (e.g. "AM (R)")
        
    Returns:
        Set of standardized position codes
    """
    if pd.isna(position_str):
        return set()
    pos_list = set()
    split_ = str(position_str).split(", ")
    for pos in split_:
        if pos == "AM (R)":
            pos_list.add("AMR")
        elif pos == "AM (L)":
            pos_list.add("AML")
        elif pos == "WB/M/AM (L)":
            pos_list.add("WBL")
            pos_list.add("ML")
            pos_list.add("AML")
        elif pos == "D/WB/M (RL)":
            pos_list.add("DR")
            pos_list.add("DL")
            pos_list.add("WBR")
            pos_list.add("WBL")
            pos_list.add("MR")
            pos_list.add("ML")
        elif pos == "WB/M/AM (L)":
            pos_list.add("WBL")
            pos_list.add("ML")
            pos_list.add("AML")
        elif pos == "WB/AM (R)":
            pos_list.add("WBR")
            pos_list.add("AMR")
        elif pos == "WB/M/AM (R)":
            pos_list.add("WBR")
            pos_list.add("MR")
            pos_list.add("AMR")
        elif pos == "AM (C)":
            pos_list.add("AMC")
        elif pos == "M (R)":
            pos_list.add("MR")
        elif pos == "M (L)":
            pos_list.add("ML")
        elif pos == "M (C)":
            pos_list.add("MC")
        elif pos == "D (R)":
            pos_list.add("DR")
        elif pos == "D (L)":
            pos_list.add("DL")
        elif pos == "D/WB (R)":
            pos_list.add("DR")
            pos_list.add("WBR")
        elif pos == "D/WB (L)":
            pos_list.add("DL")
            pos_list.add("WBL")
        elif pos == "M/AM (R)":
            pos_list.add("MR")
            pos_list.add("AMR")
        elif pos == "M/AM (L)":
            pos_list.add("ML")
            pos_list.add("AML")
        elif pos == "M/AM (C)":
            pos_list.add("MC")
            pos_list.add("AMC")
        elif pos == "D (C)":
            pos_list.add("DC")
        elif pos == "GK":
            pos_list.add("GK")
        elif pos == "ST (C)":
            pos_list.add("ST")
        elif pos == "DM":
            pos_list.add("DM")
        elif pos == "WB (L)":
            pos_list.add("WBL")
        elif pos == "WB (R)":
            pos_list.add("WBR")
        elif pos == "D (RC)":
            pos_list.add("DR")
            pos_list.add("DC")
        elif pos == "D (LC)":
            pos_list.add("DL")
            pos_list.add("DC")
        elif pos == "M (RL)":
            pos_list.add("MR")
            pos_list.add("ML")
            pos_list.add("AMR")
            pos_list.add("AML")
        elif pos == "M (RC)":
            pos_list.add("MR")
            pos_list.add("MC")
            pos_list.add("AMR")
            pos_list.add("AMC")
        elif pos == "M (LC)":
            pos_list.add("ML")
            pos_list.add("MC")
            pos_list.add("AML")
            pos_list.add("AMC")
        elif pos == "AM (RLC)":
            pos_list.add("AMR")
            pos_list.add("AML")
            pos_list.add("AMC")
        elif pos == "AM (LC)":
            pos_list.add("AML")
            pos_list.add("AMC")
        elif pos == "AM (RC)":
            pos_list.add("AMR")
            pos_list.add("AMC")
        elif pos == "AM (RL)":
            pos_list.add("AMR")
            pos_list.add("AML")
        elif pos == "D/WB (RL)":
            pos_list.add("DR")
            pos_list.add("DL")
            pos_list.add("WBR")
            pos_list.add("WBL")
        elif pos == "D/WB (RC)":
            pos_list.add("DR")
            pos_list.add("DC")
            pos_list.add("WBR")
        elif pos == "M/AM (RL)":
            pos_list.add("MR")
            pos_list.add("ML")
            pos_list.add("AMR")
            pos_list.add("AML")
        elif pos == "M/AM (LC)":
            pos_list.add("ML")
            pos_list.add("MC")
            pos_list.add("AML")
            pos_list.add("AMC")
        elif pos == "M/AM (RC)":
            pos_list.add("MR")
            pos_list.add("MC")
            pos_list.add("AMR")
            pos_list.add("AMC")
        elif pos == "D (RL)":
            pos_list.add("DR")
            pos_list.add("DL")
        elif pos == "D/WB (LC)":
            pos_list.add("DL")
            pos_list.add("DC")
            pos_list.add("WBL")
        elif pos == "D/WB/M (L)":
            pos_list.add("DL")
            pos_list.add("WBL")
            pos_list.add("ML")
        elif pos == "WB/M (L)":
            pos_list.add("WBL")
            pos_list.add("ML")
        elif pos == "D (RLC)":
            pos_list.add("DR")
            pos_list.add("DL")
            pos_list.add("DC")
        elif pos == "D/M (C)":
            pos_list.add("DC")
            pos_list.add("DM")
        elif pos == "M/AM (RLC)":
            pos_list.add("MR")
            pos_list.add("ML")
            pos_list.add("MC")
            pos_list.add("AMR")
            pos_list.add("AML")
            pos_list.add("AMC")
        elif pos == "D/WB/M/AM (L)":
            pos_list.add("DL")
            pos_list.add("WBL")
            pos_list.add("ML")
            pos_list.add("AML")
        elif pos == "D/WB/M (R)":
            pos_list.add("DR")
            pos_list.add("WBR")
            pos_list.add("MR")
        elif pos == "D/WB/AM (R)":
            pos_list.add("DR")
            pos_list.add("WBR")
            pos_list.add("AMR")
        elif pos == "D/WB/M/AM (RL)":
            pos_list.add("DR")
            pos_list.add("DL")
            pos_list.add("WBR")
            pos_list.add("WBL")
            pos_list.add("MR")
            pos_list.add("ML")
            pos_list.add("AMR")
            pos_list.add("AML")
        elif pos == "D/WB/M/AM (R)":
            pos_list.add("DR")
            pos_list.add("WBR")
            pos_list.add("MR")
            pos_list.add("AMR")
        elif pos == "WB/AM (L)":
            pos_list.add("WBL")
            pos_list.add("AML")
        elif pos == "WB/M (R)":
            pos_list.add("WBR")
            pos_list.add("MR")
        elif pos == "D/M (L)":
            pos_list.add("DL")
            pos_list.add("ML")
        elif pos == "D/WB/AM (L)":
            pos_list.add("DL")
            pos_list.add("WBL")
            pos_list.add("AML")
        elif pos == "WB (RL)":
            pos_list.add("WBR")
            pos_list.add("WBL")
        elif pos == "M (RLC)":
            pos_list.add("MR")
            pos_list.add("ML")
            pos_list.add("MC")
        elif pos == "D/M/AM (L)":
            pos_list.add("DL")
            pos_list.add("ML")
            pos_list.add("AML")
        elif pos == "D/M (R)":
            pos_list.add("DR")
            pos_list.add("MR")
        else:
            print(f"Unknown position format: {pos}")
    return pos_list


def get_attribute_mapping():
    """Get mapping from raw attribute codes to full names."""
    return {
        '1v1': 'One On Ones',
        'Acc': 'Acceleration',
        'Aer': 'Aerial Reach',  # Goalkeeper specific
        'Agg': 'Aggression',
        'Agi': 'Agility',
        'Ant': 'Anticipation',
        'Bal': 'Balance',
        'Bra': 'Bravery',
        'Cmd': 'Command Of Area',  # Goalkeeper specific
        'Cnt': 'Concentration',
        'Cmp': 'Composure',
        'Cro': 'Crossing',
        'Dec': 'Decisions',
        'Det': 'Determination',
        'Dri': 'Dribbling',
        'Fin': 'Finishing',
        'Fir': 'First Touch',
        'Fla': 'Flair',
        'Han': 'Handling',  # Goalkeeper specific
        'Hea': 'Heading',
        'Jum': 'Jumping Reach',
        'Kic': 'Kicking',  # Goalkeeper specific
        'Ldr': 'Leadership',
        'Lon': 'Long Shots',
        'Mar': 'Marking',
        'OtB': 'Off The Ball',
        'Pac': 'Pace',
        'Pas': 'Passing',
        'Pos': 'Positioning',
        'Ref': 'Reflexes',  # Goalkeeper specific
        'Sta': 'Stamina',
        'Str': 'Strength',
        'Tck': 'Tackling',
        'Tea': 'Team Work',
        'Tec': 'Technique',
        'Thr': 'Throwing',
        'TRO': 'Rushing Out',  # Goalkeeper specific
        'Vis': 'Vision',
        'Wor': 'Work Rate'
    }

def get_attribute_columns():
    """Get list of attribute columns to extract from raw data."""
    return ['Name'] + list(get_attribute_mapping().keys()) + ['UID']


def _find_column(cols, keywords):
    """Return first column name in cols that contains any keyword (case-insensitive)."""
    # Try exact match (case-insensitive), then substring match
    lower = [c.lower() for c in cols]
    kws = [k.lower() for k in keywords]
    # exact match
    for k in kws:
        for c, l in zip(cols, lower):
            if l == k:
                return c
    # startswith match
    for k in kws:
        for c, l in zip(cols, lower):
            if l.startswith(k):
                return c
    # substring match
    for k in kws:
        for c, l in zip(cols, lower):
            if k in l:
                return c
    return None


def _find_performance_columns(cols):
    """Find raw performance data columns for training rate and last 5 games."""
    training_col = _find_column(cols, ['training rate', 'training rating', 'training', 'trn rat', 'train rate', 'train'])
    last5_col = _find_column(cols, ['last 5 games', 'last 5', 'last 5 rating', 'last5 games', 'last5', 'last 5 games rating'])
    return training_col, last5_col


def _find_value_column(cols):
    """Find raw transfer/market value column."""
    return _find_column(cols, ['transfer value', 'market value', 'value', 'worth', 'transfer'])


def _append_uid_to_duplicate_names(df: pd.DataFrame) -> pd.DataFrame:
    """Append UID to duplicate player names so they become unique."""
    if 'Name' not in df.columns or 'UID' not in df.columns:
        return df

    df = df.copy()
    names = df['Name'].astype(str).str.strip()
    # Preserve missing names as NA instead of the literal 'nan'
    names = names.replace({'nan': pd.NA, 'None': pd.NA})
    df['Name'] = names

    dup_mask = df['Name'].notna() & df['Name'].duplicated(keep=False)
    if not dup_mask.any():
        return df

    for name, group in df.loc[dup_mask].groupby('Name'):
        if name is pd.NA:
            continue
        for idx, row in group.iterrows():
            uid = row['UID']
            if pd.isna(uid):
                continue
            if isinstance(uid, float) and uid.is_integer():
                uid = int(uid)
            uid_str = str(uid).strip()
            df.at[idx, 'Name'] = f"{name} ({uid_str})"

    return df


def _parse_rating(value):
    if pd.isna(value):
        return None
    raw = str(value).strip()
    if raw == '':
        return None
    raw = raw.replace(',', '.')
    try:
        return float(raw)
    except ValueError:
        return None


def _parse_attr_value(val) -> float:
    """Parse a scalar attribute value, handling ranges like '7-10' → 8.5."""
    if pd.isna(val):
        return float('nan')
    try:
        return float(val)
    except Exception:
        try:
            parts = str(val).split('-')
            return (float(parts[0]) + float(parts[1])) / 2
        except Exception:
            return float('nan')


def _normalize_col(series: pd.Series) -> 'np.ndarray':
    """StandardScaler normalize a Series; ranges resolved to midpoints, missing → 0.0."""
    values = np.array([_parse_attr_value(v) for v in series], dtype=float)
    mask = ~np.isnan(values)
    result = np.zeros(len(values))
    if mask.any():
        result[mask] = StandardScaler().fit_transform(values[mask].reshape(-1, 1)).flatten()
    return result


def _save_performance_data(merged_df, interim_dir, value_col=None, attr_df=None):
    cols = merged_df.columns.tolist()
    training_col, last5_col = _find_performance_columns(cols)
    av_rat_col = _find_column(cols, ['av rat', 'average rating', 'av rating', 'avg rating', 'av. rat'])

    # Detect "Not for Sale" before _parse_money loses the string
    not_for_sale_mask = (
        merged_df[value_col].str.lower().str.contains("not for sale", na=False)
        if value_col and value_col in merged_df.columns
        else pd.Series(False, index=merged_df.index)
    )

    performance = pd.DataFrame()
    performance['Name'] = merged_df['Name'].values
    performance['UID'] = merged_df['UID'].values if 'UID' in merged_df.columns else np.nan
    performance['Training_Rate'] = (
        merged_df[training_col].apply(_parse_rating).values
        if training_col and training_col in merged_df.columns
        else np.nan
    )
    performance['Last_5_Games_Rating'] = (
        merged_df[last5_col].apply(_parse_rating).values
        if last5_col and last5_col in merged_df.columns
        else np.nan
    )
    performance['Av_Rat'] = (
        merged_df[av_rat_col].apply(_parse_rating).values
        if av_rat_col and av_rat_col in merged_df.columns
        else np.nan
    )
    performance['TransferValue'] = (
        merged_df[value_col].apply(_parse_money).values
        if value_col and value_col in merged_df.columns
        else np.nan
    )

    for col in ['Training_Rate', 'Last_5_Games_Rating', 'Av_Rat', 'TransferValue']:
        performance[f"{col}_Normalized"] = _normalize_col(performance[col])

    # "Not for Sale" players are maximally valued
    performance.loc[not_for_sale_mask.values, 'TransferValue_Normalized'] = 1.0

    # Normalize all numeric attribute columns and append to performance
    if attr_df is not None:
        attr_reset = attr_df.reset_index(drop=True)
        # use pd.to_numeric coercion so string-typed columns (e.g. '12') are handled
        numeric_attr_cols = [
            c for c in attr_reset.columns
            if c not in ('Name', 'UID')
            and pd.to_numeric(attr_reset[c], errors='coerce').notna().any()
        ]
        attr_norm = attr_reset[['Name']].copy()
        for col in numeric_attr_cols:
            attr_norm[f"{col}_Normalized"] = _normalize_col(attr_reset[col])
        performance = performance.merge(attr_norm, on='Name', how='left')
        for col in numeric_attr_cols:
            norm_col = f"{col}_Normalized"
            if norm_col in performance.columns:
                performance[norm_col] = performance[norm_col].fillna(0.0)

    performance_file = interim_dir / 'performance.csv'
    performance.to_csv(performance_file, index=False)

    if last5_col and last5_col in merged_df.columns and performance['Last_5_Games_Rating'].notna().sum() == 0:
        print(f"Warning: found Last 5 Games column '{last5_col}' but no valid values were extracted.")
    if training_col and training_col in merged_df.columns and performance['Training_Rate'].notna().sum() == 0:
        print(f"Warning: found training rate column '{training_col}' but no valid values were extracted.")
    if av_rat_col and av_rat_col in merged_df.columns and performance['Av_Rat'].notna().sum() == 0:
        print(f"Warning: found Av Rat column '{av_rat_col}' but no valid values were extracted.")
    if value_col and value_col in merged_df.columns and performance['TransferValue'].notna().sum() == 0:
        print(f"Warning: found transfer value column '{value_col}' but no valid values were extracted.")

    print(f"Saved performance file in {performance_file} (training={training_col}, last5={last5_col}, av_rat={av_rat_col}, value={value_col})")


def _parse_money(s):
    """Parse money strings like '€2.5M' or '500K' into integer value (no currency conversion).

    Returns None if parsing fails.
    """
    if pd.isna(s):
        return None
    raw = str(s).strip()
    if raw == "":
        return None

    # Normalize separators and remove enclosing parentheses
    t = raw.replace('(', '').replace(')', '')
    t = t.replace('\u2013', '-').replace('\u2014', '-')  # normalize dashes
    t = t.replace('\xa0', ' ')

    # Remove common trailing qualifiers (per annum/week/month) and percent signs
    low = t.lower()
    for token in ['per annum', 'per year', 'p/a', 'pa', '/a', 'p.a.', 'p.w.', 'p/w', 'per week', '/week', '/yr', 'annum', 'pa.', 'pw', 'p.w', '/year', 'annual']:
        low = low.replace(token, '')
    low = low.replace('%', '')

    # If it's a range like '140K - 550K' or '€140K-€550K', split and average
    import re
    parts = re.split(r"\s*-\s*|\s+to\s+", low)
    nums = []
    for part in parts:
        p = part.strip()
        if p == '':
            continue
        # remove currency symbols and whitespace
        p = p.replace('€', '').replace('\u20ac', '').replace('£', '').replace('$', '')
        p = p.replace(',', '').strip()
        # extract numeric with optional suffix K/M/B
        m = re.search(r"([0-9]*\.?[0-9]+)\s*([kmb]?)", p, flags=re.I)
        if not m:
            # try to extract plain integer
            m2 = re.search(r"(\d+)", p)
            if m2:
                try:
                    nums.append(int(m2.group(1)))
                except Exception:
                    continue
            continue
        number = float(m.group(1))
        suffix = m.group(2).lower()
        mult = 1
        if suffix == 'k':
            mult = 1_000
        elif suffix == 'm':
            mult = 1_000_000
        elif suffix == 'b':
            mult = 1_000_000_000
        nums.append(int(number * mult))

    if len(nums) == 0:
        return None
    # if multiple numbers, take mean
    try:
        avg = int(round(sum(nums) / len(nums)))
        return avg
    except Exception:
        return None


def _parse_age(s):
    if pd.isna(s):
        return None
    t = str(s).strip()
    import re
    m = re.search(r"(\d{1,3})", t)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None


def _parse_height(s):
    """Parse height strings into centimeters.
    
    Handles formats like '184 cm', '1.84 m', "6'1\"", '6 ft 1 in'.
    Returns integer cm or None.
    """
    if pd.isna(s):
        return None
    t = str(s).strip().lower()
    if t == '':
        return None
    import re

    # centimeters
    m = re.search(r"(\d{2,3})\s*cm", t)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    # meters like 1.84 m
    m = re.search(r"(\d\.\d{1,2})\s*m", t)
    if m:
        try:
            meters = float(m.group(1))
            return int(round(meters * 100))
        except Exception:
            return None
    # feet and inches 6'1" or 6 ft 1 in
    m = re.search(r"(\d)\s*(?:'|ft)\s*(\d{1,2})", t)
    if m:
        try:
            feet = int(m.group(1))
            inches = int(m.group(2))
            cm = round((feet * 12 + inches) * 2.54)
            return int(cm)
        except Exception:
            return None
    # plain number assume cm if 3 digits, meters if 1-2 with decimal handled above
    m = re.search(r"^(\d{2,3})$", t)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None


def _parse_weight(s):
    """Parse weight strings into kilograms.

    Handles '80 kg', '176 lb', '176 lbs'. Returns integer kg or None.
    """
    if pd.isna(s):
        return None
    t = str(s).strip().lower()
    if t == '':
        return None
    t = t.replace(',', '')
    import re

    # kg
    m = re.search(r"(\d{2,3})\s*kg", t)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    # lbs
    m = re.search(r"(\d{2,3})\s*(?:lb|lbs)\b", t)
    if m:
        try:
            lbs = int(m.group(1))
            kg = round(lbs * 0.45359237)
            return int(kg)
        except Exception:
            return None
    # plain number assume kg
    m = re.search(r"^(\d{2,3})$", t)
    if m:
        try:
            return int(m.group(1))
        except Exception:
            return None
    return None


def _detect_nationality_column(df: pd.DataFrame):
    """Heuristic: find a column where many values look like country codes (e.g. 'USA', 'ITA')."""
    for col in df.columns:
        if col in ['Name', 'UID', 'Position']:
            continue
        vals = df[col].dropna().astype(str).str.strip()
        if vals.empty:
            continue
        # proportion of values that are 2-3 uppercase letters
        prop_codes = vals.str.match(r'^[A-Z]{2,3}$').mean()
        if prop_codes > 0.4:
            return col
    return None


def _detect_weight_column(df: pd.DataFrame):
    """Heuristic: find a numeric column with many values in realistic weight range (50-120 kg)."""
    for col in df.columns:
        if col in ['Name', 'UID', 'Position']:
            continue
        ser = pd.to_numeric(df[col], errors='coerce')
        if ser.notna().sum() < max(3, len(df) * 0.05):
            continue
        prop = ((ser >= 50) & (ser <= 120)).mean()
        if prop > 0.35:
            return col
    return None


def parse_raw_data(team_name: str, date: str = None):
    """Parse raw HTML data and save interim CSV files.

    Args:
        team_name: Name of the team (lowercase)
        date: Date string for the raw file (e.g. 'jan2025'). If omitted, uses the most recently modified HTML file.
    """
    data_dir = Path("data")
    team_raw_dir = data_dir / team_name / "raw"
    team_interim_dir = data_dir / team_name / "interim"

    # Ensure interim directory exists
    os.makedirs(team_interim_dir, exist_ok=True)

    # Resolve raw HTML file
    if date:
        html_file = team_raw_dir / f"{date}.html"
    else:
        html_files = sorted(team_raw_dir.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not html_files:
            raise FileNotFoundError(f"No HTML files found in {team_raw_dir}")
        html_file = html_files[0]
        print(f"No date specified, using latest: {html_file.name}")

    df_agg = pd.read_html(str(html_file), encoding="utf-8")
    merged_df = pd.concat(df_agg, axis=0, ignore_index=True)
    merged_df.columns = merged_df.columns.str.strip()
    merged_df = _append_uid_to_duplicate_names(merged_df)
    
    # Extract attributes and rename to full names
    attr = merged_df[get_attribute_columns()]
    
    # Create mapping dictionary including Name and UID
    mapping = {'Name': 'Name', 'UID': 'UID'}
    mapping.update(get_attribute_mapping())
    
    # Rename columns and save
    attr_mapped = attr.rename(columns=mapping)
    attr_file = team_interim_dir / "attributes.csv"
    attr_mapped.to_csv(attr_file, index=False)
    
    # Process and save positions
    positions_raw = merged_df[["Name", "Position", "UID"]].copy()
    
    # One-hot encode positions
    TRUE_POSITIONS = [
        'GK', 'DR', 'DC', 'DL', 'WBR', 'DM', 'WBL',
        'MR', 'MC', 'ML', 'AMR', 'AMC', 'AML', 'ST'
    ]
    
    positions_raw['Position_List'] = (
        positions_raw['Position'].apply(parse_positions)
    )
    pos = pd.DataFrame()
    pos['Name'] = positions_raw['Name']
    pos['UID'] = positions_raw['UID']
    
    for position in TRUE_POSITIONS:
        pos[position] = positions_raw['Position_List'].apply(
            lambda x: position in x
        )
    
    # Save positions
    pos_file = team_interim_dir / "positions.csv"
    pos.to_csv(pos_file, index=False)
    # Extract demographics (age, salary, transfer value, media handling, nationality, height, weight)
    cols = merged_df.columns.tolist()
    age_col = _find_column(cols, ['age', 'dob', 'date of birth', 'years'])

    # Salary (prefer 'wage' or 'salary' exact/startswith), consider weekly/annual tokens later
    salary_col = None
    for cand in ['wage', 'weekly wage', 'weekly', 'salary', 'wages', 'weekly pay']:
        salary_col = _find_column(cols, [cand])
        if salary_col:
            break

    # Transfer value / market value
    value_col = None
    for cand in ['transfer value', 'market value', 'value', 'worth', 'transfer']:
        value_col = _find_column(cols, [cand])
        if value_col:
            break
    # If value_col accidentally matched the same column as salary, try alternatives
    if value_col and salary_col and value_col == salary_col:
        for cand in ['market value', 'transfer value', 'worth', 'transfer', 'value']:
            candidate = _find_column(cols, [cand])
            if candidate and candidate != salary_col:
                value_col = candidate
                break

    media_col = _find_column(cols, ['media handling', 'media', 'media info', 'media_handling'])
    club_col = _find_column(cols, ['club', 'team', 'current club'])
    nat_col = _find_column(cols, ['nationality', 'nation', 'country', 'country of birth', 'national'])
    height_col = _find_column(cols, ['height', 'ht', 'cm', 'm'])
    weight_col = _find_column(cols, ['weight', 'wt', 'kg', 'lb', 'lbs'])
    foot_col = _find_column(cols, ['preferred foot', 'foot', 'pref foot', 'footed'])

    # Fallback heuristics when header names aren't present
    nat_fallback = False
    weight_fallback = False
    if nat_col is None:
        detected = _detect_nationality_column(merged_df)
        if detected:
            nat_col = detected
            nat_fallback = True
    if weight_col is None:
        detected_w = _detect_weight_column(merged_df)
        if detected_w:
            weight_col = detected_w
            weight_fallback = True

    # Debug: show which columns were detected (useful if mapping fails)
    print('Detected columns mapping:')
    print(f'  age_col={age_col}, salary_col={salary_col}, value_col={value_col}, media_col={media_col}')
    print(f'  nat_col={nat_col} (fallback={nat_fallback}), height_col={height_col}, weight_col={weight_col} (fallback={weight_fallback}), foot_col={foot_col}, club_col={club_col}')

    dem = pd.DataFrame()
    dem['Name'] = merged_df['Name']
    dem['UID'] = merged_df['UID']
    dem['Age'] = merged_df[age_col].apply(_parse_age) if (age_col and age_col in merged_df.columns) else pd.NA
    dem['Nationality'] = merged_df[nat_col] if (nat_col and nat_col in merged_df.columns) else pd.NA
    # keep only parsed height in cm
    dem['Height_cm'] = merged_df[height_col].apply(_parse_height) if (height_col and height_col in merged_df.columns) else pd.NA
    dem['Weight_kg'] = merged_df[weight_col].apply(_parse_weight) if (weight_col and weight_col in merged_df.columns) else pd.NA
    dem['PreferredFoot'] = merged_df[foot_col] if (foot_col and foot_col in merged_df.columns) else pd.NA
    # Normalize salary and transfer to integer values (parse ranges and strip p/a, %)
    dem['Salary'] = merged_df[salary_col].apply(_parse_money) if (salary_col and salary_col in merged_df.columns) else pd.NA
    dem['TransferValue'] = merged_df[value_col].apply(_parse_money) if (value_col and value_col in merged_df.columns) else pd.NA
    dem['TransferValue_Normalized'] = pd.NA
    value_mask = dem['TransferValue'].notna()
    if value_mask.any():
        scaled_values = StandardScaler().fit_transform(dem.loc[value_mask, ['TransferValue']].astype(float))
        dem.loc[value_mask, 'TransferValue_Normalized'] = scaled_values.flatten()
    dem['TransferValue_Normalized'].fillna(0.0, inplace=True)
    dem['Club'] = merged_df[club_col] if (club_col and club_col in merged_df.columns) else pd.NA
    dem['MediaHandling'] = merged_df[media_col] if (media_col and media_col in merged_df.columns) else pd.NA

    dem_file = team_interim_dir / "player_demographics.csv"
    dem.to_csv(dem_file, index=False)
    _save_performance_data(merged_df, team_interim_dir, value_col=value_col, attr_df=attr_mapped)
    print(f"Saved interim files in {team_interim_dir}")

def main():
    import sys
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python -m fm27.parse_raw <team_name> [date]")
        print("Example: python -m fm27.parse_raw roma jan2025")
        sys.exit(1)

    team_name = sys.argv[1].lower()
    date = sys.argv[2] if len(sys.argv) == 3 else None
    parse_raw_data(team_name, date=date)


