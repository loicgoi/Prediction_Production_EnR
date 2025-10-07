import pytest
import pandas as pd
from unittest.mock import patch


class TestDataHandler:
    """Tests pour DataHandler et ses sous-classes"""

    def test_csv_data_handler_initialization(self):
        from data_ingestion.etl_supabase import CSVDataHandler

        handler = CSVDataHandler("test.csv")
        assert handler.file_path == "test.csv"

    def test_csv_data_handler_load(self, tmp_path):
        from data_ingestion.etl_supabase import CSVDataHandler

        # Crée un fichier CSV temporaire
        csv_file = tmp_path / "test.csv"
        csv_file.write_text("id,value\n1,100\n2,200\n")

        # Initialise le handler avec le vrai chemin (str)
        handler = CSVDataHandler(file_path=str(csv_file))

        # Patch pandas.read_csv pour s'assurer qu'il appelle la vraie fonction
        with patch("pandas.read_csv", wraps=pd.read_csv) as mock_read:
            result = handler.load()
            # On compare avec str(csv_file) pour matcher ce qui est réellement passé
            mock_read.assert_called_once_with(str(csv_file))

        # Vérifie que le résultat est correct
        assert not result.empty
        assert list(result.columns) == ["id", "value"]
        assert result.shape == (2, 2)

    @patch("pandas.read_csv")
    def test_csv_data_handler_file_not_found(self, mock_read_csv):
        from data_ingestion.etl_supabase import CSVDataHandler

        mock_read_csv.side_effect = FileNotFoundError("File not found")

        handler = CSVDataHandler("nonexistent.csv")

        with pytest.raises(FileNotFoundError):
            handler.load()

    def test_api_data_handler_initialization(self):
        from data_ingestion.etl_supabase import APIDataHandler

        def mock_loader():
            return pd.DataFrame({"test": [1, 2, 3]})

        handler = APIDataHandler(mock_loader, param1="value1")
        assert handler.loader_function == mock_loader
        assert handler.loader_kwargs == {"param1": "value1"}

    def test_api_data_handler_load(self, mock_production_data):
        from data_ingestion.etl_supabase import APIDataHandler

        def mock_loader(**kwargs):
            return mock_production_data

        handler = APIDataHandler(mock_loader, param1="value1")
        result = handler.load()

        assert not result.empty


class TestSQLTypeInference:
    """Tests pour l'inférence des types SQL"""

    def test_infer_sql_type_integer(self):
        from data_ingestion.etl_supabase import DataHandler

        class TestHandler(DataHandler):
            def load(self):
                return pd.DataFrame()

        handler = TestHandler()

        # Test integer types
        int_series = pd.Series([1, 2, 3], dtype="int64")
        assert handler._infer_sql_type(int_series.dtype) == "INTEGER"

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
