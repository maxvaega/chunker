 #!/bin/bash

# Avvia l'API FastAPI utilizzando uvicorn
uvicorn app.api:app --host 0.0.0.0 --port 8000