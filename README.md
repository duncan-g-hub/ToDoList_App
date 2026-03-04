# ToDoList App

Il s'agit d'une application permettant la gestion de tâches personnelles.

L'objectif est de constituer un outil qui ne nécessite aucune connexion internet et qui permet de sauvegarder et d'afficher les données de chaques tâches.

---

## Fonctionnalités

- Gestion des taches : 
  - Ajouter des taches
  - Modifier une tache
  - Supprimer une tache 
  - Sauvegarder une tache

- Contenu d'une tache :
  - Titre
  - Couleur
  - Temps avant derniére modification 
  - Date de la derniére modification
  - Description de la tache

- Sauvegarde des données dans un fichier .json avec tinydb: 
  - Données taches : `/data/data.json`

---

## Structure du projet

```
ToDoList_App/
    app.py                              # Gestion de l'interface graphique pyside
    api.py                              # Gestion de la logique et de la sauvegarde des données
    requirements.txt                    # Dépendances
    README.md                           # Documentation
    .gitignore                          # Liste des dossiers à ignorer pour le repository
    data/                               # Données sauvegardés (ne figure pas dans le repo, création à la première éxécution)  
```

---

## Technologies utilisées

- Python 3.13
- Librairies standards : datetime, pathlib, json, logging
- tinydb
- PySide6

---

## Limitations connues

- Pas de gestion multi-utilisateur
- Données stockées localement en fichiers JSON

---

## Installation 

### Prérequis :

- Python 3.10 ou plus récent
- Connexion Internet uniquement pour la récupération du code via GitHub et l'installation des dépendances 

### Cloner le repository : 

```bash
git clone https://github.com/duncan-g-hub/ToDoList_App.git
cd ToDoList_App/
```

### Créer et activer l'environnement virtuel : 

```bash
cd ToDoList_App/
python -m venv env 
source env/Scripts/activate
```

### Installer les dépendances : 

```bash
cd ToDoList_App/
pip install -r requirements.txt
```

---

## Exécution de l'application

```bash
cd ToDoList_App/
python app.py
```
La fenêtre de la ToDoList apparaitra.

---


## Contact

Pour toute question :  
Duncan GAURAT - duncan.dev@outlook.fr

            
