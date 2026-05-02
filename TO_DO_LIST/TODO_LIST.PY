import tkinter as tk
from tkinter import messagebox, filedialog
import os

from altair import Padding


root = tk.Tk() # crea la finestra
root.title('Layout Grid') # titolo dell'app
root.geometry("800x600+700+200")  # la finestra si avvia al centro del monitor
base_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_dir, "todolist.ico")
root.iconbitmap(icon_path) 
root.resizable(True, True)

filename = os.path.join(base_dir, "todo_list.txt")

   
def crea_interfaccia():
    """Crea tutti i widget dell'interfaccia"""
    
    # === SEZIONE TITOLO ===
    titolo = tk.Frame(root, bg="#0EA04B", pady=20)
    titolo.pack(fill="x")
    
    label_titolo = tk.Label(
        titolo,
        text = "Lista Attività",
        font = ("Arial", 24, "bold"),
        bg =  "#0EA04B",
        fg="white"
    )
    label_titolo.pack()
    
    # === SEZIONE INPUT ===
    input = tk.Frame(root, bg="white", pady=15, padx=20)
    input.pack(fill="x")
    
    global entry_attivita
    # Entry per digitare nuove attività
    entry_attivita = tk.Entry(
        input,
        font=("Arial", 12),
        width=35,
        relief="solid",
        borderwidth=2
        
    )
    entry_attivita.pack(side="left", padx=(0, 10), ipady=5)
    entry_attivita.bind("<Return>", lambda e: aggiungi_attivita)

    # Focus sull'Entry per inserimento rapido
    entry_attivita.focus()
    
    # Pulsante Aggiungi
    btn_aggiungi = tk.Button(
        input,
        text="Aggiungi a lista",
        font=("Arial", 12, "bold"),
        bg="#85A00E",
        fg="white",
        relief="raised",  # tipo di tasto: flat, groove, raised, ridge, solid, sunken
        padx=20,
        pady=5,
        cursor="hand2",
        activebackground="#979FE6",  # ← Colore quando premi (verde più scuro)
        activeforeground="white",     # ← Colore testo quando premi
        command=aggiungi_attivita
    )
    btn_aggiungi.pack(side="left")
    
    # === SEZIONE LISTA ===
    frame_lista = tk.Frame(root, bg="white", padx=20, pady=10)
    frame_lista.pack(fill="both", expand=True)
    
    # Label per il titolo della lista
    label_lista = tk.Label(
        frame_lista,
        text="Le tue attività:",
        font=("Arial", 14, "bold"),
        bg="white",
        anchor="w"
    )
    label_lista.pack(fill="x", pady=(0, 10))
    
    # Frame per Listbox e Scrollbar
    frame_listbox = tk.Frame(frame_lista, bg="white", padx=20, pady=10)
    frame_listbox.pack(fill="both", expand=True)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(frame_listbox)
    scrollbar.pack(side="right", fill="y")
    
    global listbox_attivita
    
    # Listbox - il widget principale per visualizzare le attività
    listbox_attivita = tk.Listbox(
        frame_listbox,
        font=("Arial", 11),
        selectmode=tk.EXTENDED,
        relief="solid",
        borderwidth=2,
        activestyle="none",
        selectbackground="#0EA04B",
        selectforeground="white"
        
    )
    listbox_attivita.pack(padx=5, fill="both", expand=True)

    
    # Collegamento tra Listbox e Scrollbar
    listbox_attivita.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_attivita.yview)
    
    # === SEZIONE PULSANTI AZIONE ===
    frame_azioni = tk.Frame(root, bg="white", pady=15, padx=20)
    frame_azioni.pack(fill="x")
    
    # Pulsante Rimuovi
    btn_rimuovi = tk.Button(
        frame_azioni,
        text="Rimuovi Todo selezionati",
        font=("Arial", 12, "bold"),
        bg="#EF4444",
        fg="white",
        relief="flat",
        padx=20,
        pady=8,
        cursor="hand2",
        command=rimuovi_attivita
    )
    btn_rimuovi.pack(side="left", padx=(0, 10))
    
    btn_salva = tk.Button(
        frame_azioni,
        text="Salva",
        font=("Arial", 12, "bold"),
        bg="#0EA04B",
        fg="white",
        relief="flat",
        padx=16,
        pady=8,
        cursor="hand2",
        command=salva_attivita
    )
    btn_salva.pack(side="left", padx=(0, 10))
    
    btn_carica = tk.Button(
        frame_azioni,
        text="Carica",
        font=("Arial", 12, "bold"),
        bg="#0066CC",
        fg="white",
        relief="flat",
        padx=16,
        pady=8,
        cursor="hand2",
        command=carica_attivita
    )
    btn_carica.pack(side="left", padx=(0, 10))
    
    btn_carica = tk.Button(
        frame_azioni,
        text="Esci",
        font=("Arial", 12, "bold"),
        bg="#B1D60B",
        fg="white",
        relief="flat",
        padx=16,
        pady=8,
        cursor="hand2",
        command=on_closing
    )
    btn_carica.pack(side="left", padx=(0, 10))
    
    global label_contatore
    
    # Label contatore
    label_contatore = tk.Label(
        frame_azioni,
        text="Totale: 0 attività",
        font=("Arial", 10),
        bg="white",
        fg="gray"
    )
    label_contatore.pack(side="right")
