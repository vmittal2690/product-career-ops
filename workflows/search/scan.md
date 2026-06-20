# Search: scan

Read `private/sources.yml`.

1. Run configured public ATS providers:

```bash
python -m pco scan
```

2. Deduplicate discovered roles.
3. Evaluate plausible product-leadership roles using `evaluate.md`.
4. Add all evaluated roles to the workbook.
5. Active threshold is 80/100; archive the remainder with reasons.
6. Summarize new Active roles and notable rejection patterns.

Never auto-apply.

