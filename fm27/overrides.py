"""In-memory, per-run overrides of a config JSON (never written back to the file)."""
import copy

SCALAR_KEYS = {
    'ip_weight': float,
    'age_penalty': float,
    'age_threshold': int,
    'arabic_penalty': float,
}


def parse_set(items):
    """['ip_weight=0.7', ...] -> {'ip_weight': 0.7}; raises ValueError on a bad item."""
    out = {}
    for item in items or []:
        key, sep, raw = item.partition('=')
        key = key.strip()
        if not sep or key not in SCALAR_KEYS:
            raise ValueError(f"--set: '{item}' is not KEY=VALUE with KEY one of: {', '.join(SCALAR_KEYS)}")
        try:
            out[key] = SCALAR_KEYS[key](raw)
        except ValueError:
            raise ValueError(f"--set: value of {key} must be {SCALAR_KEYS[key].__name__}, got '{raw}'")
    return out


def parse_mult(items):
    """['Last 5 Games=0.1', ...] -> {'Last 5 Games': 0.1}; splits on the last '='."""
    out = {}
    for item in items or []:
        name, sep, raw = item.rpartition('=')
        name = name.strip()
        if not sep or not name:
            raise ValueError(f"--mult: '{item}' is not NAME=WEIGHT")
        try:
            out[name] = float(raw)
        except ValueError:
            raise ValueError(f"--mult: weight of '{name}' must be a number, got '{raw}'")
    return out


def build_overrides(set_items=None, mult_items=None, no_mult=False, age_penalty=None, age_threshold=None):
    """Overrides dict: {'scalars': {...}, 'mult': {...}, 'no_mult': bool}."""
    scalars = {}
    if age_penalty is not None:
        scalars['age_penalty'] = float(age_penalty)
    if age_threshold is not None:
        scalars['age_threshold'] = int(age_threshold)
    scalars.update(parse_set(set_items))
    return {'scalars': scalars, 'mult': parse_mult(mult_items), 'no_mult': bool(no_mult)}


def has_overrides(overrides):
    return bool(overrides and (overrides['scalars'] or overrides['mult'] or overrides['no_mult']))


def effective_config(base, overrides):
    """Deep copy of `base` with overrides applied (a mult weight of 0 removes that multiplier)."""
    cfg = copy.deepcopy(base)
    if not overrides:
        return cfg
    cfg.update(overrides['scalars'])
    mults = {} if overrides['no_mult'] else dict(cfg.get('multipliers') or {})
    for name, weight in overrides['mult'].items():
        # an override of an existing key replaces it whatever the case ('av rat' -> 'Av Rat')
        name = next((k for k in mults if k.casefold() == name.casefold()), name)
        mults.pop(name, None)
        if weight != 0:
            mults[name] = weight
    if 'multipliers' in cfg or mults:
        cfg['multipliers'] = mults
    return cfg


def _fmt(v):
    return '(unset)' if v is None else f"{v:g}"


def describe_overrides(base, effective):
    """One line listing what differs between the file config and the effective config, or ''."""
    parts = []
    for key in SCALAR_KEYS:
        if base.get(key) != effective.get(key):
            parts.append(f"{key} {_fmt(base.get(key))} -> {_fmt(effective.get(key))}")
    old, new = base.get('multipliers') or {}, effective.get('multipliers') or {}
    for name in dict.fromkeys([*old, *new]):
        a, b = old.get(name) or None, new.get(name) or None  # weight 0 == absent
        if a != b:
            parts.append(f"{name} {_fmt(a)} -> {'(removed)' if b is None else _fmt(b)}")
    return f"overrides: {', '.join(parts)}" if parts else ''
