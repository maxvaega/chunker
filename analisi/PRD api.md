**Documento di Analisi Tecnica Funzionale**

**Introduzione**

Questo documento descrive la struttura tecnica e funzionale necessaria per estendere l'attuale codebase al fine di esporre le sue funzionalità tramite un'API RESTful. L'API sarà sviluppata utilizzando **FastAPI** e distribuita su **Vercel** come ambiente serverless basato su **Python**. L'obiettivo principale è creare un singolo endpoint che consenta di caricare un file Markdown tramite URL, selezionare la destinazione per il caricamento dei chunk generati (locale, Pinecone, o entrambi) e restituire una risposta di successo insieme al JSON completo dei chunk.

**Struttura della Repository**

La repository sarà riorganizzata per separare le componenti dell'applicazione, facilitando la manutenzione e la scalabilità. La struttura proposta è la seguente:

/chunker

│

├── /app

│ ├── __init__.py

│ ├── main.py

│ ├── api.py

│ ├── config.py

│ ├── auth.py

│ ├── utils.py

│ └── requirements.txt

│

├── /tests

│ ├── __init__.py

│ └── test_api.py

│

├── /output

│ └── output_chunks.json

│

├── /scripts

│ └── deploy.sh

│

├── .env

├── .gitignore

└── README.md

-   **/app**: Contiene il codice dell'applicazione principale.

-   main.py: Punto di ingresso dell'applicazione.
-   api.py: Definizione degli endpoint API.
-   config.py: Configurazioni dell'applicazione, incluse le variabili d'ambiente.
-   auth.py: Implementazione del sistema di autenticazione.
-   utils.py: Funzioni di utilità e helper.
-   requirements.txt: Dipendenze del progetto.

-   **/tests**: Contiene i test unitari e di integrazione.
-   **/output**: Directory per il salvataggio dei file JSON generati.
-   **/scripts**: Script per operazioni di deployment e manutenzione.
-   **.env**: File per la configurazione delle variabili d'ambiente.
-   **README.md**: Documentazione del progetto.

**Descrizione dell'API**

L'API sarà sviluppata utilizzando **FastAPI**, che offre performance elevate e semplicità di utilizzo. Verrà creato un singolo endpoint POST che accetterà una richiesta contenente l'URL del file Markdown e i parametri operativi necessari per determinare dove caricare i chunk generati.

**Endpoint:** **/process-markdown**

-   **Metodo HTTP**: POST
-   **Autenticazione**: Token Bearer
-   **Descrizione**: Riceve l'URL di un file Markdown, processa il file generando i chunk e li carica nelle destinazioni selezionate. Restituisce un messaggio di successo e il JSON completo dei chunk generati.

**Parametri di Input**

La richiesta dovrà contenere un payload JSON con i seguenti campi:

-   file_url _(stringa, obbligatorio)_: URL del file Markdown da caricare.
-   upload_options _(array di stringhe, facoltativo, default = ["pinecone"])_: Opzioni per il caricamento dei chunk. Valori ammessi:

-   "local": Restituisce il file JSON con i chunk generati.
-   "pinecone": Carica i chunk su Pinecone e restituisce il file JSON con i chunk generati.

**Esempio di Richiesta**

{

"file_url": "https://example.com/document.md",

"upload_options": ["pinecone"]

}

**Risposta**

-   **Successo**: Codice HTTP 200

-   message _(stringa)_: Conferma del successo dell'operazione.
-   chunks _(array di oggetti)_: Lista completa dei chunk generati.

**Esempio di Risposta di Successo**

{

"message": "File processato e chunk caricati con successo su Pinecone index ="index_name".",

"chunks": [

{

"id": "document_001",

"filename": "document.md",

"datetime": "2025-02-06 19:35:21",

"title": "Introduzione",

"text": "Contenuto del primo chunk..."

},

{

"id": "document_002",

"filename": "document.md",

"datetime": "2025-02-06 19:35:21",

"title": "Capitolo 1",

"text": "Contenuto del secondo chunk..."

}

// Altri chunk...

]

}

**Errore**: Codice HTTP appropriato (es. 400, 401, 500)

-   error _(stringa)_: Descrizione dell'errore.

**Esempio di Risposta di Errore**

