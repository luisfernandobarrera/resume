"""Rendering regressions and content-proposal guards; no PDF/network/Flask needed."""

import copy
import json
import re
import unittest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ("resume_ats.html", "resume_with_projects.html")


def example_resume():
    """Representative schema fixture, not a replacement for the owner's CV."""
    companies = [
        "Nubank", "Sofía Salud", "Banco Covalto", "Banco Covalto",
        "Credijusto (now Banco Covalto)", "CIAL", "Earlier employer",
    ]
    jobs = [
        dict(company=name, position=f"Role {i}", location="Remote",
             startDate=f"{2024-i}-01-01", endDate=f"{2025-i}-01-01",
             summary=f"Summary {i}", highlights=[f"Highlight {i}"])
        for i, name in enumerate(companies)
    ]
    jobs[0].update(startDate="2024-12-10", endDate="2025-09-12")
    return dict(
        basics=dict(name="Example Engineer", label="Engineer", specialty="Systems",
                    email="example@example.com", phone="", profiles=[],
                    location=dict(city="Example city", country="Example country"),
                    summary="CANONICAL SUMMARY", about=["Existing about"]),
        work=jobs,
        projects=[dict(name="Visible project", description="Description",
                       summary="Project summary", keywords=["Python"])],
        skills=[dict(name="Python Web Development", keywords=["Django", "FastAPI"])],
        education=[dict(studyType="Studies", area="Economics", institution="University",
                        startDate="2010", endDate="2013")],
        languages=[dict(language="Spanish", fluency="Native")],
        meta=dict(lastModified="2025-11-07"),
    )


def apply_proposal_fixture(source, operations):
    """Evaluate only the RFC 6902 subset used by the proposal, on a deep copy.

    Test helper only: never reads or writes the canonical resume file.
    """
    result = copy.deepcopy(source)
    for operation in operations:
        parts = operation["path"].lstrip("/").split("/")
        parent = result
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
        op, value = operation["op"], copy.deepcopy(operation["value"])
        if op == "test":
            if parent[key] != value:
                raise ValueError(f"Proposal does not match source at {operation['path']}")
        elif op == "replace":
            if isinstance(parent, dict) and key not in parent:
                raise ValueError(f"Missing replacement field: {operation['path']}")
            parent[key] = value
        elif op == "add":
            if isinstance(parent, list):
                parent.insert(key, value)
            else:
                parent[key] = value
        else:
            raise ValueError(f"Unsupported test-helper operation: {op}")
    return result


class ResumeRenderingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                              autoescape=select_autoescape(["html"]))
        cls.patch = json.loads((ROOT / "proposals/post-nubank.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.resume = example_resume()

    def render(self, template="resume_ats.html"):
        return self.env.get_template(template).render(resume=self.resume, print=True)

    def jobs(self, limit=4):
        module = self.env.get_template("_resume_jobs.html").module
        return str(module.render_jobs(self.resume, limit))

    def test_summary_comes_from_json_in_both_variants(self):
        for template in TEMPLATES:
            with self.subTest(template=template):
                self.assertIn("CANONICAL SUMMARY", self.render(template))
                self.assertNotIn("years of experience", self.render(template))

    def test_updated_summary_propagates(self):
        self.resume = apply_proposal_fixture(self.resume, self.patch)
        for template in TEMPLATES:
            with self.subTest(template=template):
                self.assertIn("Software engineer and technical leader", self.render(template))
                self.assertNotIn("CANONICAL SUMMARY", self.render(template))

    def test_legacy_ats_selection_is_unchanged(self):
        self.assertEqual(self.jobs().count('class="job entry'), 4)
        self.assertNotIn("Credijusto", self.jobs())

    def test_legacy_projects_selection_is_unchanged(self):
        html = self.render("resume_with_projects.html")
        self.assertEqual(html.count('class="job entry'), 5)
        self.assertIn("Credijusto", html)

    def test_featured_selection_keeps_six_roles_in_both_variants(self):
        self.resume = apply_proposal_fixture(self.resume, self.patch)
        for template in TEMPLATES:
            with self.subTest(template=template):
                html = self.render(template)
                self.assertEqual(html.count('class="job entry'), 6)
                self.assertEqual(html.count('<h3 class="name">Banco Covalto</h3>'), 2)
                self.assertIn("SitesPay", html)
                self.assertIn("Credijusto", html)
                self.assertNotIn('<h3 class="name">CIAL</h3>', html)

    def test_inserting_unfeatured_role_does_not_displace_featured_history(self):
        self.resume = apply_proposal_fixture(self.resume, self.patch)
        expected = re.findall(r'<h3 class="name">(.*?)</h3>', self.jobs())
        self.resume["work"].insert(0, dict(company="Unselected new role", startDate="", endDate=""))
        self.assertEqual(re.findall(r'<h3 class="name">(.*?)</h3>', self.jobs()), expected)

    def test_hide_overrides_featured(self):
        self.resume = apply_proposal_fixture(self.resume, self.patch)
        self.resume["work"][0]["hide"] = True
        self.assertNotIn("SitesPay", self.jobs())

    def test_resume_hide_overrides_featured(self):
        self.resume = apply_proposal_fixture(self.resume, self.patch)
        self.resume["work"][0]["resumeHide"] = True
        self.assertNotIn("SitesPay", self.jobs())

    def test_only_true_flags_are_featured(self):
        self.resume["work"][0]["resumeFeatured"] = "true"
        self.resume["work"][5]["resumeFeatured"] = True
        self.assertNotIn("Nubank", self.jobs())
        self.assertIn("CIAL", self.jobs())

    def test_exact_company_grouping(self):
        self.resume = apply_proposal_fixture(self.resume, self.patch)
        html = self.jobs()
        self.assertEqual(html.count('class="job entry same-company"'), 1)
        self.assertRegex(html, r'<section class="job entry">\s*<header[^>]*>\s*<h3 class="name">Credijusto')

    def test_unknown_start_is_not_invented(self):
        self.resume["work"] = [dict(company="Current role", startDate="", endDate="", position="", location="")]
        html = self.jobs()
        self.assertNotIn('class="startDate"', html)
        self.assertIn('class="endDate">current</span>', html)
        self.assertNotIn('class="position"', html)
        self.assertNotIn("2025", html)

    def test_missing_optional_role_fields_do_not_break_preview(self):
        self.resume["work"] = [dict(company="Current role")]
        self.assertIn("Current role", self.jobs())
        self.assertNotIn("None", self.jobs())

    def test_historical_dates_are_preserved(self):
        self.assertIn("2024-12-10 -", self.jobs())
        self.assertIn("2025-09-12", self.jobs())

    def test_empty_history_renders_without_experience_arithmetic(self):
        self.resume["work"] = []
        for template in TEMPLATES:
            self.assertEqual(self.render(template).count('class="job entry'), 0)

    def test_summary_and_company_are_escaped(self):
        self.resume["basics"]["summary"] = '<script>alert("x")</script>'
        self.resume["work"][0]["company"] = "<script>company</script>"
        for template in TEMPLATES:
            html = self.render(template)
            self.assertNotIn("<script>", html)
            self.assertIn("&lt;script&gt;", html)

    def test_project_view_preserves_its_section(self):
        self.assertIn("Visible project", self.render("resume_with_projects.html"))
        self.assertNotIn("Visible project", self.render("resume_ats.html"))

    def test_hidden_projects_remain_hidden(self):
        self.resume["projects"][0]["hide"] = True
        self.assertNotIn("Visible project", self.render("resume_with_projects.html"))

    def test_inherited_contact_skills_education_languages(self):
        html = self.render("resume_with_projects.html")
        for text in ("example@example.com", "Django", "FastAPI", "Economics", "Spanish", "Technical Skills"):
            self.assertIn(text, html)
        self.assertIn('class="ats-resume"', html)

    def test_proposal_preserves_unrelated_source_and_history(self):
        before = copy.deepcopy(self.resume)
        result = apply_proposal_fixture(self.resume, self.patch)
        self.assertEqual(self.resume, before)
        for field in ("skills", "education", "languages", "projects", "meta"):
            self.assertEqual(result[field], before[field])
        self.assertEqual(result["basics"]["email"], before["basics"]["email"])
        self.assertEqual(len(result["work"]), len(before["work"]) + 1)
        for i, job in enumerate(before["work"]):
            for field, value in job.items():
                if i == 0 and field in ("summary", "highlights"):
                    continue
                self.assertEqual(result["work"][i+1][field], value)

    def test_proposal_rejects_second_application(self):
        result = apply_proposal_fixture(self.resume, self.patch)
        with self.assertRaises(ValueError):
            apply_proposal_fixture(result, self.patch)

    def test_proposal_rejects_changed_source_order(self):
        self.resume["work"][1], self.resume["work"][2] = self.resume["work"][2], self.resume["work"][1]
        with self.assertRaises(ValueError):
            apply_proposal_fixture(self.resume, self.patch)

    def test_unconfirmed_current_metadata_is_explicitly_empty(self):
        result = apply_proposal_fixture(self.resume, self.patch)
        self.assertEqual(result["work"][0]["position"], "")
        self.assertEqual(result["work"][0]["startDate"], "")
        self.assertEqual(result["work"][0]["endDate"], "")


if __name__ == "__main__":
    unittest.main()
