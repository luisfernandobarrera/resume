# Post-Nubank CV update — content proposal

Status: draft for owner review. Canonical JSON and generated site/PDFs are unchanged.

## Scope

Update the professional headline, short summary and full About text; keep Nubank as a completed role; prepend the current SitesPay work context; and explicitly select the important recent positions for both short resume variants.

The proposed wording describes systems architecture, financial/business domain modeling, direct engineering and team collaboration. It does not confer a Principal/Staff/Director title, claim a product launch, report adoption, promise quantified savings or attribute every team/AI contribution to one person.

## Reviewable JSON

`post-nubank.json` is an RFC 6902 JSON Patch proposal, not a replacement resume document. It starts with guards for the existing Nubank entry and checks each affected company before setting its selection flag. Operations updating Nubank occur before the new role is prepended.

Only the named `basics` fields, Nubank summary/highlights, five `resumeFeatured` flags and one new work entry are proposed. Contact details, historical dates, other roles, projects, skills and education are retained. Reapplying the patch to an already updated document must fail its first test rather than duplicate the role.

Per the collaboration guide, the owner applies approved content changes. This PR does not automatically apply the patch at runtime or during a build.

## Required before applying

Fill the empty current-role `position` with the confirmed title and `startDate` with the confirmed start date. Do not infer either from the preceding role's end date. Confirm the SitesPay display name; no legal group structure is asserted. Location and URL are intentionally empty rather than guessed. `endDate` is empty because this is current work.

The current-role summary proposed is:

> Design and development of financial systems, combining payment and accounting-domain modeling, software architecture, hands-on implementation and engineering-team development.

The full entry adds concise points about payment/pricing/FX/accounting flows, economic versus execution responsibilities, tests/simulators/reproducible environments, and collaboration between engineers and AI-assisted tools.

Product and customer names beyond the current work context are deliberately omitted from this first proposal. New independent-project entries can be curated separately rather than mixed into an employment record or retroactively appended to a historical project.

## Renderer changes

- Both short resumes read `basics.summary`, rather than hardcoding a summary and computing an experience count from the year 2025.
- `resumeFeatured: true` selects positions explicitly after `hide` and `resumeHide` filtering. When at least one eligible featured role exists, all eligible featured roles render in source order without a numerical cutoff.
- The proposal features SitesPay, Nubank, Sofía, both Covalto roles and Credijusto. Inserting an unrelated record will not displace these roles.
- For old documents without eligible featured entries, legacy four-job ATS and five-job project-resume defaults remain unchanged. This is compatibility behavior, not the selection strategy for the proposed CV.
- Repeated-company spacing uses exact company equality, so Credijusto's parenthetical mention of Covalto is not treated as the same employer entry.
- Blank start dates do not generate a leading dash or an invented year in short-resume previews. This is not permission to release unconfirmed data.
- The projects resume reuses the shared ATS structure while keeping its project section, title and legacy selection default.

## Verification and release

Run focused template/content tests without generating deployment artifacts:

```bash
uv run python -m unittest discover -s tests -p 'test_cv_rendering.py'
```

The regression suite uses representative data fixtures; it does not certify the final layout, content or factual metadata. It checks summary propagation, legacy/explicit selection, hidden entries, chronology preservation, duplicate protection and HTML escaping.

After content approval, apply the patch to a copy of `luisfernandobarrera.resume.json`, verify the result and let the owner replace the canonical source. Preview all four routes (`/`, `/print-cv.html`, `/print-resume.html`, `/print-resume-projects.html`) before release.

The six featured roles will require an editorial page-length decision. Do not silently drop a position or change the PDF page-count test simply to make it pass. A two-page ATS version is a candidate, not a validated output of this PR.

Generated artifacts, `docs/resume.pdf`, root `resume.pdf`, CNAME, publication configuration and the default branch are untouched. Full Flask/static/PDF rendering and page counts remain pending. Avoid `make clean`: its existing wildcard removes every `docs/*.pdf`, including the PDF protected by the collaboration guide. The build/freeze routes also need a separate check before deployment; this proposal does not run them.
