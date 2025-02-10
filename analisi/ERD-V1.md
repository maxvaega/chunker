# Documento di Requisiti Tecnici

## Introduzione
Questo documento definisce i requisiti tecnici dettagliati per lo sviluppo e il deployment dell'API RESTful descritta nel PRD. Include anche una roadmap con milestones per la realizzazione del progetto.

## Obiettivo
Implementare un'API che permetta di:
1. Ricevere un file Markdown tramite URL
2. Processare il file in chunk
3. Salvare i chunk localmente e/o su Pinecone
4. Restituire un JSON con i chunk generati

## Requisiti Fondamentali

### 1. Funzionalità Principale
- **Endpoint**: `/process-markdown` (POST)
- **Parametri**:
  - `file_url`: URL del file Markdown
  - `upload_options`: Array di stringhe ("local", "pinecone")
- **Autenticazione**: Token Bearer JWT
- **Formato Risposta**: JSON con messaggio di successo e lista dei chunk

### 2. Requisiti di Sistema
- **Framework**: FastAPI
- **Deployment**: Vercel (serverless)
- **Dipendenze**:
  - `fastapi`
  - `uvicorn`
  - `langchain`
  - `pinecone-client`
  - `python-dotenv`
  - `requests`

### 3. Autenticazione
- Implementazione JWT per validazione token
- Token deve essere incluso in ogni richiesta nell'header `Authorization`
- Gestione di errori di autenticazione (HTTP 401)

### 4. Gestione Errori
- Errori di input (HTTP 400)
- Errori di download file (HTTP 500)
- Errori di processamento (HTTP 500)
- Errori di upload su Pinecone (HTTP 500)

## Progettazione del Sistema

### 1. Componenti Principali
- **API Layer**: Gestione delle richieste e risposte
- **Processing Layer**: Suddivisione in chunk e estrazione titoli
- **Storage Layer**: Salvataggio locale e upload su Pinecone
- **Service Layer**: Autenticazione e gestione degli errori

### 2. Dipendenze
- **FastAPI**: Per la creazione dell'API
- **LangChain**: Per la gestione dei chunk e l'integrazione con Pinecone
- **Pinecone**: Per l'upload dei chunk
- **Python-Dotenv**: Per la gestione delle variabili d'ambiente

## Roadmap e Milestones

### Fase 1: Pianificazione e Setup (1 settimana)
- **Milestone 1.1**: Definizione finale dell'API endpoint
- **Milestone 1.2**: Configurazione del progetto e struttura della repository
- **Milestone 1.3**: Setup dell'ambiente di sviluppo

### Fase 2: Sviluppo Core Funzionalità (2 settimane)
- **Milestone 2.1**: Implementazione dell'endpoint `/process-markdown`
- **Milestone 2.2**: Implementazione della logica di suddivisione in chunk
- **Milestone 2.3**: Implementazione del sistema di autenticazione JWT

### Fase 3: Integrazione con Pinecone (1 settimana)
- **Milestone 3.1**: Implementazione dell'upload su Pinecone
- **Milestone 3.2**: Test di integrazione con Pinecone
- **Milestone 3.3**: Ottimizzazione delle prestazioni

### Fase 4: Testing e Validazione (1 settimana)
- **Milestone 4.1**: Implementazione dei test unitari
- **Milestone 4.2**: Esecuzione di test di integrazione
- **Milestone 4.3**: Validazione della gestione degli errori

### Fase 5: Deployment e Monitoraggio (1 settimana)
- **Milestone 5.1**: Configurazione di Vercel
- **Milestone 5.2**: Deployment in ambiente di testing
- **Milestone 5.3**: Configurazione del monitoraggio

## Considerazioni Chiave

### 1. Configurazione dell'Ambiente
- Utilizzare `python-dotenv` per gestire le variabili d'ambiente
- Configurare le credenziali di Pinecone e JWT

### 2. Monitoraggio e Logging
- Implementare logging dettagliato
- Configurare strumenti di monitoraggio per Vercel

### 3. Sicurezza
- Protezione dei dati sensibili
- Validazione robusta degli input
- Gestione sicura delle API keys

### 4. Prestazioni
- Ottimizzazione del processamento dei chunk
- Gestione efficiente delle risorse

## Conclusione
Il progetto verrà completato in 6 settimane con i milestones definiti. Ogni fase include specifiche attività e deliverable. Il progetto sarà considerato completato quando l'API sarà pienamente operativa, testata e deployata su Vercel.

## Prossimi Passi
1. Iniziare con la Fase 1 di pianificazione
2. Configurare la struttura del progetto
3. Avviare lo sviluppo delle funzionalità principali