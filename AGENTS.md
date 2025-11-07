## Collaboration Guide (Humans + AI Agents)

This repository is maintained collaboratively by humans and AI coding assistants. This guide defines how we work together to keep the codebase consistent and safe.

### Source of Truth
- `luisfernandobarrera.resume.json` is the canonical CV content.
- `docs/resume.pdf` is generated externally (Google Docs). Do not overwrite it in automation.
- The site is served by `app.py`; HTML is in `templates/` and styles compiled from `templates/sass/style.sass`.

### Editing Rules
- Prefer small, focused edits.
- Preserve existing indentation, casing, and formatting unless explicitly normalizing.
- For resume content changes, propose JSON diffs/snippets first. Human will apply all the changes.
- Avoid adding fields unused by `templates/cv.html` unless you add template support.

### JSON Change Protocol
When proposing changes to `luisfernandobarrera.resume.json`:
1) Provide a JSON snippet containing only the fields to add/change.
2) Use past tense for completed roles, present for current.
3) Lead highlights with outcomes/impact; keep bullets concise.
4) Normalize technology names (e.g., FastAPI, Django REST Framework, Tortoise ORM, Vue.js, Sass, AWS, S3, Google Cloud, Kubernetes).

### Branching & Commits
- Use feature branches: `feat/*`, `chore/*`, `fix/*`.
- Commit messages: Conventional Commits (e.g., `feat(cv): update Nubank highlights`).

### Review Checklist
- Rendering: page loads at `/` and `/print-cv.html`.
- JSON validity: file parses and fields are rendered by `cv.html`.
- Spelling/grammar and consistent tense.
- No accidental changes to `docs/resume.pdf`.

### Automation Notes
- Local dev: `python app.py` with Flask (ensure deps in `pyproject.toml`).
- CSS is built on-the-fly by `app.py` from SASS; no manual CSS commits.

### Contact & Ownership
- CV owner: Luis Fernando Barrera.
- For large content edits, open a PR with JSON suggestions and rationale.


