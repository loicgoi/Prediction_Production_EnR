import pytest
import pandas as pd
from unittest.mock import patch, Mock
<<<<<<< HEAD
from src.data_ingestion.handlers.handler_hubeau import HubeauDataHandler
=======
from data_ingestion.handlers.handler_hubeau import HubeauDataHandler
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)


def test_hubeau_handler_initialization():
    """Test l'initialisation du handler Hub'Eau."""
<<<<<<< HEAD
    handler = HubeauDataHandler(
        code_station="Y321002101", start_date="2024-01-01", end_date="2024-01-31"
    )

    assert handler.code_station == "Y321002101"
    assert handler.start_date == "2024-01-01"
    assert handler.end_date == "2024-01-31"


@patch("src.data_ingestion.handlers.handler_hubeau.get_hubeau_data")
=======
    handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-31")

    assert handler.code_station == "Y321002101"
    assert handler.table_name == "hydro_data"
    assert handler.loader_kwargs["code_station"] == "Y321002101"


@patch("data_ingestion.handlers.handler_hubeau.get_hubeau_data")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
def test_hubeau_handler_load(mock_get_data):
    """Test le chargement des données Hub'Eau."""
    mock_get_data.return_value = pd.DataFrame(
        {"date_obs_elab": ["2024-01-01", "2024-01-02"], "result_obs_elab": [10.5, 11.2]}
    )

    handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-31")
    df = handler.load()

    assert not df.empty
<<<<<<< HEAD
    mock_get_data.assert_called_once()


def test_hubeau_handler_clean():
    """Test le nettoyage des données Hub'Eau."""
    handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-31")

    # Simuler des données chargées
    original_df = pd.DataFrame(
        {
            "date_obs_elab": ["2024-01-01", "2024-01-02"],
            "result_obs_elab": [10.5, 11.2],
            "other_column": [1, 2],
        }
    )
    handler.df = original_df

    # Appeler clean
    handler.clean()

    # Vérifier que le DataFrame a été modifié (nettoyé)
    assert handler.df is not None
    assert not handler.df.empty
=======
    mock_get_data.assert_called_once_with(
        code_station="Y321002101", start_date="2024-01-01", end_date="2024-01-31"
    )


@patch("data_ingestion.handlers.handler_hubeau.DataCleaner")
def test_hubeau_handler_clean(mock_cleaner):
    """Test le nettoyage des données Hub'Eau."""
    mock_cleaner.clean_hydro_data.return_value = pd.DataFrame(
        {"date": ["2024-01-01", "2024-01-02"], "debit_l_s": [10.5, 11.2]}
    )

    handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-31")
    handler.df = pd.DataFrame({"test": [1, 2]})
    handler.clean()

    mock_cleaner.clean_hydro_data.assert_called_once()
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)


def test_hubeau_handler_clean_empty():
    """Test le nettoyage avec DataFrame vide."""
    handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-31")
    handler.df = pd.DataFrame()
    handler.clean()  # Ne devrait pas lever d'exception
