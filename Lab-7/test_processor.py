from hypothesis import given, settings, strategies as st
from processor import validate_height_and_fastpass, compute_dispatch_throughput, resolve_safety_restraint_code

# Mix of fully random text, None, and "almost valid" structured inputs
# so the fuzzer reaches deeper code paths (not just the first split()).
rider_specs = st.one_of(
    st.none(),
    st.text(),
    st.builds(lambda h, p: f"{h}:{p}", st.text(max_size=6), st.text(max_size=5)),
    st.builds(lambda h, p: f"{h}:{p}", st.integers(-1000, 1000), st.sampled_from(["YES", "NO", "yes", " no ", "MAYBE", ""])),
)

throughput_specs = st.one_of(
    st.none(),
    st.text(),
    st.builds(lambda r, m: f"{r}/{m}", st.text(max_size=6), st.text(max_size=6)),
    st.builds(lambda r, m: f"{r}/{m}", st.floats(allow_nan=True, allow_infinity=True), st.floats(allow_nan=True, allow_infinity=True)),
    st.builds(lambda r, m: f"{r}/{m}", st.integers(-100, 100), st.integers(-5, 5)),
)

zone_codes = st.one_of(
    st.none(),
    st.text(),
    st.builds(lambda p, s: f"{p}_{s}", st.sampled_from(["CST", "WTR", "DRP", "WHL", "cst", "XYZ", "C", ""]), st.text(max_size=4)),
)


@settings(max_examples=500)
@given(rider_specs)
def test_validate_height_and_fastpass_no_crash(s):
    try:
        result = validate_height_and_fastpass(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"validate_height_and_fastpass crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(throughput_specs)
def test_compute_dispatch_throughput_safe(s):
    try:
        result = compute_dispatch_throughput(s)
        # Valid result must be a finite, non-negative number; otherwise None
        if result is not None:
            assert isinstance(result, float)
            assert result == result and result not in (float("inf"), float("-inf")), f"non-finite rate {result}"
            assert result >= 0, f"negative rate {result}"
    except AssertionError:
        raise
    except Exception as e:
        assert False, f"compute_dispatch_throughput crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=500)
@given(zone_codes)
def test_resolve_safety_restraint_code_safe(s):
    try:
        result = resolve_safety_restraint_code(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"resolve_safety_restraint_code crashed on {s!r} with: {type(e).__name__}: {e}"
