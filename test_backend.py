# from models.plant import Plant
# from models.inverter import Inverter
# from models.pvstring import PVString
# from models.sensor import CurrentSensor, ACVoltageSensor, DCVoltageSensor, TemperatureSensor
# from models.simulation import Simulator
# from manager.maintenance_manager import MaintenanceManager

# plant_1 = Plant("PLT001", "Personal", "Lome")
# inverter_1 = Inverter("Personal", 5000, 360, 750, 25, 41)
# pvstring_1 = PVString(600, 36, "Risen", 8)
# acvoltagesensor1 = ACVoltageSensor("ACSensor1", 218, 240)
# dcvoltagesensor1 = DCVoltageSensor("DCSensor", 20, 100)
# currentsensor1 = CurrentSensor("CurrentSensor", 5, 100)
# temperaturesensor1 = TemperatureSensor("TempSensor", 20, 60)


# inverter_1.connect_panel(pvstring_1)
# plant_1.add_inverter(inverter_1)
# plant_1.add_sensor(acvoltagesensor1)
# plant_1.add_sensor(dcvoltagesensor1)
# plant_1.add_sensor(currentsensor1)
# plant_1.add_sensor(temperaturesensor1)

# manager = MaintenanceManager(plant_1)
# result = manager.run()

# print(result)
# print("Tickets :", manager.get_tickets())
from api import Api

# Test 1 — Initialisation depuis config.json
print("=== Test initialisation ===")
api = Api()
plant_info = api.get_plant_info()
print(f"Centrale : {plant_info['name']} — {plant_info['location']}")
print(f"Onduleurs : {len(plant_info['inverters'])}")
print(f"Capteurs : {len(plant_info['sensors'])}")
print(f"Puissance installée : {plant_info['total_installed_power']}W")

# Test 2 — Simulation
print("\n=== Test simulation ===")
result = api.run_simulation()
print(f"Status onduleur : {result['inverters'][0]['status']}")
print(f"Tickets générés : {len(api.get_tickets())}")

# Test 3 — Persistance IDs
print("\n=== Test persistance IDs ===")
inverter_id = result['inverters'][0]['id']
sensor_id = result['sensors'][0]['id']
print(f"ID onduleur : {inverter_id}")
print(f"ID capteur : {sensor_id}")
print("Ferme et relance le script — les IDs doivent rester identiques")

# Test 4 — Tickets
print("\n=== Test tickets ===")
tickets = api.get_tickets()
print(f"Nombre de tickets : {len(tickets)}")
for ticket in tickets:
    print(f"  {ticket['ticket_id']} — {ticket['equipment_name']} — {ticket['type_defaut']} — {ticket['statut']}")

# Test 5 — Update ticket
if tickets:
    premier_ticket = tickets[0]['ticket_id']
    api.update_ticket(premier_ticket, 'En cours')
    print(f"\nTicket {premier_ticket} mis à jour → 'En cours'")
    print(f"Vérification : {api.get_tickets()[0]['statut']}")