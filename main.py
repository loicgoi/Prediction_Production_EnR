import logging
import argparse
import sys
import os
import subprocess
from datetime import datetime
import time

from src.data_ingestion.fetchers.fetch_all import fetch_all

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_data_pipeline():
    logging.info("Démarrage du pipeline de données")

    try:
        # Récupération de toutes les données
        results = fetch_all()

        # Log des résultats
        for key, df in results.items():
            if hasattr(df, "shape"):  # C'est un DataFrame
                logging.info(f"{key}: {len(df)} enregistrements récupérés")
            else:
                logging.info(f"{key}: Données récupérées")

        logging.info("Pipeline terminé avec succès !")
        return True

    except Exception as e:
        logging.error(f"Erreur lors de l'exécution du pipeline: {e}")
        return False


def run_model_training():
    """Lance l'entrainement des modèles"""
    logging.info("Démarrage de l'entrainement des modèles")

    try:
        from scripts.train_models import main as train_models_main

        train_models_main()
        logging.info("Entrainement des modèles terminés avec succès !")
        return True

    except Exception as e:
        logging.error(f"Erreur lors de l'entrainement des modèles: {e}")
        return False


def run_api():
    """Lance l'API pour accèder aux modèles sauvegardés"""
    logging.info("Démarrage de l'API...")

    try:
        import uvicorn

        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
        )
        return True

    except Exception as e:
        logging.error(f"Erreur lors du démarrage de l'API: {e}")
        return False


def run_streamlit():
    """Lance l'application Streamlit"""
    logging.info("Application Streamlit lancée !")

    try:
        # Crée un dossier logs si nécessaire
        os.makedirs("logs", exist_ok=True)

        # Chemin vers l'app Streamlit
        streamlit_app_path = os.path.join("src", "frontend", "app.py")

        # Lance Streamlit
        subprocess.Popen(
            [
                "streamlit",
                "run",
                streamlit_app_path,
                "--server.port=8500",
                "--server.address=0.0.0.0",
                "--logger.level=info",
            ]
        )
        return True

    except Exception as e:
        logging.error(f"Erreur lors du démarrage de l'application Streamlit: {e}")
        return False


def run_all():
    """Lance tous les composants"""
    logging.info("Lancement du script complet")

    # 1. Pipeline de données
    if not run_data_pipeline():
        logging.error("Échec du pipeline de données")
        return False

    # 2. Entraînement des modèles (optionnel)
    train_models = (
        input("Voulez-vous lancer l'entraînement des modèles ? (o/N): ").strip().lower()
    )
    if train_models in ["o", "oui", "y", "yes"]:
        if not run_model_training():
            logging.warning("Échec de l'entraînement des modèles, continuation...")

    # 3. API FastAPI (en arrière-plan)
    logging.info("Démarrage de l'API FastAPI en arrière-plan...")

    import threading

    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    # Attendre que l'API soit prête
    import time

    time.sleep(5)

    # 4. Application Streamlit
    logging.info("Démarrage de l'application Streamlit...")
    run_streamlit()

    # 5 Garder la session active
    keep_alive()

    return True


def check_services():
    """Vérifie le statut des services"""
    logging.info("Vérification du statut des services...")

    try:
        import requests

        # Vérifier l'API
        try:
            response = requests.get("http://localhost:8000/status", timeout=5)
            api_status = "En ligne" if response.status_code == 200 else "Hors ligne"
        except:
            api_status = "Hors ligne"

        # Vérifier Streamlit
        try:
            response = requests.get("http://localhost:8500", timeout=5)
            streamlit_status = (
                "En ligne" if response.status_code == 200 else "Hors ligne"
            )
        except:
            streamlit_status = "Hors ligne"

        logging.info(f"API FastAPI: {api_status}")
        logging.info(f"Streamlit: {streamlit_status}")

        # Vérifier les modèles
        try:
            from src.prediction.model_predictor import ModelPredictor

            models_status = {}
            for producer in ["solar", "wind", "hydro"]:
                try:
                    predictor = ModelPredictor(producer)
                    models_status[producer] = "Chargé"
                except:
                    models_status[producer] = "Non chargé"

            for producer, status in models_status.items():
                logging.info(f"Modèle {producer}: {status}")

        except Exception as e:
            logging.warning(f"Impossible de vérifier les modèles: {e}")

    except Exception as e:
        logging.error(f"Erreur lors de la vérification des services: {e}")


