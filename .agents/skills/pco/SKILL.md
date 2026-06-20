---
name: pco
description: Product Career Ops command center for product-leadership job search and continuous development
arguments: mode
user_invocable: true
user-invocable: true
argument-hint: "[search | develop] [command or URL]"
---

# /pco router

Read `AGENTS.md` before executing a workflow.

## No arguments

Display:

```text
Product Career Ops

Job Search
  Evaluate an exciting role and decide whether to pursue it
  /pco search <URL or pasted JD>

Development
  Strengthen product judgment, leadership capability, and career evidence
  /pco develop
```

## Search routes

| Input | Workflow |
|---|---|
| `/pco search <URL or JD>` | `workflows/search/evaluate.md` |
| `/pco search <screenshot or image path>` | `workflows/search/evaluate.md` |
| `/pco search scan` | `workflows/search/scan.md` |
| `/pco search compare` | `workflows/search/compare.md` |
| `/pco search tracker` | `workflows/search/tracker.md` |
| `/pco search packet <OPP-ID>` | `workflows/search/packet.md` |
| `/pco search interview <OPP-ID>` | `workflows/search/interview.md` |
| `/pco search offer <OPP-ID>` | `workflows/search/offer.md` |

If the input is a job URL, job screenshot, local image path, or clearly a job description without the word `search`, route to `workflows/search/evaluate.md`.

## Development routes

| Input | Workflow |
|---|---|
| `/pco develop` | Show the Development menu |
| `/pco develop coach <problem>` | `workflows/develop/coach.md` |
| `/pco develop weekly` | `workflows/develop/weekly.md` |
| `/pco develop quarterly` | `workflows/develop/quarterly.md` |
| `/pco develop career-plan` | `workflows/develop/career-plan.md` |
| `/pco develop evidence` | `workflows/develop/evidence.md` |
| `/pco develop skill-gap` | `workflows/develop/skill-gap.md` |

Leadership problems, difficult decisions, and requests for coaching route to `coach`.

## State changes

Never edit the workbook directly. Use `python -m pco` commands described by each workflow.
