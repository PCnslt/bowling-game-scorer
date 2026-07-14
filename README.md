# Bowling Game Scorer

A small Python library that scores a ten-pin bowling game, written for the
"Score a Bowling Game!" coding exercise (see `PROBLEM_STATEMENT.pdf`).

No dependencies for the library itself; `pytest` is used for the tests.

## Input style (Option B: Rolls)

The scorer takes **a flat list of roll symbols, in order**:

| Symbol | Meaning |
|--------|---------|
| `"X"` or `"x"` | strike (all 10 pins on the first shot of a frame) |
| `"/"` | spare (the remaining pins on the second shot) |
| `"0"`–`"9"` | that many pins knocked down |

It returns the **cumulative score at the end of each frame** (10 values).

## Usage

```python
from bowling import score_game

rolls = ["8", "/", "5", "4", "9", "0", "X", "X", "5", "/",
         "5", "3", "6", "3", "9", "/", "9", "/", "X"]

print(score_game(rolls))
# [15, 24, 33, 58, 78, 93, 101, 110, 129, 149]
```

Or from the command line:

```bash
python bowling.py 8 / 5 4 9 0 X X 5 / 5 3 6 3 9 / 9 / X
```

## Running the tests

```bash
pip install pytest
pytest
```

## Scoring rules implemented

- **Strike** — 10 points plus the sum of the next two rolls.
- **Spare** — 10 points plus the next roll.
- **Open frame** — just the pins knocked down.
- **Tenth frame** — a strike earns two bonus rolls, a spare earns one,
  an open frame ends the game. The tenth-frame score is simply the total
  pins knocked down in that frame, including bonus rolls.

## Validation

`score_game` raises `ValueError` (with a message naming the frame) for:

- `/` as the first roll of a frame, or directly after a strike
- a frame total over 10 pins without a spare indicator
- tenth-frame bonus rolls that weren't earned
- extra rolls after the game is complete
- invalid symbols (anything other than `X`/`x`, `/`, `0`–`9`)
- incomplete games (missing rolls or a missing earned bonus roll)

## Assumptions (documented per the exercise)

- Only **complete** games are scored; a partial game raises `ValueError`
  rather than returning `None` for unscoreable frames.
- Two numbered rolls totaling exactly 10 (e.g. `"5", "5"`) are rejected —
  a full rack must be written as a spare (`"5", "/"`).
- `X` is only accepted where a fresh rack of 10 pins is up: the first roll
  of a frame, or a tenth-frame bonus roll. Likewise the two bonus rolls
  after a tenth-frame strike must form a legal pair (`X 5 9` is rejected).
- Symbols may be passed as strings (`"5"`) — the example input style from
  the exercise. Lowercase `x` is accepted.
