"""OPTIONAL: ask IBM watsonx.ai (Granite model) to explain the result in simple words.

The app works fully without this file being used. It only runs when the
WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables are set.
"""
import os

# Protects your IBM quota when the app is public:
# each visitor gets a few calls, and the whole server gets a hard cap too.
MAX_CALLS_PER_SESSION = 3
MAX_CALLS_TOTAL = 200
_total_calls = 0

# Model names change over time, so we try several until one works.
# Put your own choice first with the WATSONX_MODEL_ID environment variable.
DEFAULT_MODELS = ["ibm/granite-3-3-8b-instruct", "ibm/granite-4-h-small", "ibm/granite-3-8b-instruct"]


def watsonx_is_configured():
    return bool(os.getenv("WATSONX_API_KEY") and os.getenv("WATSONX_PROJECT_ID"))


def explain_with_watsonx(report_text):
    global _total_calls
    if _total_calls >= MAX_CALLS_TOTAL:
        raise RuntimeError("The demo limit for watsonx.ai calls has been reached.")
    _total_calls += 1

    # Imported here so the app still starts if the package is not installed
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference

    credentials = Credentials(
        url=os.getenv("WATSONX_URL", "https://eu-de.ml.cloud.ibm.com"),
        api_key=os.getenv("WATSONX_API_KEY"),
    )
    prompt = (
        "You are a helpful assistant for students and small teams. "
        "Explain the following EU AI Act result in simple English, in at most 150 words. "
        "Only use facts that appear in the report. Do not invent legal advice.\n\n"
        f"{report_text[:3000]}"
    )

    models = [os.getenv("WATSONX_MODEL_ID")] if os.getenv("WATSONX_MODEL_ID") else []
    models += DEFAULT_MODELS
    last_error = None
    for model_id in models:
        try:
            model = ModelInference(
                model_id=model_id,
                credentials=credentials,
                project_id=os.getenv("WATSONX_PROJECT_ID"),
                params={"max_new_tokens": 400, "temperature": 0.2},
            )
            return model.generate_text(prompt=prompt)
        except Exception as error:  # try the next model name
            last_error = error
    raise last_error
