import pytest
import pandas as pd
from unittest.mock import Mock, patch
from data_ingestion.handlers.etl_supabase import (
    DataHandler,
    CSVDataHandler,
    APIDataHandler,
)


class ConcreteDataHandler(DataHandler):
    """Implémentation concrète pour tester la classe abstraite."""

    def load(self):
        self.df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        return self.df


def test_data_handler_initialization():
    """Test l'initialisation du DataHandler."""
    handler = ConcreteDataHandler()
    assert handler.df.empty
    assert handler.client is not None


def test_data_handler_infer_sql_type():
    """Test l'inférence des types SQL."""
    handler = ConcreteDataHandler()

    assert handler._infer_sql_type(pd.Int64Dtype()) == "INTEGER"
    assert handler._infer_sql_type(pd.Float64Dtype()) == "FLOAT"
    assert handler._infer_sql_type(pd.BooleanDtype()) == "BOOLEAN"
    assert handler._infer_sql_type(pd.DatetimeTZDtype(tz="UTC")) == "TIMESTAMP"
    assert handler._infer_sql_type(pd.StringDtype()) == "TEXT"


@patch("data_ingestion.handlers.etl_supabase.os.path.exists")
def test_csv_data_handler_load(mock_exists):
    """Test le chargement des données CSV."""
    mock_exists.return_value = True

    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame({"test": [1, 2, 3]})
        handler = CSVDataHandler("test.csv")
        df = handler.load()

        assert not df.empty
        mock_read_csv.assert_called_once_with("test.csv")


@patch("data_ingestion.handlers.etl_supabase.os.path.exists")
def test_csv_data_handler_file_not_found(mock_exists):
    """Test la gestion des fichiers manquants."""
    mock_exists.return_value = False
    handler = CSVDataHandler("nonexistent.csv")

    with pytest.raises(FileNotFoundError):
        handler.load()


def test_api_data_handler_load():
    """Test le chargement des données via API."""
    mock_loader = Mock(return_value=pd.DataFrame({"api_data": [1, 2, 3]}))
    handler = APIDataHandler(loader_function=mock_loader, param1="value1")

    df = handler.load()

    assert not df.empty
    mock_loader.assert_called_once_with(param1="value1")
