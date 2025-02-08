/Users/user/Documents/GitHub/chunker/ANALISI_TECNICA_FUNZIONALE.md
# Analisi Tecnica Funzionale

Questo documento descrive l’architettura e la strutturazione della codebase per estendere l’attuale logica (basata sul file "main.py") in modo da renderla accessibile tramite API (utilizzando FastAPI) e per fornire un’interfaccia utente basata su React. L’obiettivo è di creare un’applicazione distribuita su cloud serverless (Vercel, Python per il backend e React per il frontend) con una gestione completa degli errori e un sistema di autenticazione semplice ed efficace.

---

## 1. Obiettivi e Requisiti Funzionali

- Esposizione delle funzionalità attuali (es. elaborazione del markdown, divisione in chunk, salvataggio/local upload) tramite API REST.
- Realizzazione di un backend basato su FastAPI strutturato in moduli e router, che implementi:
  - Autenticazione tramite username e password (definiti in variabili d’ambiente).
  - Protezione degli endpoint API con un token di autorizzazione (anch’esso definito in variabile d’ambiente).
  - Gestione centralizzata degli errori con messaggi di risposta strutturati.
  
- Realizzazione di un frontend in React che:
  - Fornisca una pagina di login per inserire username e password.
  - Comunichi con il backend utilizzando le API protette (aggiungendo il token nel header Authorization).
  - Gestisca le casistiche d’errore (es. errori di autenticazione, errori di rete, ecc.) mostrando messaggi chiari all’utente.

---

## 2. Struttura del Repository

Si propone di organizzare la repository in due aree principali:

├── backend/  
│   ├── app.py                    // Entry point dell’applicazione FastAPI  
│   ├── routers/                  // Router suddivisi per funzionalità (es. utenti, chunking, upload)  
│   ├── models/                   // Modelli Pydantic per validazione dei dati (es. schema login, output chunks)  
│   ├── utils/                    // Funzioni comuni (autenticazione, gestione errori, caricamento variabili d’ambiente)  
│   ├── config.py                 // Caricamento e gestione delle variabili d’ambiente (username, password, token segreto, ecc.)  
│   ├── requirements.txt          // Dipendenze Python (FastAPI, uvicorn, python-dotenv, ecc.)  
│   └── vercel.json               // Configurazione specifica per il deployment serverless su Vercel (runtime Python)  
│  
└── frontend/  
    ├── public/                   // Risorse statiche  
    ├── src/  
    │   ├── App.jsx               // Componente principale  
    │   ├── components/           // Componenti UI (es. Login.jsx, Dashboard.jsx, ErrorAlert.jsx, ecc.)  
    │   ├── services/             // Configurazioni dei servizi di comunicazione, es. api.js (basato su axios o fetch)  
    │   └── utils/                // Funzioni di utilità (es. gestione errori, formattazioni)  
    ├── package.json              // Gestione delle dipendenze di React  
    └── .env                      // Variabili d’ambiente (per esempio il token da utilizzare nelle chiamate backend)

---

## 3. Dettagli Implementativi

### 3.1 Backend (FastAPI)

- **Entry Point (app.py):**  
  Si creerà un file "app.py" che inizializza l’applicazione FastAPI, registra i router e configura i middleware per:
  - Autenticazione: Verifica nelle richieste il token d’autorizzazione (presente nell’header Authorization) e la validità della sessione.
  - Gestione errori: Handler globali per gestire eccezioni comuni (HTTPException, Exception, ecc.) e per rispondere con JSON strutturati.
  
- **Autenticazione:**  
  - Sarà implementato un endpoint POST in un router specifico (es. `/auth/login`) in cui l’utente invia username e password.  
  - Le credenziali attese saranno lette da variabili d’ambiente (configurate in "config.py").  
  - Se le credenziali sono corrette, il sistema genera e restituisce un token (ad es. JWT) il cui segreto è definito in un’altra variabile d’ambiente.  
  - Tutti gli endpoint sensibili saranno protetti da un dependency (o middleware) che verificherà la presenza e la validità del token.

- **Gestione degli Errori:**  
  - Utilizzo di try/except intorno alle funzioni principali per catturare errori ed eccezioni.  
  - Implementazione di “exception handlers” personalizzati in FastAPI per restituire risposte coerenti in caso di errori (404, 500, etc.).  
  - Log degli errori per monitoraggio e debug.

- **Integrazione della Logica Esistente:**  
  - La logica attualmente presente in "main.py" (ad esempio il parsing, la suddivisione in chunk, il caricamento dei file, ecc.) verrà integrata in moduli all’interno della cartella "utils" o in router specifici in modo da renderla facilmente riutilizzabile.
  
### 3.2 Frontend (React)

- **Interfaccia Utente e Routing:**  
  - Creazione di una pagina di login (Login.jsx) per consentire all’utente di autenticarsi inserendo username e password.  
  - Una volta effettuato il login con successo, il token restituito dal backend verrà salvato (ad esempio in localStorage) e usato per autenticare tutte le successive richieste API.
  - Una volta autenticato, l’utente verrà reindirizzato a una Dashboard dove potrà:
    - Caricare file Markdown o inserire URL per procedere con la creazione dei chunk.
    - Visualizzare lo stato delle operazioni e i messaggi di conferma/errore.

- **Comunicazione con le API:**  
  - Creazione di un modulo di servizio (es. "api.js" in services/) che configuri le chiamate HTTP verso il backend.  
  - In questo modulo verrà impostato automaticamente l'header Authorization con il token in tutte le richieste.
  
- **Gestione degli Errori:**  
  - Nel frontend, tutte le chiamate API saranno gestite con blocchi try/catch o con gestione delle promise.  
  - Visualizzazione di messaggi d’errore mediante componenti dedicati (es. modali, toast, alert) per informare l’utente in modo chiaro qualora si verifichino errori (problemi di rete, credenziali errate, token scaduto, ecc.).

---

## 4. Deployment su Vercel

- **Backend:**  
  - Configurare Vercel per il deployment di funzioni serverless Python. Un file "vercel.json" dovrà essere definito nella cartella "backend" per specificare il runtime Python ed eventuali settings di routing (es. "/" che punta a "app.py").
  - Assicurarsi che tutte le variabili d’ambiente (username, password, token segreto, API keys per Pinecone, ecc.) siano settate nelle impostazioni del progetto Vercel.

- **Frontend:**  
  - Il progetto React potrà essere distribuito su Vercel normalmente come applicazione frontend.  
  - Le variabili d’ambiente per il frontend (ad esempio URL del backend, eventuale token di autorizzazione da utilizzare nelle chiamate) saranno configurate nel file ".env" e nelle impostazioni di Vercel.

---

## 5. Conclusioni e Prossimi Passi

- Integrare la logica esistente (da "main.py") nel nuovo sistema backend modulare con FastAPI, creando appositi router per le funzionalità di chunking e salvataggio.
- Implementare il meccanismo di autenticazione con endpoint dedicato e middleware per proteggere gli endpoint sensibili.
- Sviluppare l’interfaccia utente React completa di flussi di login, gestione token e comunicazione sicura con il backend.
- Realizzare una gestione centralizzata degli errori su entrambi i lati (backend e frontend) per rendere l’applicazione più robusta e user-friendly.
- Configurare e testare il deployment sia per il backend (funzioni serverless Python) che per il frontend su Vercel, verificando la corretta lettura delle variabili d’ambiente e la sicurezza della comunicazione attraverso il token di autorizzazione.

Questo documento fungerà da guida per la strutturazione futura della repository e per garantire un’implementazione modulare, sicura e facilmente manutenibile dell’applicazione.