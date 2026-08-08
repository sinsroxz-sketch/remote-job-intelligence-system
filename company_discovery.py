import json
import re
from urllib.parse import urlparse


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.lower().strip()


def get_positive_search_terms(search_strategy):
    terms = []

    # Priority job titles
    for title in search_strategy.get("priority_job_titles", []):
        terms.append(title)

    # Search keyword groups
    keyword_groups = search_strategy.get("search_keywords", {})

    for group_values in keyword_groups.values():
        if isinstance(group_values, list):
            terms.extend(group_values)

    # Primary role families
    for role in search_strategy.get("primary_role_families", []):
        if isinstance(role, dict):
            name = role.get("name")
            if name:
                terms.append(name)

    # Adjacent role families
    for role in search_strategy.get("adjacent_role_families", []):
        if isinstance(role, dict):
            name = role.get("name")
            if name:
                terms.append(name)

    # Remove duplicates
    unique_terms = []

    seen = set()

    for term in terms:
        cleaned = clean_text(term)

        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            unique_terms.append(term)

    return unique_terms


def calculate_relevance(job, search_terms):

    title = clean_text(job.get("title"))
    description = clean_text(job.get("description"))

    score = 0
    matched_terms = []

    for term in search_terms:
        term_clean = clean_text(term)

        if len(term_clean) < 4:
            continue

        # Strong match if term appears in job title
        if term_clean in title:
            score += 10
            matched_terms.append(term)

        # Lower weight if only present in description
        elif term_clean in description:
            score += 2
            matched_terms.append(term)

    return score, list(set(matched_terms))


def extract_domain(job):
    url = job.get("url", "")

    if not url:
        return ""

    try:
        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:
        return ""


def detect_source_type(job):
    url = job.get("url", "").lower()

    if "greenhouse.io" in url:
        return "Greenhouse"

    if "lever.co" in url:
        return "Lever"

    if "ashbyhq.com" in url:
        return "Ashby"

    return "Unknown"


def discover_companies(jobs, search_strategy, minimum_score=10):

    search_terms = get_positive_search_terms(search_strategy)

    companies = {}

    for job in jobs:

        relevance_score, matched_terms = calculate_relevance(
            job,
            search_terms
        )

        if relevance_score < minimum_score:
            continue

        company_name = job.get("company")

        if not company_name:
            continue

        if company_name not in companies:

            companies[company_name] = {
                "company_name": company_name,
                "domain": extract_domain(job),
                "ats_type": detect_source_type(job),
                "relevant_jobs_found": 0,
                "highest_relevance_score": 0,
                "matched_terms": [],
                "example_jobs": []
            }

        company = companies[company_name]

        company["relevant_jobs_found"] += 1

        company["highest_relevance_score"] = max(
            company["highest_relevance_score"],
            relevance_score
        )

        company["matched_terms"].extend(matched_terms)

        if len(company["example_jobs"]) < 3:
            company["example_jobs"].append({
                "title": job.get("title"),
                "location": job.get("location"),
                "url": job.get("url"),
                "relevance_score": relevance_score
            })

    for company in companies.values():
        company["matched_terms"] = list(
            set(company["matched_terms"])
        )

    ranked_companies = sorted(
        companies.values(),
        key=lambda x: (
            x["highest_relevance_score"],
            x["relevant_jobs_found"]
        ),
        reverse=True
    )

    return ranked_companies


if __name__ == "__main__":
    print("Company Discovery Engine v2 ready.")
