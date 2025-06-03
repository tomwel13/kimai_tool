import csv
import re

def parse_ics(ics_file):
    """Parse un fichier ICS et extrait les événements avec leur statut ajusté"""
    events = []
    with open(ics_file, "r", encoding="utf-8") as file:
        content = file.read()

    event_blocks = re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', content, re.DOTALL)

    for event in event_blocks:
        summary = re.search(r'SUMMARY:(.+)', event)
        start = re.search(r'DTSTART:(\d+T\d+Z?)', event)
        end = re.search(r'DTEND:(\d+T\d+Z?)', event)
        partstat = re.search(r'PARTSTAT=(ACCEPTED|DECLINED|TENTATIVE|NEEDS-ACTION)', event)
        status = re.search(r'STATUS:(CONFIRMED|TENTATIVE|CANCELLED)', event)
        organizer = re.search(r'ORGANIZER:(?:mailto:)?(.+)', event)

        # Définition du statut final
        if organizer is None:
            final_status = "CONFIRMED"
            organizer_value = "ME"  # Remplace l'absence d'organisateur par "ME"
        else:
            final_status = partstat.group(1) if partstat else (status.group(1) if status else "Inconnu")
            organizer_value = organizer.group(1)

        events.append({
            "Titre": summary.group(1) if summary else "",
            "Début": start.group(1) if start else "",
            "Fin": end.group(1) if end else "",
            "Statut final": final_status,
            "Organisateur": organizer_value
        })
    
    return events

def export_csv(events, csv_file):
    """Exporte la liste d'événements en fichier CSV"""
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Titre", "Début", "Fin", "Statut final", "Organisateur"], delimiter=";")
        writer.writeheader()
        writer.writerows(events)

ics_file = "calendar.ics"
csv_file = "calendar.csv"

events = parse_ics(ics_file)
export_csv(events, csv_file)

print(f"✅ Conversion terminée ! Fichier CSV disponible : {csv_file}")
