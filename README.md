# nih-aims-panel

A skill that runs a mock NIH study section on a Specific Aims page.

You give it an aims page and a study section. It assigns three reviewers by expertise from that panel's real roster, adds agents for the clusters of members who will vote without writing critiques, and has them all score the page independently under NIH's Simplified Review Framework. It then writes one report: a projected score range, the faults several reviewers caught, the places where reviewers want opposite things (and wording that satisfies both), and a revision plan with before/after rewrites.

The aims page matters this much because it is the one section every member of the panel reads, and Factor 1 (Importance of the Research), which caps the overall impact score, is mostly decided there.

## Usage

Share or paste an aims page and say something like:

- "Run my aims through KURS 82."
- "Mock study section on this SA page, it's an R21 going to Kidney Physiology and Development."
- "How would reviewers see these aims?"

If you don't name a panel, the skill asks which one, plus the mechanism and resubmission status if it can't tell from the page. The report is saved as `<short-name>-mock-review.md`.

To maintain it:

- "Update the study section" or "pull the new KURS 82 roster": finds the newest meeting roster, diffs it against the stored one, re-checks who holds standing (chartered) membership, profiles new members, and repackages the skill.
- "Add the PBKD study section": builds a new panel folder from CSR's scope page and rosters.

Updating relies on the skill-creator skill to repackage. Install the resulting `.skill` file over the old one.

## Available panels

| Panel | Code | Roster | Profiles |
|---|---|---|---|
| Kidney Physiology and Development | ZRG1 KURS-L (82) | 07/22/2026 meeting | 20 of 22 |

## Layout

```
nih-aims-panel/
├── SKILL.md                      workflow that the skill follows
├── README.md                     this file
├── scripts/
│   └── parse_roster.py           parse eRA roster pages to JSON; --diff two rosters
└── references/
    ├── nih-review-criteria.md    1-9 scale, Simplified Review Framework, meeting mechanics
    ├── aims-page-faults.md       numbered checklist of common faults
    ├── reviewer-agent-prompt.md  prompts for assigned-reviewer and room agents
    ├── report-template.md        structure of the final report
    ├── profile-brief.md          how research agents build a reviewer profile
    ├── update-guide.md           refreshing rosters, adding panels, repackaging
    └── study-sections/
        ├── index.md              available panels and aliases
        └── kidney-physiology-development/
            ├── panel.md          scope, boundaries, standing members, clusters, fault lines
            ├── roster.json       parsed roster used for diffs
            └── reviewers/*.md    one profile per member
```

## How the profiles were built

Each profile summarizes public professional information: PubMed records, lab and faculty pages, grant records (mostly through RePORTER-derived listings and paper acknowledgments, because RePORTER itself couldn't be read directly), and public CSR rosters. Standing membership was checked against the chartered PBKD and KUFD membership lists. The "likely reviewing lens" in each profile is inferred from the person's own methods and published rigor standards, and is labeled that way. The profiles contain no personal information.

## Limits

- The reviewers are simulations. They are not the people, and the report says so.
- Rosters change every meeting, so the panel that reviews your application may differ from the stored one. Check the roster date in the report.
- Agents see only the aims page. Their Factor 2 (Rigor and Feasibility) and Factor 3 (Expertise and Resources) judgments are provisional, and they list what the Research Strategy would need to show.
- NIH policy (NOT-OD-22-044) forbids contacting study section members about an application. Use this to improve the science and the writing, not to tailor the page to individuals.

## Sources

- [Scoring System and Procedure](https://grants.nih.gov/grants/peer/guidelines_general/scoring_system_and_procedure.pdf)
- [Simplified Review Framework: Scoring Guidance](https://grants.nih.gov/sites/default/files/Simplified-Review-Scoring-Guidance.pdf)
- [Simplified Peer Review Framework](https://www.grants.nih.gov/policy-and-compliance/policy-topics/peer-review/simplifying-review/framework)
- [KURS(82) at CSR](https://public.csr.nih.gov/StudySections/DPPS/KURS/ZRG1KURS82)
- [07/22/2026 meeting roster](https://public.era.nih.gov/pubroster/preSepIndex.era?CID=101323&AGENDA=563184)
