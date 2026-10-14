# Lab 5 – Issues Found and Fixed (`scholarship_system.py`)

Line numbers refer to the original file.

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Use of `eval()` on user input | Bandit B307, Pylint W0123 | Security | Medium (Bandit) | 12, 24–26, 51–53 | `MERIT_FORMULA` is evaluated with `eval()`, and `main()` lets the user replace it via `input()`. Any Python expression runs, e.g. `__import__('os').system(...)` executes shell commands (arbitrary code execution). | Removed `eval()` and the formula string. Score is now computed directly as `gpa * gpa_weight + credit_count * CREDIT_WEIGHT`. The prompt now asks only for a numeric GPA weight, parsed with `float()` and validated (> 0). |
| 2 | Bare `except:` with `pass` | Bandit B110, Pylint W0702, Flake8 E722 | Bug / Security | Low (Bandit) | 35–38 | Catches every exception (even `KeyboardInterrupt`) and silently ignores it, so a missing or corrupt results file goes unnoticed. | Catch only `(OSError, json.JSONDecodeError)`, print an error message, and return an empty dict. |
| 3 | Mutable default argument | Pylint W0102 | Bug | Warning | 14 | `logs=[]` is created once and shared across every call, so log entries leak between applicants. | Default changed to `None`; a new list is created inside the function. |
| 4 | Invalid input accepted (logic bug, not flagged by any tool) | Manual (program output) | Bug | High (wrong result) | 19, 49 | U003 has GPA 12.5 (on a 10-point scale), credits −3 and income −1, yet is shortlisted with score 119. Missing income also defaults to 0, which passes the income check. | Added `is_valid_applicant()`: GPA must be 0–10, credits ≥ 0, income present and ≥ 0. Missing income is no longer treated as 0. |
| 5 | Files opened without `with` / encoding | Pylint R1732, W1514 | Bug / Quality | Refactor / Warning | 29–31, 36 | Manual `open()`/`close()` leaks the handle if an exception occurs; encoding depends on the platform. | Use `with open(..., encoding="utf-8")` and `json.dump` / `json.load`. |
| 6 | Global mutable state | Pylint W0603 | Design | Warning | 6, 25, 34 | `results` and `MERIT_FORMULA` are modified via `global`, making functions depend on hidden state. | `results` is created in `main()` and passed to functions; the GPA weight is passed as a parameter. |
| 7 | Unused imports | Flake8 F401, Pylint W0611 | Style | Warning | 2, 3 | `math` and `sys` are imported but never used. | Removed. |
| 8 | Missing blank lines (PEP 8) | Flake8 E302, E305 | Style | – | 11, 14, 24, 28, 33, 40, 46, 59 | Top-level functions need two blank lines between them. | Added two blank lines before each function and before the entry point. |
| 9 | Comparison to `True` | Flake8 E712, Pylint C0121 | Style | – | 43 | `== True` is redundant. | Changed to `if record["eligible"]:`. |
| 10 | Shadowing built-in `credits` | Pylint W0622 | Quality | Warning | 11, 16 | `credits` is a Python built-in name. | Renamed to `credit_count`. |
| 11 | Non-snake_case name | Pylint C0103 | Style | Convention | 40 | `printShortlist` violates PEP 8 naming. | Renamed to `print_shortlist`. |
| 12 | Missing docstrings | Pylint C0114, C0116 | Documentation | Convention | 1 and all functions | No module or function docstrings. | Added a module docstring and one per function. |
| 13 | Old-style `%` formatting | Pylint C0209 | Style | Convention | 21 | `"%s scored %s" % (...)` | Changed to an f-string. |
| 14 | Script runs on import | Best practice | Quality | – | 59 | `main()` runs whenever the module is imported. | Wrapped in `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.69/10 | 10.00/10 |
| Bandit | 2 issues (1 Medium, 1 Low) | No issues identified |
| Flake8 | 12 issues | 0 issues |

Program output (default input): before, U001, **U003** and U005 were shortlisted; after, only U001 and U005 (U003's data is invalid).
