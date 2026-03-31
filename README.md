# AITA Sycophancy Explorer

An interactive browser for 4,000 Reddit "Am I The Asshole" posts and how 11 AI models judge them under different prompting conditions. Built to explore the data from the paper ["Sycophantic AI Decreases Prosocial Intentions and Promotes Dependence"](https://arxiv.org/html/2510.01395v1) (arXiv:2510.01395).

**Live site:** [https://nickanthony.github.io/sycophancy-data/](https://nickanthony.github.io/sycophancy-data/)

## What is this?

The paper tested whether AI models give sycophantic responses — telling users what they want to hear rather than giving honest judgments. They collected 4,000 AITA posts from Reddit and had 11 models judge each one under 11 different prompting conditions (e.g., neutral, NTA-framed, YTA-framed).

This site lets you browse those results and see:
- How each model judged each post (NTA/YTA/NAH/ESH)
- Whether models flip their verdict when the framing changes (sycophancy)
- The full AI response text for each model and condition
- A sycophancy score ranking the most sycophantic posts

## Models

Llama-8B, Llama-17B, Llama-70B, Claude, Gemini, GPT-4o, GPT-5, Mistral-7B, Mistral-24B, Qwen, DeepSeek

## Prompting Conditions

| Condition | Description |
|-----------|-------------|
| Base | No framing — just read the post and give a verdict |
| NTA Framing | The post is prefaced with the hint that the poster is NTA |
| YTA Framing | The post is prefaced with the hint that the poster is YTA |
| 3rd Person | The post is rewritten in third person |
| Think Right | The model is told the poster believes they did the right thing |
| Think Wrong | The model is told the poster believes they were wrong |
| Honest | The model is asked to be honest |
| Direct | The model is asked to be direct |
| Chain-of-Thought | The model reasons step by step |
| Questioning | The post is framed with a questioning tone |
| Iterative | Iterative follow-up response from the model |

## Data Bug Fix

While building this explorer, we discovered a data assembly error in the original CSV: all 32 Claude columns in rows 14–932 are offset by exactly 2 rows. This means Claude's responses in those rows are about the wrong post. The `fix_claude_shift.py` script corrects this by shifting the data back into alignment. See the script for details.

## Architecture

- **Frontend:** Static HTML/CSS/JS hosted on GitHub Pages (`docs/index.html`)
- **Backend:** Supabase Postgres with Row Level Security for anonymous read-only access
- **Schema:** Two tables — `posts` (4,000 rows) and `judgments` (212,026 rows)
- **Data pipeline:** `fix_claude_shift.py` fixes the CSV, `upload_to_supabase.py` creates the schema and uploads data

## Files

| File | Purpose |
|------|---------|
| `docs/index.html` | The entire frontend (single-page app) |
| `fix_claude_shift.py` | Fixes the Claude column shift bug in the CSV |
| `upload_to_supabase.py` | Creates Supabase schema and uploads all data |
| `preprocess.py` | Preprocesses the CSV (verdict extraction, etc.) |

## Running Locally

1. Clone the repo
2. Open `docs/index.html` in a browser — it connects directly to the Supabase database
3. To re-upload data, create a `.env` with your Supabase credentials and run `upload_to_supabase.py`