# Brief for reviewer-profile research agents

Practical notes from the first build (Nov 2026): the shell sandbox usually cannot reach nih.gov or NCBI, so use the PubMed MCP tools and web_fetch rather than curl. NIH RePORTER pages are JavaScript and its API is POST-only, so web_fetch returns nothing useful; institutional profile pages (Profiles RNS sites list NIH grants), grant acknowledgments in papers, and RePORTER-derived aggregators are workable substitutes. Label the provenance of every grant number. eRA pubroster pages do render through web_fetch. If a fetch is blocked or refused, do not try to get around it; use another source and note the gap.

These profiles feed a skill that simulates an NIH study section critiquing a Specific Aims page. When the skill runs, an agent will role-play each reviewer, so the profile has to tell that agent what this person knows deeply, what they work on, what methods they trust, and what they are likely to push on when reading someone else's aims. Accuracy matters more than color: every factual claim should come from a source you actually read. Mark inferences about reviewing style as inferences.

The panel name, code, meeting date and output directory are given in the prompt that sent you here. Write profiles into `references/study-sections/<panel-folder>/reviewers/`.

Before searching, read the panel's `panel.md` if it exists, and check the chartered rosters it lists: if this person appears on a chartered CSR roster (`roster.era?CID=...`, where "(27)" means the term ends 6/30/2027), record that as standing membership. Chartered meeting rosters mark temporary members with "*"; a name without "*" on a chartered meeting roster is a standing member.

## How to research each person

1. Confirm identity first. Common names collide (there are many "Jane Yu"s). Match the institution and department on the roster to the person's PubMed affiliations and lab page.
2. PubMed: use the PubMed MCP tools if available (load them with ToolSearch, query "pubmed"), otherwise WebSearch + web_fetch on pubmed.ncbi.nlm.nih.gov. Pull their publication list, focusing on the last ~8 years plus their most cited/defining papers. Read abstracts of at least 10-15 representative papers, more for senior people.
3. Lab / faculty web page and any lab website: research mission, current projects, techniques.
4. NIH RePORTER (https://reporter.nih.gov, or the API https://api.reporter.nih.gov/v2/projects/search via web_fetch if allowed; otherwise WebSearch "<name> RePORTER"): active and recent grants, mechanisms (R01, U01, K, P30, etc.), which institute (NIDDK, NHLBI...), titles. This shows what they get funded for and how they frame work.
5. Note any evidence of study section service: is this person a chartered (standing) member of a CSR study section? Search "<name> chartered member study section" or check CSR rosters on public.era.nih.gov/pubroster. Record what you find, even if just "no evidence found".
6. Optional: editorial roles, society leadership (ASN, APS), awards, clinical trials (ClinicalTrials.gov) if they do clinical research.

Do NOT include personal/non-professional information (family, home, social media life). Professional public record only.

## Output: one Markdown file per person

File name: `<lastname>.md` lowercase, hyphenate multiword surnames (e.g., `arroyo-ornelas.md`, `pastor-soler.md`, `roy-chaudhury.md`). Write with the Write tool to the directory this brief is in.

Use exactly this structure:

```markdown
# LASTNAME, Firstname M., DEGREES

- Roster role: Chair | Member
- Position: (title, division, department, institution as on roster)
- Career stage: (early / mid / senior; years since first independent paper if you can tell)
- Standing-member status: (chartered member of X study section, term dates, source) or "No evidence of chartered CSR membership found; likely temporary/ad hoc for this SEP"
- Primary NIH funding: (institute, mechanisms, 1-line titles with RePORTER project numbers)

## Research focus
3-6 sentences. The questions they ask, organ/cell type, disease.

## Model systems and methods
Bulleted list: organisms, mouse lines, cell systems, human cohorts, techniques (e.g., micropuncture, single-cell RNA-seq, patch clamp, ciliary imaging, registry epidemiology, RCTs).

## Representative publications
8-15 entries: Authors (first, ..., theirs), Title, Journal Year. PMID. One line on why it matters to their perspective.

## Expertise keywords
Comma-separated list of 15-30 specific terms that would appear in an aims page this person would be assigned (genes, pathways, cell types, diseases, methods). Used for reviewer matching.

## Likely reviewing lens (inferred)
Bullets, each grounded in the evidence above:
- What they will value (rigor standards from their own work, e.g., "uses sex as a biological variable in all rodent studies", "large prospective cohorts with hard outcomes")
- What they will scrutinize hardest in an aims page in their area (e.g., cilia-localization claims without super-resolution, Cre-driver specificity, clinical endpoint choice, confounding in observational data)
- Where they are an outsider (topics they would read as a generalist)
- Likely questions they'd raise at the table

## Sources
Bulleted URLs you actually read.
```

When done with all your assigned people, reply with a short summary: each file written, confidence in identity match (high/medium/low), and anything notable (e.g., found evidence of standing membership on a chartered panel, or could not confirm identity).
