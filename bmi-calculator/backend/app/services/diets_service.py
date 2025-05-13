from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.utils.openai_configs_diets import generate_diets_with_openai
from app.db.models import Diet

router = APIRouter()


def calculate_diet(db: Session, user_bmi, bmi_status_id: int, user_id: int, diet: Diet, intolerances: List[str]):
    status_map = {
        1: "abaixo do peso",
        2: "com o peso normal",
        3: "acima do peso",
        4: "obesa"
    }

    status_text = status_map.get(user_bmi.bmi_status_id, "com status de IMC desconhecido")
    prompt = (
        f"Crie uma dieta simples para uma pessoa {status_text}. "
        f"NÃO crie uma dieta utilizando ingredientes que o usuário tem alergia: {intolerances}. Crie apenas refeições que não contenha alimentos que o usuário é intolerante."
        "A dieta DEVE conter exatamente 3 períodos: manhã, tarde e noite. "
        "Cada um desses períodos deve ter pelo menos uma refeição. "
        "Use o seguinte formato: 'Manhã: arroz, 150g; ovo, 2; Tarde: frango grelhado, 120g; batata doce, 100g; Noite: sopa de legumes, 250ml; salada, 50g;' "
        "Não use quebras de linha (\\n), apenas ponto e vírgula (;) para separar os itens. "
        "Inclua o nome do período (Manhã, Tarde, Noite), os alimentos e suas quantidades. "
        "Não escreva introduções ou explicações, apenas a lista no formato acima. "
        "Evite alimentos caros ou difíceis de encontrar em supermercados do Brasil. "
        "A dieta deve conter no máximo 5 refeições no total."
    )


    diet_text = generate_diets_with_openai(prompt)

    if not diet_text:
        raise ValueError("Não foi possível gerar a dieta com o ChatGPT.")

    diet_text = generate_diets_with_openai(prompt).replace('\n', ' ').replace('\r', '')

    diet.description = diet_text
    diet.user_id = user_id
    diet.bmi_status_id = bmi_status_id
    diet.intolerances =", ".join(intolerances)

    db.add(diet)
    db.commit()
    db.refresh(diet)

    return diet
