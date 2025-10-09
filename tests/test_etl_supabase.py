import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.data_ingestion.handlers.etl_supabase import SupabaseHandler, CSVDataHandler


def test_supabase_handler_initialization():
    """Test l'initialisation du SupabaseHandler."""
    with patch("src.data_ingestion.handlers.etl_supabase.create_client") as mock_client:
        mock_instance = Mock()
        mock_client.return_value = mock_instance

        handler = SupabaseHandler()

        assert handler.supabase is not None
        mock_client.assert_called_once()


@patch("src.data_ingestion.handlers.etl_supabase.create_client")
def test_supabase_handler_upsert_dataframe(mock_client):
    """Test l'upsert d'un DataFrame."""
    mock_supabase = Mock()
    mock_client.return_value = mock_supabase
    mock_supabase.table.return_value.insert.return_value.execute.return_value = None

    handler = SupabaseHandler()
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    handler.upsert_dataframe(df, "test_table")

    mock_supabase.table.assert_called_with("test_table")


def test_csv_data_handler_initialization():
    """Test l'initialisation du CSVDataHandler."""
    mock_supabase = Mock()
    handler = CSVDataHandler(mock_supabase)

    assert handler.supabase_handler == mock_supabase
    assert handler.raw_path is not None


@patch("pandas.read_csv")
def test_csv_data_handler_load_csv(mock_read_csv):
    """Test le chargement des données CSV."""
    mock_supabase = Mock()
    mock_read_csv.return_value = pd.DataFrame({"test": [1, 2, 3]})

    handler = CSVDataHandler(mock_supabase)
    df = handler.load_csv("test.csv")

    assert not df.empty
    mock_read_csv.assert_called_once_with("test.csv")


@patch("pandas.DataFrame.to_csv")
def test_csv_data_handler_save_csv(mock_to_csv):
    """Test la sauvegarde des données CSV."""
    mock_supabase = Mock()
    handler = CSVDataHandler(mock_supabase)
    df = pd.DataFrame({"test": [1, 2, 3]})

    handler.save_csv(df, "test.csv")

    mock_to_csv.assert_called_once()


@patch("src.data_ingestion.utils.data_cleaner.DataCleaner")
def test_csv_data_handler_upload_to_supabase_solar(mock_cleaner):
    """Test l'upload des données solaires vers Supabase."""
    mock_supabase_handler = Mock()

    handler = CSVDataHandler(mock_supabase_handler)
    df = pd.DataFrame({"time": ["2024-01-01", "2024-01-02"]})

    mock_cleaner.clean_solar_data.return_value = df

    handler.upload_to_supabase(df, "solar_data")

    mock_supabase_handler.upsert_dataframe.assert_called()
    mock_cleaner.clean_solar_data.assert_called_once()
