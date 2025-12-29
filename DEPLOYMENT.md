# Deploying Nexus Research Assistant on Streamlit Cloud

This guide walks you through deploying the application for free using **Streamlit Cloud**.

## 1. Prerequisites (Already Completed)

- The code is pushed to GitHub.
- The `requirements.txt` is updated.
- The ChromaDB data (`data/chroma_db`) is included in the repo, so the app works immediately without re-ingesting documents.

## 2. Connect to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and ensure you are logged in with your GitHub account.
2. Click the **"New app"** button.
3. Fill in the deployment form:
   - **Repository**: Select `Arv-ind-s/Nexus-Research-Assistant`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom subdomain if available (e.g., `nexus-research-assistant`)

## 3. Configure Secrets (API Keys)

**CRITICAL STEP**: The app will fail to run if it cannot access your API keys. Streamlit Cloud does not read from `.env` files for security; it uses a "Secrets" manager.

1. Before clicking "Deploy", click on **"Advanced settings"** (or look for the "Settings" menu after creating the app).
2. Paste the following TOML configuration into the "Secrets" text area:

```toml
# .streamlit/secrets.toml

OPENAI_API_KEY = "sk-..."
TAVILY_API_KEY = "tvly-..."
```
*(Replace the values above with your actual API keys found in your local `.env` file)*

## 4. Deploy & Verify

1. Click **"Deploy"**.
2. Streamlit will verify your repo, install dependencies, and launch the app.
3. Once the balloon animation finishes, your app is live!

### Troubleshooting

- **"ModuleNotFoundError"**: Ensure `requirements.txt` contains all libraries (e.g., `chromadb`, `langchain`, `pysqlite3-binary`).
- **"OpenAI API Error"**: Double-check your secrets for typos or whitespace.
- **"SQLite Error"**: Streamlit Cloud runs on Linux. If you see SQLite version errors, ensure `pysqlite3-binary` is in requirements and properly imported (the code already handles this patch).

## 5. Maintenance

To update the app, simply push changes to the `github` `main` branch. Streamlit Cloud will detect the commit and automatically redeploy.
