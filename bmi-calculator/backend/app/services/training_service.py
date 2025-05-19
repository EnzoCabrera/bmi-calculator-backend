from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.utils.openai_configs_trainings import generate_training_with_openai
from app.db.models import Training

router = APIRouter()


# Method to create the training
def calculate_training(db: Session, user_bmi, bmi_status_id: int, user_id: int, training:Training, free_time: int):

    # Dictionary of existing bmi_status_id
    status_map = {
        1: "abaixo do peso",
        2: "com o peso normal",
        3: "acima do peso",
        4: "obesa"
    }

    if free_time == 0:
        raise ValueError("Você tem que ter um tempo livre para fazer os exercícios")
    elif free_time > 3:
        raise ValueError("Um usuário só pode possuir 3 horas livres por dia.")

    status_text = status_map.get(user_bmi.bmi_status_id, "com status de IMC desconhecido")
    prompt = (
        f"Crie um treino simples para uma pessoa {status_text} com {free_time} hora{'s' if free_time > 1 else ''} livre por dia. "
        f"Independentemente da quantidade de horas livres do usuário. Crie um treino para cada dia da semana."
        f"Os treinos devem ser desse modo: Segunda: exercicio: 4x15; exercicio: 4x12; exercicio: 3x45s; exercicio: 4x10; Terça: exercicio: 4x15; exercicio: 4x12; exercicio: 3x10; exercicio: 4x10; Quarta: exercicio: 4x15; exercicio: 4x12; exercicio: 3x45s; exercicio: 4x10; Quinta: exercicio: 4x15; exercicio: 4x12; exercicio: 3x10; exercicio: 4x10; Sexta: exercicio: 4x15; exercicio: 4x12; exercicio: 3x45s; exercicio: 4x10. Isso é apenas um exemplo a ser seguido, crie os treinos com exercícios reais."
        f"SEMPRE utilize exercícios diversos."
        f"NÃO utilize quebra de linha para dividir os dias da semana, apenas ponto e vírgula."
        f"Retorne apenas os dias da semana, os exercícios e suas repetições separados por ponto e vírgula, sem explicações ou introduções."
        f"NÃO utilize quebras de linha, apenas ponto e vírgula. Exemplo de formato: 'Agachamento: 3x15; Flexão: 3x12; Prancha: 3x30s'"
        f"Quando o usuário tiver apenas 1 hora livre por dia, ofereça no máximo 4 exercicios diferentes. Se o usuário tiver 2 horas livres por dia, ofereça 7 exercicios diferentes. Se o usuário tiver 3 horas livres por dia, ofereça 9 exercicios diferentes"
    )


    training_text = generate_training_with_openai(prompt)

    training.description = training_text
    training.user_id = user_id
    training.bmi_status_id = bmi_status_id
    training.free_time = free_time
    training.created_at = datetime.utcnow()

    db.add(training)
    db.commit()
    db.refresh(training)

    return training


