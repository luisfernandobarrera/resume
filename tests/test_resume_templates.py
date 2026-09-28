"""Data and inheritance regressions; no Flask server or PDF renderer required."""

import copy
import json
from pathlib import Path
import re
import unittest

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
VIEWS = ("resume_ats.html", "resume_with_projects.html")


def resume_fixture():
    return {
        "basics": {
            "name": "Example Engineer",
            "label": "Systems Engineer",
            "specialty": "Business Systems",
            "summary": "Canonical summary marker.",
            "email": "engineer@example.com",
            "phone": "",
            "profiles": [],
            "location": {"city": "Mexico City", "country": "Mexico"},
        },
        "work": [
            {
                "company": f"Company-{i}",
                "position": "Engineer",
                "startDate": f"{2025 - i}-01",
                "endDate": f"{2025 - i}-12",
                "summary": f"Role summary {i}.",
            }
            for i in range(8)
        ],
        "skills": [
            {"name": "Clojure", "keywords": ["Datomic", "ClojureScript"]},
            {"name": "New Domain", "keywords": ["Domain Modeling"]},
        ],
        "languages": [{"language": "English", "fluency": "Professional"}],
        "education": [],
        "projects": [],
        "meta": {},
    }


class ResumeTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = Environment(
            loader=FileSystemLoader(ROOT / "templates"),
            autoescape=select_autoescape(["html"]),
        )

    def setUp(self):
        self.document = resume_fixture()

    def render(self, view=VIEWS[0]):
        return self.env.get_template(view).render(resume=self.document, print=True)

    def test_both_views_use_canonical_summary(self):
        for view in VIEWS:
            with self.subTest(view=view):
                html = self.render(view)
                self.assertIn("Canonical summary marker.", html)
                self.assertNotIn("years of experience", html)
                self.assertNotIn("high-performing teams", html)

    def test_summary_update_reaches_both_views(self):
        self.document["basics"]["summary"] = "Updated & verified summary."
        for view in VIEWS:
            html = self.render(view)
            self.assertIn("Updated &amp; verified summary.", html)
            self.assertNotIn("Canonical summary marker.", html)

    def test_existing_limits_and_overflow_notice(self):
        for view, count in zip(VIEWS, (4, 5)):
            html = self.render(view)
            self.assertEqual(len(re.findall(r'<section class="job entry', html)), count)
            self.assertIn("Additional experience is available in the full CV.", html)

    def test_configured_limits_preserve_lending_role(self):
        names = ["SitesPay", "Nubank", "Sofia", "Covalto", "Covalto", "Credijusto"]
        for job, name in zip(self.document["work"], names):
            job["company"] = name
        self.document["meta"].update(atsJobLimit=6, projectsJobLimit=6)
        for view in VIEWS:
            html = self.render(view)
            self.assertIn('class="name">SitesPay</h3>', html)
            self.assertIn('class="name">Credijusto</h3>', html)
            self.assertNotIn('class="name">Company-6</h3>', html)
            self.assertEqual(html.count("same-company"), 1)

    def test_zero_means_all_visible_roles(self):
        self.document["meta"].update(atsJobLimit=0, projectsJobLimit=0)
        for view in VIEWS:
            html = self.render(view)
            self.assertEqual(html.count('<section class="job entry'), 8)
            self.assertNotIn("Additional experience is available", html)

    def test_hide_flags_apply_before_limit(self):
        self.document["work"][0]["hide"] = True
        self.document["work"][1]["resumeHide"] = True
        html = self.render()
        self.assertNotIn('class="name">Company-0</h3>', html)
        self.assertNotIn('class="name">Company-1</h3>', html)
        self.assertIn('class="name">Company-5</h3>', html)
        self.assertEqual(html.count('<section class="job entry'), 4)

    def test_missing_or_invalid_limits_preserve_defaults(self):
        for value in (None, "six", -1, True, 4.5):
            with self.subTest(value=value):
                self.document["meta"]["atsJobLimit"] = value
                self.assertEqual(self.render().count('<section class="job entry'), 4)
        del self.document["meta"]
        self.assertEqual(self.render().count('<section class="job entry'), 4)

    def test_current_role_does_not_invent_start_or_print_leading_dash(self):
        self.document["work"] = [{"company": "Current", "summary": "Work today."}]
        html = self.render()
        dates = re.search(r'<div class="date">(.*?)</div>', html, re.S).group(1)
        self.assertIn("Present", dates)
        self.assertNotIn("startDate", dates)
        self.assertNotIn("–", dates)
        self.assertNotIn("None", html)

    def test_complete_dates_keep_both_ends(self):
        self.assertIn('class="startDate">2025-01</span> –', self.render())
        self.assertIn('class="endDate">2025-12</span>', self.render())

    def test_compact_summary_and_highlights_are_opt_in(self):
        job = self.document["work"][0]
        job["highlights"] = ["Full CV detail not selected for compact version."]
        self.assertNotIn(job["highlights"][0], self.render())
        job["resumeSummary"] = "Concise selected summary."
        job["resumeHighlights"] = ["Specific compact evidence."]
        html = self.render()
        self.assertIn("Concise selected summary.", html)
        self.assertIn("Specific compact evidence.", html)
        self.assertNotIn("Role summary 0.", html)

    def test_all_skill_groups_render_without_keyword_allowlist(self):
        for view in VIEWS:
            html = self.render(view)
            self.assertIn("Datomic, ClojureScript", html)
            self.assertIn("New Domain:", html)
            self.assertIn("Domain Modeling", html)

    def test_hidden_and_empty_skills_are_excluded(self):
        self.document["skills"].extend([
            {"name": "Hidden skill", "hide": True, "keywords": ["HiddenKeyword"]},
            {"name": "Empty skill", "keywords": []},
        ])
        html = self.render()
        self.assertNotIn("HiddenKeyword", html)
        self.assertNotIn("Empty skill:", html)

    def test_projects_remain_visible_only_in_projects_view(self):
        self.document["projects"] = [
            {"name": "Project Visible", "keywords": ["TypeScript"], "summary": "Project summary."},
            {"name": "Project Hidden", "hide": True},
        ]
        self.assertNotIn("Project Visible", self.render())
        html = self.render(VIEWS[1])
        self.assertIn("Project Visible", html)
        self.assertIn("TypeScript", html)
        self.assertNotIn("Project Hidden", html)
        self.assertEqual(html.count('<header id="header">'), 1)
        self.assertEqual(html.count("Canonical summary marker."), 1)

    def test_text_is_escaped_and_render_is_pure(self):
        payload = '<script>alert("x")</script>'
        self.document["basics"]["summary"] = payload
        self.document["work"][0]["company"] = payload
        self.document["work"][0]["resumeHighlights"] = [payload]
        self.document["skills"][0]["keywords"] = [payload]
        before = copy.deepcopy(self.document)
        for view in VIEWS:
            html = self.render(view)
            self.assertNotIn(payload, html)
            self.assertIn("&lt;script&gt;", html)
        self.assertEqual(before, self.document)

    def test_review_proposal_preserves_confirmed_role_without_auto_loading(self):
        path = ROOT / "proposals" / "post-nubank.json"
        proposal = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(path.name.endswith(".resume.json"))
        role = proposal["workToPrepend"]
        self.assertEqual(role["startDate"], "2025-12-15")
        self.assertEqual(role["position"], "Engineering Manager & Software Architect")
        self.assertEqual(role["endDate"], "")
        self.assertEqual(proposal["confirmedRoleFacts"]["startDate"], role["startDate"])
        self.assertEqual(proposal["confirmedRoleFacts"]["publicTitle"], role["position"])
        self.assertIn("draft", proposal["status"])
        self.assertTrue(proposal["needsConfirmation"])
        self.document["basics"].update(proposal["basicsPatch"])
        self.document["work"].insert(0, role)
        self.document["meta"].update(proposal["metaPatch"])
        for view in VIEWS:
            html = self.render(view)
            self.assertIn('class="name">SitesPay</h3>', html)
            self.assertIn('class="startDate">2025-12-15</span>', html)
            self.assertIn('class="endDate">Present</span>', html)
            self.assertIn("Engineering Manager &amp; Software Architect", html)
            self.assertIn("financial systems spanning payments", html)
            self.assertIn("PayGlobal", html)
            self.assertIn("treasury ERP", html)
            self.assertIn("hands-on AI-assisted implementation", html)


if __name__ == "__main__":
    unittest.main()
