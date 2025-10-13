import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.data_ingestion.handlers.etl_supabase import (
    SupabaseHandler,
    DataUploader,
)


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
    # CHANGEMENT : utiliser upsert() au lieu de insert()
    mock_supabase.table.return_value.upsert.return_value.execute.return_value = None

    handler = SupabaseHandler()
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

    handler.upsert_dataframe(df, "test_table")

    mock_supabase.table.assert_called_with("test_table")


def test_data_uploader_initialization():
    """Test l'initialisation du DataUploader."""
    mock_supabase = Mock()
    handler = DataUploader(mock_supabase)

    assert handler.supabase_handler == mock_supabase


@patch("src.data_ingestion.handlers.etl_supabase.SupabaseHandler")
def test_data_uploader_upload_raw_dataset(mock_supabase_handler):
    """Test l'upload des données brutes."""
    mock_instance = Mock()
    mock_supabase_handler.return_value = mock_instance

    uploader = DataUploader(mock_instance)
    df = pd.DataFrame({"date": ["2024-01-01"], "value": [100]})

    uploader.upload_raw_dataset(df, "test_dataset")

    mock_instance.upsert_dataframe.assert_called_once()


@patch("src.data_ingestion.handlers.etl_supabase.SupabaseHandler")
def test_data_uploader_upload_clean_dataset(mock_supabase_handler):
    """Test l'upload des données nettoyées."""
    mock_instance = Mock()
    mock_supabase_handler.return_value = mock_instance

    uploader = DataUploader(mock_instance)
    df = pd.DataFrame({"date": ["2024-01-01"], "value": [100]})

    uploader.upload_clean_dataset(df, "test_dataset")

    mock_instance.upsert_dataframe.assert_called_once()
