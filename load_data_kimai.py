import os
import csv
import requests

# Chargement des variables d'environnement
KIMAI_URL = os.getenv("KIMAI_URL")
API_TOKEN = os.getenv("KIMAI_API_TOKEN")

if not KIMAI_URL or not API_TOKEN:
    raise ValueError("Les variables d'environnement KIMAI_URL et KIMAI_API_TOKEN doivent être définies.")

HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Accept": "application/json"}

def api_request(method, endpoint, payload=None):
    """Envoie une requête API et affiche les erreurs éventuelles"""
    url = f"{KIMAI_URL}/{endpoint}"
    response = requests.request(method, url, json=payload, headers=HEADERS)
    
    if response.status_code not in [200, 201]:
        print(f"⚠️ ERREUR API ({method} {endpoint}) : {response.status_code} - {response.text}")
    
    return response.json() if response.status_code in [200, 201] else {}

def get_existing_objects(endpoint):
    """Récupère les objets existants via leur nom"""
    response = api_request("GET", endpoint)
    return {obj["name"]: obj["id"] for obj in response}

def create_client(name):
    """Crée un client s'il n'existe pas déjà"""
    existing_clients = get_existing_objects("customers")
    if name in existing_clients:
        print(f"✅ Client '{name}' existe déjà (ID: {existing_clients[name]})")
        return existing_clients[name]
    
    payload = {"name": name, "country": "FR", "currency": "EUR", "timezone": "Europe/Paris", "visible": True}
    client_id = api_request("POST", "customers", payload).get("id")
    
    if client_id:
        print(f"🆕 Client '{name}' créé (ID: {client_id})")
    
    return client_id


def update_project_number(project_id, project_number):
    """Met à jour le numéro du projet via PATCH"""
    payload = {"number": project_number}
    response = api_request("PATCH", f"projects/{project_id}", payload)

    if response:
        print(f"✅ Project Number '{project_number}' mis à jour pour projet ID: {project_id}")

def get_existing_projects():
    """Récupère les projets existants en les associant à leurs clients"""
    projects = api_request("GET", "projects")
    
    # Vérification que proj["customer"] est bien un ID
    return {(proj["name"], proj["customer"]): proj["id"] for proj in projects} if projects else {}


def create_project(name, customer_id, project_number=None):
    """Crée un projet en le liant au client et en activant les activités globales"""
    existing_projects = get_existing_projects()

    if (name, customer_id) in existing_projects:
        print(f"✅ Projet '{name}' existe déjà (ID: {existing_projects[(name, customer_id)]})")
        return existing_projects[(name, customer_id)]

    # Création du projet avec activités globales activées
    payload = {
        "name": name,
        "customer": customer_id,
        "visible": True,
        "globalActivities": True  # Activation des activités globales
    }
    
    project_data = api_request("POST", "projects", payload)
    project_id = project_data.get("id")

    if project_id:
        print(f"🆕 Projet '{name}' créé et associé à Client ID {customer_id} (ID: {project_id})")

        # Mise à jour du numéro du projet via PATCH
        if project_number:
            update_project_number(project_id, project_number)

    return project_id


def create_activity(name, project_id):
    """Crée une activité s'il n'existe pas déjà"""
    existing_activities = get_existing_objects("activities")
    if name in existing_activities:
        print(f"✅ Activité '{name}' existe déjà (ID: {existing_activities[name]})")
        return existing_activities[name]
    
    payload = {"name": name, "project": project_id, "visible": True}
    activity_id = api_request("POST", "activities", payload).get("id")
    
    if activity_id:
        print(f"🆕 Activité '{name}' créée (ID: {activity_id})")
    
    return activity_id

def process_csv(file_path):
    """Lit le CSV et crée les objets nécessaires avec contrôle de présence"""
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            client_name = row["CLIENT"]
            project_name = row["PROJET"]
            project_number = row["PROJET_NUMBER"] if row["PROJET_NUMBER"] else f"PN-{project_name[:3]}-{row['CLIENT'][:3]}"
            activity_name = row["ACTIVITE"]

            # Vérification & création du client
            client_id = create_client(client_name)

            # Vérification & création du projet
            project_id = create_project(project_name, client_id, project_number)

            # Vérification & création de l'activité
            activity_id = create_activity(activity_name, project_id)

if __name__ == "__main__":
    process_csv("data.csv")  # Remplacez par le chemin du fichier CSV à traiter
