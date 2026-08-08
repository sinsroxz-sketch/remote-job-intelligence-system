def score_company(company):
    score = 0

    remote = company.get("remote_profile", {})

    if remote.get("remote_friendly") == "Yes":
        score += 25

    if remote.get("hires_in_india") == "Yes":
        score += 25

    if remote.get("hires_worldwide") == "Yes":
        score += 10

    relevant_jobs = company.get(
        "hiring_activity", {}
    ).get("relevant_jobs", 0)

    if relevant_jobs >= 5:
        score += 25
    elif relevant_jobs >= 2:
        score += 15
    elif relevant_jobs == 1:
        score += 5

    role_families = company.get("role_families", [])

    if role_families:
        score += 10

    industries = company.get("industries", [])

    if industries:
        score += 5

    if score >= 80:
        tier = "Tier 1"
        frequency = "Daily"

    elif score >= 60:
        tier = "Tier 2"
        frequency = "Every 3 days"

    else:
        tier = "Tier 3"
        frequency = "Weekly"

    return {
        "score": score,
        "tier": tier,
        "check_frequency": frequency
    }
