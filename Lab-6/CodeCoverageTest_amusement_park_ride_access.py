"""Lab 6 - Code (line) coverage tests for amusement_park_ride_access.py"""
import pytest
from amusement_park_ride_access import process_ride_admissions, inspect_safety_restraints


def adult(h=150):
    return {"height_cm": h, "health_warning": False, "is_child": False}


# ---------- process_ride_admissions ----------

def test_single_adult_family_ride():
    groups = [{"is_open": True, "ride_type": "family", "has_fast_lane": False,
               "patrons": [adult()]}]
    result = process_ride_admissions(groups, 5.0)
    assert result == {"total_revenue": 10.0, "status": "COMPLETED"}


def test_invalid_groups_raises():
    with pytest.raises(ValueError):
        process_ride_admissions("not a list", 5.0)


def test_negative_fee_raises():
    with pytest.raises(ValueError):
        process_ride_admissions([], -1.0)


def test_closed_group_is_skipped():
    groups = [{"is_open": False, "ride_type": "family", "patrons": [adult()]}]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_roller_coaster_adult_with_fast_lane():
    groups = [{"is_open": True, "ride_type": "roller_coaster", "has_fast_lane": True,
               "patrons": [adult()]}]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 30.0, "status": "COMPLETED"}


def test_water_ride_child_discount():
    groups = [{"is_open": True, "ride_type": "water_ride",
               "patrons": [{"height_cm": 130, "health_warning": False, "is_child": True}]}]
    # 18.0 * 0.60 = 10.8
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 10.8, "status": "COMPLETED"}


def test_unknown_ride_type_rejected():
    groups = [{"is_open": True, "ride_type": "haunted_house", "patrons": [adult()]}]
    assert process_ride_admissions(groups, 5.0)["status"] == "ZERO_ADMISSIONS"


def test_invalid_height_short_and_health_warning_trigger_safety_audit():
    # 2 invalid heights + 2 too short + 1 health warning on roller coaster = 5 rejected (> 4)
    groups = [
        {"is_open": True, "ride_type": "family",
         "patrons": [adult(0), adult(-5), adult(100), adult(110)]},
        {"is_open": True, "ride_type": "roller_coaster",
         "patrons": [{"height_cm": 160, "health_warning": True, "is_child": False}]},
    ]
    assert process_ride_admissions(groups, 5.0) == {"total_revenue": 0.0, "status": "SAFETY_AUDIT"}


# ---------- inspect_safety_restraints ----------

def test_restraints_no_data():
    assert inspect_safety_restraints([]) == "NO_DATA"


def test_restraints_emergency_lock():
    assert inspect_safety_restraints([[1, 0, 0, 1]]) == "EMERGENCY_LOCK"


def test_restraints_safe():
    assert inspect_safety_restraints([[1, 0, 1, 0, 1]]) == "SAFE"
