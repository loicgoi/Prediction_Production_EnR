import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from datetime import date


class TestBaseProducer:
    """Tests pour la classe de base"""

    def test_base_producer_initialization(self):
        from producers.base_producer import BaseProducer

        # Test que la classe abstraite ne peut pas être instanciée directement
        with pytest.raises(TypeError):
            BaseProducer("Test", "Location", 100.0)


class TestSolarProducer:
    """Tests pour SolarProducer"""

    def test_solar_producer_initialization(self):
        from producers.solar_producer import SolarProducer

        producer = SolarProducer(
            name="Parc solaire test",
            location="Montpellier",
            nominal_power=150.0,
            data_file="test_solar.csv",
        )

        assert producer.name == "Parc solaire test"
        assert producer.location == "Montpellier"
        assert producer.nominal_power == 150.0
        assert producer.data_file == "test_solar.csv"

    @patch("data_ingestion.etl_supabase.CSVDataHandler.load")
    def test_load_production_data_success(self, mock_load, mock_production_data):
        from producers.solar_producer import SolarProducer

        # Mock CSV loading
        mock_load.return_value = mock_production_data

        producer = SolarProducer(
            name="Test Solar",
            location="Montpellier",
            nominal_power=150.0,
            data_file="test.csv",
        )

        result = producer.load_production_data(
            start_date=date(2024, 1, 1), end_date=date(2024, 1, 5)
        )

        assert not result.empty
        assert len(result) == 5
        mock_load.assert_called_once()

    @patch("data_ingestion.etl_supabase.CSVDataHandler.load")
    def test_load_production_data_empty(self, mock_load):
        from producers.solar_producer import SolarProducer

        # Mock empty data
        mock_load.return_value = pd.DataFrame()

        producer = SolarProducer(
            name="Test Solar",
            location="Montpellier",
            nominal_power=150.0,
            data_file="test.csv",
        )

        result = producer.load_production_data(
            start_date=date(2024, 1, 1), end_date=date(2024, 1, 5)
        )

        assert result.empty

    @patch("data_ingestion.etl_supabase.CSVDataHandler.load")
    def test_calculate_statistics(self, mock_load, mock_production_data):
        from producers.solar_producer import SolarProducer

        # Mock CSV loading
        mock_load.return_value = mock_production_data

        producer = SolarProducer(
            name="Test Solar",
            location="Montpellier",
            nominal_power=150.0,
            data_file="test.csv",
        )

        stats = producer.calculate_statistics(
            start_date=date(2024, 1, 1), end_date=date(2024, 1, 5)
        )

        assert "total_production" in stats
        assert "average_daily_production" in stats
        assert "max_daily_production" in stats
        assert "min_daily_production" in stats
        assert "capacity_factor" in stats
        assert stats["total_production"] > 0
        assert 0 <= stats["capacity_factor"] <= 1

    @patch("data_ingestion.etl_supabase.CSVDataHandler.load")
    def test_calculate_statistics_empty_data(self, mock_load):
        from producers.solar_producer import SolarProducer

        # Mock empty data
        mock_load.return_value = pd.DataFrame()

        producer = SolarProducer(
            name="Test Solar",
            location="Montpellier",
            nominal_power=150.0,
            data_file="test.csv",
        )

        stats = producer.calculate_statistics(
            start_date=date(2024, 1, 1), end_date=date(2024, 1, 5)
        )

        assert stats["total_production"] == 0
        assert stats["capacity_factor"] == 0.0


class TestWindProducer:
    """Tests pour WindProducer"""

    def test_wind_producer_initialization(self):
        from producers.wind_producer import WindProducer

        producer = WindProducer(
            name="Éolienne test",
            location="Montpellier",
            nominal_power=100.0,
            data_file="test_wind.csv",
        )

        assert producer.name == "Éolienne test"
        assert producer.location == "Montpellier"
        assert producer.nominal_power == 100.0

    @patch("data_ingestion.etl_supabase.CSVDataHandler.load")
    def test_wind_producer_statistics(self, mock_load, mock_production_data):
        from producers.wind_producer import WindProducer

        # Mock CSV loading
        mock_load.return_value = mock_production_data

        producer = WindProducer(
            name="Test Wind",
            location="Montpellier",
            nominal_power=100.0,
            data_file="test.csv",
        )

        stats = producer.calculate_statistics(
            start_date=date(2024, 1, 1), end_date=date(2024, 1, 5)
        )

        assert "total_production" in stats
        assert stats["total_production"] > 0


class TestHydroProducer:
    """Tests pour HydroProducer"""

    def test_hydro_producer_initialization(self):
        from producers.hydro_producer import HydroProducer

        producer = HydroProducer(
            name="Centrale hydro test",
            location="Montpellier",
            nominal_power=200.0,
            data_file="test_hydro.csv",
        )

        assert producer.name == "Centrale hydro test"
        assert producer.location == "Montpellier"
        assert producer.nominal_power == 200.0

    @patch("data_ingestion.etl_supabase.CSVDataHandler.load")
    def test_hydro_producer_statistics(self, mock_load, mock_production_data):
        from producers.hydro_producer import HydroProducer

        # Mock CSV loading
        mock_load.return_value = mock_production_data

        producer = HydroProducer(
            name="Test Hydro",
            location="Montpellier",
            nominal_power=200.0,
            data_file="test.csv",
        )

        stats = producer.calculate_statistics(
            start_date=date(2024, 1, 1), end_date=date(2024, 1, 5)
        )

        assert "total_production" in stats
        assert stats["total_production"] > 0
