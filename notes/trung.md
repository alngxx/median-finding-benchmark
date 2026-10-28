# Notes: Thanh Trung Le

One entry per working session. Copy the block below for each new session.

## 2026-10-28 / 29

## What I did
- Ran pytest (207 passed) on Windows, Python 3.13.1, in a new .venv.
- Ran the full e1-e6 (3230 s) before predictions were locked. Moved the output to ../pilot-run-28oct without opening it. Will re-run after the predictions-locked tag.

## Bugs
- `python` pointed to MSYS2 Python without pip, while `pytest` used another Python, so matplotlib was missing for `python`. Fixed with a .venv from `py`.

## Decisions
- Always run through .venv\Scripts\python so tests, runner and plots use one interpreter.
- Re-run all experiments after the tag instead of keeping the early run.