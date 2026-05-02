
Copia

# Python GUI Apps
 
Raccolta di applicazioni desktop sviluppate con Python e tkinter.
Architettura modulare con separazione tra layer UI, logica applicativa e accesso ai dati.
 
---
 
## Applicazioni
 
### Gestione Utenti
 
Applicazione desktop CRUD per la gestione anagrafica utenti con interfaccia tkinter.
 
**Funzionalità:**
- Aggiunta, modifica ed eliminazione utenti tramite form validato
- Visualizzazione dati in tabella Treeview con scrollbar e selezione riga
- Caricamento automatico dei dati nel form al click sulla riga
- Hashing sicuro delle password con **bcrypt** (salt casuale)
- Validazione input lato GUI con messaggi di errore specifici
- Registrazione automatica della data di iscrizione
**Architettura:**
 
| File | Responsabilità |
|---|---|
| `main.py` | Layer UI — classe `UserApp(tk.Tk)`, form, Treeview, gestione eventi |
| `database.py` | Layer dati — connessione SQLite, operazioni CRUD, controllo duplicati |
| `utils.py` | Utility — hashing e verifica password con bcrypt |
 
**Stack:**
 
<p>
  <img src="https://img.shields.io/badge/Python-3.x-f7c948?style=flat-square&logo=python&logoColor=1a1a1a" alt="Python"/>
  <img src="https://img.shields.io/badge/tkinter-GUI-4a6cf7?style=flat-square&logo=python&logoColor=white" alt="tkinter"/>
  <img src="https://img.shields.io/badge/SQLite-database-f7c948?style=flat-square&logo=sqlite&logoColor=1a1a1a" alt="SQLite"/>
  <img src="https://img.shields.io/badge/bcrypt-password_hashing-4a6cf7?style=flat-square&logo=python&logoColor=white" alt="bcrypt"/>
</p>
**Avvio:**
 
```bash
pip install bcrypt
python "Gestione Clienti/main.py"
```
 
---
 
### To-Do List
 
Applicazione desktop per la gestione di attività con persistenza automatica su file.
 
**Funzionalità:**
- Aggiunta attività tramite Entry con pulsante e tasto Invio
- Rimozione singola o multipla con conferma messagebox
- Salvataggio manuale su file `.txt` tramite finestra di dialogo
- Caricamento da file con gestione automatica righe vuote
- **Autosave alla chiusura** — intercetta `WM_DELETE_WINDOW` e salva silenziosamente prima di chiudere
- Contatore attività aggiornato in tempo reale
- Icona personalizzata (`todolist.ico`)
**Architettura:**
 
| File | Responsabilità |
|---|---|
| `TODO_LIST.PY` | Applicazione completa — UI, logica e persistenza su file |
| `todo_list.txt` | File di persistenza generato automaticamente |
| `todolist.ico` | Icona personalizzata della finestra |
 
**Stack:**
 
<p>
  <img src="https://img.shields.io/badge/Python-3.x-f7c948?style=flat-square&logo=python&logoColor=1a1a1a" alt="Python"/>
  <img src="https://img.shields.io/badge/tkinter-GUI-4a6cf7?style=flat-square&logo=python&logoColor=white" alt="tkinter"/>
  <img src="https://img.shields.io/badge/Persistenza-file_.txt-f7c948?style=flat-square&logo=python&logoColor=1a1a1a" alt="File txt"/>
</p>
**Avvio:**
 
```bash
python TO_DO_LIST/TODO_LIST.PY
```
 
---
 
## Struttura del repository
 
```
TKinter-dashboard/
├── Gestione Clienti/
│   ├── main.py         # UI principale — classe UserApp
│   ├── database.py     # Accesso dati SQLite — operazioni CRUD
│   └── utils.py        # Utility — hashing password bcrypt
├── TO_DO_LIST/
│   ├── TODO_LIST.PY    # Applicazione completa
│   └── todolist.ico    # Icona personalizzata
└── README.md
```
 
---
 
## Requisiti
 
```
bcrypt
```
 
Genera `requirements.txt` con:
 
```bash
pip freeze > requirements.txt
```
 
---
 
## Note tecniche
 
- Le password in `Gestione Clienti` vengono salvate come hash bcrypt — mai in chiaro nel database
- Il controllo duplicati su username ed email esclude correttamente l'utente corrente durante la modifica
- `sqlite3.Row` come `row_factory` permette l'accesso ai campi per nome colonna invece che per indice
- In `To-Do List` la chiusura della finestra è gestita con `root.protocol("WM_DELETE_WINDOW")` per garantire il salvataggio automatico anche in caso di chiusura tramite il pulsante X del sistema operativo
