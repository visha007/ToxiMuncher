# ToxiMuncher: A Context-Aware Toxicity Detection System
A CMPT 419 Final Project by Miro, Aroofa, and Shatavisha (Visha!)

ToxiMuncher is a two-part project combining contextual toxicity classification using transformer models with agent-based governance simulations.
Our goal is to explore how AI-driven toxicity detection tools influence online communities across different domains (general comments, forums, and gaming chat).

## Project Structure

This repository contains two major components:

## 1. ToxiMuncher Toxicity Classifier
A contextual language model based on DistilRoBERTa, fine-tuned to assign continuous toxicity scores on a 1–5 scale.

## Key features:
- Learns context beyond keywords
- Handles slang, sarcasm, and conversational nuance
- Avoids falsely flagging repeated punctuation
- Provides continuous toxicity scores (more nuanced than binary classifiers)

Two model variants:
### 1.1 ToxiMuncher-Lite: 
    - Trained on general-comment datasets
    - Captures toxicity commonly found on social media & forums
    - Datasets used:
        - Jigsaw Toxic Comment Classification Challenge [https://www.kaggle.com/datasets/julian3833/]jigsaw-toxic-comment-classification-challenge
        - Ruddit Dataset [https://github.com/hadarishav/Ruddit/tree/main/Dataset]
        - Real Toxicity Prompts (RTP) [https://huggingface.co/datasets/allenai/real-toxicity-prompts]

### 1.2 ToxiMuncher-Pro
    - Initialized with "-Lite" model weights
    - Fine-tuned on GameTox, a gaming-specific toxicity dataset
    - Tailored for fast-paced in-game chat, abbreviations, and gaming slang
    - Dataset: GameTox (NAACL 2025) [https://github.com/shucoll/GameTox/blob/main/gametox.csv]

## 2. Governance Simulation (Agents & Visualization)
Agent-based simulations demonstrate the downstream effects of deploying automated moderation. We implement two simulations, each with its own ecosystem and moderation dynamics.

### Game Chat Simulation (League of Legends Inspired)
A simulation of in-game team communication using:
- Mesa (agent-based modeling)
- GPT-5 Mini (chat generation)
- ToxiMuncher-Pro (toxic message scoring)

#### How it works:
Five PlayerAgents simulate game chat during a simplified “race to five coin-flip wins.” Each agent:
- has a “kind” or “rude/irritated” personality
- generates chat messages using an LLM prompt
- receives toxicity scores from ToxiMuncher-Pro
- may have messages removed depending on moderation threshold

#### Both unmoderated and moderated chat logs are saved:
- game_state.csv
- agent_messages.csv
- raw_chat_log.txt
- moderated_chat_log.txt

### Reddit Thread Simulation
A synthetic mini-Reddit built using:
- Mesa (user agents)
- GPT-5 Mini (post/comment generation)
- ToxiMuncher-Lite (toxicity scoring)
- Streamlit (interface for reviewing threads)

#### Simulated communities:
- r/vancouver
- r/students
- r/changemyview

### How it works: 
Each agent:
- creates a post or reply
- stores thread metadata (thread ID, parent ID, author ID, timestep)
- is scored for toxicity using ToxiMuncher-Lite
- is moderated if toxicity exceeds a threshold

The Streamlit app displays:
- an unmoderated reconstruction of threads
- a moderated version with removed toxic comments

## Installation & Dependencies

### Python Environment Setup

Recommended:
`python -m venv toximuncher-env`
`source toximuncher-env/bin/activate`         # Mac / Linux
`toximumcher-env\Scripts\activate`            # Windows

### Core Dependencies

Transformers (HuggingFace) -> rewuired for DistilRoBERTa
`pip install transformers` (or %pip install transformers - if running within jupyter notebook code cell) 

#### Required for DistilRoBERTa:
`pip install transformers`

#### PyTorch

Needed for model training & inference:
`pip install torch`

#### Data & Utilities
`pip install pandas numpy matplotlib datasets`

### Simulation Dependencies

#### Mesa (agent-based modeling)
`pip install mesa`

#### Solara (web visualization)

Follow official instructions:
https://solara.dev/documentation/getting_started/installing

Steps:
`python -m venv solara-env`
`source solara-env/bin/activate`
`pip install solara`

#### NetworkX
`pip install networkx`

#### Altair
`pip install altair`

### LLM Dependencies

#### If using GPT for simulation:
`pip install openai`

#### Helpful Documentation

- OpenAI API Best Practices (https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)
- OpenAI API Reference (https://platform.openai.com/docs/api-reference/introduction)
- Bearer Auth Reference (Swagger) (https://swagger.io/docs/specification/v3_0/authentication/bearer-authentication/)