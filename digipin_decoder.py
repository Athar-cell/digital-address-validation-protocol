# digipin_decoder.py
# DIGIPIN encoder/decoder based on the DIGIPIN spec used in the project.

L = [
    ['F', 'C', '9', '8'],
    ['J', '3', '2', '7'],
    ['K', '4', '5', '6'],
    ['L', 'M', 'P', 'T']
]

MIN_LAT = 2.5
MAX_LAT = 38.5
MIN_LON = 63.5
MAX_LON = 99.5

def decode_digipin(digipin):
    """Convert a 10-char DIGIPIN into centroid (lat, lon).
    Accepts digipin with or without dashes, returns (lat, lon) of grid centre."""
    code = digipin.replace('-', '').strip().upper()
    if len(code) != 10:
        raise ValueError('DIGIPIN must be 10 characters (excluding dashes)')
    min_lat, max_lat = MIN_LAT, MAX_LAT
    min_lon, max_lon = MIN_LON, MAX_LON
    for ch in code:
        # find row, col in L
        found = False
        lat_div = (max_lat - min_lat) / 4.0
        lon_div = (max_lon - min_lon) / 4.0
        for r in range(4):
            for c in range(4):
                if L[r][c] == ch:
                    # r=0 => topmost band; compute new lat bounds accordingly
                    new_max_lat = max_lat - (lat_div * r)
                    new_min_lat = new_max_lat - lat_div
                    new_min_lon = min_lon + (lon_div * c)
                    new_max_lon = new_min_lon + lon_div
                    min_lat, max_lat = new_min_lat, new_max_lat
                    min_lon, max_lon = new_min_lon, new_max_lon
                    found = True
                    break
            if found:
                break
        if not found:
            raise ValueError(f'Invalid DIGIPIN character: {ch}')
    # centroid
    c_lat = (min_lat + max_lat) / 2.0
    c_lon = (min_lon + max_lon) / 2.0
    return (round(c_lat, 7), round(c_lon, 7))

def encode_digipin(lat, lon):
    """Encode given lat, lon into a 10-char DIGIPIN using the DIGIPIN grid logic."""
    if not (MIN_LAT <= lat <= MAX_LAT and MIN_LON <= lon <= MAX_LON):
        raise ValueError('Latitude/Longitude out of DIGIPIN bounds')
    min_lat, max_lat = MIN_LAT, MAX_LAT
    min_lon, max_lon = MIN_LON, MAX_LON
    code = []
    for lvl in range(10):
        lat_div = (max_lat - min_lat)/4.0
        lon_div = (max_lon - min_lon)/4.0
        found = False
        for r in range(4):
            candidate_max_lat = max_lat - (lat_div * r)
            candidate_min_lat = candidate_max_lat - lat_div
            if candidate_min_lat <= lat < candidate_max_lat or (r == 3 and lat == candidate_min_lat):
                for c in range(4):
                    candidate_min_lon = min_lon + lon_div * c
                    candidate_max_lon = candidate_min_lon + lon_div
                    if candidate_min_lon <= lon < candidate_max_lon or (c == 3 and lon == candidate_max_lon):
                        code.append(L[r][c])
                        # update bounding box for next level
                        min_lat, max_lat = candidate_min_lat, candidate_max_lat
                        min_lon, max_lon = candidate_min_lon, candidate_max_lon
                        found = True
                        break
                if found:
                    break
        if not found:
            # numerical edge cases: clamp to last cell
            code.append(L[3][3])
            min_lat, max_lat = max_lat - lat_div, max_lat
            min_lon, max_lon = min_lon + 3*lon_div, min_lon + 4*lon_div
    return ''.join(code)
