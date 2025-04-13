import random

# Lista de consejos para ahorro de agua
water_saving_tips = [
    {
        "id": 1,
        "description": "Cierra el grifo mientras te cepillas los dientes. Puedes ahorrar hasta 12 litros por minuto.",
        "potential_savings": 12,
        "activity": "brush_teeth"
    },
    {
        "id": 2,
        "description": "Instala cabezales de ducha de bajo flujo para reducir el consumo de agua hasta en un 50%.",
        "potential_savings": 0.5,  # Factor de reducción
        "activity": "shower"
    },
    {
        "id": 3,
        "description": "Repara grifos que gotean. Un grifo que gotea puede desperdiciar hasta 20 litros al día.",
        "potential_savings": 20,
        "activity": None  # Aplica a consumo general
    },
    {
        "id": 4,
        "description": "Lava los platos en una tina llena de agua en lugar de hacerlo con el grifo abierto.",
        "potential_savings": 0.6,  # Factor de reducción
        "activity": "wash_dishes"
    },
    {
        "id": 5,
        "description": "Utiliza la lavadora sólo con carga completa para maximizar la eficiencia del agua.",
        "potential_savings": 0.3,  # Factor de reducción
        "activity": "washing_machine"
    },
    {
        "id": 6,
        "description": "Recoge agua de lluvia para regar las plantas.",
        "potential_savings": 0.8,  # Factor de reducción
        "activity": "water_plants"
    },
    {
        "id": 7,
        "description": "Toma duchas más cortas. Reducir tu ducha en 2 minutos puede ahorrar hasta 20 litros.",
        "potential_savings": 20,
        "activity": "shower"
    },
    {
        "id": 8,
        "description": "Utiliza un sistema de doble descarga en el inodoro para ahorrar agua en cada uso.",
        "potential_savings": 0.5,  # Factor de reducción
        "activity": "toilet"
    },
    {
        "id": 9,
        "description": "No uses el inodoro como papelera. Cada descarga innecesaria gasta entre 6 y 10 litros.",
        "potential_savings": 8,
        "activity": "toilet"
    },
    {
        "id": 10,
        "description": "Lava frutas y verduras en un recipiente con agua en lugar de bajo el grifo corriente.",
        "potential_savings": 5,
        "activity": "cooking"
    }
]

def get_water_saving_tips(consumption):
    """
    Devuelve consejos relevantes basados en el consumo actual
    """
    if consumption <= 0:
        return []
    
    # Si el consumo es bajo, mostrar consejos generales
    if consumption < 50:
        return [tip for tip in water_saving_tips if tip["id"] in [3, 6, 10]]
    
    # Si el consumo es moderado
    elif consumption < 100:
        return [tip for tip in water_saving_tips if tip["id"] in [1, 4, 5, 8, 10]]
    
    # Si el consumo es alto
    else:
        return [tip for tip in water_saving_tips if tip["id"] in [2, 5, 7, 8, 9]]

def calculate_savings(tip, current_consumption):
    """
    Calcula el ahorro potencial basado en el tip y el consumo actual
    """
    # Si el tip tiene un valor fijo de ahorro
    if tip["potential_savings"] <= 1:  # Es un factor de reducción
        if tip["activity"] is None:  # Aplica al consumo general
            return current_consumption * tip["potential_savings"]
        else:
            # Asumimos que el 20% del consumo viene de esta actividad como estimación
            return (current_consumption * 0.2) * tip["potential_savings"]
    else:  # Es un valor absoluto de ahorro
        return tip["potential_savings"]

def calculate_cost_savings(water_savings, city):
    """
    Calcula el ahorro en soles basado en el ahorro de agua y la tarifa de la ciudad
    
    Args:
        water_savings: Ahorro de agua en litros
        city: Ciudad del usuario
    
    Returns:
        Tuple con (ahorro diario en soles, ahorro mensual en soles)
    """
    from data import water_rates, DEFAULT_WATER_RATE
    
    # Obtener tarifa de agua para la ciudad
    rate = water_rates.get(city, DEFAULT_WATER_RATE)
    
    # Convertir litros a metros cúbicos (1 m³ = 1000 litros)
    water_savings_m3 = water_savings / 1000
    
    # Calcular ahorro en soles
    daily_savings = water_savings_m3 * rate
    monthly_savings = daily_savings * 30
    
    return daily_savings, monthly_savings

def calculate_equivalent_bottles(water_liters):
    """
    Calcula el equivalente en botellas de agua
    
    Args:
        water_liters: Cantidad de agua en litros
    
    Returns:
        Número de botellas equivalentes (500ml)
    """
    return water_liters / 0.5  # Una botella estándar es de 500ml = 0.5 litros

def calculate_visual_impact(water_liters):
    """
    Calcula valores visuales para mostrar el impacto del agua
    
    Args:
        water_liters: Cantidad de agua en litros
    
    Returns:
        Dict con diferentes equivalencias visuales
    """
    impact = {
        "bottles": int(calculate_equivalent_bottles(water_liters)),
        "showers": int(water_liters / 70),  # Una ducha promedio usa 70 litros
        "toilets": int(water_liters / 9),   # Una descarga promedio usa 9 litros
        "plants": int(water_liters / 2),    # Regar una planta usa aprox. 2 litros
        "swimming_pools": water_liters / 50000,  # Una piscina típica contiene ~50,000 litros
        "elephants": water_liters / 150,    # Un elefante bebe ~150 litros diarios
        "days_for_person": water_liters / 100,  # Una persona consume ~100 litros diarios
    }
    return impact
