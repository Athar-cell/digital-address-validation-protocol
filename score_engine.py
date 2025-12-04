# score_engine.py
# score_engine: combines rule_score (0-40), ml_score (0-40), geo_score (0-20)

def compute_confidence(rule_score, ml_score, geo_score):
    # Expect inputs in their native ranges:
    # rule_score: 0..40, ml_score: 0..40, geo_score: 0..20
    R = rule_score or 0.0
    M = ml_score or 0.0
    G = geo_score or 0.0
    # weighted sum (produces 0..40)
    total = 0.4 * R + 0.4 * M + 0.2 * G
    # map 0..40 to 0..100
    C = (total / 40.0) * 100.0
    return round(C, 2)

def interpretation(confidence):
    if confidence is None:
        return 'Unknown'
    if confidence >= 95:
        return 'Auto Approved'
    elif confidence >= 85:
        return 'High Confidence'
    elif confidence >= 70:
        return 'Verified'
    elif confidence >= 55:
        return 'Needs Attention'
    else:
        return 'Physical Verification Required'
