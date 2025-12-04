# main.py (interactive version)
from digipin_decoder import decode_digipin, encode_digipin
from address_parser import parse_address
from ml_similarity import similarity_score
from geo_validator import distance_meters
from score_engine import compute_confidence, interpretation

def rule_checks(parsed, digipin):
    from digipin_decoder import decode_digipin
    AAR = {
        'Karnataka': {'districts': ['Bengaluru', 'Mysuru'], 'pincodes': ['560001','560002','560003']},
        'Delhi': {'districts': ['New Delhi', 'South Delhi'], 'pincodes': ['110001','110002']},
        'Rajasthan': {'districts': ['Jaipur', 'Jodhpur'], 'pincodes': ['302001','302002']}
    }

    score = 0.0
    reasons = []
    try:
        centroid = decode_digipin(digipin)
        score += 10
    except:
        reasons.append("Invalid DIGIPIN")
        return 0.0, reasons, None

    p = parsed.get("pincode")
    if p:
        matched = any(p in info['pincodes'] for info in AAR.values())
        if matched:
            score += 8
        else:
            reasons.append("Pincode does not match AAR sample")
    else:
        reasons.append("No pincode found")

    district = parsed.get("district_guess")
    if district:
        d_lower = district.lower()
        matched = any(d_lower in [dd.lower() for dd in info['districts']] for info in AAR.values())
        if matched:
            score += 6
        else:
            reasons.append("District mismatch")
    else:
        reasons.append("No district guess available")

    if parsed.get("house_no"):
        score += 6
    if parsed.get("locality_guess"):
        score += 4

    return min(score, 40), reasons, centroid

def ml_checks(text, reference):
    sim = similarity_score(text, reference or text)
    ml_score = sim * 40
    return round(ml_score, 2), round(sim, 3)

def geo_checks(centroid, claim):
    from geo_validator import distance_meters
    if centroid is None:
        return 0, None
    if claim is None:
        return 5, None
    dist = distance_meters(centroid, claim)
    if dist <= 10:
        return 20, dist
    if dist <= 50:
        return 14, dist
    if dist <= 200:
        return 8, dist
    if dist <= 1000:
        return 4, dist
    return 0, dist

def validate_address(digipin, text, lat=None, lon=None, reference=None):
    parsed = parse_address(text)
    rule_score, reasons, centroid = rule_checks(parsed, digipin)
    ml_score, sim = ml_checks(text, reference)
    geo_score, dist = geo_checks(centroid, (lat, lon) if lat and lon else None)
    confidence = compute_confidence(rule_score, ml_score, geo_score)
    decision = interpretation(confidence)

    return {
        "digipin": digipin,
        "address": text,
        "parsed": parsed,
        "rule_score": rule_score,
        "ml_score": ml_score,
        "geo_score": geo_score,
        "similarity": sim,
        "distance_m": None if dist is None else round(dist, 2),
        "confidence": confidence,
        "decision": decision,
        "reasons": reasons
    }

if __name__ == "__main__":
    print("\n=== AAVA Address Validation Interactive Mode ===\n")

    while True:
        digipin = input("Enter DIGIPIN (or 'exit'): ").strip()
        if digipin.lower() == "exit":
            break

        text = input("Enter Address: ").strip()

        lat_input = input("Latitude (press Enter to skip): ").strip()
        lon_input = input("Longitude (press Enter to skip): ").strip()

        lat = float(lat_input) if lat_input else None
        lon = float(lon_input) if lon_input else None

        reference = input("Reference Address (optional): ").strip() or None

        print("\nValidating... Please wait...\n")

        result = validate_address(digipin, text, lat, lon, reference)

        import json
        print(json.dumps(result, indent=2))
        print("\n-----------------------------------------\n")
