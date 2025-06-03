# kimai_tool

## Exemple installation kimai en mode container via podman:

```
podman run --rm --name kimai-mysql-testing -e MYSQL_DATABASE=kimai -e MYSQL_USER=kimai -e MYSQL_PASSWORD=kimai -e MYSQL_ROOT_PASSWORD=kimai -p 3399:3306 -d docker.io/library/mysql
podman run --rm --name kimai-test -ti -p 8001:8001 -e DATABASE_URL=mysql://kimai:kimai@host.docker.internal:3399/kimai --add-host=host.docker.internal:host-gateway docker.io/kimai/kimai2:apache
```

## Se connecter à l'URL http port 8001 et finalier la configuration

## Créer une clef api
Créer une clef api dans la partie ustilisateur qui va servir à renseigner la variable KIMAI_API_TOKEN pour la connexion api via python.

## Creation du venv python:

```
cd kimai_tool
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Exemple de lancement python:

```
export KIMAI_URL="http://127.0.0.1:8001/api"
export KIMAI_API_TOKEN="465e3dba8aa1493644xxxxxx"

python test_list_activity.py
```

## Exemple de chargement de données clients/projets

cf. exemple de csv: data.csv\
et chargement du csv dans kimai:\
```
python load_data_kimai.py
```

