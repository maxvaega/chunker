# Test Scenarios per Backend FastAPI

## 1. Autenticazione

### 1.1 Login Success
- **Descrizione**: Verifica che l'utente possa effettuare il login con credenziali corrette
- **Endpoint**: POST /auth/login
- **Test Case**: test_login_success
- **Expected**:
  - Status code: 200
  - Response contiene token JWT
- **Prerequisiti**: 
  - Variabili d'ambiente APP_USERNAME e APP_PASSWORD configurate

### 1.2 Login Failed
- **Descrizione**: Verifica che l'utente non possa effettuare il login con credenziali errate
- **Endpoint**: POST /auth/login
- **Test Case**: test_login_failed
- **Expected**: 
  - Status code: 401 Unauthorized

## 2. Protezione Endpoint

### 2.1 Accesso Senza Token
- **Descrizione**: Verifica che gli endpoint protetti non siano accessibili senza token
- **Endpoint**: POST /api/chunk
- **Test Case**: test_protected_endpoint_without_token
- **Expected**:
  - Status code: 401 Unauthorized

### 2.2 Accesso Con Token Invalido
- **Descrizione**: Verifica che gli endpoint protetti non siano accessibili con token invalido
- **Endpoint**: POST /api/chunk
- **Test Case**: test_protected_endpoint_with_invalid_token
- **Expected**:
  - Status code: 401 Unauthorized

## 3. Elaborazione Markdown

### 3.1 Chunking Success
- **Descrizione**: Verifica la corretta elaborazione di contenuto markdown
- **Endpoint**: POST /api/chunk
- **Test Case**: test_chunk_markdown
- **Expected**:
  - Status code: 200
  - Response contiene array "chunks"
- **Prerequisiti**:
  - Login effettuato con successo
  - Token JWT valido

## 4. Gestione Errori

### 4.1 Input Invalido
- **Descrizione**: Verifica la gestione di input markdown invalido
- **Endpoint**: POST /api/chunk
- **Test Case**: test_invalid_markdown
- **Expected**:
  - Status code: 422 Unprocessable Entity

### 4.2 Errore Server
- **Descrizione**: Verifica la gestione di errori server (es. file path invalido)
- **Endpoint**: POST /api/upload
- **Test Case**: test_server_error_handling
- **Expected**:
  - Status code: 500 Internal Server Error
  - Response contiene campo "error"

## 5. Copertura Test

I test coprono le seguenti aree funzionali:
- Autenticazione e gestione token
- Protezione degli endpoint
- Elaborazione markdown e chunking
- Gestione errori e validazione input
- Upload file

## 6. Prerequisiti per Esecuzione Test

1. Python 3.7+ installato
2. Dipendenze installate:

```bash
pip install pytest pytest-asyncio httpx
```

3. Variabili d'ambiente configurate:

```python
APP_USERNAME=admin
APP_PASSWORD=secure_password
JWT_SECRET_KEY=your_secret_key
```

## 7. Esecuzione test

```python
pytest backend/tests/test_app.py -v
```

Questa documentazione fornisce una panoramica strutturata dei test cases implementati, facilitando la manutenzione e l'espansione futura della test suite.