{

"error": "Token di autenticazione mancante o non valido."

}

**Parametri di Input**

L'API accetta i seguenti parametri di input:

1.  **file_url**:

-   **Tipo**: Stringa
-   **Descrizione**: L'URL pubblico del file Markdown (.md) che l'utente desidera processare.
-   **Validazioni**:

-   Deve essere un URL valido.
-   Deve puntare a un file con estensione .md.

1.  **upload_options**:

-   **Tipo**: Array di stringhe
-   **Descrizione**: Seleziona le destinazioni dove caricare i chunk generati.
-   **Valori Ammissibili**:

-   "local": Per restituire il file JSON con i chunk generati senza caricare i chunk su Pinecone.
-   "pinecone" (default): Per caricare i chunk su Pinecone e restituire il file JSON con i chunk generati.

-   **Validazioni**:

-   I valori devono essere tra quelli ammessi.
-   Se non specificato, il valore di default è "pinecone".

**Gestione degli Errori**

L'API implementa una robusta gestione degli errori per garantire che gli utenti ricevano feedback chiari e utili in caso di problemi. Le principali casistiche di errore gestite includono:

1.  **Input non valido**:

-   **Codice HTTP**: 400 Bad Request
-   **Descrizione**: Quando i parametri di input mancanti o non conformi alle specifiche.
-   **Esempio**: URL non valido, mancanza di file_url, opzioni di upload non riconosciute.

1.  **Autenticazione fallita**:

-   **Codice HTTP**: 401 Unauthorized
-   **Descrizione**: Quando il token di autenticazione è mancante o non valido.

1.  **Errore durante il download del file**:

-   **Codice HTTP**: 500 Internal Server Error
-   **Descrizione**: Problemi nel scaricare il file Markdown dall'URL fornito.

1.  **Errore nel processamento del file**:

-   **Codice HTTP**: 500 Internal Server Error
-   **Descrizione**: Problemi durante la suddivisione in chunk o estrazione dei titoli.

1.  **Errore durante il salvataggio su Pinecone**:

-   **Codice HTTP**: 500 Internal Server Error
-   **Descrizione**: Problemi di connessione o configurazione con Pinecone.

1.  **Errore generico del server**:

-   **Codice HTTP**: 500 Internal Server Error
-   **Descrizione**: Altri errori imprevisti durante l'esecuzione.

Ogni messaggio di errore conterrà una descrizione chiara del problema per facilitare la risoluzione.

**Autenticazione**

Per garantire che solo utenti autorizzati possano accedere all'API, verrà implementato un sistema di autenticazione semplice ma efficace basato su token Bearer. I dettagli dell'implementazione sono i seguenti:

1.  **Metodo di Autenticazione**:

-   Utilizzo di **JSON Web Tokens (JWT)** per l'autenticazione.
-   Gli utenti devono includere un token valido nell'intestazione Authorization di ogni richiesta.

1.  **Generazione dei Token**:

-   I token saranno generati e gestiti tramite una componente di autenticazione separata (da implementare separatamente).

1.  **Validazione dei Token**:

-   L'API verificherà la validità del token in ogni richiesta.
-   In caso di token mancante o non valido, l'API risponderà con un errore HTTP 401.

1.  **Sicurezza**:

-   I token saranno firmati digitalmente per prevenire manomissioni.
-   Le chiavi segrete per la firma dei token saranno archiviate in modo sicuro tramite variabili d'ambiente.

**Flusso di Lavoro**

1.  **Richiesta dell'Utente**:

-   L'utente invia una richiesta POST all'endpoint /process-markdown con il payload JSON contenente file_url e upload_options (facoltativo, default = "pinecone"), e un token di autenticazione valido nell'intestazione Authorization.

1.  **Autenticazione**:

-   L'API verifica la validità del token.
-   Se il token è valido, procede; altrimenti, risponde con un errore 401.

1.  **Validazione dell'Input**:

-   L'API controlla che file_url sia un URL valido che punti a un file .md.
-   Verifica che upload_options contenga almeno una delle opzioni ammesse (se vuoto, prende come default = "pinecone").

1.  **Download del File Markdown**:

-   Utilizza la funzione download_markdown_from_url per scaricare il contenuto del file.

