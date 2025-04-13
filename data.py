# Base de datos predefinida con actividades comunes y su consumo de agua

water_activities = {
    "shower": {
        "name": "Ducharse",
        "liters": 70,  # Litros promedio por ducha
        "description": "Ducha de aproximadamente 7 minutos"
    },
    "bath": {
        "name": "Tomar un baño de tina",
        "liters": 150,  # Litros promedio por baño de tina
        "description": "Llenar una bañera estándar"
    },
    "toilet": {
        "name": "Usar el inodoro",
        "liters": 9,  # Litros promedio por descarga
        "description": "Cada descarga del inodoro"
    },
    "brush_teeth": {
        "name": "Cepillarse los dientes",
        "liters": 10,  # Con el grifo abierto
        "description": "Cepillado de dientes con grifo abierto"
    },
    "wash_hands": {
        "name": "Lavarse las manos",
        "liters": 3,
        "description": "Lavado de manos con el grifo abierto"
    },
    "wash_dishes_by_hand": {
        "name": "Lavar platos a mano",
        "liters": 20,
        "description": "Lavar platos para 4 personas con el grifo abierto"
    },
    "dishwasher": {
        "name": "Usar lavavajillas",
        "liters": 15,
        "description": "Ciclo estándar de lavavajillas"
    },
    "washing_machine": {
        "name": "Usar lavadora",
        "liters": 60,
        "description": "Ciclo de lavado completo"
    },
    "cooking": {
        "name": "Cocinar",
        "liters": 10,
        "description": "Preparación de comidas y limpieza de alimentos"
    },
    "water_plants": {
        "name": "Regar plantas",
        "liters": 15,
        "description": "Riego de plantas interiores o pequeño jardín"
    },
    "drink_water": {
        "name": "Beber agua",
        "liters": 2,
        "description": "Consumo personal diario recomendado"
    },
    "car_wash": {
        "name": "Lavar el auto",
        "liters": 150,
        "description": "Lavado de auto con manguera"
    },
    "mop_floor": {
        "name": "Trapear pisos",
        "liters": 15,
        "description": "Limpieza de pisos de una casa pequeña"
    },
    "laundry_by_hand": {
        "name": "Lavar ropa a mano",
        "liters": 30,
        "description": "Lavado manual de ropa"
    },
    "face_wash": {
        "name": "Lavarse la cara",
        "liters": 5,
        "description": "Lavado de cara con grifo abierto"
    },
    "shave": {
        "name": "Afeitarse",
        "liters": 7,
        "description": "Afeitado con grifo abierto"
    },
    "leak_repair": {
        "name": "Reparar una fuga",
        "liters": -20,  # Ahorro (valor negativo)
        "description": "Reparar un grifo o tubería con fuga"
    },
    "water_lawn": {
        "name": "Regar el césped/jardín",
        "liters": 35,
        "description": "Riego de jardín pequeño"
    },
    "clean_bathroom": {
        "name": "Limpiar el baño",
        "liters": 12,
        "description": "Limpieza completa de un baño"
    },
    "wash_pet": {
        "name": "Bañar mascota",
        "liters": 30,
        "description": "Baño para perro o gato"
    },
    "wash_bike": {
        "name": "Lavar bicicleta/moto",
        "liters": 25,
        "description": "Limpieza de bicicleta o moto"
    }
}

# Tarifas de agua por regiones (soles por m³)
# Fuente: SUNASS (Superintendencia Nacional de Servicios de Saneamiento)
water_rates = {
    "Lima": 3.26,  # Sedapal, categoría doméstica
    "Arequipa": 2.40,  # Sedapar
    "Trujillo": 2.20,  # Sedalib
    "Chiclayo": 2.15,  # Epsel
    "Piura": 2.30,  # EPS Grau
    "Iquitos": 1.85,  # Sedaloreto
    "Cusco": 2.10,  # Sedacusco
    "Huancayo": 1.95,  # Sedam Huancayo
    "Tacna": 2.25,  # EPS Tacna
    "Pucallpa": 1.80,  # Emapacop
    "Chimbote": 2.05,  # Sedachimbote
    "Juliaca": 1.75,  # Seda Juliaca
    "Ica": 2.35,  # Emapica
    "Cajamarca": 2.15,  # Sedacaj
    "Sullana": 2.25,  # EPS Grau (Sullana)
    "Ayacucho": 1.90,  # Seda Ayacucho
    "Huánuco": 1.85,  # Seda Huánuco
    "Puno": 1.80,  # Emsapuno
    "Tarapoto": 1.95,  # Emapa San Martín
    "Tumbes": 2.20,  # Aguas de Tumbes
}

