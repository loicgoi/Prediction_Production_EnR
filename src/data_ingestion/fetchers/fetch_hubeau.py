import requests
import pandas as pd


def get_hubeau_data(code_station: str, start_date: str, end_date: str):
    """
    Récupère les données hydrométriques (débit moyen journalier) à partir de l'API
    Hubeau pour une station hydrométrique donnée et une période spécifiée.

    Args:
        code_station (str): Code de la station hydrométrique (ex. 'Y321002101').
        start_date (str): Date de début au format 'YYYY-MM-DD'.
        end_date (str): Date de fin au format 'YYYY-MM-DD'.

    Returns:
        pd.DataFrame: Tableau contenant les observations hydrométriques issues de l'API,
        avec notamment :
            - code_station : identifiant de la station
            - date_obs_elab : date de l'observation
            - result_obs_elab : valeur mesurée (ex. débit en m³/s)
            - autres colonnes descriptives fournies par l'API

    Raises:
        requests.HTTPError: Si la requête à l'API échoue.

    Exemple:
        >>> df = get_hubeau_data("Y321002101", "2024-01-01", "2024-12-31")
        >>> df.head()
    """
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab"
    params = {
        "code_entite": code_station,
        "date_debut_obs_elab": start_date,
        "date_fin_obs_elab": end_date,
        "grandeur_hydro_elab": "QmnJ",
        "size": 20000,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return pd.DataFrame(data.get("data", []))
