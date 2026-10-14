"""Student scholarship eligibility screener.

Computes a merit score from GPA and extracurricular credits, checks family
income against a limit, and saves the shortlist to a JSON file.
"""
import json

DEFAULT_GPA_WEIGHT = 10
CREDIT_WEIGHT = 2
INCOME_LIMIT = 800000
CUTOFF = 85
MAX_GPA = 10.0
RESULTS_FILE = "scholarships.json"


def calculate_merit_score(gpa, credit_count, gpa_weight=DEFAULT_GPA_WEIGHT):
    """Return the merit score for a GPA and extracurricular credit count."""
    return gpa * gpa_weight + credit_count * CREDIT_WEIGHT


def is_valid_applicant(gpa, credit_count, income):
    """Return True only if the applicant's data is in a sensible range."""
    return (0 <= gpa <= MAX_GPA and credit_count >= 0
            and income is not None and income >= 0)


def evaluate_applicant(results, student_id, test_scores, logs=None,
                       gpa_weight=DEFAULT_GPA_WEIGHT):
    """Score one applicant, record the result and return eligibility."""
    if logs is None:
        logs = []
    gpa = test_scores["gpa"]
    credit_count = test_scores.get("credits", 0)
    income = test_scores.get("income")
    score = calculate_merit_score(gpa, credit_count, gpa_weight)
    eligible = (is_valid_applicant(gpa, credit_count, income)
                and score >= CUTOFF and income < INCOME_LIMIT)
    results[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible


def read_gpa_weight():
    """Ask for a GPA weight; fall back to the default on empty/bad input."""
    raw = input(f"GPA weight (Enter to keep default {DEFAULT_GPA_WEIGHT}): ")
    raw = raw.strip()
    if not raw:
        return DEFAULT_GPA_WEIGHT
    try:
        weight = float(raw)
    except ValueError:
        print("Not a number; keeping the default weight.")
        return DEFAULT_GPA_WEIGHT
    if weight <= 0:
        print("Weight must be positive; keeping the default weight.")
        return DEFAULT_GPA_WEIGHT
    return weight


def persist_results(results, file=RESULTS_FILE):
    """Write the results dictionary to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(results, handle)


def load_results(file=RESULTS_FILE):
    """Load results from a JSON file; return an empty dict on failure."""
    try:
        with open(file, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as err:
        print(f"Could not load results from {file}: {err}")
        return {}


def print_shortlist(results):
    """Print every eligible applicant with their score."""
    print("Shortlisted applicants:")
    for student_id, record in results.items():
        if record["eligible"]:
            print(" ", student_id, "score =", record["score"])


def main():
    """Evaluate the sample applicants and print the shortlist."""
    results = {}
    evaluate_applicant(results, "U001",
                       {"gpa": 9.1, "credits": 4, "income": 450000})
    evaluate_applicant(results, "U002",
                       {"gpa": 7.2, "credits": 1, "income": 300000})
    evaluate_applicant(results, "U003",
                       {"gpa": 12.5, "credits": -3, "income": -1})
    evaluate_applicant(results, "U004", {"gpa": 6.5})
    gpa_weight = read_gpa_weight()
    evaluate_applicant(results, "U005",
                       {"gpa": 8.4, "credits": 3, "income": 600000},
                       gpa_weight=gpa_weight)
    persist_results(results)
    print_shortlist(load_results())


if __name__ == "__main__":
    main()
