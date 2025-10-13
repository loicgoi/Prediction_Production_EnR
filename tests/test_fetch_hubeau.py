import pytest
import pandas as pd
from unittest.mock import patch, Mock
<<<<<<< HEAD
<<<<<<< HEAD
from src.data_ingestion.fetchers.fetch_hubeau import get_hubeau_data


@patch("src.data_ingestion.fetchers.fetch_hubeau.requests.get")
<<<<<<< HEAD
=======
from data_ingestion.fetchers.fetch_hubeau import get_hubeau_data
=======
from src.data_ingestion.fetchers.fetch_hubeau import get_hubeau_data
>>>>>>> 5594093 (màj des test + commentires code + README.md)


@patch("data_ingestion.fetchers.fetch_hubeau.requests.get")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
>>>>>>> b6ddba9 (update tests)
def test_get_hubeau_data_success(mock_get):
    """Test la récupération réussie des données Hub'Eau."""
    # Mock de la réponse
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": [
            {
                "code_station": "Y321002101",
                "date_obs_elab": "2024-01-01",
<<<<<<< HEAD
<<<<<<< HEAD
                "resultat_obs_elab": 10.5,
=======
                "result_obs_elab": 10.5,
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
                "resultat_obs_elab": 10.5,
>>>>>>> b6ddba9 (update tests)
            }
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    # Appel de la fonction
    df = get_hubeau_data("Y321002101", "2024-01-01", "2024-01-31")

    # Vérifications
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "code_station" in df.columns
    assert "date_obs_elab" in df.columns
<<<<<<< HEAD
<<<<<<< HEAD
    assert "resultat_obs_elab" in df.columns


@patch("src.data_ingestion.fetchers.fetch_hubeau.requests.get")
=======
    assert "result_obs_elab" in df.columns


@patch("data_ingestion.fetchers.fetch_hubeau.requests.get")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
    assert "resultat_obs_elab" in df.columns


@patch("src.data_ingestion.fetchers.fetch_hubeau.requests.get")
>>>>>>> b6ddba9 (update tests)
def test_get_hubeau_data_empty(mock_get):
    """Test la récupération avec données vides."""
    mock_response = Mock()
    mock_response.json.return_value = {"data": []}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    df = get_hubeau_data("Y321002101", "2024-01-01", "2024-01-31")

    assert isinstance(df, pd.DataFrame)
    assert df.empty


<<<<<<< HEAD
<<<<<<< HEAD
@patch("src.data_ingestion.fetchers.fetch_hubeau.requests.get")
=======
@patch("data_ingestion.fetchers.fetch_hubeau.requests.get")
>>>>>>> 6242f1e (restructuration des fichiers + tests fonctionnels)
=======
@patch("src.data_ingestion.fetchers.fetch_hubeau.requests.get")
>>>>>>> b6ddba9 (update tests)
def test_get_hubeau_data_http_error(mock_get):
    """Test la gestion des erreurs HTTP."""
    mock_get.side_effect = Exception("HTTP Error")

    with pytest.raises(Exception):
        get_hubeau_data("Y321002101", "2024-01-01", "2024-01-31")
