from models.equipment import Equipment

class Sensor(Equipment):
    _counter = 0
    def __init__(self, name, min_threshold, max_threshold, id = None):
        if id:
            generated_id = id
        else:     
            Sensor._counter += 1
            generated_id = f"SEN-{str(Sensor._counter).zfill(3)}"
        super().__init__(generated_id, name)
        
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        
        self._current_value = None
        
    def update(self, value):
        self._current_value = value
        self.status = 'nominal' if not self.check_alertes() else 'warning'
    
    def check_alertes(self):
        if self._current_value is None:
            return {}
        
        alertes = {}
        if self._current_value < self.min_threshold:
            alertes['valeur'] = 'Valeur en dessous du seuil minimum'
        elif self.max_threshold < self._current_value:
            alertes['valeur'] = 'Valeur au dessus du seuil maximum'
        return alertes
        
    
    def get_measurements(self):
        return { 
                'current_value' : self._current_value
                }
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'min_threshold': self.min_threshold,
            'max_threshold': self.max_threshold,
            'current_value': self._current_value,
            'unit': getattr(self, 'unit', None),
            'type': type(self).__name__
        })
        return data
    

class VoltageSensor(Sensor):
    def __init__(self, name, min_threshold, max_threshold, id = None, unit = 'V'):
        super().__init__(name, min_threshold, max_threshold, id)
        self.unit = unit
        

class DCVoltageSensor(VoltageSensor):        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'type': 'DC'
        })
        return data
    

class ACVoltageSensor(VoltageSensor):
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'type':'AC'
        })
        return data

class CurrentSensor(Sensor):
    def __init__(self, name, min_threshold, max_threshold, id = None, unit = 'A'):
        super().__init__(name, min_threshold, max_threshold, id)
        self.unit = unit
    

class TemperatureSensor(Sensor):
    def __init__(self, name, min_threshold, max_threshold, id = None, unit = '°C'):
        super().__init__(name, min_threshold, max_threshold, id)
        self.unit = unit
        