# Tarifa promedio para ciudades no listadas
DEFAULT_WATER_RATE = 2.20  # soles por m³

# Datos de consumo promedio por ciudad (litros por persona por día)
city_avg_consumption = {
    "Lima": 163,
    "Arequipa": 145,
    "Trujillo": 158,
    "Chiclayo": 152,
    "Piura": 149,
    "Iquitos": 135,
    "Cusco": 125,
    "Huancayo": 120,
    "Tacna": 140,
    "Pucallpa": 133,
    "Chimbote": 142,
    "Juliaca": 118,
    "Ica": 160,
    "Cajamarca": 122,
    "Sullana": 147,
    "Ayacucho": 115,
    "Huánuco": 119,
    "Puno": 116,
    "Tarapoto": 130,
    "Tumbes": 155
}

# Consumo promedio nacional
NATIONAL_AVG_CONSUMPTION = 145  # litros por persona por día

# Huella hídrica de alimentos comunes (litros por kg o litro)
food_water_footprint = {
    "carne_res": {
        "name": "Carne de res",
        "water_footprint": 15400,
        "unit": "litros/kg"
    },
    "carne_pollo": {
        "name": "Carne de pollo",
        "water_footprint": 4325,
        "unit": "litros/kg"
    },
    "carne_cerdo": {
        "name": "Carne de cerdo",
        "water_footprint": 5988,
        "unit": "litros/kg"
    },
    "arroz": {
        "name": "Arroz",
        "water_footprint": 3400,
        "unit": "litros/kg"
    },
    "papa": {
        "name": "Papa",
        "water_footprint": 290,
        "unit": "litros/kg"
    },
    "maiz": {
        "name": "Maíz",
        "water_footprint": 1222,
        "unit": "litros/kg"
    },
    "trigo": {
        "name": "Pan/Trigo",
        "water_footprint": 1608,
        "unit": "litros/kg"
    },
    "leche": {
        "name": "Leche",
        "water_footprint": 1020,
        "unit": "litros/litro"
    },
    "queso": {
        "name": "Queso",
        "water_footprint": 5060,
        "unit": "litros/kg"
    },
    "huevos": {
        "name": "Huevos",
        "water_footprint": 3300,
        "unit": "litros/kg"
    },
    "tomate": {
        "name": "Tomate",
        "water_footprint": 214,
        "unit": "litros/kg"
    },
    "lechuga": {
        "name": "Lechuga",
        "water_footprint": 237,
        "unit": "litros/kg"
    },
    "manzana": {
        "name": "Manzana",
        "water_footprint": 822,
        "unit": "litros/kg"
    },
    "platano": {
        "name": "Plátano/Banana",
        "water_footprint": 790,
        "unit": "litros/kg"
    },
    "cafe": {
        "name": "Café",
        "water_footprint": 18900,
        "unit": "litros/kg"
    },
    "chocolate": {
        "name": "Chocolate",
        "water_footprint": 17196,
        "unit": "litros/kg"
    },
    "azucar": {
        "name": "Azúcar",
        "water_footprint": 1782,
        "unit": "litros/kg"
    },
    "aceite_oliva": {
        "name": "Aceite de oliva",
        "water_footprint": 14431,
        "unit": "litros/litro"
    },
    "cerveza": {
        "name": "Cerveza",
        "water_footprint": 298,
        "unit": "litros/litro"
    },
    "vino": {
        "name": "Vino",
        "water_footprint": 869,
        "unit": "litros/litro"
    }
}

