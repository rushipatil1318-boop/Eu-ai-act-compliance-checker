"""Ready-made example systems so the app is useful from the very first click."""
from src.classifier import Answers

EXAMPLES = {
    "CV screening tool (a company builds it)": Answers(
        system_name="CV Screening Assistant",
        description="Ranks job applicants by analysing their CVs.",
        annex_iii_areas=["employment"], does_profiling=True),
    "Customer support chatbot": Answers(
        system_name="Support Chatbot",
        description="Answers customer questions in a chat window.",
        talks_to_people=True),
    "Credit scoring model for a bank": Answers(
        system_name="Credit Score Engine",
        description="Predicts whether a person will repay a loan.",
        annex_iii_areas=["essential_services"], does_profiling=True),
    "Email spam filter": Answers(
        system_name="Spam Filter",
        description="Moves unwanted emails into the spam folder."),
    "Social scoring of citizens": Answers(
        system_name="Citizen Score",
        description="Gives every citizen a score based on their social behaviour.",
        prohibited=["social_scoring"]),
    "AI image generator app": Answers(
        system_name="Picture Maker",
        description="Creates images from text prompts.",
        generates_content=True),
    "CV formatting helper (narrow task)": Answers(
        system_name="CV Formatter",
        description="Only fixes the layout of CVs. It does not rate or rank anyone.",
        annex_iii_areas=["employment"], narrow_task=True),
}
