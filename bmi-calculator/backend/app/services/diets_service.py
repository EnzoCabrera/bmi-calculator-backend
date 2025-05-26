from datetime import datetime
from typing import List, Dict, Any

from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.utils.openai_configs_diets import generate_diets_with_openai
from app.db.models import Diet
import re
from collections import defaultdict


router = APIRouter()

# Method to create the diet
def calculate_diet(db: Session, user_bmi, bmi_status_id: int, user_id: int, diet: Diet, intolerances: List[str]):

    # Dictionary of existing bmi_status_id
    status_map = {
        1: "abaixo do peso",
        2: "com o peso normal",
        3: "acima do peso",
        4: "obesa"
    }

    status_text = status_map.get(user_bmi.bmi_status_id, "com status de IMC desconhecido")
    prompt = (
        f"Crie uma dieta semanal completa para uma pessoa {status_text}. "
        f"Não utilize NENHUM prato que contenha ingredientes aos quais o usuário tem alergia ou intolerância: {intolerances}. "
        f"Todos os pratos listados abaixo já são seguros, portanto podem ser utilizados sem modificações. "
        f"A dieta deve conter EXATAMENTE 7 dias: Segunda, Terça, Quarta, Quinta, Sexta, Sábado e Domingo. "
        f"Cada dia deve conter EXATAMENTE 4 refeições: Café da Manhã, Almoço, Café da Tarde e Jantar — NESSA ORDEM. "
        f"Cada refeição deve conter EXATAMENTE 1 prato, com: "
        f"1) nome do prato (obrigatoriamente precedido por 'Prato:') e "
        f"2) lista de ingredientes (obrigatoriamente precedida por 'Ingredientes:'), SEMPRE acompanhados das quantidades. "
        f"As quantidades DEVEM ser explícitas, usando unidades como: gramas (g), mililitros (ml), colheres de sopa, unidades (ex: 2 ovos), fatias, copos ou xícaras. "
        f"NUNCA escreva ingredientes sem quantidade — use sempre: '2 ovos', '30g de aveia', '1 xícara de brócolis', etc. "
        f"O nome do dia (ex: Segunda:) deve ser usado APENAS no início de cada dia, antes do Café da Manhã. "
        f"NUNCA repita o nome do dia em outras refeições do mesmo dia. "
        f"NUNCA pule dias nem refeições. Finalize exatamente no jantar de Domingo. "
        f"NUNCA omita ou altere palavras-chave obrigatórias: Café da Manhã:, Almoço:, Café da Tarde:, Jantar:, Prato:, Ingredientes:. "
        f"NUNCA escreva 'Almoço:' ou 'Jantar:' dentro da seção de ingredientes. "
        f"NUNCA use títulos, quebras de linha (\\n), listas, explicações ou comentários. "
        f"Use apenas ponto e vírgula (;) para separar blocos de informação — NUNCA antes do nome do dia. "
        f"Siga exatamente o modelo abaixo para cada dia:\n"
        f"Segunda: Café da Manhã: Prato: [nome]; Ingredientes: [quantidades]; "
        f"Almoço: Prato: [nome]; Ingredientes: [quantidades]; "
        f"Café da Tarde: Prato: [nome]; Ingredientes: [quantidades]; "
        f"Jantar: Prato: [nome]; Ingredientes: [quantidades];\n"
        f"Use os nomes dos dias da semana exatamente assim: Segunda, Terça, Quarta, Quinta, Sexta, Sábado, Domingo — SEM '-feira'. "
        f"Utilize apenas os pratos abaixo, sem alterar nomes nem ingredientes:\n"
        f"Café da Manhã: Omelete com espinafre e tomate, Tapioca com ovo mexido, Pão integral com pasta de abacate, Panqueca de banana e aveia, Pão de queijo fit com batata-doce, Mingau de aveia com banana e chia, Tapioca com pasta de grão-de-bico (homus), Smoothie de frutas com linhaça, Pão integral com pasta de amendoim e banana, Crepioca com espinafre.\n"
        f"Almoço: Peito de frango grelhado com arroz integral e brócolis, Tilápia grelhada com batata-doce e salada, Quinoa com frango desfiado e legumes, Estrogonofe de frango leve com arroz e salada, Arroz com lentilha e legumes salteados, Escondidinho de batata-doce com carne moída, Abobrinha recheada com arroz e legumes, Polenta cremosa com legumes refogados, Frango desfiado com purê de mandioquinha e couve refogada, Carne bovina grelhada com arroz integral e vagem.\n"
        f"Café da Tarde: Frutas picadas com granola sem açúcar, Pão integral com ovo cozido e tomate, Iogurte vegetal com morangos e linhaça, Tâmara com castanha ou pasta de amendoim, Bolo de banana com aveia (vegano), Cookies de aveia e uva-passa, Pão integral com homus e cenoura ralada, Mix de castanhas com frutas secas, Torrada integral com guacamole.\n"
        f"Jantar: Sopa de abóbora com gengibre, Omelete de legumes com arroz integral, Legumes assados no forno com frango desfiado, Salada morna de batata-doce, grão-de-bico e couve, Sopa de lentilha com legumes, Arroz integral com tofu grelhado e couve refogada, Panqueca de aveia com recheio de legumes, Purê de inhame com cogumelos salteados, Tabule com grão-de-bico e hortelã."
    )

    diet_text = generate_diets_with_openai(prompt).replace('\n', ' ').replace('\r', '')

    if not diet_text:
        raise ValueError("Não foi possível gerar a dieta com o ChatGPT.")

    diet_text = sanitize_diet_text(diet_text)

    diet.description = diet_text
    diet.user_id = user_id
    diet.bmi_status_id = bmi_status_id
    diet.intolerances =", ".join(intolerances)
    diet.created_at = datetime.utcnow()

    db.add(diet)
    db.commit()
    db.refresh(diet)

    return diet

