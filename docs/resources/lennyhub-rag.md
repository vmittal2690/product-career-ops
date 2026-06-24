# LennyHub RAG

External transcript and RAG reference for product leadership, growth, and career
development questions.

## Source

- **Your fork:** [vmittal2690/lennyhub-rag](https://github.com/vmittal2690/lennyhub-rag)
- **Upstream:** [mgbotoe/lennyhub-rag](https://github.com/mgbotoe/lennyhub-rag)
- **License:** Apache-2.0 for the repository
- **Data shape:** 297 podcast transcript text files under `data/`, plus RAG tooling for
  Qdrant, LightRAG, Streamlit, and graph exploration

## How to pull the data locally

Keep this dataset outside the public Product Career Ops engine repo and treat it as
reference material:

```bash
git clone https://github.com/vmittal2690/lennyhub-rag.git ../lennyhub-rag
```

Then point development work at:

```text
../lennyhub-rag/data/
```

## How to use it with Product Career Ops

- Use `develop coach` for specific live decisions where a Lenny's Podcast guest has
  relevant operating experience.
- Use `develop skill-gap` to find transcript-backed examples for product strategy,
  growth, leadership, decision quality, and career development.
- Cite the transcript filename and source repository when a recommendation depends on
  this dataset.
- Do not copy raw transcript text into public application packets, resumes, or interview
  materials; summarize the principle in your own words and link to the source repo when
  provenance matters.

## Good starter queries

- What product leadership behaviors show up repeatedly across high-growth companies?
- What career decision frameworks appear in the transcripts?
- Which examples are most relevant to product leaders moving into AI, health, or platform
  roles?
- What patterns distinguish strong product strategy from feature-level execution?
