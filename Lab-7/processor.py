import math

MIN_HEIGHT_CM = 120
MAX_HEIGHT_CM = 300
PASS_MAP = {"YES": True, "NO": False}
RESTRAINT_TYPES = {
    "CST": "Over-the-Shoulder Harness",
    "WTR": "Lap Bar and Seatbelt",
    "DRP": "Hydraulic Shoulder Vest",
    "WHL": "Manual Safety Bar",
}


def validate_height_and_fastpass(rider_spec):
    # Fix 1: reject None / non-string input (was AttributeError on .strip())
    if not isinstance(rider_spec, str):
        return "Error: rider spec must be a string"

    # Fix 2: require exactly one ':' (was ValueError on unpacking)
    parts = rider_spec.strip().split(':')
    if len(parts) != 2:
        return "Error: expected format Height:FastPass (e.g. 140:YES)"
    height_str, pass_str = parts[0].strip(), parts[1].strip()

    # Fix 3: height must be plain ASCII digits (int() alone accepts '1_2', '+5',
    # Unicode digits, and raises on '' / 'abc')
    if not height_str.isascii() or not height_str.isdigit():
        return "Error: height must be a whole number in cm"
    height = int(height_str)

    # Fix 4: physically plausible range (rejects 0 and absurd values)
    if height <= 0 or height > MAX_HEIGHT_CM:
        return f"Error: height must be between 1 and {MAX_HEIGHT_CM} cm"

    # Fix 5: unknown FastPass value (was KeyError)
    pass_key = pass_str.upper()
    if pass_key not in PASS_MAP:
        return "Error: FastPass must be YES or NO"
    has_fastpass = PASS_MAP[pass_key]

    eligible = height >= MIN_HEIGHT_CM
    status = "FastPass Priority" if has_fastpass else "Standard Entry"
    return f"Height {height}cm: {'Approved' if eligible else 'Denied'} ({status})"


def compute_dispatch_throughput(ride_metric_str):
    # Returns a finite, non-negative float, or None for invalid input.
    # Fix 1: reject None / non-string input (was AttributeError on .split())
    if not isinstance(ride_metric_str, str):
        return None

    # Fix 2: require exactly one '/' (was ValueError on unpacking)
    parts = ride_metric_str.split('/')
    if len(parts) != 2:
        return None

    # Fix 3: non-numeric parts (was ValueError from float())
    try:
        riders = float(parts[0].strip())
        cycle_mins = float(parts[1].strip())
    except ValueError:
        return None

    # Fix 4: reject nan / inf (float() accepts 'nan', 'inf')
    if not (math.isfinite(riders) and math.isfinite(cycle_mins)):
        return None

    # Fix 5: negative riders, and zero/negative cycle time (was ZeroDivisionError)
    if riders < 0 or cycle_mins <= 0:
        return None

    rate = riders / cycle_mins
    # Fix 6: overflow, e.g. 1e308 / 1e-308 -> inf
    if not math.isfinite(rate):
        return None
    return round(rate, 2)


def resolve_safety_restraint_code(zone_code):
    # Fix 1: reject None / non-string input (was AttributeError on .strip())
    if not isinstance(zone_code, str):
        return "Error: zone code must be a string"

    code = zone_code.strip().upper()
    # Fix 2: too short to contain a prefix
    if len(code) < 3:
        return "Error: zone code too short (e.g. CST_01)"

    # Fix 3: unknown prefix (was KeyError)
    return RESTRAINT_TYPES.get(code[:3], "Error: unknown ride zone code")


def main():
    print("==== Running validate_height_and_fastpass ====")
    r_input = input("Enter rider spec (Height:FastPass, e.g. 140:YES): ")
    print(validate_height_and_fastpass(r_input))

    print("\n==== Running compute_dispatch_throughput ====")
    t_input = input("Enter riders/mins (e.g. 48/2.5): ")
    rate = compute_dispatch_throughput(t_input)
    if rate is None:
        print("Error: invalid input, expected riders/mins with mins > 0 (e.g. 48/2.5)")
    else:
        print("Throughput (riders/min):", rate)

    print("\n==== Running resolve_safety_restraint_code ====")
    z_input = input("Enter ride zone code (e.g. CST_01, WTR_A): ")
    print("Restraint:", resolve_safety_restraint_code(z_input))


if __name__ == "__main__":
    main()
