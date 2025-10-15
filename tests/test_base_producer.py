import pytest
import pandas as pd
from datetime import date
from src.producers.base_producer import BaseProducer


class ConcreteProducer(BaseProducer):
    """Implémentation concrète pour tester la classe abstraite."""

    def load_production_data(self, start_date: date, end_date: date):
        return pd.DataFrame(
            {"date": [start_date, end_date], "production_kwh": [100.5, 150.2]}
        )

    def calculate_statistics(self, start_date: date, end_date: date):
        return {"total": 250.7}


def test_base_producer_initialization():
    """Test l'initialisation du producteur de base."""
    producer = ConcreteProducer("Test Producer", "Montpellier", 100.0)

    assert producer.name == "Test Producer"
    assert producer.location == "Montpellier"
    assert producer.nominal_power == 100.0
    assert producer.logger is not None


def test_base_producer_capacity_factor():
    """Test le calcul du facteur de capacité."""
    producer = ConcreteProducer("Test Producer", "Montpellier", 100.0)

    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 2)

    capacity_factor = producer.get_production_capacity_factor(start_date, end_date)

    assert isinstance(capacity_factor, float)
    assert 0 <= capacity_factor <= 1


def test_base_producer_capacity_factor_empty_data():
    """Test le facteur de capacité avec données vides."""
    producer = EmptyDataProducer("Test Producer", "Montpellier", 100.0)

    capacity_factor = producer.get_production_capacity_factor(
        date(2024, 1, 1), date(2024, 1, 2)
    )

    assert capacity_factor == 0.0


class EmptyDataProducer(BaseProducer):
    """Producteur avec données vides pour les tests."""

    def load_production_data(self, start_date: date, end_date: date):
        return pd.DataFrame()

    def calculate_statistics(self, start_date: date, end_date: date):
        return {}
