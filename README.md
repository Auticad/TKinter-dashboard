# Python GUI Apps
 
Raccolta di applicazioni desktop sviluppate con Python, tkinter e SQLite.
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
 
Applicazione desktop per la gestione di attività con interfaccia tkinter.
 
> Documentazione in aggiornamento.
 
---
 
## Struttura del repository
 
```
TKinter-dashboard/
├── Gestione Clienti/
│   ├── main.py         # UI principale — classe UserApp
│   ├── database.py     # Accesso dati SQLite — operazioni CRUD
│   └── utils.py        # Utility — hashing password bcrypt
├── TO_DO_LIST/
│   └── ...
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
 
- Le password vengono salvate come hash bcrypt — mai in chiaro nel database
- Il controllo duplicati su username ed email esclude correttamente l'utente corrente durante la modifica
- `sqlite3.Row` come `row_factory` permette l'accesso ai campi per nome colonna invece che per indice
