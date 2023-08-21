import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  # Import the DateEntry widget
import json
import datetime

class HeuresTravailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des heures de travail")
        self.root.configure(bg="#f0f0f0")  # Set background color

        # Create and place widgets using grid layout
        self.create_widgets()

        # Load initial data
        self.base_de_donnees = self.charger_base_de_donnees()

    def create_widgets(self):
        tk.Label(self.root, text="Date:", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.entry_date = DateEntry(self.root, font=("Helvetica", 12))  # Use DateEntry widget
        self.entry_date.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Heure de début (HH:MM):", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
        self.entry_heure_debut = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_heure_debut.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Heure de fin (HH:MM):", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5)
        self.entry_heure_fin = tk.Entry(self.root, font=("Helvetica", 12))
        self.entry_heure_fin.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Enregistrer", font=("Helvetica", 12), command=self.enregistrer_heures).grid(row=3, columnspan=2, padx=10, pady=10)

        tk.Button(self.root, text="Jour off", command=self.enregistrer_jour_off).grid(row=4, columnspan=2, padx=10, pady=5)
        tk.Button(self.root, text="Jour de vacances", command=self.enregistrer_vacances).grid(row=5, columnspan=2, padx=10, pady=5)
        tk.Button(self.root, text="Afficher infos", command=self.afficher_informations).grid(row=6, columnspan=2, padx=10, pady=10)

    def charger_base_de_donnees(self):
        try:
            with open("heures_travail.json", "r") as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            return {"heures_travail": {}, "total_heures_supplementaires": 0.0, "jours_vacances": 20}
    
    def enregistrer_base_de_donnees(self,base_de_donnees):
        with open("heures_travail.json", "w") as fichier:
            json.dump(base_de_donnees, fichier, indent=4)
    
    def enregistrer_heures_travail(self,date, heures):
        self.base_de_donnees["heures_travail"][date] = heures

    def calculer_heures_supplementaires(self,heures_travaillees):
        heures_normales = 7  # Heures normales par jour
        if heures_travaillees > heures_normales:
            heures_supplementaires = heures_travaillees - heures_normales
            return heures_supplementaires
        else:
            return 0

    def calculer_total_heures_supplementaires(self):
        total_heures_supplementaires = 0
        for heures in self.base_de_donnees["heures_travail"].values():
            total_heures_supplementaires += self.calculer_heures_supplementaires(heures)
        return total_heures_supplementaires

    def calculer_temps_passe(self, heure_debut, heure_fin):
        try:
            heure_debut_obj = datetime.datetime.strptime(heure_debut, "%H:%M")
            heure_fin_obj = datetime.datetime.strptime(heure_fin, "%H:%M")
            temps_passe = heure_fin_obj - heure_debut_obj
            return temps_passe
        except ValueError:
            return None

    def enregistrer_heures(self):
        date = self.entry_date.get()
        heure_debut = self.entry_heure_debut.get()
        heure_fin = self.entry_heure_fin.get()

        temps_passe = self.calculer_temps_passe(heure_debut, heure_fin)
        if temps_passe is None:
            messagebox.showerror("Erreur", "Heure de début ou heure de fin invalide")
            return

        self.enregistrer_heures_travail(date, temps_passe.total_seconds() / 3600)  # Convert to hours
        heures_supplementaires = self.calculer_heures_supplementaires(temps_passe.total_seconds() / 3600)

        # Mettre à jour les heures supplémentaires et la base de données
        self.base_de_donnees["total_heures_supplementaires"] = self.calculer_total_heures_supplementaires()
        self.enregistrer_base_de_donnees(self.base_de_donnees)

        # Afficher les résultats dans une boîte de dialogue
        messagebox.showinfo("Enregistrement", f"Temps enregistré pour le {date} : {temps_passe}\n"
                                             f"Heures supplémentaires : {heures_supplementaires} heures\n"
                                             f"Total heures supplémentaires : {self.base_de_donnees['total_heures_supplementaires']} heures")

    def enregistrer_jour_off(self):
        date = self.entry_date.get()

        # Enregistrer un jour off
        self.enregistrer_heures_travail(date, 0)
        self.base_de_donnees["total_heures_supplementaires"] -= 7

        # Mettre à jour la base de données
        self.enregistrer_base_de_donnees(self.base_de_donnees)

        messagebox.showinfo("Enregistrement", f"Jour off enregistré pour le {date}\n"
                                             f"7 heures soustraites des heures supplémentaires\n"
                                             f"Total heures supplémentaires : {self.base_de_donnees['total_heures_supplementaires']} heures")

    def enregistrer_vacances(self):
        jours_vacances = int(input("Entrez le nombre de jours de vacances à soustraire : "))
        self.base_de_donnees["jours_vacances"] -= jours_vacances

        # Mettre à jour la base de données
        self.enregistrer_base_de_donnees(self.base_de_donnees)

        messagebox.showinfo("Vacances", f"{jours_vacances} jours de vacances soustraits\n"
                                       f"Jours de vacances disponibles : {self.base_de_donnees['jours_vacances']} jours")

    def afficher_informations(self):
        total_heures_semaine = self.calculer_total_heures_semaine(self.base_de_donnees)
        total_heures_supplementaires = self.base_de_donnees["total_heures_supplementaires"]
        jours_vacances = self.base_de_donnees["jours_vacances"]

        messagebox.showinfo("Informations", f"Nombre d'heures faites dans la semaine : {total_heures_semaine} heures\n"
                                           f"Nombre total d'heures supplémentaires : {total_heures_supplementaires} heures\n"
                                           f"Nombre de jours de vacances disponibles : {jours_vacances} jours")

    def calculer_total_heures_semaine(self, base_de_donnees):
        total_heures_semaine = 0
        semaine_actuelle = datetime.date.today().isocalendar()[1]  # Numéro de la semaine actuelle
        for date, heures in base_de_donnees["heures_travail"].items():
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            if date_obj.isocalendar()[1] == semaine_actuelle:
                total_heures_semaine += heures
        return total_heures_semaine
0
if __name__ == "__main__":
    root = tk.Tk()
    app = HeuresTravailApp(root)
    root.mainloop()