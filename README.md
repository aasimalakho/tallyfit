---
title: Tallyfit
emoji: 🟢
colorFrom: green
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# Tallyfit

**A scorecard for people who bid for a living.**

Every freelance proposal costs something — a credit, time, a little hope.
Tallyfit reads your CV and a job description, scores how well they actually
match, and hands you a ready-to-use opening line — before you spend any of
it on a job that isn't worth it.

## What it does

- Upload your CV (PDF, DOCX, or TXT) — parsed entirely in your browser
- Paste any job description — title, requirements, all of it
- See live skill detection as you type, before you even click anything
- Get a fit score, what's aligned, what's missing, and a pitch opener for
  your proposal

## How it works

Tallyfit is **pure rule-based skill matching** — no AI model, no API key,
no inference cost, and no hallucination risk. It compares your CV against
the job description using a curated vocabulary of ~140 skills, tools, and
domains (with synonym handling, e.g. "ML" → "machine learning"), and scores
the overlap as a real percentage. Every matched skill and every flagged gap
is guaranteed to actually appear in the text — nothing is inferred or
invented.

## Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, vanilla JavaScript (pdf.js for PDF parsing,
  Mammoth.js for DOCX parsing)
- **Deployment:** Docker, hosted on Hugging Face Spaces

## Who it's for

Freelancers on Upwork, Fiverr, and similar platforms who want a fast,
honest gut-check before spending a proposal credit on a job that might
not be worth it.

## Built for

[Mind the Product's World Product Day: Everyone Ships Now](https://aihackathon.devpost.com) hackathon, June 2026.

