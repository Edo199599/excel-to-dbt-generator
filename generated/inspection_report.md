# Excel Inspection Report

## Indice

- Rows: 6
- Columns: 4
- Detected header row: None
- Candidate sheet: False

## DIM_UTENTI

- Rows: 22
- Columns: 20
- Detected header row: 7
- Candidate sheet: True

### Metadata

- **LEGACY  Alimentante**: SC - SICUREZZA LOGICA
- **Alimentata da Bronze layer**: B38_SC_UTENZE_ZB
- **Nome tabella Livello Silver**: DIM_UTENTI
- **Tipologia Alimentazione**: SCD2
- **Frequenza**: Giornaliero
- **Tipologia estrazione**: full

### Column inspection

#### Missing standard columns
- None

#### Present aliases
- **SOURCE_DATATYPE**: DATATYPE SORG

#### Ignored columns
- DUBBI
- RISPOSTE

#### Unknown columns
- None

### Warnings

- None

## DIM_RAPPORTI_BIOMETRIA

- Rows: 31
- Columns: 20
- Detected header row: 7
- Candidate sheet: True

### Metadata

- **LEGACY  Alimentante**: WS - SICUREZZA WEB
- **Alimentata da Bronze layer**: B38_SC_RAPPORTI_BIOMETRIA _ZB
- **Nome tabella Livello Silver**: DIM_RAPPORTI_BIOMETRIA
- **SCD2**: Upsert
- **Frequenza**: Giornaliera
- **Tipologia estrazione**: Delta

### Column inspection

#### Missing standard columns
- None

#### Present aliases
- **SOURCE_DATATYPE**: DATATYPE

#### Ignored columns
- DUBBI
- RISPOSTE

#### Unknown columns
- None

### Warnings

- None

## FCT_TRS_DISPOSITIVE_SICUREZZA

- Rows: 18
- Columns: 20
- Detected header row: 7
- Candidate sheet: True

### Metadata

- **LEGACY  Alimentante**: WS - SICUREZZA WEB
- **Alimentata da Bronze layer**: B38_SC_DISPOSITIVE_SICUREZZA_ZB
- **Nome tabella Livello Silver**: FCT_TRS_DISPOSITIVE_SICUREZZA
- **Tipologia Alimentazione**: APPEND
- **Frequenza**: Giornaliera
- **Tipologia estrazione**: delta

### Column inspection

#### Missing standard columns
- None

#### Present aliases
- **SOURCE_DATATYPE**: DATATYPE

#### Ignored columns
- DUBBI
- RISPOSTE

#### Unknown columns
- None

### Warnings

- None

## FCT_TRS_EVENTI_TOKEN

- Rows: 22
- Columns: 20
- Detected header row: 7
- Candidate sheet: True

### Metadata

- **LEGACY  Alimentante**: WS - SICUREZZA WEB
- **Alimentata da Bronze layer**: B38_SC_EVENTI_TOKEN_ZB
- **Nome tabella Livello Silver**: FCT_TRS_EVENTI_TOKEN
- **Tipologia Alimentazione**: Merge
- **Frequenza**: Giornaliera
- **Tipologia estrazione**: FULL

### Column inspection

#### Missing standard columns
- None

#### Present aliases
- **SOURCE_DATATYPE**: DATATYPE

#### Ignored columns
- DUBBI
- RISPOSTE

#### Unknown columns
- None

### Warnings

- None

## FCT_TRS_EVENTI_AUTENTICAZIONE

- Rows: 18
- Columns: 19
- Detected header row: 7
- Candidate sheet: True

### Metadata

- **LEGACY  Alimentante**: WS - SICUREZZA WEB
- **Alimentata da Bronze layer**: B38_SC_EVENTI_AUTENTICAZIONE_ZB
- **Nome tabella Livello Silver**: FCT_TRS_EVENTI_AUTENTICAZIONE
- **Tipologia Alimentazione**: APPEND
- **Frequenza**: Giornaliera
- **Tipologia estrazione**: delta

### Column inspection

#### Missing standard columns
- None

#### Present aliases
- **SOURCE_DATATYPE**: DATATYPE

#### Ignored columns
- DUBBI
- RISPOSTE

#### Unknown columns
- None

### Warnings

- None
