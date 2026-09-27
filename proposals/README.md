# Post-Nubank CV refresh — content proposal

The canonical CV currently starts with Nubank, ending on 2025-09-12. This proposal adds the subsequent work without inferring a start date or assigning a formal seniority level.

## Review snippets, then apply

`post-nubank.json` is a proposal, not a complete JSON Resume file and not an automatically applied patch. The application's `*.resume.json` loader does not load this file. Following the content-change protocol in `AGENTS.md`, the canonical JSON remains unchanged for owner review.

The proposal contains:

- `basicsPatch`: replace only the corresponding keys in `basics`; preserve contact details and profiles.
- `workToPrepend`: add the current SitesPay role at the beginning of `work` after confirming the start date, public title and proposed scope. The title is a functional description, not a confirmed contractual title. Empty dates are unresolved fields, not an invented employment chronology.
- `workUpdates`: locate Nubank by company and start date and replace only the supplied fields. Existing dates remain unchanged; completed-role prose is in the past tense.
- `projectsToPrepend`: optional project snippets, kept separate from employer work. Select projects for the intended CV; no commercial adoption or ownership transfer is asserted.
- `metaPatch`: review the job limits before copying them into `meta`. Six slots preserve the current role, Nubank, Sofía, both Covalto entries and Credijusto in the existing ordering. This can require more than one page.

No private source notes, unverified launch, monetary migration figure, comparative ranking or performance metric are introduced.

## Template fixes

The compact templates now use `basics.summary`; they no longer substitute hard-coded promotional text or a fixed 2025 experience calculation. They render skill groups directly, so Clojure and future groups are not silently dropped by keyword whitelists.

`meta.atsJobLimit` and `meta.projectsJobLimit` control the respective visible-role limits. Defaults remain 4 and 5; 0 includes all visible roles. Both `hide` and `resumeHide` remain respected. A visible note indicates when additional roles have been omitted. Optional `resumeSummary` and `resumeHighlights` support concise copy without replacing full-CV detail.

The projects view inherits the ATS header, summary and skills rather than maintaining a second copy. Existing full-CV and screen templates are unchanged.

## Verification and release

Run the template regression tests with:

```bash
uv run python -m unittest discover -s tests -p 'test_resume_templates.py' -v
```

These tests exercise Jinja rendering, data selection and escaping. They are not browser/PDF layout tests. The existing one-page ATS / two-page projects assertions still require a real build after content approval; do not infer page count from HTML tests.

This change does not regenerate `docs/`, overwrite `docs/resume.pdf`, modify the static site, or merge/publish the proposed CV. The existing build/clean rules conflict with the protected external `docs/resume.pdf`; use a disposable checkout or back up that asset before invoking those targets. That build-policy repair is separate from this focused content/template change.
