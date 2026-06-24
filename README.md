# Product Career Ops (PCO)

**PCO** stands for **Product Career Ops**: an agent-first operating system for managing two connected loops in a product leader's career.

1. **Job Search** - evaluate promising roles, decide what to pursue, and create grounded application and interview materials.
2. **Development** - improve product judgment, leadership capability, career evidence, and decision quality over time.

```text
Development builds capability and evidence
              |
              v
Job Search converts them into opportunities
              |
              v
Market feedback reveals gaps and strengths
              |
              v
Development chooses the next growth experiments
```

This public repository contains only fictional demonstration data. The sample candidate, employers, jobs, achievements, and compensation figures are invented composites created to demonstrate the workflow.

## What it can do

```text
/pco search <job URL or pasted description>
/pco search <job screenshot or image path>
/pco search compare
/pco search tracker
/pco search packet <OPP-ID>
/pco search interview <OPP-ID>
/pco search offer <OPP-ID>

/pco develop coach <problem or decision>
/pco develop weekly
/pco develop quarterly
/pco develop career-plan
/pco develop evidence
/pco develop skill-gap
```

For screenshot intake, the agent reads visible clues, locates the authoritative employer posting, verifies the match, captures the full description, and runs the normal Search evaluation. Ambiguous matches must be shown to the user rather than guessed.

## Try the fictional demo

The `demo/` directory includes:

- a fictional senior product leader profile and résumé
- a structured evidence bank
- three fictional job descriptions
- ready-to-run opportunity scorecards and packet inputs
- `product-career-ops-demo.xlsx`, a populated read-only example of the tracker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

pco demo-init
pco opportunity add --input demo/opportunities/northstar-health.json
pco opportunity add --input demo/opportunities/kinetic-robotics.json
pco opportunity add --input demo/opportunities/signalcare-ai.json
pco opportunity list
```

To generate a packet:

```bash
pco packet build \
  --id OPP-0001 \
  --input demo/packets/northstar-health.json
```

`pco demo-init` will not overwrite an existing `private/` directory unless you explicitly pass `--force`.

## Use it with your own career data

1. Run `pco demo-init`.
2. Replace the fictional files in `private/` with your own profile, résumé, evidence, and job sources.
3. Run `pco reset --confirm RESET` to rebuild the canonical workbook.
4. Use `/pco search` when a role excites you and `/pco develop` for ongoing coaching and growth.

The canonical database is `private/product-career-ops.xlsx`. All writes are validated, backed up, audited, and atomically saved through the Python infrastructure.

## Recommended setup: separate the engine from your data

Keep **two repositories**, split on *code vs. data* — not on public vs. private branches:

- **This repo (public):** the engine and fictional demo. It never contains your real data. Clone it, pull updates, and contribute improvements here.
- **A separate private repo (yours):** *only* your real career files — `profile.yml`, `resume.md`, `evidence.*`, `sources.yml`, and your `product-career-ops.xlsx`. No engine code.

> ⚠️ A "private branch" of a public repo does **not** keep anything private. On GitHub every branch of a public repo is public, and forks of public repos are public too. The only reliable boundary is a separate **private repository**. Splitting on code vs. data means the two repos hold different kinds of files and physically can't cross-contaminate.

`private/` is already in `.gitignore`, so the simplest wiring is to make `private/` itself a clone of your private data repo:

```bash
# 1. Clone the public engine
git clone https://github.com/<you>/product-career-ops.git
cd product-career-ops

# 2. Create a separate PRIVATE repo on GitHub for your data, then make
#    the gitignored private/ folder a clone of it
git clone https://github.com/<you>/product-career-ops-data.git private

# 3. Populate and build
pco demo-init          # scaffolds private/ if empty (won't overwrite without --force)
# ...replace the files in private/ with your real data...
pco reset --confirm RESET
```

Now you commit engine changes in the outer repo and your career data in `private/` — they never touch. Pull tool updates with a normal `git pull` in the outer repo; your private data lives in its own repo underneath and is untouched.

Before publishing any customized version of the **engine**, always run `pco export-public` (see Privacy below) so no real identifiers leak into the public repo.

## Resource library

A curated product-management resource library lives in [`docs/resources/`](docs/resources/README.md)
to support the development loop:

- [Books](docs/resources/books.md)
- [Newsletters & Podcasts](docs/resources/newsletters-and-podcasts.md)
- [Frameworks & Mental Models](docs/resources/frameworks.md)
- [Courses & Communities](docs/resources/courses-and-communities.md)
- [AI Product Management](docs/resources/ai-product-management.md)
- [Regulated, MedTech & Digital Health](docs/resources/regulated-and-digital-health.md)
- [LennyHub RAG](docs/resources/lennyhub-rag.md)

## Architecture

- `AGENTS.md` - canonical operating contract
- `.agents/skills/pco/SKILL.md` - Codex-compatible skill router
- `.claude/skills/pco/SKILL.md` - Claude Code entry point
- `workflows/search/` - job-search workflows
- `workflows/develop/` - coaching and development workflows
- `docs/resources/` - curated product-management resource library
- `pco/` - validated workbook, scoring, packet, privacy, and export infrastructure
- `demo/` - fictional public example data

Agents perform research and judgment. Scripts perform controlled state changes.

## Privacy

Never store credentials, patient information, confidential employer data, unreleased roadmaps, or unsupported career claims. Run:

```bash
pco export-public
```

before publishing a customized version. The exporter fails closed when it detects private identifiers or prohibited files.

## License

MIT. See [LICENSE](LICENSE).