# Huella hídrica de productos comunes (litros por unidad)
product_water_footprint = {
    "camiseta_algodon": {
        "name": "Camiseta de algodón",
        "water_footprint": 2700,
        "unit": "litros/unidad"
    },
    "jeans": {
        "name": "Jeans/pantalón",
        "water_footprint": 8000,
        "unit": "litros/unidad"
    },
    "zapatos_cuero": {
        "name": "Zapatos de cuero",
        "water_footprint": 8000,
        "unit": "litros/par"
    },
    "papel": {
        "name": "Papel (hoja A4)",
        "water_footprint": 10,
        "unit": "litros/hoja"
    },
    "smartphone": {
        "name": "Smartphone",
        "water_footprint": 13000,
        "unit": "litros/unidad"
    },
    "computadora": {
        "name": "Computadora/Laptop",
        "water_footprint": 20000,
        "unit": "litros/unidad"
    }
}

# Desafíos predefinidos para ahorrar agua
water_challenges = [
    {
        "id": 1,
        "name": "Ducha de 5 minutos",
        "description": "Limita tus duchas a 5 minutos por día durante una semana.",
        "target": 50,  # litros a ahorrar
        "duration": 7,  # días
        "difficulty": "fácil"
    },
    {
        "id": 2,
        "name": "Reutiliza el agua",
        "description": "Reutiliza el agua de la lavadora para limpiar pisos o el inodoro durante 5 días.",
        "target": 100,
        "duration": 5,
        "difficulty": "medio"
    },
    {
        "id": 3,
        "name": "Sin carne por una semana",
        "description": "Reduce tu huella hídrica evitando carne por 7 días completos.",
        "target": 2000,
        "duration": 7,
        "difficulty": "difícil"
    },
    {
        "id": 4,
        "name": "Instala aireadores",
        "description": "Instala aireadores en todos los grifos de tu casa y mide la diferencia.",
        "target": 300,
        "duration": 14,
        "difficulty": "medio"
    },
    {
        "id": 5,
        "name": "Detector de fugas",
        "description": "Revisa tu casa en busca de fugas y repáralas para ahorrar agua.",
        "target": 500,
        "duration": 30,
        "difficulty": "difícil"
    },
    {
        "id": 6,
        "name": "Riego eficiente",
        "description": "Riega plantas y jardín solo al anochecer para evitar evaporación.",
        "target": 150,
        "duration": 10,
        "difficulty": "fácil"
    },
    {
        "id": 7,
        "name": "Doble descarga",
        "description": "Instala un sistema de doble descarga en tu inodoro.",
        "target": 400,
        "duration": 30,
        "difficulty": "medio"
    },
    {
        "id": 8,
        "name": "Cerrar el grifo",
        "description": "Cierra el grifo mientras te cepillas, te afeitas o lavas platos.",
        "target": 200,
        "duration": 7,
        "difficulty": "fácil"
    },
    {
        "id": 9,
        "name": "Desafío extremo",
        "description": "Mantén tu consumo diario por debajo de 80 litros durante 3 días.",
        "target": 300,
        "duration": 3,
        "difficulty": "extremo"
    },
    {
        "id": 10,
        "name": "Lavado eficiente",
        "description": "Utiliza la lavadora y lavavajillas solo con carga completa durante 2 semanas.",
        "target": 250,
        "duration": 14,
        "difficulty": "medio"
    }
]

