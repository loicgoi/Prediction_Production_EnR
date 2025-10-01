import requests
import pandas as pd


def get_hubeau_data(code_station: str, start_date: str, end_date: str):
    """
    Récupère les données hydrométriques Hubeau (débit, etc.) pour une station donnée.
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

    df = pd.DataFrame(data.get("data", []))

    return df


df = get_hubeau_data(
    code_station="Y321002101",
    start_date="2024-01-01",
    end_date="2025-09-30",
)

# Sauvegarde dans un CSV
df.to_csv("data/raw/data_hubeau.csv", index=True)

print(df)
