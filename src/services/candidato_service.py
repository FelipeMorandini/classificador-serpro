from repositories.candidato_repository import CandidatoRepository

class CandidatoService:
    def __init__(self, repository: CandidatoRepository):
        self.repository = repository

    def add_candidato(self, candidato_data):
        return self.repository.create(candidato_data)

    def update_candidato(self, inscricao, updated_data):
        return self.repository.update(inscricao, updated_data)
    
    def get_all_candidatos(self):
        return self.repository.get_all()

    def get_candidato_by_id(self, id):
        return self.repository.get_by_id(id)
    
    def get_candidato_by_inscricao(self, id):
        return self.repository.get_by_inscricao(id)

    def delete_candidato_by_id(self, id):
        self.repository.delete_by_id(id)