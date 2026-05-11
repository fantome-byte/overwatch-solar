class PVString:
    _counter = 0
    def __init__(self, power_wc, pv_voltage, fabricant, quantity, id = None):
        if id:
            generated_id = id
        else:
            PVString._counter += 1
            generated_id = f"STR-{str(PVString._counter).zfill(3)}"
        self._power_wc = power_wc    # puissance crête en Wc
        self._quantity = quantity
        self._pv_voltage = pv_voltage
        self._fabricant = fabricant
        self._id = generated_id

    def total_power(self):
        return self._power_wc * self._quantity
    
    def string_voltage(self):
        return self._pv_voltage * self._quantity

    def to_dict(self):
        return {
            'id' : self._id,
            'power_wc': self._power_wc,
            'fabricant': self._fabricant,
            'string_voltage': self.string_voltage(),
            'quantity' : self._quantity,
            'total_power': self.total_power()
        }
    
    def __str__(self):
        return f"[{self._id}] {self._power_wc}Wc x{self._quantity} — Total : {self.total_power()}W"