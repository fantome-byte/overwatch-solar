class Plant:
    _counter = 0
    def __init__(self, name, location, id = None):
        if id:
            generated_id = id
        else:
            Plant._counter += 1
            generated_id = f"PLT-{str(Plant._counter).zfill(3)}"
        self.id = generated_id
        self.name = name
        self.location = location
        
        self._inverters = []
        self._sensors = []
    
    def add_inverter(self, inverter):
        self._inverters.append(inverter)
        print(f"Onduleur {inverter.id} ajoute au parc {self.name}")
        
    
    def add_sensor(self, sensor):
        self._sensors.append(sensor)
        print(f"Capteur {sensor.id} ajoute au parc {self.name}")
        
    
    
    def total_installed_power(self):
        return sum(
            panel.total_power()
            for inverter in self._inverters
            for panel in inverter._panels_connected
        )
    
    def get_all_alerts(self):
        all_alerts = []
        for inverter in self._inverters:
            alertes = inverter.check_alertes()
            if alertes:
                all_alerts.append({
                    'equipment_id': inverter.id,
                    'equipment_name': inverter.name,
                    'alertes': alertes
                })
        for sensor in self._sensors:
            alertes = sensor.check_alertes()
            if alertes:
                all_alerts.append({
                    'equipment_id': sensor.id,
                    'equipment_name': sensor.name,
                    'alertes': alertes
                })
        return all_alerts
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'inverters': [i.to_dict() for i in self._inverters],
            'sensors': [s.to_dict() for s in self._sensors],
            'total_installed_power': self.total_installed_power()
        }

    def __str__(self):
        return f"[{self.id}] {self.name} — {self.location} | {len(self._inverters)} onduleurs, {len(self._sensors)} capteurs"