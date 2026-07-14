"""Score a ten-pin bowling game.

Input style: Option B -- a flat list of roll symbols, in order.
    "X" or "x"  -> strike (all 10 pins on the first shot of a frame)
    "/"         -> spare  (remaining pins on the second shot of a frame)
    "0"-"9"     -> that many pins knocked down

Example:
    score_game(["8", "/", "5", "4", "9", "0", "X", "X", "5", "/",
                "5", "3", "6", "3", "9", "/", "9", "/", "X"])
    -> [15, 24, 33, 58, 78, 93, 101, 110, 129, 149]
"""


def score_game(rolls):
    """Score a complete bowling game.

    Args:
        rolls: flat list of roll symbols, e.g. ["8", "/", "5", "4", ...]

    Returns:
        A list of 10 cumulative scores, one per frame.

    Raises:
        ValueError: if the game is invalid or incomplete.
    """
    pins = _to_pin_counts(rolls)
    _validate_frames(rolls, pins)

    scores = []
    total = 0
    roll = 0  # index of the first roll of the current frame

    for _frame in range(9):  # frames 1-9
        if pins[roll] == 10:  # strike: 10 + the next two rolls
            total += 10 + pins[roll + 1] + pins[roll + 2]
            roll += 1
        elif pins[roll] + pins[roll + 1] == 10:  # spare: 10 + the next roll
            total += 10 + pins[roll + 2]
            roll += 2
        else:  # open frame: just the pins knocked down
            total += pins[roll] + pins[roll + 1]
            roll += 2
        scores.append(total)

    # Frame 10: simply all pins knocked down in it, including bonus rolls.
    total += sum(pins[roll:])
    scores.append(total)
    return scores


def _to_pin_counts(rolls):
    """Translate each symbol into the number of pins that roll knocked down."""
    pins = []
    for i, symbol in enumerate(rolls):
        s = str(symbol)
        if s in ("X", "x"):
            pins.append(10)
        elif s == "/":
            # A spare closes out the pins left by the previous roll,
            # so it only makes sense right after a numbered roll.
            if i == 0 or not str(rolls[i - 1]).isdigit():
                raise ValueError(f"Roll {i + 1}: '/' must follow a numbered roll")
            pins.append(10 - pins[i - 1])
        elif s.isdigit() and len(s) == 1:
            pins.append(int(s))
        else:
            raise ValueError(f"Roll {i + 1}: invalid symbol {symbol!r}")
    return pins


def _validate_frames(rolls, pins):
    """Check that the rolls form exactly one complete, legal 10-frame game."""
    roll = 0

    for frame in range(1, 10):  # frames 1-9
        if roll >= len(rolls):
            raise ValueError(f"Frame {frame}: game is incomplete")
        if str(rolls[roll]) == "/":
            raise ValueError(f"Frame {frame}: '/' cannot be the first roll of a frame")
        if pins[roll] == 10:  # strike: the frame ends after one roll
            roll += 1
            continue
        if roll + 1 >= len(rolls):
            raise ValueError(f"Frame {frame}: game is incomplete")
        _check_second_roll(frame, rolls[roll + 1], pins[roll], pins[roll + 1])
        roll += 2

    # Frame 10
    tenth, tenth_pins = rolls[roll:], pins[roll:]
    if len(tenth) < 2:
        raise ValueError("Frame 10: game is incomplete")
    if str(tenth[0]) == "/":
        raise ValueError("Frame 10: '/' cannot be the first roll of a frame")

    if tenth_pins[0] == 10:  # strike -> two bonus rolls
        allowed = 3
        # The two bonus rolls are thrown at a fresh rack, so they must
        # also be a legal pair (e.g. "X", "5", "9" is impossible).
        if len(tenth) == 3 and tenth_pins[1] != 10:
            _check_second_roll(10, tenth[2], tenth_pins[1], tenth_pins[2])
    elif str(tenth[1]) == "/":  # spare -> one bonus roll
        allowed = 3
    else:  # open frame -> no bonus rolls
        allowed = 2
        _check_second_roll(10, tenth[1], tenth_pins[0], tenth_pins[1])

    if len(tenth) > allowed:
        raise ValueError("Frame 10: extra rolls after the game is complete")
    if len(tenth) < allowed:
        raise ValueError("Frame 10: game is incomplete (bonus roll missing)")


def _check_second_roll(frame, symbol, first_pins, second_pins):
    """Validate the second roll of a pair thrown at the same rack of pins."""
    if str(symbol) in ("X", "x"):
        raise ValueError(f"Frame {frame}: 'X' is only valid as the first roll of a frame")
    if str(symbol) == "/":
        return  # a spare pairs with any first roll
    frame_total = first_pins + second_pins
    if frame_total == 10:
        raise ValueError(f"Frame {frame}: 10 pins in two rolls must be written as a spare '/'")
    if frame_total > 10:
        raise ValueError(f"Frame {frame}: frame total {frame_total} exceeds 10 pins")


if __name__ == "__main__":
    # Tiny command-line convenience (no UI required by the exercise):
    #   python bowling.py 8 / 5 4 9 0 X X 5 / 5 3 6 3 9 / 9 / X
    import sys

    print(score_game(sys.argv[1:]))
