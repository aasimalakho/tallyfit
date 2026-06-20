import re
import random
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from skills import ALL_VARIANTS_SORTED, VARIANT_TO_CANONICAL

app = FastAPI()


def find_skills_in_text(text: str):
    """Return the set of canonical skills whose variant appears in text,
    matched on word boundaries so 'r' doesn't match inside 'react'."""
    text_lower = text.lower()
    found = set()
    for variant in ALL_VARIANTS_SORTED:
        pattern = r"(?<![a-z0-9])" + re.escape(variant) + r"(?![a-z0-9])"
        if re.search(pattern, text_lower):
            found.add(VARIANT_TO_CANONICAL[variant])
    return found


def word_overlap_score(cv_text: str, job_text: str) -> int:
    """Fallback scorer when the job post doesn't contain any vocabulary
    skill — falls back to general word overlap between the two texts."""
    stop = {
        "the", "and", "for", "with", "you", "your", "a", "an", "to", "of",
        "in", "on", "is", "are", "we", "our", "this", "that", "be", "as",
        "or", "will", "have", "has", "it", "at", "by", "from", "their",
    }
    def words(t):
        return {w for w in re.findall(r"[a-zA-Z]{3,}", t.lower()) if w not in stop}
    cv_w, job_w = words(cv_text), words(job_text)
    if not job_w:
        return 50
    overlap = len(cv_w & job_w)
    score = int(min(100, (overlap / max(1, len(job_w))) * 220))
    return max(15, score)


HEADLINES = {
    "strong": [
        "This is squarely in your lane — worth a proposal.",
        "Strong overlap here. This one's worth your time.",
        "You tick most of the boxes this client is after.",
    ],
    "mid": [
        "A real overlap, with a few gaps worth addressing upfront.",
        "Decent fit — frame your gaps as things you're already across.",
        "You're in the running, but not a slam dunk.",
    ],
    "weak": [
        "Not much overlap — this one's a stretch.",
        "Thin alignment here. Probably not your best use of a credit.",
        "This is a reach more than a fit, based on what's stated.",
    ],
}


def band_name(score: int) -> str:
    if score >= 70:
        return "strong"
    if score >= 40:
        return "mid"
    return "weak"


def build_pitch(matched, score: int) -> str:
    if not matched:
        return ""
    top = list(matched)[:3]
    if len(top) == 1:
        skill_phrase = top[0]
    elif len(top) == 2:
        skill_phrase = f"{top[0]} and {top[1]}"
    else:
        skill_phrase = f"{', '.join(top[:-1])}, and {top[-1]}"

    if score >= 70:
        return f"I've worked extensively with {skill_phrase}, and this role lines up closely with what I already do — happy to share examples."
    elif score >= 40:
        return f"I bring hands-on experience with {skill_phrase}, and I'd be glad to walk through how that applies here, along with how I'd close the remaining gaps."
    else:
        return f"While {skill_phrase} is where my experience is strongest, I'm confident I can ramp up quickly on the rest if given the chance."


@app.post("/api/match")
async def match(request: Request):
    body = await request.json()
    cv_text = (body.get("cv_text") or "").strip()
    job_text = (body.get("job_text") or "").strip()

    if not cv_text or not job_text:
        return JSONResponse({"error": "Both a CV and a job post are required."}, status_code=400)

    if len(cv_text) < 20 or len(job_text) < 20:
        return JSONResponse({"error": "That text looks too short to score reliably."}, status_code=400)

    job_skills = find_skills_in_text(job_text)
    cv_skills = find_skills_in_text(cv_text)

    if job_skills:
        matched = job_skills & cv_skills
        gaps = job_skills - cv_skills
        score = int(round((len(matched) / len(job_skills)) * 100))
        score = max(5, min(100, score))
    else:
        matched = cv_skills
        gaps = set()
        score = word_overlap_score(cv_text, job_text)

    band = band_name(score)
    headline = random.choice(HEADLINES[band])
    pitch = build_pitch(matched, score)

    return JSONResponse({
        "score": score,
        "headline": headline,
        "matching_skills": sorted(matched)[:6],
        "gaps": sorted(gaps)[:5],
        "pitch_opener": pitch,
    })


from fastapi.responses import FileResponse

@app.get("/")
async def root():
    return FileResponse("index.html")
