import uvicorn
import os
import sys

# Ajoute le répertoire src au path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )