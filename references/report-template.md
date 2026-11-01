# Mock review report template

Write the final report as Markdown in this order. The applicant reads the first screen and decides whether to keep going, so put the verdict and the top fixes first and the per-reviewer detail last.

```markdown
# Mock study section: {short project title}
{Panel name} ({code}) · roster from {meeting date} · simulated {today}

## Bottom line
Three to five sentences: predicted outcome (discussed or likely ND; impact score range as e.g. "30-45"), the one thing that most limits the score, and the one change most likely to move it. State plainly that this is a simulation built from public information, not a prediction of the real panel.

## Simulated scores
| Reviewer | Role | Standing? | Factor 1 | Factor 2 | Factor 3 | Impact |
|---|---|---|---|---|---|---|
| ... | R1 | yes/no | n | n | Appropriate/Gaps | n |
Room clusters: one line each with their gut Factor 1 range.
Projected panel range: x-y (impact score x10: xx-yy). Explain in one sentence how you got there (assigned reviewers' range, adjusted by where the room clusters would likely vote).

## Common faults
Faults raised independently by two or more reviewers or clusters. For each: what it is, who raised it, the quoted sentence from the aims page, and the fix. Order by how much score it costs.

## Conflicting demands and how to satisfy both
Where reviewers want opposite things (e.g., more mechanism vs more translation; mouse vs rat; one more model vs smaller scope). For each, the specific wording or design choice that gives each side what it needs at the least cost in page space. Name the fault lines from panel.md that this application touches.

## Revision plan
Numbered, most score-moving first. Each item: the edit, which reviewers it wins, and roughly how much it could move their scores. Include at least one concrete rewrite (hypothesis sentence, aim title, or gap statement), shown as before -> after.

## Fit and assignment
Is KURS(82) (or the chosen panel) the right home? Mention any boundary risk from panel.md and, if relevant, what to request in the assignment request form or cover letter. Who is most likely to be assigned (by expertise), with the caveat that the real roster changes each meeting.

## Discussion simulation
A short narrative (150-300 words) of how discussion would likely go: R1's opening, where R2/R3 agree or push back, which room cluster speaks up, and where the chair steers. Keep it grounded in the critiques.

## Individual critiques
The full critique of each assigned reviewer, then each room cluster, as written by the agents (lightly cleaned for length; keep scores and quotes intact).

## Caveats
- Built from public publications, lab pages and grant records; reviewer lenses are inferred, not known.
- The roster is from {date}; the panel that reviews your application may differ. Unprofiled members: {list}.
- Simulated from the aims page alone; Factor 2 and Factor 3 judgments are provisional.
- NIH policy (NOT-OD-22-044) forbids contacting study section members about an application. Use this to improve the science and the writing, not to tailor the page to individuals (for example, do not cite someone's work unless it is directly relevant).
```

Style: plain declarative sentences, specific nouns, no hype. Quote the aims page when criticizing it. No em dashes.
