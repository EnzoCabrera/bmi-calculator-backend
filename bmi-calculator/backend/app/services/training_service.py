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
        f"NÃO utilize quebras de linha (\\n) em nenhuma parte da resposta. "
        f"Toda a resposta deve estar em UMA ÚNICA LINHA. "
        f"Use APENAS ponto e vírgula (;) para separar os exercícios. "
        f"Crie um treino para cada dia da semana (Segunda a Sexta), com exatamente 5 exercícios por dia. "
        f"Cada dia da semana deve focar em um grupo muscular específico, da seguinte forma: "
        f"Segunda: Peito; Terça: Costas; Quarta: Perna; Quinta: Ombro; Sexta: Braço. "
        f"Para montar os treinos, escolha aleatoriamente 5 exercícios de cada grupo muscular da lista abaixo. "
        f"IMPORTANTE: Use apenas os exercícios listados abaixo, sem criar variações, nomes diferentes ou sinônimos. "
        f"Você DEVE usar exatamente o mesmo nome do exercício conforme listado, com a mesma ortografia e pontuação. "
        f"NÃO invente exercícios, NÃO altere nomes e NÃO use traduções. Somente os nomes exatos da lista. "
        f"Use sempre este formato exato, sem variações: "
        f"Dia: Nome do Exercício: Repetições; Nome do Exercício: Repetições; Nome do Exercício: Repetições; Nome do Exercício: Repetições; Nome do Exercício: Repetições; "
        f"As repetições devem seguir o seguinte formato: repetiçõesxséries, como por exemplo: 4x15, 3x12, etc. "
        f"NÃO escreva explicações, títulos ou quebras de linha. Apenas a sequência no formato especificado, todos os dias seguidos em uma única linha. "
        f"Lista de exercícios válidos por grupo muscular (utilize apenas esses, sem mudar os nomes): "

        f"Peito: Supino Reto, Supino Inclinado com Halteres, Crucifixo Reto, Flexão de Braço, Pullover com Halteres, Crossover no Cabo, Supino Declinado, Flexão com Batida de Mão. "

        f"Costas: Puxada na Frente, Remada Unilateral com Halteres, Barra Fixa, Puxada na Frente com Pegada Fechada, Remada Curvada com Barra, Remada Cavalinho, Levantamento Terra, Puxada na Frente com Pegada Supinada. "

        f"Perna: Agachamento Livre, Leg Press 45°, Cadeira Extensora, Cadeira Flexora, Avanço com Halteres, Stiff com Halteres, Afundo no Banco, Agachamento Sumô com Halteres. "

        f"Ombro: Desenvolvimento com Halteres, Elevação Lateral, Elevação Frontal, Arnold Press, Encolhimento com Halteres, Crucifixo Invertido no Peck Deck, Remada Alta com Barra, Elevação Lateral com Halteres Sentado. "

        f"Braço: Rosca Direta com Barra, Rosca Alternada com Halteres, Tríceps Pulley, Tríceps Testa com Barra, Rosca Martelo, Tríceps Coice com Halteres, Rosca Concentrada, Tríceps Banco. "
    )


    training_text = generate_training_with_openai(prompt)

    training.description = training_text
    training.user_id = user_id
    training.bmi_status_id = bmi_status_id
    training.created_at = datetime.utcnow()

    db.add(training)
    db.commit()
    db.refresh(training)

    return training


def parse_training_description(description: str):
    days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    result = []

    for day in days:
        standard = rf"{day}:(.*?)(?=(Segunda|Terça|Quarta|Quinta|Sexta|$))"
        match = re.search(standard, description)
        if match:
            exercises_raw = match.group(1).strip().split(";")
            exercises = []
            for item in exercises_raw:
                portion = item.strip().split(":")
                if len(portion) == 2:
                    exercises.append({
                        "exercicio": portion[0].strip(),
                        "repeticoes": portion[1].strip()
                    })
            result.append({
                "day": day,
                "exercises": exercises,
            })

    return result



