from models.equipment import Equipment

class Inverter(Equipment):
    _counter = 0
    def __init__(self, name, output_power, min_pv_voltage, max_pv_voltage, min_operating_temperature, max_operating_temperature, id = None):
        if id:
            generated_id = id
        else:     
            Inverter._counter += 1
            generated_id = f"INV-{str(Inverter._counter).zfill(3)}"
        super().__init__(generated_id, name)
        
        # Configuration
        self._output_power = output_power
        self._min_pv_voltage = min_pv_voltage
        self._max_pv_voltage = max_pv_voltage
        self._min_operating_temperature = min_operating_temperature
        self._max_operating_temperature = max_operating_temperature
        # Telemetrie
        self._current_temperature = None
        self._current_pv_voltage = None
        self._current_output_power = None
        
        self._panels_connected = []
        
        
    def update(self, temperature, pv_voltage, output_power):
        """Met a jour les valeurs telemesures, appele par le simulateur """
        self._current_temperature = temperature
        self._current_pv_voltage = pv_voltage
        self._current_output_power = output_power
        
        self.status = 'nominal' if not self.check_alertes() else 'warning'
    
    def get_measurements(self):
        """Recupere les mesures de l'onduleur"""
        return {
        'current_temperature': self._current_temperature,
        'current_pv_voltage': self._current_pv_voltage,
        'current_output_power': self._current_output_power
        }
        
    def connect_panel(self, pvstring):
        total_power = sum(s.total_power() for s in self._panels_connected)
        if total_power + pvstring.total_power() <= self._output_power:
            self._panels_connected.append(pvstring)
            print(f"{self.id} : String {pvstring._id} connecte")
            return True
        print(f"{self.id} : Capacite maximale atteinte")
        return False
        
    
    def check_alertes(self):
        """Verifie s'il y'a une alerte"""
        if self._current_temperature is None:
            return {}
        alertes = {}
        if self._current_output_power > self._output_power :
            alertes['puissance'] = 'Surcharge'
        if self._current_temperature < self._min_operating_temperature :
            alertes['temperature'] = 'Temperature trop basse'
        elif self._current_temperature > self._max_operating_temperature:
            alertes['temperature'] = 'Temperature trop elevee'
        if self._current_pv_voltage < self._min_pv_voltage :
            alertes['pv_voltage'] = 'Sous-tension'
        elif self._current_pv_voltage > self._max_pv_voltage :
            alertes['pv_voltage'] = 'Surtension'
        
        return alertes
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'output_power': self._output_power,
            'min_pv_voltage': self._min_pv_voltage,
            'max_pv_voltage': self._max_pv_voltage,
            'min_operating_temperature': self._min_operating_temperature,
            'max_operating_temperature': self._max_operating_temperature,
            'panels_connected': [p.to_dict() for p in self._panels_connected],
            
            'current_temperature': self._current_temperature,
            'current_pv_voltage': self._current_pv_voltage,
            'current_output_power': self._current_output_power
        })
        return data 