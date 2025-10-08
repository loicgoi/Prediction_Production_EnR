import pytest
import pandas as pd
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b95c547 (restructuration des fichiers + tests fonctionnels)
from unittest.mock import Mock, patch
<<<<<<< HEAD
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
=======
from data_ingestion.handlers.etl_supabase import (
    DataHandler,
    CSVDataHandler,
    APIDataHandler,
)
<<<<<<< HEAD


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
<<<<<<< HEAD
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
=======
from unittest.mock import patch
=======
>>>>>>> b95c547 (restructuration des fichiers + tests fonctionnels)


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

<<<<<<< HEAD
    def test_infer_sql_type_float(self):
        from data_ingestion.etl_supabase import DataHandler

        class TestHandler(DataHandler):
            def load(self):
                return pd.DataFrame()

        handler = TestHandler()

        # Test float types
        float_series = pd.Series([1.1, 2.2, 3.3], dtype="float64")
        assert handler._infer_sql_type(float_series.dtype) == "FLOAT"

    def test_infer_sql_type_text(self):
        from data_ingestion.etl_supabase import DataHandler

        class TestHandler(DataHandler):
            def load(self):
                return pd.DataFrame()

        handler = TestHandler()

        # Test text types
        text_series = pd.Series(["a", "b", "c"], dtype="object")
        assert handler._infer_sql_type(text_series.dtype) == "TEXT"
>>>>>>> 3c7ab3c (réalisation des tests + correction erreurs d'import)
<<<<<<< HEAD
>>>>>>> 049f2e8 (réalisation des tests + correction erreurs d'import)
=======
=======
    assert not df.empty
    mock_loader.assert_called_once_with(param1="value1")
>>>>>>> b95c547 (restructuration des fichiers + tests fonctionnels)
>>>>>>> 0497523 (restructuration des fichiers + tests fonctionnels)
