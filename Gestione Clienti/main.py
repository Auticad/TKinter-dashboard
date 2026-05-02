import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import datetime

# Classe principale dell'applicazione
class UserApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestione Utenti")
        self.geometry("800x600")

        # Memorizza l'ID dell'utente selezionato per la modifica
        self.selected_user_id = None

        # Crea la tabella del database se non esiste
        db.create_table()

        # Configura il layout a griglia
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Crea i frame principali
        self.main_frame = ttk.Frame(self, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=("NSWE"))
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Crea e posiziona il frame del form per aggiungere/modificare utenti
        self.form_frame = ttk.LabelFrame(self.main_frame, text="Gestisci Utente", padding="10")
        self.form_frame.grid(column=0, row=0, sticky=("WE"), pady=10)
        self.form_frame.columnconfigure(1, weight=1)
        
        # Campi di input del form
        self.setup_form_widgets()

        # Crea e posiziona la tabella Treeview per visualizzare gli utenti
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.grid(column=0, row=1, sticky=("NSWE"))
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)

        # Setup della tabella Treeview
        self.setup_treeview()
        
        # Popola la tabella con i dati iniziali
        self.populate_treeview()

    def setup_form_widgets(self):
        """Crea tutti i widget del form di input."""
        ttk.Label(self.form_frame, text="Username:").grid(column=0, row=0, sticky="W", pady=2)
        self.username_entry = ttk.Entry(self.form_frame)
        self.username_entry.grid(column=1, row=0, sticky=("WE"), padx=5, pady=2)

        ttk.Label(self.form_frame, text="Email:").grid(column=0, row=1, sticky="W", pady=2)
        self.email_entry = ttk.Entry(self.form_frame)
        self.email_entry.grid(column=1, row=1, sticky=("WE"), padx=5, pady=2)

        ttk.Label(self.form_frame, text="Età:").grid(column=0, row=2, sticky="W", pady=2)
        self.age_entry = ttk.Entry(self.form_frame)
        self.age_entry.grid(column=1, row=2, sticky=("WE"), padx=5, pady=2)
        
        ttk.Label(self.form_frame, text="Data di Nascita (AAAA-MM-GG):").grid(column=0, row=3, sticky="W", pady=2)
        self.dob_entry = ttk.Entry(self.form_frame)
        self.dob_entry.grid(column=1, row=3, sticky=("WE"), padx=5, pady=2)

        ttk.Label(self.form_frame, text="Password:").grid(column=0, row=4, sticky="W", pady=2)
        self.password_entry = ttk.Entry(self.form_frame, show="*")
        self.password_entry.grid(column=1, row=4, sticky=("WE"), padx=5, pady=2)
        
        # Frame per i pulsanti del form
        self.form_buttons_frame = ttk.Frame(self.form_frame)
        self.form_buttons_frame.grid(column=0, row=5, columnspan=2, pady=10)

        # Pulsante Salva/Aggiorna Utente
        self.save_button = ttk.Button(self.form_buttons_frame, text="Salva Utente", command=self.save_or_update_user)
        self.save_button.pack(side="left", padx=5)
        
        # Pulsante Elimina Utente
        self.delete_button = ttk.Button(self.form_buttons_frame, text="Elimina Utente", command=self.delete_user)
        self.delete_button.pack(side="left", padx=5)
        
        # Pulsante Annulla
        self.cancel_button = ttk.Button(self.form_buttons_frame, text="Annulla", command=self.clear_form)
        self.cancel_button.pack(side="left", padx=5)

    def setup_treeview(self):
        """Crea la tabella Treeview e la configura."""
        columns = ("id_utente", "username", "email", "eta", "data_di_nascita", "data_di_registrazione")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")
        self.tree.grid(column=0, row=0, sticky=("NSWE"))

        # Definisce le intestazioni delle colonne
        self.tree.heading("id_utente", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("email", text="Email")
        self.tree.heading("eta", text="Età")
        self.tree.heading("data_di_nascita", text="Data di Nascita")
        self.tree.heading("data_di_registrazione", text="Data di Registrazione")

        # Configura la larghezza delle colonne
        self.tree.column("id_utente", width=50, anchor="center")
        self.tree.column("username", width=100)
        self.tree.column("email", width=150)
        self.tree.column("eta", width=50, anchor="center")
        self.tree.column("data_di_nascita", width=120)
        self.tree.column("data_di_registrazione", width=120)

        # Aggiunge una scrollbar al Treeview
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(column=1, row=0, sticky=("NS"))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Lega l'evento di selezione della riga al metodo load_user_to_form
        self.tree.bind("<<TreeviewSelect>>", self.load_user_to_form)

    def populate_treeview(self):
        """Svuota la tabella e la ripopola con i dati dal database."""
        # Rimuove tutti gli elementi esistenti
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ottiene tutti gli utenti dal database e li inserisce nella tabella
        users = db.get_all_users()
        for user in users:
            self.tree.insert("", "end", values=(user["id_utente"], user["username"], user["email"], user["eta"], user["data_di_nascita"], user["data_di_registrazione"]))

    def save_or_update_user(self):
        """Salva un nuovo utente o aggiorna uno esistente in base allo stato del form."""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        eta_str = self.age_entry.get().strip()
        dob_str = self.dob_entry.get().strip()
        password = self.password_entry.get()

        # Validazione del form
        if not username or not email or not dob_str:
            messagebox.showerror("Errore", "Username, Email e Data di Nascita sono campi obbligatori.")
            return

        try:
            eta = int(eta_str) if eta_str else None
            datetime.date.fromisoformat(dob_str)
        except ValueError:
            messagebox.showerror("Errore", "L'età deve essere un numero intero e la data di nascita nel formato AAAA-MM-GG.")
            return

        # Logica di salvataggio vs. aggiornamento
        if self.selected_user_id is None:
            # Salvataggio di un nuovo utente
            if not password:
                messagebox.showerror("Errore", "La password è obbligatoria per un nuovo utente.")
                return
            success, message = db.save_user(username, email, eta, dob_str, password)
        else:
            # Aggiornamento di un utente esistente
            success, message = db.update_user(self.selected_user_id, username, email, eta, dob_str, password if password else None)
            
        if success:
            messagebox.showinfo("Successo", message)
            self.clear_form()
            self.populate_treeview()
        else:
            messagebox.showerror("Errore", message)

    def delete_user(self):
        """Elimina l'utente selezionato."""
        if self.selected_user_id is None:
            messagebox.showwarning("Selezione", "Seleziona un utente dalla tabella per eliminarlo.")
            return

        if messagebox.askyesno("Conferma Eliminazione", "Sei sicuro di voler eliminare questo utente?"):
            db.delete_user(self.selected_user_id)
            messagebox.showinfo("Successo", "Utente eliminato correttamente.")
            self.clear_form()
            self.populate_treeview()

    def load_user_to_form(self, event):
        """Carica i dati dell'utente selezionato nel form per la modifica."""
        selected_item = self.tree.focus()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.selected_user_id = values[0]
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, values[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[2])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, values[3])
            self.dob_entry.delete(0, tk.END)
            self.dob_entry.insert(0, values[4])
            # La password non viene caricata nel campo di input per sicurezza
            self.password_entry.delete(0, tk.END)
            
    def clear_form(self):
        """Svuota il form e resetta lo stato di modifica."""
        self.selected_user_id = None
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = UserApp()
    app.mainloop()
