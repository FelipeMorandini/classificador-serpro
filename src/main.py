import os
from services.candidato_service import CandidatoService
from database.database_config import SessionLocal, engine, Base
from repositories.candidato_repository import CandidatoRepository
from readers.pdf_reader import extract_data_from_pdf_1, extract_data_from_pdf_2


Base.metadata.create_all(bind=engine)

session = SessionLocal()

candidato_service = CandidatoService(CandidatoRepository(session))

extract_data_from_pdf_1(os.path.abspath("src/pdfs/resultado_definitivo_objetiva.pdf"), candidato_service)
extract_data_from_pdf_2(os.path.abspath("src/pdfs/resultado_provisorio_pratica.pdf"), candidato_service)


session.close()
