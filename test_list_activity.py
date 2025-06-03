import os
import sys
import requests
from collections import defaultdict

# Chargement des variables d'environnement
KIMAI_URL = os.getenv("KIMAI_URL")
API_TOKEN = os.getenv("KIMAI_API_TOKEN")

if not KIMAI_URL or not API_TOKEN:
    raise ValueError("Les variables d'environnement KIMAI_URL et KIMAI_API_TOKEN doivent être définies.")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Accept": "application/json"}

def get_timesheets():
    """Récupère toutes les entrées de temps via l'API Kimai"""
    response = requests.get(f"{KIMAI_URL}/timesheets", headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return []

def get_project_details(project_id):
    """Récupère les détails d'un projet, notamment le client associé"""
    response = requests.get(f"{KIMAI_URL}/projects/{project_id}", headers=HEADERS)
    if response.status_code == 200:
        # print (response.json())
        # sys.exit(0)
        #return response.json().get("parentTitle", {}).get("name", "Client inconnu")
        return response.json().get("parentTitle", {})
    else:
        print(f"Erreur récupération projet {project_id}: {response.status_code} - {response.text}")
        return "Client inconnu"

def process_data(timesheets):
    """Organise les données par jour et par client"""
    data = defaultdict(lambda: defaultdict(float))
    project_cache = {}  # Cache pour éviter des requêtes répétées

    for entry in timesheets:
        date = entry["begin"].split("T")[0]  # Extraire la date
        project_id = entry["project"]

        if project_id not in project_cache:
            project_cache[project_id] = get_project_details(project_id)

        customer = project_cache[project_id]
        duration = entry["duration"] / 3600  # Convertir en heures
        data[date][customer] += duration

    return data

def display_data(data):
    """Affiche les résultats"""
    for date, customers in sorted(data.items()):
        print(f"\nDate: {date}")
        for customer, hours in customers.items():
            print(f"  - Client: {customer}, Temps total: {hours:.2f} heures")

if __name__ == "__main__":
    timesheets = get_timesheets()
    if timesheets:
        processed_data = process_data(timesheets)
        display_data(processed_data)
