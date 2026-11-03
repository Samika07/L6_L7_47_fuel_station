
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# Fuel bill: test all decision branches

@pytest.mark.parametrize("grade,litres,tier,expected", [
    ("regular", 10, "silver", 0),
    ("regular", 15, "gold", 0),
    ("regular", 20, "silver", 1050),
    ("diesel", 25, "silver", 450),
    ("premium", 50, "silver", 3465),
    ("regular", 50, "gold", 3325),
    ("diesel", 60, "gold", 3200),
])
def test_fuel_bill_branches(grade, litres, tier, expected):
    assert fuel_bill(grade, litres, tier) == expected


@pytest.mark.parametrize("grade,litres,message", [
    ("unknown", 10, "unknown fuel grade"),
    ("regular", -1, "invalid litres"),
])
def test_fuel_bill_validation(grade, litres, message):
    with pytest.raises(ValueError, match=message):
        fuel_bill(grade, litres, "silver")


# Pump permission: test fleet and non-fleet branches

@pytest.mark.parametrize("litres,containers,is_fleet,expected", [
    (200, 3, True, True),
    (201, 3, True, False),
    (60, 1, False, True),
    (61, 1, False, False),
    (30, 2, False, False),
])
def test_pump_allowed_branches(litres, containers, is_fleet, expected):
    assert pump_allowed(litres, containers, is_fleet) is expected


# Session status: test all timing and payment branches

@pytest.mark.parametrize("seconds,card,night,expected", [
    (60, True, False, "active"),
    (45, False, True, "warning"),
    (14, False, False, "timed_out"),
    (90, True, True, "active"),
])
def test_session_status_branches(seconds, card, night, expected):
    assert session_status(seconds, card, night) == expected
