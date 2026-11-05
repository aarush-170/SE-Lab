# Lab 7 — Fuzzing for Input Validation Bugs

Name: Aarush Muralidhara | SRN: PES1UG24CS010 | Class: 5A
Problem statement: L6_L7_11 — Amusement Park Ride Access

## Files

| File | Description |
|------|-------------|
| `processor.py` | Fixed module (hardened against invalid input) |
| `test_processor.py` | Property-based fuzz tests using Hypothesis |
| `Lab7_Screenshots.pdf` | Screenshots for Steps 2, 4, 5 and 6 |

## Bugs found by fuzzing

| Function | Crashing inputs (original code) | Fix |
|----------|--------------------------------|-----|
| `validate_height_and_fastpass` | `None`, `""`, `":"`, unknown FastPass value | Type check, part-count check, strict digit/range check on height, membership check on pass value |
| `compute_dispatch_throughput` | `None`, `""`, `"/"`, `"0/0"`, `inf`/negative results | Type and part-count checks, `try/except ValueError`, reject `nan`/`inf`, require riders ≥ 0 and mins > 0 |
| `resolve_safety_restraint_code` | `None`, unknown prefix | Type and length check, `dict.get()` with error message |

## Run

```
pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py
```
