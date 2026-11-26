"""Real-world style cases. Each row: (description, answers, expected risk level)."""
import pytest

from src.classifier import HIGH, LIMITED, MINIMAL, PROHIBITED_LEVEL, Answers, classify

CASES = [
    ("CV ranking tool", dict(annex_iii_areas=["employment"], does_profiling=True), HIGH),
    ("Employee monitoring system", dict(annex_iii_areas=["employment"], does_profiling=True), HIGH),
    ("Exam proctoring software", dict(annex_iii_areas=["education"]), HIGH),
    ("University admission scoring", dict(annex_iii_areas=["education"], does_profiling=True), HIGH),
    ("Bank credit scoring", dict(annex_iii_areas=["essential_services"], does_profiling=True), HIGH),
    ("Health insurance pricing", dict(annex_iii_areas=["essential_services"], does_profiling=True), HIGH),
    ("Border control risk tool", dict(annex_iii_areas=["migration"]), HIGH),
    ("Judge assistant", dict(annex_iii_areas=["justice_democracy"]), HIGH),
    ("Power grid safety component", dict(annex_iii_areas=["critical_infrastructure"]), HIGH),
    ("Medical device software", dict(annex_i_product=True), HIGH),
    ("Credit scoring chatbot", dict(annex_iii_areas=["essential_services"], talks_to_people=True), HIGH),
    ("Social scoring", dict(prohibited=["social_scoring"]), PROHIBITED_LEVEL),
    ("Emotion detection in classrooms", dict(prohibited=["emotion_work_school"], annex_iii_areas=["education"]), PROHIBITED_LEVEL),
    ("Crime prediction by personality", dict(prohibited=["crime_prediction"]), PROHIBITED_LEVEL),
    ("Face database from internet images", dict(prohibited=["face_scraping"]), PROHIBITED_LEVEL),
    ("Fake intimate image generator", dict(prohibited=["harmful_content"], generates_content=True), PROHIBITED_LEVEL),
    ("Customer FAQ chatbot", dict(talks_to_people=True), LIMITED),
    ("Image generator app", dict(generates_content=True), LIMITED),
    ("Deepfake video tool", dict(generates_content=True, deepfake_or_public_text=True), LIMITED),
    ("Shop emotion analytics", dict(emotion_or_biometric=True), LIMITED),
    ("Resume layout helper", dict(annex_iii_areas=["employment"], narrow_task=True), MINIMAL),
    ("Narrow tool that still profiles", dict(annex_iii_areas=["employment"], narrow_task=True, does_profiling=True), HIGH),
    ("Email spam filter", dict(), MINIMAL),
    ("Movie recommender", dict(), MINIMAL),
    ("Smart thermostat", dict(), MINIMAL),
]


@pytest.mark.parametrize("name, answers, expected", CASES, ids=[case[0] for case in CASES])
def test_case(name, answers, expected):
    assert classify(Answers(**answers)).level == expected
