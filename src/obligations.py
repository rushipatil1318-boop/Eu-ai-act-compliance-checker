"""What a team has to DO for each risk level and role. Each item is (article, plain-English text)."""

HIGH_RISK = {
    "Provider": [
        ("Art. 9", "Set up a risk management system that runs through the whole life of the AI system."),
        ("Art. 10", "Use training, validation and test data that is relevant, representative and checked for bias."),
        ("Art. 11", "Prepare technical documentation before placing the system on the market."),
        ("Art. 12", "Let the system log events automatically so its results can be traced."),
        ("Art. 13", "Give deployers clear instructions for use."),
        ("Art. 14", "Design the system so humans can oversee it and step in."),
        ("Art. 15", "Reach suitable accuracy, robustness and cybersecurity."),
        ("Art. 17", "Run a quality management system."),
        ("Art. 43, 47, 48", "Complete the conformity assessment, sign the EU declaration of conformity and add the CE marking."),
        ("Art. 49", "Register the system in the EU database."),
        ("Art. 72, 73", "Monitor the system after launch and report serious incidents."),
    ],
    "Deployer": [
        ("Art. 26", "Use the system as the instructions say and give oversight to trained, competent people."),
        ("Art. 26", "Keep the automatically generated logs for at least six months."),
        ("Art. 26", "Tell workers and affected people that a high-risk AI system is used on them."),
        ("Art. 27", "Public bodies, and some private deployers (e.g. credit scoring, life/health insurance), must do a fundamental rights impact assessment first."),
        ("Art. 86", "Explain individual decisions to an affected person who asks."),
    ],
    "Importer": [
        ("Art. 23", "Check that the provider did the conformity assessment, has the documentation and added the CE marking before the system enters the EU market."),
    ],
    "Distributor": [
        ("Art. 24", "Check the CE marking, documentation and instructions before making the system available."),
    ],
}

EXEMPTION_DUTIES = [
    ("Art. 6(4)", "Write down why you believe the system is NOT high-risk, and keep it ready for authorities."),
    ("Art. 49(2)", "Register the system in the EU database even though it is not high-risk."),
]

PROHIBITED_DUTIES = [
    ("Art. 5", "Do not place this system on the EU market, put it into service or use it. Redesign it so it no longer does the banned practice."),
]

MINIMAL_DUTIES = [
    ("Art. 95", "No legal duties beyond the basics. Following voluntary codes of conduct is encouraged."),
]

# Applies to everybody, whatever the risk level
BASIC_DUTIES = [
    ("Art. 4", "Take measures to support the AI literacy of staff and others who operate AI systems for you. The Digital Omnibus softened this duty but did not remove it."),
]

GPAI_DUTIES = [
    ("Art. 53", "Keep technical documentation, share information with downstream providers, have a copyright policy and publish a training-data summary."),
    ("Art. 55", "If the model has systemic risk (very large compute, above 10^25 FLOPs): run model evaluations, report serious incidents and secure the model."),
]

# Article 50 - transparency duties: key -> (article, text, roles the duty applies to)
TRANSPARENCY = {
    "talks_to_people": ("Art. 50(1)", "Tell people they are talking to an AI, unless it is obvious.", ("Provider",)),
    "generates_content": ("Art. 50(2)", "Mark AI-generated audio, image, video or text in a machine-readable way. Systems already on the market before 2 Aug 2026 have until 2 Dec 2026.", ("Provider",)),
    "emotion_or_biometric": ("Art. 50(3)", "Inform people who are exposed to emotion recognition or biometric categorisation.", ("Deployer",)),
    "deepfake_or_public_text": ("Art. 50(4)", "Disclose deepfakes and AI-written text published to inform the public on public-interest topics.", ("Deployer",)),
}


def get_obligations(result, answers):
    """Return a list of (article, text) for this risk result and the user's role."""
    if result.level == "Prohibited":
        return list(PROHIBITED_DUTIES)

    duties = list(BASIC_DUTIES)

    if result.level == "High risk":
        duties += HIGH_RISK[answers.role]
    elif result.exemption_used:
        duties += EXEMPTION_DUTIES
    elif not result.transparency:
        duties += MINIMAL_DUTIES

    # Only show the transparency duties that belong to the user's role
    other_role_duty = False
    for article, text, roles in result.transparency:
        if answers.role in roles:
            duties.append((article, text))
        else:
            other_role_duty = True
    if other_role_duty:
        duties.append(("Art. 50", "Some transparency duties in your case belong to another role. "
                                  "Ask the other party (for example your provider) to confirm they meet them."))

    # General-purpose AI model duties are for the provider of the model
    if answers.is_gpai and answers.role == "Provider":
        duties += GPAI_DUTIES

    return duties