1.  **Processamento del File**:

-   Suddivide il testo in chunk utilizzando la split_into_chunks già definita in main.py:

```python
splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=0,
        separators=[separator],
        keep_separator=True
    )
```

-   Estrae i titoli con extract_title.
```python
def extract_title(chunk):
    """
    Extracts the title from a markdown chunk.
    The title is expected to be in the first line, preceded by # characters.
    """
    first_line = chunk.strip().split('\n')[0]
    title = re.sub(r'^#+\s*', '', first_line).strip()
    return title
```
-   Genera gli ID dei chunk e i titoli tramite prepare_chunks_data.
```python
    chunk_ids = [f"{metadata['filename']}_{str(i+1).zfill(3)}" for i in range(len(chunks))]
    chunk_titles = [extract_title(chunk) for chunk in chunks]

    chunk_data = {
        'id': chunk_id,
        'filename': metadata['filename'],
        'datetime': metadata['datetime'],
        'title': title,
        'text': text
    }
    chunks_data.append(chunk_data)
    
    # Metadata for Pinecone
    pinecone_metadata.append({
        'filename': metadata['filename'],
        'datetime': metadata['datetime'],
        'title': title
    })    
```

1.  **Caricamento dei Chunk**:

-   A seconda delle upload_options selezionate:

-   **Local**: Salva i chunk in un file JSON da ritornare come risposta.
-   **Pinecone**: Salva i chunk in un file JSON da ritornare come risposta e inoltre li carica su Pinecone utilizzando upload_to_pinecone.

```python
# load env variables
load_dotenv()

# load pinecone credentials
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')

# upload to pinecone
def upload_to_pinecone(chunk_ids, chunks, metadatas):
    try:
        index_name = 'aistruttore'
        namespace = 'aistruttore1'

        # Initialize embeddings
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        # Upload data using LangChain's Pinecone VectorStore
        vectorstore = PineconeVectorStore.from_texts(
            texts=chunks,
            embedding=embeddings,
            index_name=index_name,
            namespace=namespace,
            metadatas=metadatas,
            ids=chunk_ids,
            text_key="text"
        )
        print(f"Chunks successfully uploaded to Pinecone in index '{index_name}' and namespace '{namespace}'.")
    except Exception as e:
        print(f"Error uploading to Pinecone: {e}")
```

1.  **Risposta all'Utente**:

-   Se tutte le operazioni hanno successo, l'API restituisce un messaggio di conferma e il JSON completo dei chunk.
-   In caso di errore in una delle fasi, restituisce un messaggio di errore appropriato.

**Deployment su Vercel**

Per distribuire l'API su **Vercel** in ambiente serverless, seguire i passaggi seguenti:

1.  **Configurazione del Progetto**:

-   Assicurarsi che il progetto sia configurato per funzionare con Vercel, includendo un file vercel.json se necessario.

1.  **Gestione delle Variabili d'Ambiente**:

-   Configurare le variabili d'ambiente necessarie (es. chiavi API, segreti di autenticazione) tramite il pannello di controllo di Vercel.

1.  **File di Requirements**:

-   Assicurarsi che tutte le dipendenze siano elencate in requirements.txt per permettere a Vercel di installarle automaticamente.

1.  **Script di Deployment**:

-   Creare script automatizzati per facilitare il processo di deployment, ad esempio deploy.sh nella directory /scripts (non necessario)

1.  **Testing**:

-   Dettagliare i test da eseguire per garantire che l'API funzioni correttamente nell'ambiente serverless.
-   Eseguire test approfonditi per garantire che l'API funzioni correttamente nell'ambiente serverless.

1.  **Monitoraggio e Logging**:

-   Configurare strumenti di monitoraggio per tracciare le performance e gli eventuali errori dell'API una volta distribuita.

**Conclusioni**

L'implementazione di un'API RESTful tramite FastAPI e la sua distribuzione su Vercel permetterà di rendere accessibili le funzionalità attuali del programma in modo scalabile e sicuro. La struttura proposta facilita l'estensibilità futura, la manutenzione e l'integrazione di ulteriori funzionalità. Una gestione accurata degli input, degli errori e dell'autenticazione garantirà un servizio robusto e affidabile per gli utenti finali.
