"""
Script de démonstration du projet Overwatcch - Solar
Ce script montre le fonctionnement complet du système de supervision :
- Initialisation de la centrale depuis config.json
- Simulation des mesures et détection d'alertes
- Création automatique de tickets de maintenance
- Gestion du cycle de vie des tickets
"""

import json
from api import Api


def afficher_centrale(plant_info):
    """Affiche les informations de la centrale"""
    print("=== Configuration de la centrale ===")
    print(f"Nom : {plant_info['name']}")
    print(f"Localisation : {plant_info['location']}")
    print(f"Puissance installée : {plant_info['total_installed_power']}W")
    print(f"Nombre d'onduleurs : {len(plant_info['inverters'])}")
    print(f"Nombre de capteurs : {len(plant_info['sensors'])}")

    print("\nOnduleurs :")
    for inv in plant_info['inverters']:
        print(f"  - {inv['name']} ({inv['id']}) : {inv['output_power']}W")

    print("\nCapteurs :")
    for sensor in plant_info['sensors']:
        sensor_type = sensor.get('type', 'Sensor')
        print(f"  - {sensor['name']} ({sensor['id']}) : {sensor_type}")


def afficher_resultats_simulation(result, alertes):
    """Affiche les résultats de la simulation"""
    print("\n=== Résultats de la simulation ===")

    print("État des onduleurs :")
    for inv in result['inverters']:
        print(f"  - {inv['name']} ({inv['id']}) : {inv['status']}")
        if inv['current_temperature'] is not None:
            print(f"    Température : {inv['current_temperature']:.1f}°C")
            print(f"    Tension PV : {inv['current_pv_voltage']:.1f}V")
            print(f"    Puissance sortie : {inv['current_output_power']:.1f}W")

    print("\nMesures des capteurs :")
    for sensor in result['sensors']:
        print(f"  - {sensor['name']} ({sensor['id']}) : {sensor['status']}")
        if sensor['current_value'] is not None:
            unit = sensor.get('unit', '')
            print(f"    Valeur : {sensor['current_value']:.2f}{unit}")

    print(f"\nAlertes détectées : {len(alertes)}")
    for alerte in alertes:
        print(f"  - {alerte['equipment_name']} ({alerte['equipment_id']}) :")
        for type_defaut, description in alerte['alertes'].items():
            print(f"    {type_defaut} : {description}")


def afficher_tickets(tickets):
    """Affiche la liste des tickets"""
    print(f"\n=== Tickets de maintenance ({len(tickets)}) ===")
    if not tickets:
        print("Aucun ticket ouvert.")
        return

    for ticket in tickets:
        print(f"  {ticket['ticket_id']} - {ticket['equipment_name']}")
        print(f"    Défaut : {ticket['type_defaut']} - {ticket['description']}")
        print(f"    Statut : {ticket['statut']}")
        print(f"    Créé le : {ticket['date_creation']}")
        if ticket['date_cloture']:
            print(f"    Clôturé le : {ticket['date_cloture']}")
        print()


def tester_cycle_tickets(api):
    """Démontre le cycle de vie des tickets"""
    print("\n=== Test du cycle de vie des tickets ===")

    # Affichage des tickets initiaux
    print("1. Affichage des tickets actuels...")
    tickets1 = api.get_tickets()
    afficher_tickets(tickets1)

    # Mise à jour d'un ticket
    if tickets1:
        ticket_id = tickets1[0]['ticket_id']
        print(f"2. Mise à jour du ticket {ticket_id} vers 'En cours'...")
        api.update_ticket(ticket_id, 'En cours')
        tickets_updated = api.get_tickets()
        afficher_tickets(tickets_updated)

        print(f"3. Clôture du ticket {ticket_id}...")
        api.update_ticket(ticket_id, 'Cloture')
        tickets_closed = api.get_tickets()
        afficher_tickets(tickets_closed)

    # Deuxième simulation réelle
    print("4. Exécution d'une deuxième simulation...")
    result2 = api.run_simulation()
    alertes2 = api.get_alerts()
    afficher_resultats_simulation(result2, alertes2)
    
    # Affichage des tickets après la deuxième simulation
    print("\n5. Tickets après la deuxième simulation :")
    tickets2 = api.get_tickets()
    afficher_tickets(tickets2)
    
    print(f"Nombre total de tickets en attente : {len(tickets2)}")


def main():
    """Fonction principale de démonstration"""
    print("Démonstration du système Overwatch - Solar")
    print("=" * 50)

    # Initialisation
    print("\n=== Initialisation ===")
    api = Api()
    plant_info = api.get_plant_info()
    afficher_centrale(plant_info)

    # Simulation initiale
    print("\n=== Simulation initiale ===")
    result = api.run_simulation()
    alertes = api.get_alerts()
    afficher_resultats_simulation(result, alertes)

    # Affichage des tickets créés
    tickets = api.get_tickets()
    afficher_tickets(tickets)

    # Test du cycle de vie des tickets
    tester_cycle_tickets(api)

    print("\n=== Fin de la démonstration ===")
    print("Le système a montré :")
    print("- Initialisation depuis config.json")
    print("- Simulation réaliste des mesures")
    print("- Détection automatique d'alertes")
    print("- Création de tickets de maintenance")
    print("- Gestion du cycle de vie des tickets")
    print("- Persistance des données")


if __name__ == "__main__":
    main()