from abc import ABC, abstractmethod

class Equipment(ABC):
    """Classe abstraite pour tous les equipements typique d'une centrale"""
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._status = 'offline' #'nominal', 'warning', 'critical', 'offline'
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def status(self):
        """Getter pour le status de l'equipement"""
        return self._status
    
    @status.setter
    def status(self, valeur):
        valeurs_valides = ['nominal', 'warning', 'critical', 'offline']
        if valeur not in valeurs_valides:
            raise ValueError(f"Status invalide. Valeurs acceptées : {valeurs_valides}")
        self._status = valeur
            
    
    @abstractmethod
    def get_measurements(self):
        """Recupere les mesures et retourne un dict"""
        pass
    
    @abstractmethod
    def check_alertes(self):
        """Verifie s'il y'a une alerte"""
        pass
    
    def to_dict(self):
        """Convertir l'object python en dict"""
        return {
            'id': self.id,
            'name': self.name,
            'status': self._status
        }
    
    def __str__(self):
        return f"[{self.id}] - {self.name} - Status : {self._status}"