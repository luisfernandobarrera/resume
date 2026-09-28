# Post-Nubank CV refresh — content proposal

The canonical CV currently starts with Nubank, ending on 2025-09-12. This proposal adds the subsequent work without inferring chronology or assigning an unconfirmed seniority level.

## Confirmed current-role facts

The owner confirmed the start date as **2025-12-15** and described the role as **Manager de ingeniería de desarrollo y Arquitecto**, with substantial hands-on coding assisted by AI. The proposed English rendering is **Engineering Manager & Software Architect**; it does not introduce a Principal, Staff or Director title.

The owner also approved mentioning **PayGlobal** and **a treasury ERP with banking connectivity**. These appear as current design/development work, not as claims of a completed launch, customer adoption or measured business impact. No legal employer name beyond the existing SitesPay work context is inferred.

The date, role and permission to name these projects are no longer outstanding questions. Remaining owner review concerns final profile wording and independent-project selection.

## Review snippets, then apply

`post-nubank.json` is a proposal, not a complete JSON Resume file and not an automatically applied patch. The application's `*.resume.json` loader does not load this file. Following the content-change protocol in `AGENTS.md`, the canonical JSON remains unchanged for owner application.

The proposal contains:

- `confirmedRoleFacts`: the owner's factual confirmation and the corresponding English title; editorial provenance, not a JSON Resume field to copy.
- `basicsPatch`: replace only the corresponding keys in `basics`; preserve contact details and profiles.
- `workToPrepend`: the confirmed SitesPay role to add at the beginning of `work`. The empty `endDate` means the role is current; the start date is known.
- `workUpdates`: locate Nubank by company and start date and replace only the supplied fields. Existing dates remain unchanged; completed-role prose is in the past tense.
- `projectsToPrepend`: optional independent-project snippets, kept separate from employer work. No commercial adoption or ownership transfer is asserted.
- `metaPatch`: review job limits before copying into `meta`. Six slots preserve SitesPay, Nubank, Sofía, both Covalto entries and Credijusto in the existing ordering. This can require more than one page.

PayGlobal and the treasury ERP belong under SitesPay experience, not in a list that implies personal ownership. Selection of other projects must distinguish a repository's documented scope from deployed results and individual attribution.

## Template fixes

The compact templates use `basics.summary`; they no longer substitute hard-coded promotional text or a fixed 2025 experience calculation. They render skill groups directly, so Clojure and future groups are not silently dropped by keyword whitelists.

`meta.atsJobLimit` and `meta.projectsJobLimit` control visible-role limits. Defaults remain 4 and 5; 0 includes all visible roles. Both `hide` and `resumeHide` remain respected. A note indicates when additional roles have been omitted. Optional `resumeSummary` and `resumeHighlights` support concise copy without replacing full-CV detail.

The projects view inherits the ATS header, summary and skills. Existing full-CV and screen templates are unchanged.

## Verification and release

Run the template regression tests with:

```bash
uv run python -m unittest discover -s tests -p 'test_resume_templates.py' -v
```

The proposal regression now checks the confirmed start date, title, present-role display, PayGlobal/treasury scope and hands-on AI-assisted work. The missing-date fixture remains separate to test rendering when a different role genuinely lacks a start date.

Targeted JSON and date-macro smoke checks were executed for this content revision. The full template suite and PDF build were not rerun in this revision. HTML checks do not establish browser layout or PDF pagination; page budgets require a real build after content application.

This change does not regenerate `docs/`, overwrite `docs/resume.pdf`, update the static site or merge the PR. The existing build/clean rules conflict with the protected external `docs/resume.pdf`; use a disposable checkout or back up that asset before invoking those targets. That build-policy repair remains separate from this content update.
