def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # Fixed: Hard is now the widest range. Was 1-50, which made it easier than Normal.
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # Fixed: return just the outcome string (was returning an (outcome, message) tuple,
    # which the tests didn't expect). Also removed the lexicographic string-compare
    # fallback that produced wrong hints.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def message_for_outcome(outcome: str):
    """Return the player-facing hint message for an outcome."""
    # Fixed: hints now point the right way. The original had them reversed
    # ("Too High" said Go HIGHER), which is why the hints "lied".
    return {
        "Win": "🎉 Correct!",
        "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }.get(outcome, "")


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    A win awards more points the fewer attempts it took (min 10).
    Incorrect guesses do not change the score.
    """
    if outcome == "Win":
        # Fixed: off-by-one in the points formula (was attempt_number + 1, double-counting
        # the already-incremented attempt), so a first-guess win is now a full 100.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # Fixed: wrong guesses no longer change the score. The original added/subtracted
    # points on "Too High"/"Too Low".
    return current_score
