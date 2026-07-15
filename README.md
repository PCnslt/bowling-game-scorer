# Bowling Game Scorer 🎳

A Python library that scores a ten-pin bowling game, with an arcade-style
web UI that runs the same Python code in your browser.

## Run it locally

```bash
# 1. Clone the repo
git clone https://github.com/PCnslt/bowling-game-scorer.git
cd bowling-game-scorer

# 2. Run the test suite (34 tests)
pip install pytest
pytest

# 3. Score a game from the command line
python bowling.py 8 / 5 4 9 0 X X 5 / 5 3 6 3 9 / 9 / X
# -> [15, 24, 33, 58, 78, 93, 101, 110, 129, 149]

# 4. Run the web UI locally
mkdir -p _site && cp docs/index.html bowling.py test_bowling.py _site/
python -m http.server 8000 -d _site
# then open http://localhost:8000 in your browser
```

## Use the website

Open **https://pcnslt.github.io/bowling-game-scorer/** (give it a few
seconds on first load — it downloads the Python runtime).

- **Tap the number buttons** (0–9) to bowl — the number is how many pins
  you knock down. **X** = a strike (all 10 pins), **/** = a spare
  (the rest of the pins). Buttons that aren't legal turn themselves off.
- **Watch the scoreboard** at the top fill in as you bowl — each frame
  shows your rolls and the running total. "…" means a frame is still
  waiting on its bonus rolls.
- Use **Undo / Reset** to fix a roll or start over, or tap a
  **famous game chip** (Example · 149, Perfect · 300, All spares · 150)
  to see a full scorecard instantly.
- Scroll to the bottom and press **▶ Run pytest** to run the project's
  real test suite right in your browser.
