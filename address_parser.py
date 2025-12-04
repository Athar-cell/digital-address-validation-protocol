# address_parser.py
import re

PIN_REGEX = re.compile(r'\b(\d{6})\b')
HOUSE_REGEX = re.compile(r'\b(house|h|flat|apt|apartment|no\.|no|#)\s*[:\-]??\s*([A-Za-z0-9/\-]+)', re.I)
SECTOR_REGEX = re.compile(r'\bsector\s*(\d+)\b', re.I)
NEAR_REGEX = re.compile(r'near\s+([A-Za-z0-9\s,\-]+)', re.I)

def parse_address(text):
    text = text or ''
    raw = text.strip()
    # pincode
    p = PIN_REGEX.search(raw)
    pincode = p.group(1) if p else None
    # house number heuristics
    h = HOUSE_REGEX.search(raw)
    house_no = h.group(2) if h else None
    # sector
    s = SECTOR_REGEX.search(raw)
    sector = s.group(1) if s else None
    # near landmark
    n = NEAR_REGEX.search(raw)
    near = n.group(1).strip() if n else None
    # fallback simple tokens for locality and district guessing (last tokens)
    tokens = re.split('[,;\n]+', raw)
    locality = tokens[-3].strip() if len(tokens) >= 3 else (tokens[-2].strip() if len(tokens) >= 2 else None)
    district = tokens[-2].strip() if len(tokens) >= 2 else tokens[-1].strip() if len(tokens) >= 1 else None
    # normalize empty strings to None
    def norm(x):
        return x if x and x.strip() else None
    return {
        'raw': raw,
        'pincode': norm(pincode),
        'house_no': norm(house_no),
        'sector': norm(sector),
        'near': norm(near),
        'locality_guess': norm(locality),
        'district_guess': norm(district)
    }
