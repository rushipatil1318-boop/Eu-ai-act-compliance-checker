from pathlib import Path

import pytest

from src import watsonx_helper
from src.classifier import Answers, classify
from src.examples import EXAMPLES
from src.obligations import get_obligations
from src.report import build_report


def test_every_example_gives_the_expected_level():
    expected = ["High risk", "Limited risk", "High risk", "Minimal risk",
                "Prohibited", "Limited risk", "Minimal risk"]
    levels = [classify(example).level for example in EXAMPLES.values()]
    assert levels == expected


def test_deployer_does_not_get_provider_transparency_duty():
    answers = Answers(role="Deployer", talks_to_people=True)
    articles = [article for article, text in get_obligations(classify(answers), answers)]
    assert "Art. 50(1)" not in articles
    assert "Art. 50" in articles  # the hint that another role is responsible


def test_provider_gets_chatbot_duty():
    answers = Answers(role="Provider", talks_to_people=True)
    articles = [article for article, text in get_obligations(classify(answers), answers)]
    assert "Art. 50(1)" in articles


def test_gpai_duties_are_for_providers_only():
    provider = Answers(role="Provider", is_gpai=True)
    deployer = Answers(role="Deployer", is_gpai=True)
    assert len(get_obligations(classify(provider), provider)) > len(get_obligations(classify(deployer), deployer))


def test_report_contains_level_sources_and_date():
    answers = Answers(system_name="Demo", annex_iii_areas=["employment"])
    report = build_report(answers, classify(answers))
    assert "High risk" in report and "eur-lex.europa.eu" in report and "last reviewed" in report


def test_watsonx_total_limit_blocks_calls(monkeypatch):
    monkeypatch.setattr(watsonx_helper, "_total_calls", watsonx_helper.MAX_CALLS_TOTAL)
    with pytest.raises(RuntimeError):
        watsonx_helper.explain_with_watsonx("report")


def test_ui_first_visit_and_check_button():
    from streamlit.testing.v1 import AppTest
    app_file = str(Path(__file__).parent.parent / "app.py")
    at = AppTest.from_file(app_file, default_timeout=30).run()
    assert not at.exception
    at.button[0].click().run()
    assert not at.exception
    assert [w.value for w in at.warning] == ["Risk level: High risk"]


def test_ui_role_change_filters_duties():
    from streamlit.testing.v1 import AppTest
    app_file = str(Path(__file__).parent.parent / "app.py")
    at = AppTest.from_file(app_file, default_timeout=30).run()
    at.selectbox(key="example_choice").select("Customer support chatbot").run()
    at.selectbox(key="f_role").select("Deployer")
    at.button[0].click().run()
    assert at.session_state["answers"].role == "Deployer"
    shown = " ".join(m.value for m in at.markdown)
    assert "Art. 50(1)" not in shown
