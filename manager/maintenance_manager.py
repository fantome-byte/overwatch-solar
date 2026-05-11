from models.simulation import Simulator
from datetime import datetime

class MaintenanceManager:
    _counter = 0
    def __init__(self, plant):
        self._plant = plant
        self._simulator = Simulator(plant)
        self._tickets = []  # liste des tickets d'intervention. Ne serait il pas mieux de créer un dict ? 
    
    # À implémenter :
    # - run()               → lance la simulation
    # - get_alerts()        → récupère les alertes actives
    # - create_ticket()     → crée un ticket depuis une alerte
    # - get_tickets()       → retourne tous les tickets
    # - update_ticket()     → change le statut d'un ticket
    def get_alerts(self):
        return self._plant.get_all_alerts()
    
    def run(self):
        self._simulator.run()
        alertes = self.get_alerts()
        
        if self._simulator._solar_factor() > 0:
            for alerte in alertes:
                for type_defaut, description in alerte['alertes'].items():
                    self.create_ticket(
                        equipment_id=alerte['equipment_id'],
                        equipment_name=alerte['equipment_name'],
                        type_defaut=type_defaut,
                        description=description
                    )
        
        return self._plant.to_dict()
    
    def create_ticket(self, equipment_id, equipment_name, type_defaut, description):
        ticket_existe = any(
        t['equipment_id'] == equipment_id 
        and t['type_defaut'] == type_defaut
        and t['statut'] != 'Cloture'
        for t in self._tickets
        )
        
        if not ticket_existe:
            MaintenanceManager._counter += 1
            ticket = {
                'ticket_id': f"TKT-{str(MaintenanceManager._counter).zfill(3)}",
                'equipment_id': equipment_id,
                'equipment_name': equipment_name,
                'type_defaut': type_defaut,
                'description': description,
                'statut': 'Ouvert',
                'date_creation': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'date_cloture': None
            }
            self._tickets.append(ticket) 
            return ticket
        return None
                    
    
    def get_tickets(self):
        return self._tickets
    
    def update_ticket(self, ticket_id, nouveau_statut):
        statuts_valides = ['Ouvert', 'En cours', 'Cloture']
        if nouveau_statut not in statuts_valides:
            raise ValueError(f"Statut invalide. Valeurs acceptées : {statuts_valides}")
        
        for ticket in self._tickets:
            if ticket['ticket_id'] == ticket_id:
                ticket['statut'] = nouveau_statut
                if nouveau_statut == 'Cloture':
                    ticket['date_cloture'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return ticket
        return None