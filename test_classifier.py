from src.classifier import HIGH, LIMITED, MINIMAL, PROHIBITED_LEVEL, Answers, classify
from src.obligations import get_obligations


def test_banned_practice_wins_over_everything():
    result = classify(Answers(prohibited=["social_scoring"], annex_iii_areas=["employment"]))
    assert result.level == PROHIBITED_LEVEL


def test_cv_screening_is_high_risk():
    result = classify(Answers(annex_iii_areas=["employment"]))
    assert result.level == HIGH


def test_annex_i_product_is_high_risk():
    assert classify(Answers(annex_i_product=True)).level == HIGH


def test_narrow_task_exemption_applies():
    result = classify(Answers(annex_iii_areas=["education"], narrow_task=True))
    assert result.level == MINIMAL
    assert result.exemption_used


def test_profiling_blocks_the_exemption():
    result = classify(Answers(annex_iii_areas=["employment"], narrow_task=True, does_profiling=True))
    assert result.level == HIGH


def test_chatbot_is_limited_risk():
    result = classify(Answers(talks_to_people=True))
    assert result.level == LIMITED
    assert len(result.transparency) == 1


def test_spam_filter_is_minimal_risk():
    assert classify(Answers()).level == MINIMAL


def test_high_risk_provider_has_more_duties_than_deployer():
    provider = Answers(role="Provider", annex_iii_areas=["employment"])
    deployer = Answers(role="Deployer", annex_iii_areas=["employment"])
    assert len(get_obligations(classify(provider), provider)) > len(get_obligations(classify(deployer), deployer))


def test_gpai_adds_extra_duties():
    plain = Answers()
    gpai = Answers(is_gpai=True)
    assert len(get_obligations(classify(gpai), gpai)) > len(get_obligations(classify(plain), plain))
