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

## Architecture

- `AGENTS.md` - canonical operating contract
- `.agents/skills/pco/SKILL.md` - Codex-compatible skill router
- `.claude/skills/pco/SKILL.md` - Claude Code entry point
- `workflows/search/` - job-search workflows
- `workflows/develop/` - coaching and development workflows
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