# Preguntas para el quiz sobre agua
water_quiz = [
    {
        "question": "¿Qué porcentaje del agua en la Tierra es agua dulce accesible para consumo humano?",
        "options": ["3%", "0.5%", "10%", "25%"],
        "correct_answer": "0.5%",
        "explanation": "Aunque el 3% del agua de la Tierra es dulce, la mayor parte está en glaciares y solo aproximadamente el 0.5% es accesible para consumo humano."
    },
    {
        "question": "¿Cuánta agua se necesita para producir una hamburguesa de res?",
        "options": ["500 litros", "1,000 litros", "2,400 litros", "3,000 litros"],
        "correct_answer": "2,400 litros",
        "explanation": "Se necesitan aproximadamente 2,400 litros de agua para producir una hamburguesa de 150g, principalmente debido al agua necesaria para criar al ganado."
    },
    {
        "question": "¿Cuál de estas actividades consume más agua en un hogar promedio?",
        "options": ["Lavar platos a mano", "Usar el inodoro", "Ducharse", "Lavar ropa"],
        "correct_answer": "Ducharse",
        "explanation": "La ducha es típicamente la actividad que más agua consume en un hogar promedio, especialmente si las duchas son largas."
    },
    {
        "question": "¿Cuánta agua puede ahorrar un grifo que gotea si se repara?",
        "options": ["Hasta 5 litros al día", "Hasta 20 litros al día", "Hasta 100 litros al día", "Hasta 300 litros al día"],
        "correct_answer": "Hasta 100 litros al día",
        "explanation": "Un grifo con fuga constante puede desperdiciar entre 20 y 100 litros de agua al día, dependiendo de la velocidad del goteo."
    },
    {
        "question": "¿Qué país tiene la mayor huella hídrica per cápita del mundo?",
        "options": ["Estados Unidos", "China", "India", "Brasil"],
        "correct_answer": "Estados Unidos",
        "explanation": "Estados Unidos tiene la mayor huella hídrica per cápita, en gran parte debido a su alto consumo de bienes que requieren mucha agua para producirse."
    },
    {
        "question": "¿Cuánto tiempo puede sobrevivir una persona sin agua?",
        "options": ["1-2 días", "3-4 días", "7-10 días", "2 semanas"],
        "correct_answer": "3-4 días",
        "explanation": "Aunque varía según el clima y la condición física, una persona generalmente no puede sobrevivir más de 3-4 días sin agua."
    },
    {
        "question": "¿Qué porcentaje del agua dulce disponible se usa en la agricultura globalmente?",
        "options": ["30%", "50%", "70%", "90%"],
        "correct_answer": "70%",
        "explanation": "Aproximadamente el 70% del agua dulce disponible se utiliza en la agricultura para el riego de cultivos."
    },
    {
        "question": "¿Cuánta agua usa una ducha de 10 minutos?",
        "options": ["20-40 litros", "60-80 litros", "100-150 litros", "200-250 litros"],
        "correct_answer": "100-150 litros",
        "explanation": "Una ducha típica usa entre 10-15 litros por minuto, por lo que una ducha de 10 minutos consume entre 100-150 litros."
    },
    {
        "question": "¿Qué medida ahorra más agua?",
        "options": ["Cerrar el grifo al cepillarse", "Usar lavadora con carga completa", "Reducir ducha 5 minutos", "Reparar fugas"],
        "correct_answer": "Reducir ducha 5 minutos",
        "explanation": "Aunque todas ahorran agua, reducir la ducha en 5 minutos ahorra aproximadamente 75 litros, lo que suele ser más que las otras opciones."
    },
    {
        "question": "¿Cuál es la recomendación diaria de consumo de agua por persona según la ONU?",
        "options": ["20 litros", "50 litros", "100 litros", "150 litros"],
        "correct_answer": "50 litros",
        "explanation": "La ONU recomienda un mínimo de 50 litros de agua por persona al día para cubrir necesidades básicas de higiene y consumo."
    }
]

# Datos de fuentes de agua gratuitas o económicas por ciudad
water_sources = {
    "Lima": [
        {"name": "Punto de agua ANA", "address": "Av. República de Panamá 3636, San Isidro", "type": "Gratuito"},
        {"name": "Sedapal - Atarjea", "address": "El Agustino", "type": "Económico"},
        {"name": "Pileta Municipal Miraflores", "address": "Parque Kennedy", "type": "Gratuito"}
    ],
    "Arequipa": [
        {"name": "Sedapar - La Tomilla", "address": "Via de Evitamiento km 7", "type": "Económico"},
        {"name": "Plaza de Armas", "address": "Centro Histórico", "type": "Gratuito"}
    ],
    "Trujillo": [
        {"name": "Sedalib - Planta Alto Moche", "address": "Carretera Panamericana Norte km 570", "type": "Económico"},
        {"name": "Plaza Mayor", "address": "Centro Histórico", "type": "Gratuito"}
    ],
    "Cusco": [
        {"name": "Sedacusco - Planta Santa Ana", "address": "Av. Ejército", "type": "Económico"},
        {"name": "Pileta Plaza de Armas", "address": "Centro Histórico", "type": "Gratuito"}
    ]
}
