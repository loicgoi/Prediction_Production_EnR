import pytest
import pandas as pd
from unittest.mock import patch, Mock
from src.data_ingestion.handlers.handler_hubeau import HubeauDataHandler


def test_hubeau_handler_initialization():
    """Test l'initialisation du handler Hub'Eau."""
    handler = HubeauDataHandler(
        code_station="Y321002101", start_date="2024-01-01", end_date="2024-01-31"
    )

    assert handler.code_station == "Y321002101"
    assert handler.start_date == "2024-01-01"
    assert handler.end_date == "2024-01-31"


@patch("src.data_ingestion.handlers.handler_hubeau.get_hubeau_data")
def test_hubeau_handler_load(mock_get_data):
    """Test le chargement des données Hub'Eau."""
    mock_get_data.return_value = pd.DataFrame(
        {"date_obs_elab": ["2024-01-01", "2024-01-02"], "result_obs_elab": [10.5, 11.2]}
    )

    handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-31")
    df = handler.load()

    assert not df.empty
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


def test_hubeau_handler_clean_empty():
    """Test le nettoyage avec DataFrame vide."""
    handler = HubeauDataHandler("Y321002101", "2024-01-01", "2024-01-31")
    handler.df = pd.DataFrame()
    handler.clean()  # Ne devrait pas lever d'exception
