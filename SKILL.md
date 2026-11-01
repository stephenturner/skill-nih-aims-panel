---
name: nih-aims-panel
description: Run a mock NIH study section on a Specific Aims page. Parallel reviewer agents, each modeled on a real roster member's published work, critique and score the page under NIH's Simplified Review Framework (Factor 1/2/3, 1-9 scale), then a synthesis names common faults, conflicting demands and a revision plan that pleases the most reviewers. Use this whenever someone shares or pastes an aims page or says "specific aims," "SA page," "mock review," "mock study section," "how will reviewers see this," "will this score," "critique my aims," or names a CSR study section (e.g., KURS 82, Kidney Physiology and Development) with a grant draft, even if they don't say "skill." Also use it to update itself, e.g. "update the study section," "refresh the roster," "pull the new roster," "add study section X," or "profile the new reviewers."
---

# NIH Specific Aims mock panel

The aims page is the one part of an application every member of the study section reads, and Factor 1 (Importance of the Research), which caps the overall score, is decided there. This skill rehearses that read. Assigned-reviewer agents built from real roster members' public work write critiques the way a summary statement would. Cluster agents stand in for the rest of the room, which votes after skimming the page. Then everything is merged into one report the applicant can act on.

There are two modes: **Review**, the default, and **Update**, used when the user asks to refresh rosters, add a study section, or profile reviewers. For Update, read `references/update-guide.md` and follow it.

## Files

- `references/study-sections/index.md`: which panels are available, with aliases. Read it first.
- `references/study-sections/<folder>/panel.md`: scope, boundaries, standing members, roster table with clusters, room dynamics and fault lines. Read it fully for the chosen panel.
- `references/study-sections/<folder>/reviewers/<slug>.md`: one profile per member. Agents read these. You only need to skim the ones you are considering for assignment.
- `references/nih-review-criteria.md`: scoring rules, how meetings work, what can be judged from an aims page alone, and how mechanisms differ.
- `references/aims-page-faults.md`: numbered checklist of common faults.
- `references/reviewer-agent-prompt.md`: prompt templates for the agents.
- `references/report-template.md`: structure of the final report.
- `references/update-guide.md` and `references/profile-brief.md`: for Update mode.
- `scripts/parse_roster.py`: parses eRA roster pages and diffs two rosters.

## Review mode

### 1. Get the aims page

Accept a file (.docx, .pdf, .md, .txt) or pasted text. Convert it to plain text and save it as `aims.txt` in a working folder: use `pandoc` or python-docx for .docx and `pdftotext -layout` for .pdf. Check that the text came through whole (aim headings present, roughly 400-700 words for one page). If there is no aims page, ask for one; there is nothing to review without it.

### 2. Settle the study section and application facts

If the user named a panel, match it against `index.md` aliases. If not, ask with AskUserQuestion. List the available panels, add an option for "another panel (I'll add it)," and in the same call ask anything you can't infer from the page: mechanism (R01, R21, K, F...), new or resubmission, and ESI status if it matters. Skip a question whenever the page or the user's message already answers it. If the user picks a panel that isn't built yet, offer to build it in Update mode, or to run a generic review with criteria-only reviewers (no roster). Say which one you're doing.

Once the panel is chosen, read its `panel.md`. Compare the aims page with the panel's scope and boundary notes. If the page reads like a neighboring panel's territory, that's a finding for the report's "Fit and assignment" section. Don't refuse to review it.

### 3. Choose the panel for this application

Real SROs assign about three reviewers by expertise. Do the same:

- R1: the member whose profile best matches the page's core system and methods. Use the expertise keywords and the "Model systems and methods" section.
- R2: the next best match, preferably from a different cluster, so the critique covers a second angle (mechanism vs. translation, cell vs. whole animal).
- R3: someone with adjacent but not identical expertise. They play the informed outsider who often decides whether the application gets discussed.
- Break ties toward standing members (listed in panel.md). They review kidney applications every cycle and calibrate the room.
- Skip members marked "not profiled" for assigned roles. Don't make up expertise for them.

Room agents: pick the 2-4 clusters from panel.md that the assigned reviewers don't already cover, favoring the clusters most likely to vote against the page's grain (for a basic mechanism page, the clinical clusters; for a clinical page, the mechanism clusters). Always include the cluster that contains the Chair, because the Chair frames the discussion.

Tell the user in one line who you picked and why before launching. For example: "R1 Park (nephron progenitors, Cre lineage), R2 Rauchman (chromatin in progenitors), R3 Lin (low nephron number); room: clinical trials, transplant, transport physiology."

### 4. Launch the agents in parallel

Make a working folder `mock-review-<short-name>/` with `aims.txt` and a `critiques/` subfolder. Fill the templates in `references/reviewer-agent-prompt.md` (A for assigned reviewers, B for room clusters) with absolute paths and the application facts. Send every Agent call in a single message so they run concurrently and stay independent. Their value comes from not seeing each other's work.

Without a subagent tool, follow section C of the prompt file and say so in the report.

### 5. Synthesize

Read every critique, then write the report following `references/report-template.md`. Most of the value is in this step, so don't paste critiques together:

- **Projected range.** Start from the assigned reviewers' Overall Impact scores. Adjust by where the room clusters say they'd vote. Factor 1 sets the ceiling. Most real scores land within a point of the assigned range, so if your projection moves further than that, explain why.
- **Common faults.** A fault counts as common when two or more agents raised it independently. Faults raised from different clusters count most. Quote the aims sentence. Rank by score cost.
- **Conflicting demands.** Find where reviewers want opposite things, and check the panel's fault lines in panel.md. For each, write wording or a design choice that satisfies both sides at the lowest page cost. This is how to "please as many as possible." Usually it means one sentence that names the mechanism and one that names the clinical consequence, or a design choice (both sexes, a second model, a named collaborator) that disarms several critics at once.
- **Revision plan.** Make the edits concrete and include before→after rewrites of the hypothesis, the gap statement, or an aim title. An applicant should be able to revise the page from this section alone.
- **Discussion simulation.** Keep it short and grounded in what the critiques actually say.

Save the report to the outputs folder as `<short-name>-mock-review.md` and present it. In the reply, give the projected range, the top two fixes, and the file. Keep it to a few sentences, since the report holds the detail.

### Writing style for everything the skill produces

Plain, specific, declarative sentences. Quote the page when criticizing it. Use numbers where you have them. No em dashes, no filler openers, no "it's worth noting." When a judgment is inferred from a reviewer's publications rather than known, call it that.

## Honesty and integrity

- The agents are simulations built from public professional records. They are not the people, and the report has to say so. Never put words in a real person's mouth beyond what the profile supports, and never add personal (non-professional) details.
- The roster that reviews the user's application may differ from the one on file. Give the roster date in the report.
- NIH policy (NOT-OD-22-044) forbids applicants from contacting reviewers about an application. If the user asks for help reaching out to a panel member, or for ways to flatter specific people, decline that part and steer back to improving the science and the writing.
- Don't predict percentiles or funding. Paylines vary by institute and year.

## Update mode (summary)

Follow `references/update-guide.md`. In short: find the newest roster on the panel's CSR page, parse and diff it with `scripts/parse_roster.py`, re-check standing status against the chartered rosters, profile new members with parallel research agents using `references/profile-brief.md`, move departed members to `reviewers/former/`, update panel.md, roster.json and index.md, then repackage the skill with skill-creator's `package_skill` script and present the `.skill` file so the user can reinstall it.
