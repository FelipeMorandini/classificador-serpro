import pdfplumber
import re

from models.candidato import Candidato
from services.candidato_service import CandidatoService

def extract_data_from_pdf_1(file_path, candidato_service: CandidatoService):
    with pdfplumber.open(file_path) as pdf:
        current_type = 0
        full_text = ''

        for page in pdf.pages:
            text = page.extract_text()
            
            text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE) 
            text = text.replace('\n', ' ')
            text = re.sub(r'(?<=\d)\n(?=\d)', '', text)
            
            full_text = full_text + text
        
        category_patterns = {
            r"Resultado final nas provas objetivas": ("General", 1),
            r"Resultado final dos candidatos que solicitaram concorrer às vagas reservadas às pessoas com deficiência": ("Persons with disabilities", 2),
            r"Resultado final dos candidatos que se autodeclararam negros": ("Self-declared black candidates", 3)
        }

        positions = {pattern: re.search(pattern, full_text).start() for pattern in category_patterns if re.search(pattern, full_text)}

        sorted_patterns = sorted(positions.items(), key=lambda x: x[1])

        for i, (pattern, start_pos) in enumerate(sorted_patterns):
            end_pos = sorted_patterns[i+1][1] if i+1 < len(sorted_patterns) else None
            sliced_text = full_text[start_pos:end_pos]
            
            current_category, current_type = category_patterns[pattern]
            
            candidate_pattern = r"(\d{8}), ([A-Za-z\s\.\'\-]+), ([\d\.-]+), (\d+), ([\d\.-]+), (\d+), ([\d\.-]+), (\d+), ([\d\.-]+), (\d+), ([\d\.-]+), (\d+), ([\d\.-]+), (\d+), ([\d\.-]+), (\d+), ([\d\.-]+)"
            matches = re.findall(candidate_pattern, sliced_text)

            for match in matches:
                registration_number = match[0]
                name = match[1]
                nota_p1 = float(match[12])
                nota_p2 = float(match[14])

                data = {
                    'inscricao': registration_number,
                    'tipo': current_type,
                    'nome': name,
                    'nota_p1': nota_p1,
                    'nota_p2': nota_p2,
                }
                
                candidato_existente = candidato_service.get_candidato_by_inscricao(registration_number)
                
                if candidato_existente == None:
                    candidato_service.add_candidato(data)
                else:
                    print(f"Candidato {name} / {registration_number} já existe")
    
def extract_data_from_pdf_2(file_path, candidato_service: CandidatoService):
    with pdfplumber.open(file_path) as pdf:
        current_type = 0
        full_text = ''
        data = []

        for page in pdf.pages:
            text = page.extract_text()
            
            text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE) 
            text = text.replace('\n', ' ')
            text = re.sub(r'(?<=\d)\n(?=\d)', '', text)
            
            full_text = full_text + text
        
        category_patterns = {
            r"Resultado provisório na prova de conhecimentos aplicados": ("General", 1),
            r"Resultado provisório dos candidatos que solicitaram concorrer às vagas reservadas às pessoas com deficiência": ("Persons with disabilities", 2),
            r"Resultado provisório dos candidatos que se autodeclararam negros": ("Self-declared black candidates", 3)
        }

        positions = {pattern: re.search(pattern, full_text).start() for pattern in category_patterns if re.search(pattern, full_text)}

        sorted_patterns = sorted(positions.items(), key=lambda x: x[1])

        for i, (pattern, start_pos) in enumerate(sorted_patterns):
            end_pos = sorted_patterns[i+1][1] if i+1 < len(sorted_patterns) else None
            sliced_text = full_text[start_pos:end_pos]
            
            current_category, current_type = category_patterns[pattern]
            
            candidate_pattern = r"(\d{8}), ([A-Za-z\s\.\'\-]+), ([\d]+\.[\d]{2})"
            matches = re.findall(candidate_pattern, sliced_text)

            for match in matches:
                registration_number = match[0]
                name = match[1]
                nota_p3 = float(match[2])

                existing_candidato = candidato_service.get_candidato_by_inscricao(registration_number)
                
                if existing_candidato:
                    updated_data = {'nota_p3': nota_p3}
                    try:
                        candidato_service.update_candidato(registration_number, updated_data)
                    except Exception as e:
                        print(e)

        return data