def sanitize_diet_text(text: str) -> str:
    # Remove quebras de linha e múltiplos espaços
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s{2,}', ' ', text)

    # Corrige ;; para ; apenas uma vez
    text = re.sub(r';\s*;', ';', text)

    # Garante espaço depois dos dois-pontos nas palavras-chave
    text = re.sub(r'(Café da Manhã|Almoço|Café da Tarde|Jantar|Prato|Ingredientes):', r'\1: ', text)

    # Corrige pontuação duplicada em final de frase
    text = re.sub(r'\.\s*\.', '.', text)

    # Garante que as palavras-chave estejam sempre seguidas de espaço e ponto e vírgula corretos
    text = re.sub(r'\s*;\s*', '; ', text)
    text = re.sub(r'\s*:\s*', ': ', text)

    # Remove espaço extra entre palavras e pontuação
    text = re.sub(r'\s+,', ',', text)
    text = re.sub(r',\s+', ', ', text)

    return text.strip()


def parse_diet_description(diet_text: str) -> List[Dict[str, Any]]:
    days = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    result: List[Dict[str, Any]] = []

    portions = re.split(r"(Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo):", diet_text)
    portions = [p.strip() for p in portions if p.strip()]

    for i in range(0, len(portions), 2):
        day = portions[i]
        content = portions[i + 1]
        day_data = {"day": day, "meals": []}

        standard = re.findall(
            r"(Café da Manhã|Almoço|Café da Tarde|Jantar):\s*"
            r"Prato:\s*(.*?);\s*"
            r"Ingredientes:\s*(.*?)(?=(?:Café da Manhã|Almoço|Café da Tarde|Jantar|$))",
            content
        )

        for meal, dish, ingredients in standard:
            day_data["meals"].append({
                "meal": meal,
                "dish": dish.strip(),
                "ingredients": ingredients.strip()
            })

        result.append(day_data)

    return result