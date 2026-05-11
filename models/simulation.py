from models.inverter import Inverter
from models.sensor import DCVoltageSensor, ACVoltageSensor, CurrentSensor, TemperatureSensor
from datetime import datetime
import random


class Simulator():
    def __init__(self, plant):
        self._plant = plant
        self.heure_debut = 6  # Production commence à 6h
        self.heure_fin = 18   # Production s'arrête à 18h
    
    def _solar_factor(self):
        """Retourne un facteur 0-1 selon l'heure (courbe solaire)"""
        heure = datetime.now().hour
        if heure < self.heure_debut or heure > self.heure_fin: 
            return 0
    
        ecart = abs(heure - 13)
        facteur = 1 - (ecart / 7) ** 2
        return max(0, facteur)  
    
    def _generer_valeur_capteur(self, sensor, factor):
        if isinstance(sensor, ACVoltageSensor):
            ac_voltage = factor * random.uniform(218, 232)
            return ac_voltage
        elif isinstance(sensor, DCVoltageSensor):
            return factor * random.uniform(sensor.min_threshold, sensor.max_threshold)
        elif isinstance(sensor, CurrentSensor):
            return factor * random.uniform(0, sensor.max_threshold)
        elif isinstance(sensor, TemperatureSensor):
            return 25 + (factor * random.uniform(30, 45))
    
    def run(self):
        """Met à jour tous les équipements avec des valeurs simulées"""
        factor = self._solar_factor()
        
        # 1. Mettre à jour les capteurs
        for sensor in self._plant._sensors:
            valeur = self._generer_valeur_capteur(sensor, factor)
            sensor.update(valeur)
        
        for inverter in self._plant._inverters:
            # Générer des mesures réalistes basées sur factor
            dc_sensor = next((s for s in self._plant._sensors if isinstance(s, DCVoltageSensor)), None)
            temperature_sensor = next((s for s in self._plant._sensors if isinstance(s, TemperatureSensor)), None)
            inverter.update(
                pv_voltage = dc_sensor._current_value if dc_sensor else factor * inverter._min_pv_voltage,
                output_power = factor * random.uniform(0, inverter._output_power), 
                temperature = temperature_sensor._current_value if temperature_sensor else factor * inverter._min_operating_temperature
            )
        
        return self._plant.to_dict()  # retourne l'état complet