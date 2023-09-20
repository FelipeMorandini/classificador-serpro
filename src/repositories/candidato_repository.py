from sqlalchemy.orm import Session
from models.candidato import Candidato

class CandidatoRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, candidato_data):
        candidato = Candidato(**candidato_data)
        self.session.add(candidato)
        self.session.commit()
        self.session.refresh(candidato)
        return candidato
    
    def update(self, inscricao, updated_data):
        candidato = self.session.query(Candidato).filter(Candidato.inscricao == inscricao).first()
        for key, value in updated_data.items():
            setattr(candidato, key, value)
        self.session.commit()
        return candidato
    
    def get_all(self):
        return self.session.query(Candidato).all()

    def get_by_id(self, id):
        return self.session.query(Candidato).filter(Candidato.id == id).first()
    
    def get_by_inscricao(self, inscricao):
        return self.session.query(Candidato).filter(Candidato.inscricao == inscricao).first()

    def delete_by_id(self, id):
        candidato = self.session.query(Candidato).filter(Candidato.id == id).first()
        if candidato:
            self.session.delete(candidato)
            self.session.commit()