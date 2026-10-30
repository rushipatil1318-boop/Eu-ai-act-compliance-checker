"""Static facts from the EU AI Act (Regulation (EU) 2024/1689) used by the checker.

Keeping the facts in ONE file means that when the law changes (it already did,
through the Digital Omnibus), you only update this file and not the logic.
"""

# Article 5 - practices that are banned outright
PROHIBITED = {
    "manipulation": "Uses subliminal or manipulative techniques that distort people's behaviour and can cause significant harm",
    "vulnerabilities": "Exploits vulnerabilities of people (age, disability, social or economic situation)",
    "social_scoring": "Scores or classifies people by social behaviour or personality, leading to unfair treatment",
    "crime_prediction": "Predicts whether a person will commit a crime based only on profiling or personality traits",
    "face_scraping": "Builds facial-recognition databases by untargeted scraping of internet or CCTV images",
    "emotion_work_school": "Detects emotions of people at work or in education (except for medical or safety reasons)",
    "biometric_categorisation": "Uses biometric data to infer race, political opinions, religion, sexual orientation, etc.",
    "harmful_content": "Generates non-consensual intimate imagery or child sexual abuse material (new ban from 2 Dec 2026)",
    "realtime_biometric_id": "Real-time remote biometric identification in public spaces for law enforcement",
}

# Annex III - areas where a stand-alone AI system is considered high-risk
ANNEX_III_AREAS = {
    "biometrics": "Biometrics (remote identification, biometric categorisation, emotion recognition)",
    "critical_infrastructure": "Critical infrastructure (safety components for road traffic, water, gas, heating, electricity)",
    "education": "Education and training (admissions, grading, exam proctoring, assessing learning level)",
    "employment": "Employment and workers (recruiting, CV screening, promotion, task allocation, monitoring)",
    "essential_services": "Essential services (credit scoring, public benefits, life/health insurance pricing, emergency call triage)",
    "law_enforcement": "Law enforcement (risk assessment of persons, evidence reliability, profiling in investigations)",
    "migration": "Migration, asylum and border control",
    "justice_democracy": "Administration of justice and democratic processes (e.g. assisting judges, influencing elections)",
}

# Dates can change when the law is amended, so keep them here and double-check
# them on the official EU sources before using the tool for real decisions.
KEY_DATES = [
    ("2 Feb 2025", "Banned practices (Art. 5) apply"),
    ("2 Aug 2025", "Rules for general-purpose AI models apply"),
    ("2 Aug 2026", "Transparency duties (Art. 50) apply"),
    ("2 Dec 2026", "Marking of AI-generated content (Art. 50(2)) for systems already on the market before 2 Aug 2026; new ban on harmful generated content"),
    ("2 Dec 2027", "High-risk rules for stand-alone systems (Annex III) apply - delayed by the Digital Omnibus"),
    ("2 Aug 2028", "High-risk rules for AI inside regulated products (Annex I) apply - delayed by the Digital Omnibus"),
]

# Article 99 - maximum fines (for SMEs the LOWER of the two amounts applies)
FINES = {
    "Prohibited": "up to EUR 35 million or 7% of worldwide yearly turnover",
    "High risk": "up to EUR 15 million or 3% of worldwide yearly turnover",
    "Limited risk": "up to EUR 15 million or 3% of worldwide yearly turnover",
}

# When the legal content of this file was last checked against official sources
LAST_REVIEWED = "30 Oct 2026"

LINKS = {
    "EU AI Act - Regulation (EU) 2024/1689": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
    "Digital Omnibus on AI - Regulation (EU) 2026/1744": "https://eur-lex.europa.eu/eli/reg/2026/1744/oj",
}
