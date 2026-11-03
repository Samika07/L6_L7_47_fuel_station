
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# Fuel bill tests

def test_unknown_fuel_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 10, "silver")


def test_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_regular_within_voucher():
    assert fuel_bill("regular", 8, "silver") == 0


def test_gold_non_diesel_voucher():
    assert fuel_bill("regular", 15, "gold") == 0


def test_regular_extra_litres():
    assert fuel_bill("regular", 20, "silver") == 1050


def test_diesel_extra_litres():
    assert fuel_bill("diesel", 25, "silver") == 450


def test_large_silver_purchase():
    assert fuel_bill("premium", 50, "silver") == 3465


def test_large_gold_purchase():
    assert fuel_bill("regular", 50, "gold") == 3325


def test_large_gold_diesel_purchase():
    assert fuel_bill("diesel", 60, "gold") == 3200


# Pump permission tests

def test_fleet_at_limit():
    assert pump_allowed(200, 4, True) is True


def test_fleet_over_limit():
    assert pump_allowed(201, 1, True) is False


def test_non_fleet_allowed():
    assert pump_allowed(60, 1, False) is True


def test_non_fleet_over_limit():
    assert pump_allowed(61, 1, False) is False


def test_non_fleet_multiple_containers():
    assert pump_allowed(40, 2, False) is False


# Session status tests

def test_card_payment_day_active():
    assert session_status(60, True, False) == "active"


def test_cash_payment_night_warning():
    assert session_status(45, False, True) == "warning"


def test_cash_payment_day_timed_out():
    assert session_status(14, False, False) == "timed_out"


def test_card_payment_night_active():
    assert session_status(90, True, True) == "active"
