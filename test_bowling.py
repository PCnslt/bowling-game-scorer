"""Tests for bowling.py (run with: pytest)."""

import pytest

from bowling import score_game


EXAMPLE_GAME = ["8", "/", "5", "4", "9", "0", "X", "X", "5", "/",
                "5", "3", "6", "3", "9", "/", "9", "/", "X"]


# ---------------------------------------------------------------- scoring

def test_example_game_from_the_exercise():
    assert score_game(EXAMPLE_GAME) == [15, 24, 33, 58, 78, 93, 101, 110, 129, 149]


def test_perfect_game_is_300():
    assert score_game(["X"] * 12)[-1] == 300


def test_perfect_game_cumulative_scores():
    assert score_game(["X"] * 12) == [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]


def test_all_spares_with_five_bonus_is_150():
    assert score_game(["5", "/"] * 10 + ["5"])[-1] == 150


def test_all_open_frames():
    # ten frames of 1 + 2 = 3 pins each, no bonuses anywhere
    assert score_game(["1", "2"] * 10) == [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]


def test_lowercase_x_counts_as_strike():
    assert score_game(["x"] * 12)[-1] == 300


# ---------------------------------------------------------- tenth frame

NINE_OPEN_FRAMES = ["1", "2"] * 9  # 27 pins going into frame 10


def test_tenth_frame_strike_earns_two_bonus_rolls():
    scores = score_game(NINE_OPEN_FRAMES + ["X", "4", "3"])
    assert scores[-1] == 27 + 17


def test_tenth_frame_spare_earns_one_bonus_roll():
    scores = score_game(NINE_OPEN_FRAMES + ["4", "/", "7"])
    assert scores[-1] == 27 + 17


def test_tenth_frame_open_frame_ends_the_game():
    scores = score_game(NINE_OPEN_FRAMES + ["4", "3"])
    assert scores[-1] == 27 + 7


# ----------------------------------------------------------- validation

@pytest.mark.parametrize("rolls, reason", [
    (["/", "5"] + ["1", "2"] * 9, "spare as the very first roll"),
    (["1", "2", "/", "5"] + ["1", "2"] * 8, "spare as the first roll of a frame"),
    (["1", "F"] + ["1", "2"] * 9, "invalid character"),
    (["1", "2"] * 9 + ["4", "3", "5"], "bonus roll in 10th without strike/spare"),
    (["5", "9"] + ["1", "2"] * 9, "frame pin count exceeds 10 without spare"),
    (["X"] * 13, "extra rolls after the game is complete"),
    (["1", "2"] * 8 + ["1"], "incomplete game"),
    (["1", "2"] * 9 + ["4", "/"], "missing bonus roll after a 10th-frame spare"),
    (["5", "5"] + ["1", "2"] * 9, "10 pins in two rolls must be written as '/'"),
    (["1", "X"] + ["1", "2"] * 9, "strike as the second roll of a frame"),
    (["X", "/"] + ["1", "2"] * 8 + ["1", "2"], "spare directly after a strike"),
    (["1", "2"] * 9 + ["X", "5", "9"], "impossible bonus pair in the 10th"),
])
def test_invalid_games_raise_value_error(rolls, reason):
    with pytest.raises(ValueError):
        score_game(rolls)