def kill_existing_streamlit():
    """Tuer les processus Streamlit existants"""
    try:
        import psutil

        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if proc.info["cmdline"] and any(
                    "streamlit" in cmd for cmd in proc.info["cmdline"]
                ):
                    logging.info(
                        f"Arrêt du processus Streamlit existant (PID: {proc.info['pid']})"
                    )
                    proc.terminate()
                    proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    except ImportError:
        logging.warning(
            "psutil non installé, impossible de vérifier les processus existants"
        )


def keep_alive():
    """Maintient le script actif pour garder les processus enfants vivants"""
    try:
        print("\n" + "=" * 60)
        print("SYSTÈME EN FONCTIONNEMENT")
        print("=" * 60)
        print("API FastAPI: http://localhost:8000")
        print("Documentation API: http://localhost:8000/docs")
        print("Interface Streamlit: http://localhost:8500")
        print("")
        print("Appuyez sur Ctrl+C pour arrêter tous les services")
        print("=" * 60)

        # Boucle de maintien en vie
        while True:
            time.sleep(1)  # Maintenant c'est le module time, pas datetime.time

    except KeyboardInterrupt:
        print("\nArrêt du système...")
        # Tuer les processus Streamlit existants
        kill_existing_streamlit()
        sys.exit(0)


def main():
    """Fonction principale avec gestion des arguments"""

    parser = argparse.ArgumentParser(
        description="Système de prévision de production d'énergie renouvelable",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py all                    # Lance tous les composants
  python main.py data                   # Lance seulement le pipeline de données
  python main.py train                  # Lance seulement l'entraînement des modèles
  python main.py api                    # Lance seulement l'API FastAPI
  python main.py streamlit              # Lance seulement Streamlit
  python main.py status                 # Vérifie le statut des services
  python main.py data train             # Lance données + entraînement
        """,
    )

    parser.add_argument(
        "command",
        nargs="*",
        default=["all"],
        help="Commandes à exécuter: all, data, train, api, streamlit, status",
    )

    parser.add_argument(
        "--host", default="0.0.0.0", help="Adresse d'hébergement (défaut: 0.0.0.0)"
    )

    parser.add_argument(
        "--api-port",
        type=int,
        default=8000,
        help="Port de l'API FastAPI (défaut: 8000)",
    )

    parser.add_argument(
        "--streamlit-port",
        type=int,
        default=8500,
        help="Port de Streamlit (défaut: 8500)",
    )

    args = parser.parse_args()

    # Créer le dossier logs
    os.makedirs("logs", exist_ok=True)

    logging.info("SYSTÈME DE PRÉVISION PRODUCTION ÉNERGIE RENOUVELABLE")
    logging.info("=" * 60)

    # Traitement des commandes
    commands = args.command if isinstance(args.command, list) else [args.command]

    success = True

    for command in commands:
        if command == "all":
            success = run_all() and success
        elif command == "data":
            success = run_data_pipeline() and success
        elif command == "train":
            success = run_model_training() and success
        elif command == "api":
            success = run_api() and success
        elif command == "streamlit":
            success = run_streamlit() and success
        elif command == "status":
            check_services()
        else:
            logging.error(f"Commande inconnue: {command}")
            parser.print_help()
            success = False
            break

        # Pause entre les commandes
        if len(commands) > 1 and command != commands[-1]:
            import time

            time.sleep(2)

    if success:
        logging.info("Toutes les opérations terminées avec succès !")
    else:
        logging.error("Certaines opérations ont échoué")
        sys.exit(1)


if __name__ == "__main__":
    main()
