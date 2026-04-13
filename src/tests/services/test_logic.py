import pytest
from pydantic import ValidationError
from tests.services.pricing import PricingService
from models.users import UserSignup


def test_pricing_calculation():
    service = PricingService(rate=2.0)
    cost = service.calculate_cost(minutes=10)
    assert cost == 20.0


def test_user_signup_password_too_short():
    with pytest.raises(ValidationError):
        UserSignup(username="alice", email="alice@test.com", password="abc")


def test_user_signup_invalid_email():
    with pytest.raises(ValidationError):
        UserSignup(username="alice", email="not-an-email", password="Password1")
