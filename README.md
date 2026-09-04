# Gomoku — Competitive AI & Streamlit App

This repository is a compact, production-minded prototype of a Gomoku (Five-in-a-Row) game featuring a playable Streamlit front-end and an AI opponent built from modular heuristics and search algorithms. It demonstrates algorithm design, heuristic engineering, and clean Python architecture.

**What to look for**
- **Algorithmic design**: modular search and heuristic components that show decision-making logic and trade-offs.
- **Engineering quality**: small, testable modules in `src/` (game rules, move validation, heuristics, search, and bot orchestration).
- **Product thinking**: a lightweight Streamlit app for quick evaluation and interactive testing.

**Highlights**
- Playable UI via Streamlit for rapid evaluation.
- An AI bot combining heuristic capture logic and search-based move selection.
- Clear separation of concerns: `src/game.py`, `src/valid_move.py`, `src/heuristic.py`, `src/search_algo.py`, `src/bot.py`.

Quickstart (run locally)

1. Verify Python and pip:

```
python --version
```

2. Create and activate a virtual environment:

Linux / macOS

```
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell)

```
.venv\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Launch the app:

```
streamlit run gomoku.py
```

Where to explore in the codebase
- `src/search_algo.py` — the search controller and decision logic.
- `src/heuristic.py` and `dev/heuristic.ipynb` — how heuristics are designed and tested.
- `src/bot.py` — ties heuristics and search into a playable opponent.

Skills demonstrated
- Python, algorithm & heuristic design, game-state modeling
- Search algorithms (customizable), heuristics, and decision logic
- Streamlit for rapid product evaluation, modular code organization


This project is intended as a compact technical artifact you can run in 5 minutes and use as a talking point in interviews. It shows practical algorithm work (trade-offs between speed and accuracy), the ability to produce interactive experiences, and a clean, modular code layout ready for extension.
