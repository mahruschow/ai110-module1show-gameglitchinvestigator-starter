# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game ran and looked normal at first, but it was basically unwinnable. The hints were backwards — when I guessed too high it told me to "Go HIGHER," which sent me in the wrong direction every time. On top of that, the secret seemed to flip behavior between guesses: on even-numbered attempts the code converted the secret to a string and compared it lexicographically, so the same guess could get a different hint depending on which turn it was. The score also dropped on wrong guesses, "New Game" wouldn't actually restart after a win, and the info box always said "between 1 and 100" even on Easy mode (which is really 1–20).

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret = 50, guess 60 | Hint says "Go LOWER" (too high) | Hint said "Go HIGHER" — hints were reversed | None (silent logic bug) |
| Secret = 9, guess 40 on an even attempt | "Too High" since 40 > 9 | Got "Too Low" because the secret was a string and `"40" > "9"` is False lexicographically | None (silent type bug) |
| Click "New Game" after winning | Fresh game, status back to "playing" | Stayed on the "You already won" screen; status/score/history never reset | None |
| Run `pytest tests/` | Tests pass | 3 failed | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

---

## 2. How did you use AI as a teammate?

I used an AI assistant to scan `app.py` and `logic_utils.py` and explain what each function was doing. One suggestion that was correct: it pointed out that on even attempts the code did `secret = str(...)`, which forced a string comparison and made the hints unreliable, and it recommended always comparing against the integer secret. I verified this by removing the string conversion and replaying the game — every guess then gave a consistent, correct hint. A suggestion I had to push back on was around `check_guess` returning a `(outcome, message)` tuple; the existing tests expected just the string `"Win"`, so blindly keeping the tuple would have kept the tests red. I verified the right shape by re-reading `tests/test_game_logic.py` and changing `check_guess` to return only the outcome string, with the message split into a separate helper.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed by reproducing the exact situation that triggered it and confirming the new behavior, instead of just assuming the code change worked. For testing I ran `pytest tests/`, which started at "3 failed" with `NotImplementedError` because the logic still lived in `app.py`, and ended at "3 passed in 0.00s" once I moved the functions into `logic_utils.py` and made `check_guess` return the outcome string the tests expected. That test run was useful because it forced me to match the function's real contract rather than the version I assumed. AI helped me understand the tests by walking through why `check_guess(50, 50) == "Win"` was failing — it was comparing a string against a tuple — which made the fix obvious.

---

## 4. What did you learn about Streamlit and state?

I'd tell a friend that Streamlit re-runs your entire script from top to bottom every time you click a button or change an input — it's not like a normal program that pauses and waits. Because of that, any normal variable gets recreated from scratch on every interaction, so it "forgets" everything. `st.session_state` is the fix: it's a dictionary that survives between reruns, so that's where you store things you want to persist, like the secret number, score, and attempt count. The key pattern is to only initialize a value `if "secret" not in st.session_state`, otherwise you'd overwrite it with a fresh random number on every single rerun. The "New Game" bug taught me that you have to remember to reset *all* of the related state keys, not just one or two.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is running the tests *first* to see them fail before I start fixing, so I have a clear signal for when the code is actually working instead of guessing. Next time I'd be more careful to read the existing tests and function docstrings before accepting any AI-written code, since the tuple-vs-string mismatch would have wasted time if I hadn't checked the contract. This project changed how I think about AI-generated code: it can look clean and "production-ready" while being full of silent logic bugs, so I now treat AI output as a draft to be verified, not as an answer to trust.
