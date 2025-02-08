# Engineering Requirements Document (ERD)

## 1. Introduzione

Questo documento definisce i requisiti ingegneristici per realizzare un’applicazione web distribuita che esponga le funzionalità esistenti (parsificazione Markdown, chunking e upload) tramite API REST sicure e una interfaccia utente intuitiva. L’obiettivo è integrare la logica attualmente presente in "main.py" in un sistema modulare che impieghi FastAPI per il backend e React per il frontend, garantendo scalabilità, sicurezza e manutenzione semplificata tramite deployment serverless su Vercel.

## 2. Obiettivi e Requisiti Funzionali

**Fornire un backend basato su FastAPI che:**
Esponga le vecchie funzionalità tramite API REST.
Implementi un sistema di autenticazione (endpoint POST /auth/login) basato su username e password, letti da variabili d’ambiente.
Protegga gli endpoint sensibili tramite autenticazione e tramite validazione del token d’autorizzazione.
Gestisca centralmente gli errori con messaggi JSON strutturati ed exception handlers personalizzati.

**Fornire un frontend in React che:**
Offra una pagina di login per l’autenticazione.
Comunichi con il backend utilizzando il token inserito nell’header Authorization.
Presenti una Dashboard per operazioni quali upload di file Markdown e visualizzazione degli output.
Gestisca in modo chiaro le casistiche di errore (autenticazione, rete, ecc.).

## 3. Architettura del Sistema

La struttura proposta del repository è la seguente:

├── backend/
│ ├── app.py // Entry point dell’applicazione FastAPI
│ ├── routers/ // Router per autenticazione, chunking, upload
│ ├── models/ // Modelli Pydantic per la validazione dei dati
│ ├── utils/ // Funzioni comuni, gestione autenticazione ed errori
│ ├── config.py // Caricamento e gestione delle variabili d’ambiente
│ ├── requirements.txt // Dipendenze Python (FastAPI, uvicorn, etc.)
│ └── vercel.json // Configurazione per il deployment serverless su Vercel
│
└── frontend/
├── public/ // Risorse statiche
├── src/
│ ├── App.jsx // Componente principale
│ ├── components/ // Componenti UI (Login.jsx, Dashboard.jsx, etc.)
│ ├── services/ // Modulo di gestione delle chiamate API (es. api.js)
│ └── utils/ // Funzioni di supporto e gestione errori
├── package.json // Dipendenze di React
└── .env // Variabili d’ambiente del frontend

## 4. Dettagli Implementativi e Considerazioni Tecniche

**Il backend utilizza FastAPI per creare endpoint REST sicuri, incluse le funzionalità:**
Autenticazione con endpoint dedicato (/auth/login).
Validazione del token tramite middleware o dependency.
Integrazione modulare della logica esistente (chunking e upload) in moduli strutturati.
Gestione centralizzata degli errori e log per il monitoraggio.

**Il frontend utilizza React per:**
Realizzare un’interfaccia utente reattiva e intuitiva.
Gestire login e comunicare con il backend attraverso un modulo di servizi (api.js) che imposta automaticamente il token nell’header Authorization.
Mostrare feedback immediato all’utente per ogni eventuale errore o conferma operativa.

**Deployment:**
Il backend sarà distribuito su Vercel come funzioni serverless.
Il frontend verrà deployato come applicazione React con la corretta configurazione delle variabili d’ambiente.

## 5. Roadmap e Milestones

Per garantire la consegna puntuale e la qualità della soluzione, si propone la seguente roadmap:

### Fase 1: Pianificazione e Setup Iniziale (Settimane 1-2)

Analisi dettagliata dei requisiti e definizione dell’architettura.
Configurazione del repository e impostazione degli ambienti di sviluppo.
Creazione della struttura iniziale per backend e frontend.
Configurazione e validazione delle variabili d’ambiente.

### Fase 2: Sviluppo del Backend (Settimane 3-4)

Implementazione dell’entry point (app.py) e configurazione dei router.
Realizzazione dell’endpoint di autenticazione e integrazione del sistema di token.
Integrazione e modularizzazione della logica di chunking/upload da "main.py".
Implementazione dei meccanismi di logging e gestione degli errori.

### Fase 3: Sviluppo del Frontend (Settimane 5-6)

Creazione della pagina di login e implementazione dell’interfaccia utente.
Sviluppo della Dashboard per la gestione dei file e visualizzazione dei risultati.
Integrazione del modulo di servizi per la comunicazione sicura con il backend.
Implementazione della gestione degli errori lato client.

### Fase 4: Integrazione, Testing e Ottimizzazione (Settimana 7)

Integrazione completa delle componenti backend e frontend.
Testing end-to-end, compresi test di sicurezza e performance.
Correzione di bug e ottimizzazione della gestione delle eccezioni.

### Fase 5: Deployment e Messa in Produzione (Settimana 8)

Configurazione finale e deployment del backend e frontend su Vercel.
Verifica della corretta lettura delle variabili d’ambiente in produzione.
Fase di monitoraggio post-deployment e supporto iniziale.
Documentazione finale e formazione al team per la manutenzione.

## 6. Conclusioni

Il documento definisce un approccio modulare e scalabile per convertire la logica esistente in un’applicazione web moderna. L’adozione di FastAPI e React, supportata da una strategia serverless tramite Vercel, consente di raggiungere rapidamente il mercato mantenendo elevati standard di sicurezza e management degli errori. Le fasi di roadmap e le milestone garantiscono un monitoraggio strutturato del progetto, facilitando una consegna puntuale ed efficiente.