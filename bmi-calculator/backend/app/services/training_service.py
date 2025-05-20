from datetime import datetime
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.utils.openai_configs_trainings import generate_training_with_openai
from app.db.models import Training
import re

router = APIRouter()


# Method to create the training
def calculate_training(db: Session, user_bmi, bmi_status_id: int, user_id: int, training:Training):

    # Dictionary of existing bmi_status_id
    status_map = {
        1: "abaixo do peso",
        2: "com o peso normal",
        3: "acima do peso",
        4: "obesa"
    }


    status_text = status_map.get(user_bmi.bmi_status_id, "com status de IMC desconhecido")

    prompt = (
        f"Crie um treino simples para uma pessoa {status_text}. "
        f"NÃO utilize quebras de linha (\n) em nenhuma parte da resposta. "
        f"Toda a resposta deve estar em UMA ÚNICA LINHA. "
        f"Use APENAS ponto e vírgula (;) para separar os exercícios. "
        f"Crie um treino para cada dia da semana (Segunda a Sexta), com exatamente 5 exercícios por dia. "
        f"Use sempre este formato exato, sem variações: "
        f"Dia: Nome do Exercício: Repetições; Nome do Exercício: Repetições; Nome do Exercício: Repetições; Nome do Exercício: Repetições; Nome do Exercício: Repetições; "
        f"Exemplo: Segunda: Agachamento: 4x15; Flexão de Braço: 4x12; Prancha Ventral: 3x45s; Abdominal: 4x20; Polichinelo: 4x30s; Terça: ... "
        f"IMPORTANTE: Não escreva explicações, títulos ou quebras de linha. Apenas a sequência no formato especificado, todos os dias seguidos em uma única linha. "
        f"Sempre utilize exercícios variados e realistas."
       )


    training_text = generate_training_with_openai(prompt)

    parsed_training = parse_training_description(training_text)
    print(parsed_training)

    training.description = training_text
    training.user_id = user_id
    training.bmi_status_id = bmi_status_id
    training.created_at = datetime.utcnow()

    db.add(training)
    db.commit()
    db.refresh(training)

    return training


def parse_training_description(description: str) -> dict:
    days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    result = {}

    for day in days:
        standard = rf"{day}:(.*?)(?=(Segunda|Terça|Quarta|Quinta|Sexta|$))"
        match = re.search(standard, description)
        if match:
            exercicios_raw = match.group(1).strip().split(";")
            exercicios = []
            for item in exercicios_raw:
                portion = item.strip().split(":")
                if len(portion) == 2:
                    exercicios.append({
                        "exercicio": portion[0].strip(),
                        "repeticoes": portion[1].strip()
                    })
            result[day] = exercicios

    return result



