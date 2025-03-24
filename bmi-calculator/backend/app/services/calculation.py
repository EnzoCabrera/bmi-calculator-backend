def calculate_bmi(weight: float, height: float):
    height = height / 100
    bmi = weight / (height ** 2)

    return bmi