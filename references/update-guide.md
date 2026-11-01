# Updating the skill

Two jobs: refresh an existing study section's roster and profiles, or add a new study section. Both end with repackaging the skill so the changes persist.

The installed skill directory is read-only. Copy it to a writable working folder first (e.g., `cp -r <skill dir> <outputs>/nih-aims-panel`), do all edits there, then repackage.

## Finding the right roster pages

- CSR study section page: `https://public.csr.nih.gov/StudySections/<Division>/<Branch>/<Section>` (for SEPs the section part looks like `ZRG1KURS82`). Each page lists "List of Reviewers on <date>" links to the meeting rosters. CSR announced its site moves into grants.nih.gov in November 2026; if these paths 404, search "<panel name> CSR study section roster" and look for the new location.
- SEP meeting roster: `https://public.era.nih.gov/pubroster/preSepIndex.era?CID=101323&AGENDA=<id>` (CID 101323 is ZRG1, CSR's SEP umbrella). SEP rosters do not mark temporary members; everyone on an SEP is technically temporary for that meeting.
- Chartered meeting roster: `https://public.era.nih.gov/pubroster/preRosIndex.era?AGENDA=<id>&CID=<cid>`. A "*" marks temporary members; names without it are standing members.
- Chartered membership list (current terms): `https://public.era.nih.gov/pubroster/roster.era?CID=<cid>`. "(27)" after a name means the term ends 6/30/2027.
- Meeting list for a chartered section by year: `https://public.era.nih.gov/pubroster/standingCommitteRoster.era?CID=<cid>&YEAR=<yyyy>` (the misspelling "Committe" is real).
- Roster index: `https://public.era.nih.gov/pubroster/rosterIndex.era`.
- Known CIDs: PBKD 102470, KUFD 105220 (ended 2026), KEDD 105433, ITA 105774, IVPP 105269.

Rosters are posted about 30 days before a meeting. Use web_fetch (the shell sandbox usually cannot reach nih.gov). web_fetch caches pages for an hour; if it says a page was "already fetched" and you do not have the content, append a harmless query parameter (e.g., `&v=2`).

## Refresh an existing section

1. Read the section's `panel.md` to get its CSR page and the related chartered CIDs.
2. Fetch the CSR page and find the newest "List of Reviewers" link. If it is the same meeting already in `roster.json`, tell the user nothing new has been posted and stop (unless they asked to re-research existing profiles).
3. Fetch the new roster, save the text to a file, and parse it:
   `python3 scripts/parse_roster.py roster_page.txt --url <url> -o new_roster.json`
4. Diff against the old roster:
   `python3 scripts/parse_roster.py new_roster.json --diff references/study-sections/<folder>/roster.json`
5. Re-check standing status. Fetch each related chartered membership roster (`roster.era?CID=...`) and note which members appear and their term years. Check the CSR page's "Shared Interests and Overlaps" section for newly listed neighbor panels and add their CIDs to panel.md. If the SEP has been replaced by a chartered section, record the new code, CID and scope.
6. Profile new members. Spawn research agents in parallel, three or four people per agent, each told to read `references/profile-brief.md` and write to the section's `reviewers/` folder. Give each agent the exact roster lines for its people. Also offer to finish any profiles that panel.md lists as "not profiled."
7. Departed members: move their profiles to `reviewers/former/` rather than deleting them. Members often rotate back, and the profile is expensive to rebuild.
8. Update `panel.md`: roster table, standing-members table, cluster assignments (place new people into the existing clusters A-F or add a cluster if a new area appears), panel dynamics if the balance shifted, scope text if CSR changed it, and an Update log line with the date and what changed. Replace `roster.json` with the new one. Update the row in `study-sections/index.md`.
9. Spot-check two or three new profiles yourself: identity match (common names collide), PMIDs resolve, and no personal or non-professional details.
10. Repackage (below).

## Add a new study section

1. Ask the user for the panel name or code if not given, and find its CSR page. Read the scope, topics and "Shared Interests and Overlaps." Note whether it is chartered (has a `roster.era?CID=` membership list) or an SEP.
2. Get the most recent meeting roster and, for chartered panels, the membership list. Parse both with `scripts/parse_roster.py`.
3. Create `references/study-sections/<kebab-name>/` with `panel.md`, `roster.json` and `reviewers/`. Use `kidney-physiology-development/panel.md` as the model for panel.md's sections.
4. Identify standing members: for chartered panels, everyone on the membership list; for SEPs, cross-check members against the chartered rosters of the neighbor panels named on the CSR page.
5. Profile members with parallel research agents as above. For large rosters (30+), profile standing members first, then the rest.
6. Group members into 4-7 perspective clusters by shared methods and rigor standards (not just topic), and write the cluster archetypes, panel dynamics and fault lines from the profiles. Mark anything inferred as inferred.
7. Add a row to `study-sections/index.md`.
8. Repackage.

## Repackage

Use the skill-creator skill's packager so the updated skill can be reinstalled:

```bash
cd <skill-creator dir> && python -m scripts.package_skill <path to working copy of nih-aims-panel>
```

Present the resulting `nih-aims-panel.skill` to the user with present_files; the card's "Save skill" button installs it over the old version. Tell the user in one or two sentences what changed (who joined, who left, standing-status changes, new sections).

Note: saving only SKILL.md through a save-skill tool does not carry the references folder, so always deliver the packaged `.skill` file for updates.