def aggiungi_attivita():
    
    # Recupera il testo dall'Entry
    attivita = entry_attivita.get().strip()
    
    # Verifica che non sia vuoto
    if attivita == "":
        messagebox.showwarning(
            "Attenzione",
            "Per favore, inserisci un'attività!"
            )
        return
    
    # Inserisco attività nella Listbox
    listbox_attivita.insert(tk.END, attivita)
    
    # Pulisco il campo Entry
    entry_attivita.delete(0, tk.END)
    
    # Aggiorno il contatore
    aggiorna_contatore()
    
    
def rimuovi_attivita():
    
    # Ottengo l'indice dell'elemento selezionato
    #curselection() ritorna → (2,)
    #curselection()[0] ritorna → 2
    try:
        indice_selezionato = listbox_attivita.curselection()[0]
    except IndexError:
        # Nessun elemento selezionato
        messagebox.showwarning(
            "Attenzione",
            "Seleziona un'attività da rimuovere!"
        )
        return
    
    # Chiedi conferma
    attivita = listbox_attivita.get(indice_selezionato)
    conferma = messagebox.askyesno(
        "Conferma"
        f"Vuoi davvero rimuovere:\n'{attivita}'?"
    )
    
    if conferma:
        # Elimina l'elemento dalla Listbox
        listbox_attivita.delete(indice_selezionato)
        
        # Aggiorna il contatore
        aggiorna_contatore()

def salva_attivita():
    
     # Apri finestra di dialogo per salvare
    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("File di testo", "*.txt"), ("Tutti i file", "*.*")],
        title="Salva file di testo"
    )
    
    # Se l'utente ha specificato un percorso
    if file:
        try:
            with open(file, 'w', encoding='utf-8') as file:
                attivita = listbox_attivita.get(0, tk.END)
            
                # Scrivi ogni attività su una nuova riga
                for attivita_singola in attivita:
                    file.write(attivita_singola + '\n')
                    
            print(f"✅ Attività salvate in '{file}'")        
                
            messagebox.showinfo("Successo", "File salvato correttamente!")
        
        except Exception as e:
            messagebox.showerror(
                "Errore",
                f"🔴 Impossibile salvare le attività:\n{e}"
            )

def carica_attivita():
   
    # if not filename:
    #     print("Caricamento annullato.")
    #     return
        
    # Verifica se il file esiste
    if not os.path.exists(filename):
        print("ℹ️ File non trovato. Primo avvio.")
        return
    
    try:
        # Apri il file in modalità lettura
        with open(filename, 'r', encoding='utf-8') as file:
            # Leggi tutte le righe
            righe = file.readlines()
            
            # Svuota la listbox prima di caricare (opzionale ma consigliato)
            listbox_attivita.delete(0, tk.END)
            
            # Inserisci ogni riga (attività) nella Listbox
            for riga in righe:
                attivita = riga.strip()
                if attivita:  # Ignora righe vuote
                    listbox_attivita.insert(tk.END, attivita)
            
        # Aggiorno il contatore
        aggiorna_contatore()
        print(f"✅ Attività caricate da '{filename}'")
    except Exception as e:
        print(f"❌ Errore durante il caricamento: {e}")

def autosave_to_default():
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            attivita = listbox_attivita.get(0, tk.END)
            for att in attivita:
                file.write(att + '\n')
    except Exception as e:
        # non blocchiamo la chiusura per un errore di salvataggio; log su console
        print("Errore autosave:", e)

def aggiorna_contatore():
    """Aggiorna il label del contatore"""
    
    totale = listbox_attivita.size()
    label_contatore.config(text=f"Totale: {totale} attività")

def on_closing():
    """
    PASSO 10: Gestisce la chiusura dell'applicazione
    """
    # Salva le attività prima di chiudere
    #salva_attivita()
    autosave_to_default()
    # Chiudi la finestra
    root.destroy()

crea_interfaccia()

carica_attivita()

# Configura il salvataggio automatico alla chiusura
# Senza parentesi () a on_closing
# Passa la funzione come oggetto
# È come dire: "Ecco la funzione, chiamala TU quando serve"
root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()
