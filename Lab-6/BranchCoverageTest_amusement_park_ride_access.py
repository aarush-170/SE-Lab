"""Lab 6 - Branch coverage tests for amusement_park_ride_access.py
Every if/elif/else and loop exit is driven both ways (True and False)."""
import pytest
from amusement_park_ride_access import process_ride_admissions, inspect_safety_restraints


def patron(h=150, warn=False, child=False):
    return {"height_cm": h, "health_warning": warn, "is_child": child}


# ---------- input validation (both sides of the `or`) ----------

def test_groups_not_a_list_raises():
    with pytest.raises(ValueError):
        process_ride_admissions({"is_open": True}, 5.0)


def test_negative_fee_raises():
    with pytest.raises(ValueError):
        process_ride_admissions([], -0.01)


def test_empty_groups_list_zero_admissions():
    # outer for-loop never executes
    assert process_ride_admissions([], 0.0) == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


# ---------- is_open ----------

def test_closed_group_skipped():
    groups = [{"is_open": False, "ride_type": "family", "patrons": [patron()]}]
    assert process_ride_admissions(groups, 5.0)["status"] == "ZERO_ADMISSIONS"


def test_missing_is_open_defaults_to_closed():
    groups = [{"ride_type": "family", "patrons": [patron()]}]
    assert process_ride_admissions(groups, 5.0)["status"] == "ZERO_ADMISSIONS"


# ---------- ride_type branches ----------

@pytest.mark.parametrize("ride_type, expected", [
    ("roller_coaster", 25.0),
    ("water_ride", 18.0),
    ("family", 10.0),
])
def test_each_ride_type_base_price(ride_type, expected):
    groups = [{"is_open": True, "ride_type": ride_type, "patrons": [patron()]}]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": expected, "status": "COMPLETED"}


def test_missing_ride_type_defaults_to_family():
    groups = [{"is_open": True, "patrons": [patron()]}]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


def test_unknown_ride_type_rejected():
    groups = [{"is_open": True, "ride_type": "go_karts", "patrons": [patron()]}]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


# ---------- patron loop branches ----------

def test_group_with_no_patrons_only_fast_lane_fee():
    # inner loop never executes; fast-lane fee still charged
    groups = [{"is_open": True, "ride_type": "family", "has_fast_lane": True, "patrons": []}]
    assert process_ride_admissions(groups, 7.5) == {"total_revenue": 7.5, "status": "COMPLETED"}


def test_zero_height_rejected():
    groups = [{"is_open": True, "ride_type": "family", "patrons": [patron(0), patron()]}]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


def test_boundary_height_120_admitted():
    groups = [{"is_open": True, "ride_type": "family", "patrons": [patron(120)]}]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


def test_height_119_rejected():
    groups = [{"is_open": True, "ride_type": "family", "patrons": [patron(119), patron()]}]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 10.0


def test_child_discount():
    groups = [{"is_open": True, "ride_type": "roller_coaster", "patrons": [patron(130, child=True)]}]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 15.0  # 25 * 0.60


def test_health_warning_on_roller_coaster_voids_group():
    # paying adult first, then health warning -> group_total reset to 0 and loop breaks,
    # so the third patron is never charged
    groups = [{"is_open": True, "ride_type": "roller_coaster",
               "patrons": [patron(), patron(warn=True), patron()]}]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_health_warning_on_non_roller_coaster_only_rejects_that_patron():
    groups = [{"is_open": True, "ride_type": "water_ride",
               "patrons": [patron(warn=True), patron()]}]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 18.0


def test_patron_with_missing_keys_rejected():
    groups = [{"is_open": True, "ride_type": "family", "patrons": [{}]}]
    assert process_ride_admissions(groups, 5.0)["status"] == "ZERO_ADMISSIONS"


# ---------- fast lane ----------

def test_fast_lane_added():
    groups = [{"is_open": True, "ride_type": "family", "has_fast_lane": True, "patrons": [patron()]}]
    assert process_ride_admissions(groups, 5.0)["total_revenue"] == 15.0


# ---------- final status branches ----------

def test_exactly_four_rejections_not_audit():
    groups = [{"is_open": True, "ride_type": "family",
               "patrons": [patron(0), patron(0), patron(0), patron(0), patron()]}]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_five_rejections_triggers_safety_audit():
    groups = [{"is_open": True, "ride_type": "family",
               "patrons": [patron(0)] * 5 + [patron()]}]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 10.0, "status": "SAFETY_AUDIT"}


def test_multiple_groups_revenue_summed_and_rounded():
    groups = [
        {"is_open": True, "ride_type": "water_ride", "patrons": [patron(child=True)]},  # 10.8
        {"is_open": True, "ride_type": "family", "patrons": [patron(child=True)]},      # 6.0
    ]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 16.8, "status": "COMPLETED"}


# ---------- inspect_safety_restraints ----------

@pytest.mark.parametrize("streams", [[], None])
def test_restraints_no_data(streams):
    assert inspect_safety_restraints(streams) == "NO_DATA"


def test_restraints_two_consecutive_zeros_emergency():
    assert inspect_safety_restraints([[0, 0]]) == "EMERGENCY_LOCK"


def test_restraints_streak_resets_on_latched_reading():
    assert inspect_safety_restraints([[0, 1, 0, 1]]) == "SAFE"


def test_restraints_emergency_in_later_stream():
    # streak does not carry across streams; second stream trips the lock
    assert inspect_safety_restraints([[1, 0], [0, 1, 0, 0]]) == "EMERGENCY_LOCK"


def test_restraints_empty_reading_list_is_safe():
    assert inspect_safety_restraints([[]]) == "SAFE"


def test_restraints_all_latched_safe():
    assert inspect_safety_restraints([[1, 1, 1], [1]]) == "SAFE"
