# Search: evaluate a role

## Inputs

- Job URL, pasted description, local text file, screenshot, or local image path
- `private/profile.yml`
- `private/evidence.md`
- current workbook records

## Workflow

1. Capture the complete role and verify it appears active.
   - For an image, extract visible identifiers: company, title, location, work model, compensation, posting age, and distinctive job-description phrases.
   - Search the employer's official careers site and official ATS for the role.
   - Confirm the match using at least two identifiers. Company + title is required; location, compensation, or distinctive text should provide the second confirmation.
   - Do not infer a URL from title alone when multiple postings are plausible.
   - Save the complete authoritative job description as Markdown under `outputs/search/<OPP-ID>/` after the opportunity ID is assigned.
   - Record the original screenshot path as provenance, but do not copy a user's photo-library asset into the repository.
2. Research the company, product, leadership, market, and recent material developments from public sources.
3. Evaluate the actual mandate, not merely the title.
4. Score each weighted dimension from 0 to its maximum:
   - mandate and decision authority: 20
   - target-role alignment: 15
   - product and clinical/domain fit: 15
   - scope and organizational leadership: 15
   - evidence match: 10
   - strategic career growth: 10
   - company and product quality: 5
   - commercial upside: 5
   - practical constraints: 5
5. Explain the evidence, gaps, risks, assumptions, and diligence questions.
6. Create a structured JSON input and call:

```bash
python -m pco opportunity add --input <json-file>
```

7. A score of 80 or above becomes Active. Lower scores become Archived.
8. If the user asks for materials, call `python -m pco packet build --id <OPP-ID>`.

## Required outputs

- concise recommendation
- 100-point score and dimension table
- evidence map
- risks and unknowns
- diligence questions
- workbook opportunity ID
- authoritative job URL and saved job-description path
- screenshot-to-posting match confidence and the identifiers used
