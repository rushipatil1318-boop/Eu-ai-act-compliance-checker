"""Streamlit user interface. Run with:  streamlit run app.py"""
import streamlit as st

from src.classifier import HIGH, LIMITED, PROHIBITED_LEVEL, Answers, classify
from src.examples import EXAMPLES
from src.obligations import get_obligations
from src.report import build_report
from src.rules import ANNEX_III_AREAS, FINES, KEY_DATES, LAST_REVIEWED, LINKS, PROHIBITED
from src.watsonx_helper import MAX_CALLS_PER_SESSION, explain_with_watsonx, watsonx_is_configured

ROLES = ["Provider", "Deployer", "Importer", "Distributor"]
EMPTY_FORM = "(start with an empty form)"

st.set_page_config(page_title="EU AI Act Compliance Checker", page_icon="⚖️", layout="wide")


def fill_form(a):
    """Copy an Answers object into the form. Every widget has a key starting with f_."""
    st.session_state["f_name"] = a.system_name
    st.session_state["f_description"] = a.description
    st.session_state["f_role"] = a.role
    st.session_state["f_gpai"] = a.is_gpai
    st.session_state["f_annex_i"] = a.annex_i_product
    st.session_state["f_areas"] = a.annex_iii_areas
    st.session_state["f_profiling"] = a.does_profiling
    st.session_state["f_narrow"] = a.narrow_task
    st.session_state["f_talks"] = a.talks_to_people
    st.session_state["f_generates"] = a.generates_content
    st.session_state["f_emotion"] = a.emotion_or_biometric
    st.session_state["f_deepfake"] = a.deepfake_or_public_text
    for key in PROHIBITED:
        st.session_state[f"f_prohibited_{key}"] = key in a.prohibited


def load_example():
    choice = st.session_state["example_choice"]
    fill_form(EXAMPLES.get(choice, Answers(system_name="")))
    # An old result would not match the new form, so remove it
    for key in ("answers", "result", "explanation"):
        st.session_state.pop(key, None)


# First visit: pre-fill the form with the first example so the page is never empty
if "example_choice" not in st.session_state:
    first_example = list(EXAMPLES)[0]
    st.session_state["example_choice"] = first_example
    fill_form(EXAMPLES[first_example])

st.title("⚖️ EU AI Act Compliance Checker")
st.write("Answer a few questions about your AI system and get its risk level, "
         "the duties that come with it, and a report you can download.")

with st.sidebar:
    st.header("Key dates")
    for when, what in KEY_DATES:
        st.markdown(f"**{when}** - {what}")
    st.header("Official sources")
    for title, url in LINKS.items():
        st.markdown(f"- [{title}]({url})")
    st.caption(f"Legal content last reviewed: {LAST_REVIEWED}. A learning project, not legal advice.")

st.selectbox("Load an example", [EMPTY_FORM] + list(EXAMPLES), key="example_choice", on_change=load_example)

# ---------- The questionnaire ----------
with st.form("checker"):
    st.subheader("1. About your AI system")
    name = st.text_input("System name", key="f_name")
    description = st.text_area("What does it do? (short)", key="f_description")
    st.caption("Please do not enter personal data or company secrets.")
    role = st.selectbox("Your role", ROLES, key="f_role",
                        help="Provider = builds it. Deployer = uses it. Importer/Distributor = brings it to the EU market.")
    is_gpai = st.checkbox("It is a general-purpose AI model (for example a large language model that others build on)",
                          key="f_gpai")

    st.subheader("2. Banned practices (Article 5)")
    st.caption("Tick everything that applies to your system.")
    prohibited = []
    for key, text in PROHIBITED.items():
        if st.checkbox(text, key=f"f_prohibited_{key}"):
            prohibited.append(key)

    st.subheader("3. High-risk check (Article 6, Annexes I and III)")
    annex_i_product = st.checkbox("It is, or is a safety component of, a regulated product "
                                  "(medical device, toy, vehicle, lift...)", key="f_annex_i")
    annex_iii_areas = st.multiselect("Is it used in any of these areas?", options=list(ANNEX_III_AREAS),
                                     format_func=lambda key: ANNEX_III_AREAS[key], key="f_areas")
    does_profiling = st.checkbox("It profiles people (automatically evaluates personal traits, behaviour or performance)",
                                 key="f_profiling")
    narrow_task = st.checkbox("It ONLY does a narrow procedural task, improves the result of a human activity already "
                              "done, spots patterns without replacing human judgement, or does a preparatory task",
                              key="f_narrow")

    st.subheader("4. Transparency check (Article 50)")
    talks_to_people = st.checkbox("It talks directly to people (chatbot, voice assistant)", key="f_talks")
    generates_content = st.checkbox("It generates synthetic audio, images, video or text", key="f_generates")
    emotion_or_biometric = st.checkbox("It does emotion recognition or biometric categorisation", key="f_emotion")
    deepfake_or_public_text = st.checkbox("It creates deepfakes or AI text published to inform the public",
                                          key="f_deepfake")

    submitted = st.form_submit_button("Check my system", type="primary")

# ---------- Save the result ----------
# Streamlit re-runs this whole script on every click. We store the result in
# session_state so it does not disappear when the user clicks another button.
if submitted:
    answers = Answers(
        system_name=name, description=description, role=role, is_gpai=is_gpai, prohibited=prohibited,
        annex_i_product=annex_i_product, annex_iii_areas=annex_iii_areas, does_profiling=does_profiling,
        narrow_task=narrow_task, talks_to_people=talks_to_people, generates_content=generates_content,
        emotion_or_biometric=emotion_or_biometric, deepfake_or_public_text=deepfake_or_public_text)
    st.session_state["answers"] = answers
    st.session_state["result"] = classify(answers)
    st.session_state["explanation"] = None

# ---------- Show the result ----------
if "result" in st.session_state:
    answers = st.session_state["answers"]
    result = st.session_state["result"]

    st.divider()
    message = f"Risk level: {result.level}"
    if result.level == PROHIBITED_LEVEL:
        st.error(message)
    elif result.level == HIGH:
        st.warning(message)
    elif result.level == LIMITED:
        st.info(message)
    else:
        st.success(message)

    left, right = st.columns(2)
    with left:
        st.subheader("Why this level?")
        for reason in result.reasons:
            st.markdown(f"- {reason}")
        if result.level in FINES:
            st.caption(f"Possible fines: {FINES[result.level]}.")
    with right:
        st.subheader("What you need to do")
        for article, text in get_obligations(result, answers):
            st.markdown(f"- **{article}**: {text}")

    report = build_report(answers, result)
    st.download_button("Download report (.md)", report, file_name="ai_act_report.md")

    st.subheader("Plain-English explanation (optional, IBM watsonx.ai)")
    if watsonx_is_configured():
        calls_used = st.session_state.get("ai_calls", 0)
        calls_left = MAX_CALLS_PER_SESSION - calls_used
        if st.button(f"Explain with watsonx.ai ({calls_left} left)", disabled=calls_left <= 0):
            try:
                st.session_state["explanation"] = explain_with_watsonx(report)
                st.session_state["ai_calls"] = calls_used + 1
            except Exception as error:
                # Only the error type is shown, so no secret can leak on a public app
                st.error(f"watsonx.ai could not answer right now ({type(error).__name__}). Please try again later.")
        if st.session_state.get("explanation"):
            st.write(st.session_state["explanation"])
    else:
        st.caption("This button appears when WATSONX_API_KEY and WATSONX_PROJECT_ID are set. See the README.")
