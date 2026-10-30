# EU AI Act Compliance Checker

![tests](https://github.com/rushipatil1318-boop/eu-ai-act-compliance-checker/actions/workflows/ci.yml/badge.svg)

**Live demo:** _paste your Streamlit link here after deploying_

A small web app that helps students, startups and small teams find out **which risk level of the EU AI Act their AI system falls into** and **what they have to do about it**.

You answer a short questionnaire (or load one of 7 ready examples). The app then shows:

- the risk level: **Prohibited, High risk, Limited risk or Minimal risk**
- the reasons behind that level, with article numbers
- the duties for **your role** (provider, deployer, importer or distributor)
- possible fines and key dates, with links to the official EUR-Lex texts
- a downloadable Markdown report
- an optional plain-English explanation from **IBM watsonx.ai (Granite)**

> This is a learning and portfolio project. It is **not legal advice**. Check the official text before making real decisions.

## How it works

The rules follow the same order as the AI Act itself:

1. Is a banned practice involved (Art. 5)? -> **Prohibited**
2. Is it part of a regulated product (Annex I) or used in a high-risk area (Annex III)? -> **High risk** (unless the Art. 6(3) exemption applies, which never applies to profiling)
3. Does it have transparency duties (Art. 50)? -> **Limited risk**
4. Otherwise -> **Minimal risk**

The classifier is plain Python with no AI, so the result is deterministic and easy to test. The optional watsonx.ai step only *explains* the result, it never decides it.

## Up to date with the Digital Omnibus

The AI Act was amended by the Digital Omnibus on AI (Regulation (EU) 2026/1744, in force since 27 July 2026). The tool reflects:

- Annex III high-risk duties moved to **2 Dec 2027**, Annex I to **2 Aug 2028**
- Transparency duties (Art. 50) apply since **2 Aug 2026**, with a grace period until **2 Dec 2026** for marking AI-generated content in systems already on the market
- A new ban on systems that generate non-consensual intimate imagery or child abuse material (**2 Dec 2026**)
- A softer, but still present, AI literacy duty (Art. 4)

All dates and legal texts live in `src/rules.py` and `src/obligations.py` (last reviewed: 30 Oct 2026), so updating the tool means editing those two files.

## Limitations (please read)

- It is a **simplified screening**. Annex III has sub-cases and exceptions that a short questionnaire cannot cover (for example fraud detection is excluded from credit scoring).
- Product-safety rules (Annex I), for example machinery, are more complex after the Omnibus. Treat that answer as a first hint only.
- It does not check data protection law (GDPR) or other regulations.
- Answers are only as good as the information you give.

## Evaluation

`tests/test_evaluation.py` contains 25 real-world style cases (CV screening, credit scoring, chatbots, social scoring, and more) with the expected risk level. Run `pytest` to check them all. There are also tests for roles, reports, the watsonx.ai usage limit and the user interface.

## Project structure

```
app.py                  Streamlit user interface
src/rules.py            Facts from the law: banned practices, Annex III areas, dates, fines, links
src/classifier.py       Risk classification logic
src/obligations.py      Duties per risk level and role
src/examples.py         Ready-made example systems
src/report.py           Markdown report builder
src/watsonx_helper.py   Optional IBM watsonx.ai explanation, with usage limits
tests/                  Pytest unit, evaluation and UI tests
Dockerfile              For cloud deployment
```

## Run it on your computer

```bash
git clone https://github.com/rushipatil1318-boop/eu-ai-act-compliance-checker.git
cd eu-ai-act-compliance-checker
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
streamlit run app.py
pytest
```

## Optional: switch on watsonx.ai

1. Create an IBM Cloud account, a watsonx.ai project and an API key.
2. Set `WATSONX_API_KEY` and `WATSONX_PROJECT_ID` (see `.env.example`, or Streamlit secrets in the cloud).
3. Restart the app. A button appears under the result.

Safety for public apps: each visitor gets 3 calls and the whole server is capped at 200 calls, so nobody can use up your quota. Model names change over time, so the app tries `granite-3-3-8b-instruct`, `granite-4-h-small` and `granite-3-8b-instruct` in turn. You can force your own with `WATSONX_MODEL_ID`.

## Deploy to the cloud

**Option A - Streamlit Community Cloud (free, easiest)**

1. Push this repo to a *public* GitHub repository.
2. Go to share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose your repo, branch `main` and main file `app.py`.
4. Optional: **Advanced settings -> Secrets**, paste the content of `.streamlit/secrets.toml.example` with your real values.
5. Click **Deploy**. Free apps go to sleep when nobody visits, so open the link once before sharing it.

**Option B - Render with Docker**

1. Create a new **Web Service** on render.com and connect the GitHub repo.
2. Choose **Docker** as runtime (it finds the `Dockerfile` automatically) and the free instance type.
3. Add the watsonx values as environment variables if you want them.

**Option C - Docker on your own machine**

```bash
docker build -t ai-act-checker .
docker run -p 8501:8501 ai-act-checker
```

## License

MIT
