import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CANDIDATE_PROFILE = """
12+ years of experience.

Core experience:
- Banking Operations
- Client Lifecycle Management
- Corporate account opening, maintenance and closure
- Process migration and transition management
- Operational governance
- KPI and SLA management
- Process improvement
- Stakeholder management

IAM experience:
- Access provisioning and deprovisioning
- RBAC
- Entitlement reviews
- Active Directory
- CyberArk safe management
- ServiceNow
- Access governance

Career preferences:
- Fully remote
- Must be workable from India
- Mid-senior / manager / lead level
- Good work-life balance
- High autonomy
- Avoid mandatory office work
- Avoid rotational night shifts

Career directions:
- Operations Management
- Business Operations
- Client Operations
- Service Delivery
- Client Lifecycle Management
- IAM Operations
- Identity Governance
- Operations Transformation
"""

job_title = input("Job title: ")
job_location = input("Job location: ")

print("\nPaste the job description.")
print("When finished, type END on a new line.\n")

lines = []

while True:
    line = input()

    if line.strip() == "END":
        break

    lines.append(line)

job_description = "\n".join(lines)

prompt = f"""
You are the Job Matching Engine for a Remote Job Intelligence System.

CANDIDATE PROFILE:

{CANDIDATE_PROFILE}

JOB TITLE:
{job_title}

JOB LOCATION:
{job_location}

JOB DESCRIPTION:
{job_description}

Evaluate whether this candidate should spend time applying.

Be strict.

Do not give a high score simply because some keywords overlap.

Distinguish between:
- direct experience
- transferable experience
- genuine skill gaps

Pay particular attention to whether a role is highly technical,
engineering-heavy, architecture-heavy or implementation-heavy.

Return exactly this format:

MATCH SCORE: <0-100>

DECISION: <APPLY / REVIEW / SKIP>

ROLE FAMILY: <best classification>

REMOTE / INDIA FIT: <GOOD / UNCLEAR / POOR>

STRENGTHS:
- ...
- ...

GAPS:
- ...
- ...

REASON:
<2-4 sentence explanation>
"""

response = client.responses.create(
    model="gpt-5-mini",
    input=prompt
)

print("\n----- RJIS MATCH RESULT -----\n")
print(response.output_text)
