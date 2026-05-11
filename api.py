from pathlib import Path
import json
from models.plant import Plant
from models.inverter import Inverter
from models.pvstring import PVString
from models.sensor import DCVoltageSensor, ACVoltageSensor, CurrentSensor, TemperatureSensor
from manager.maintenance_manager import MaintenanceManager

_BASE_DIR = Path(__file__).parent
_DATA_DIR = _BASE_DIR / 'data'
_TICKETS_FILE = _DATA_DIR / 'tickets.json'
_CONFIG_FILE = _DATA_DIR / 'config.json'

class Api:
    def __init__(self):
        self._verifier_fichiers()
        self._plant = self._initialiser_centrale()
        self._manager = MaintenanceManager(self._plant)
        self._manager._tickets = self._charger_tickets()
        self._sauvegarder_config()
    
    def _verifier_fichiers(self):
        """Vérifie et crée les fichiers/dossiers obligatoires"""
        # Créer le dossier data/ s'il n'existe pas
        _DATA_DIR.mkdir(parents=True, exist_ok=True)

        if not _TICKETS_FILE.exists() or _TICKETS_FILE.stat().st_size == 0:
            with open(_TICKETS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print("Fiche tickets.json crée")
        
        if not _CONFIG_FILE.exists():
            raise FileNotFoundError(
            "config.json introuvable — créez ce fichier avant de lancer l'application."
            )
        
    def _initialiser_centrale(self):
        
        types_capteurs = {
            'DCVoltageSensor': DCVoltageSensor,
            'ACVoltageSensor': ACVoltageSensor,
            'CurrentSensor': CurrentSensor,
            'TemperatureSensor': TemperatureSensor
        }
        
        with open (_CONFIG_FILE, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            if config_data is not None:
                for plant_data in config_data["plants"]:
                    plant = Plant(
                        plant_data["name"],
                        plant_data["location"],
                        id = plant_data["id"]
                    )
                    
                for inverter_data in config_data["inverters"]:
                    inverter = Inverter(
                        inverter_data["name"],
                        inverter_data["output_power"],
                        inverter_data["min_pv_voltage"],
                        inverter_data["max_pv_voltage"],
                        inverter_data["min_operating_temperature"],
                        inverter_data["max_operating_temperature"],
                        id = inverter_data["id"]
                    )
                    plant.add_inverter(inverter)
                
                for sensor_data in config_data["sensors"]:
                    classe = types_capteurs[sensor_data['type']]
                    capteur = classe(sensor_data['name'], sensor_data['min_threshold'], sensor_data['max_threshold'], sensor_data["id"])
                    plant.add_sensor(capteur)
                
                for string_data in config_data["strings"]:
                    targert_inverter = next(
                        (inv for inv in plant._inverters if inv.name == string_data["inverter"]), 
                        None
                    )
                    if targert_inverter:
                        pvstring = PVString(
                            string_data["power_wc"],
                            string_data["pv_voltage"],
                            string_data["fabricant"],
                            string_data["quantity"],
                            id = string_data["id"]
                            )
                        targert_inverter.connect_panel(pvstring)
        
                return plant
                    
    def _charger_tickets(self):
        with open(_TICKETS_FILE, 'r', encoding='utf-8') as f:
            contenu = f.read()
            if not contenu.strip():
                return []
            return json.loads(contenu)
        
    
    def _sauvegarder_tickets(self):
        with open(_TICKETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._manager._tickets, f, indent = 4, ensure_ascii = False)
    
    def _construire_config(self):
        """Construit proprement le contenu du fichier config.json"""
        inverters_config = []
        strings_config = []
        for inv in self._plant._inverters:
            inverters_config.append({
                'id': inv.id,
                'name': inv.name,
                'output_power': inv._output_power,
                'min_pv_voltage': inv._min_pv_voltage,
                'max_pv_voltage': inv._max_pv_voltage,
                'min_operating_temperature': inv._min_operating_temperature,
                'max_operating_temperature': inv._max_operating_temperature,
                'strings': [s._id for s in inv._panels_connected]
                })
            
            for s in inv._panels_connected:
                strings_config.append({
                    'id': s._id,
                    'power_wc': s._power_wc,
                    'pv_voltage': s._pv_voltage,
                    'fabricant': s._fabricant,
                    'quantity': s._quantity,
                    'inverter': inv.name
                    })
        
        sensors_config = []
        for sensor in self._plant._sensors:
            sensors_config.append({
            'id': sensor.id,
            'type': type(sensor).__name__,
            'name': sensor.name,
            'min_threshold': sensor.min_threshold,
            'max_threshold': sensor.max_threshold
        })
        
        return {
            'plants': [{
                'id': self._plant.id,
                'name': self._plant.name,
                'location': self._plant.location
            }],
            'inverters': inverters_config,
            'strings': strings_config,
            'sensors': sensors_config
        }
        
    def _sauvegarder_config(self):
        with open(_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._construire_config(), f, indent = 4, ensure_ascii=False)
        
    
    # Méthodes exposées au JS :
    def run_simulation(self):
        result = self._manager.run()
        self._sauvegarder_tickets()
        return result
    
    def get_tickets(self):
        return self._manager._tickets
    
    def update_ticket(self, ticket_id, nouveau_statut):
        result = self._manager.update_ticket(ticket_id, nouveau_statut)
        self._sauvegarder_tickets()
        return result   
    
    def ajouter_inverter(self):
        """Methode à completer pour prendre en compte plusieurs onduleurs dans une installation"""
        pass    
    
    def get_plant_info(self):
        # self, name, output_power, min_pv_voltage, max_pv_voltage, min_temp, max_temp
        return self._plant.to_dict()