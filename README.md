# Gestion des heures de travail avec Tkinter

Ce programme Python est une application de gestion des heures de travail développée avec la bibliothèque Tkinter. L'application permet à l'utilisateur d'enregistrer ses heures de travail, de gérer les jours off et les jours de vacances, et d'afficher des informations utiles sur les heures travaillées.

## Fonctionnalités

L'application propose les fonctionnalités suivantes :

- **Enregistrement des heures de travail :** L'utilisateur peut saisir la date, l'heure de début et l'heure de fin de son travail. L'application calcule ensuite le temps passé et enregistre les heures de travail dans la base de données.

- **Calcul des heures supplémentaires :** Le programme calcule automatiquement les heures supplémentaires en fonction des heures travaillées. Si l'utilisateur travaille plus que les heures normales par jour, les heures supplémentaires sont calculées.

- **Gestion des jours off :** L'utilisateur peut enregistrer des jours off en saisissant simplement la date. Les heures travaillées pour ces jours sont définies à zéro et les heures supplémentaires sont ajustées en conséquence.

- **Gestion des jours de vacances :** L'application permet de soustraire un nombre donné de jours de vacances disponibles. Les jours de vacances restants sont mis à jour dans la base de données.

- **Affichage d'informations :** L'utilisateur peut afficher des informations telles que le nombre total d'heures travaillées dans la semaine, le nombre total d'heures supplémentaires accumulées et le nombre de jours de vacances disponibles.

## Utilisation

Pour exécuter l'application, assurez-vous d'avoir Python installé sur votre machine. Vous devez également installer les bibliothèques Tkinter et tkcalendar en utilisant la commande suivante :

```python
pip install tk tkcalendar
```

Une fois les bibliothèques installées, vous pouvez exécuter le programme en exécutant le fichier Python. Une fenêtre GUI s'ouvrira, vous permettant d'utiliser les fonctionnalités de l'application.
