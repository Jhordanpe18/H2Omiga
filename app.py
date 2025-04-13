import streamlit as st
import pandas as pd
import json
import os
import io
import csv
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
from utils import (
    get_water_saving_tips, calculate_savings, calculate_cost_savings,
    calculate_equivalent_bottles, calculate_visual_impact
)
from data import (
    water_activities, water_rates, DEFAULT_WATER_RATE,
    city_avg_consumption, NATIONAL_AVG_CONSUMPTION,
    food_water_footprint, product_water_footprint,
    water_challenges, water_quiz, water_sources
)
from assets.water_facts import water_facts

# Configuración de la página
st.set_page_config(
    page_title="H2Omiga - Monitor de Consumo de Agua",
    page_icon="💧",
    layout="wide"
)

# Función para cargar datos de usuario
def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as f:
            return json.load(f)
    return {}

# Función para guardar datos de usuario
def save_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f)

# Función para crear o actualizar usuario
def create_or_update_user(name, city):
    user_data = load_user_data()
    
    if name not in user_data:
        user_data[name] = {
            "city": city,
            "consumption": {},
            "tips_shown": []
        }
    else:
        user_data[name]["city"] = city
    
    save_user_data(user_data)
    return name

# Función para registrar consumo
def register_consumption(username, activities):
    user_data = load_user_data()
    
    today = datetime.now().strftime("%Y-%m-%d")
    total_consumption = sum(water_activities[activity]["liters"] * quantity for activity, quantity in activities.items() if quantity > 0)
    
    if today not in user_data[username]["consumption"]:
        user_data[username]["consumption"][today] = {}
    
    for activity, quantity in activities.items():
        if quantity > 0:
            if activity not in user_data[username]["consumption"][today]:
                user_data[username]["consumption"][today][activity] = 0
            user_data[username]["consumption"][today][activity] += quantity
    
    save_user_data(user_data)
    return total_consumption

# Función para obtener consumo total por día
def get_daily_consumption(username):
    user_data = load_user_data()
    
    if username not in user_data:
        return {}
    
    daily_consumption = {}
    
    for date, activities in user_data[username]["consumption"].items():
        daily_total = sum(water_activities[activity]["liters"] * quantity 
                        for activity, quantity in activities.items())
        daily_consumption[date] = daily_total
    
    return daily_consumption

# Función para obtener consumo semanal
def get_weekly_consumption(username):
    daily_consumption = get_daily_consumption(username)
    
    # Obtener fechas de la última semana
    today = datetime.now().date()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    
    weekly_consumption = {}
    for date in dates:
        if date in daily_consumption:
            weekly_consumption[date] = daily_consumption[date]
        else:
            weekly_consumption[date] = 0
    
    return weekly_consumption

# Función para mostrar gráfico de consumo semanal
def show_weekly_chart(username):
    weekly_consumption = get_weekly_consumption(username)
    
    # Convertir fechas a formato más legible
    days = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }
    
    df = pd.DataFrame({
        "Fecha": weekly_consumption.keys(),
        "Consumo (litros)": weekly_consumption.values()
    })
    
    # Convertir fechas a objetos datetime
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    
    # Añadir el día de la semana
    df["Día"] = df["Fecha"].dt.day_name().map(days)
    
    # Ordenar por fecha
    df = df.sort_values("Fecha")
    
    # Crear gráfico
    fig = px.bar(
        df, 
        x="Día", 
        y="Consumo (litros)",
        color="Consumo (litros)",
        color_continuous_scale=["#A3E5FA", "#0097CE", "#005C85"],
        labels={"Consumo (litros)": "Consumo de agua (litros)"},
        title="Consumo de agua semanal"
    )
    
    # Añadir línea de límite en 100 litros
    fig.add_hline(
        y=100, 
        line_dash="dash", 
        line_color="red", 
        annotation_text="Límite recomendado", 
        annotation_position="bottom right"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Función para mostrar consejos
def show_tips(username, daily_consumption):
    user_data = load_user_data()
    
    if username not in user_data:
        return
        
    tips = get_water_saving_tips(daily_consumption)
    
    if not tips:
        return
    
    # Obtener la ciudad del usuario para calcular ahorro en dinero
    city = user_data[username].get("city", "Lima")
    
    # Mostrar solo tips que no han sido mostrados antes
    shown_tips = user_data[username].get("tips_shown", [])
    new_tips = [tip for tip in tips if tip["id"] not in shown_tips]
    
    if not new_tips:
        # Si todos los tips ya se han mostrado, reiniciar
        new_tips = tips
        user_data[username]["tips_shown"] = []
    
    # Seleccionar un tip aleatorio de los nuevos
    tip = random.choice(new_tips)
    
    # Guardar que se ha mostrado este tip
    user_data[username]["tips_shown"].append(tip["id"])
    save_user_data(user_data)
    
    # Calcular ahorro potencial en litros
    potential_savings_liters = calculate_savings(tip, daily_consumption)
    
    # Calcular ahorro potencial en dinero
    daily_cost_savings, monthly_cost_savings = calculate_cost_savings(potential_savings_liters, city)
    
    # Obtener tarifa de agua actual
    water_rate = water_rates.get(city, DEFAULT_WATER_RATE)
    
    st.info(f"💧 **Consejo de ahorro:** {tip['description']}")
    
    # Mostrar información de ahorro
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"""
        **Ahorro de agua:**
        - {potential_savings_liters:.1f} litros al día
        - {(potential_savings_liters * 30):.1f} litros al mes
        """)
    
    with col2:
        st.success(f"""
        **Ahorro económico:**
        - S/ {daily_cost_savings:.2f} al día
        - S/ {monthly_cost_savings:.2f} al mes
        
        _Basado en tarifa de agua: S/ {water_rate:.2f} por m³_
        """)
    

# Inicialización de sesión
if 'step' not in st.session_state:
    st.session_state.step = 'intro'
    st.session_state.intro_page = 0

if 'user' not in st.session_state:
    st.session_state.user = None

# Definición de frases para la introducción
fact1 = random.choice(water_facts)
remaining_facts = [f for f in water_facts if f != fact1]
fact2 = random.choice(remaining_facts)

intro_content = [
    {
        "title": "💧 El agua es vida",
        "text": "El agua es un recurso vital pero limitado en nuestro planeta.",
        "color": "blue"
    },
    {
        "title": "⚠️ Crisis hídrica",
        "text": fact1,
        "color": "orange"
    },
    {
        "title": "🏙️ Ciudades sin agua",
        "text": fact2,
        "color": "red"
    },
    {
        "title": "💡 Soluciones individuales",
        "text": "Cada persona puede hacer la diferencia. Pequeñas acciones diarias pueden generar un gran impacto en la conservación del agua.",
        "color": "green"
    },
    {
        "title": "📊 H2Omiga",
        "text": "Esta aplicación te ayudará a monitorear y reducir tu consumo diario de agua, ahorrando dinero y contribuyendo a la sostenibilidad del planeta.",
        "color": "blue"
    }
]

# Pantalla de introducción
if st.session_state.step == 'intro':
    current_page = st.session_state.intro_page
    
    # Si ya pasamos por todas las páginas de introducción
    if current_page >= len(intro_content):
        st.session_state.step = 'register'
        st.rerun()
    
    current = intro_content[current_page]
    
    # Título centrado
    st.markdown(f"<h1 style='text-align: center; font-size: 2.5rem;'>{current['title']}</h1>", unsafe_allow_html=True)
    
    # Texto centrado y con estilo en un contenedor con color de fondo según el tema
    color_bg = f"rgba({','.join(['0', '0', '255', '0.1'])});" if current['color'] == 'blue' else \
               f"rgba({','.join(['255', '165', '0', '0.1'])});" if current['color'] == 'orange' else \
               f"rgba({','.join(['255', '0', '0', '0.1'])});" if current['color'] == 'red' else \
               f"rgba({','.join(['0', '128', '0', '0.1'])});" if current['color'] == 'green' else \
               "rgba(0,0,0,0.05);"
    
    st.markdown(f"""
    <div style='text-align: center; margin: 40px 0; padding: 30px; border-radius: 15px; background-color: {color_bg}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h2 style='font-size: 1.8rem;'>{current["text"]}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar el número de página actual
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 20px;'>
        {current_page + 1} de {len(intro_content)}
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de navegación
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if current_page == len(intro_content) - 1:
            if st.button("Comenzar aplicación", type="primary", use_container_width=True):
                st.session_state.intro_page += 1
                st.rerun()
        else:
            if st.button("Siguiente", type="primary", use_container_width=True):
                st.session_state.intro_page += 1
                st.rerun()

# Pantalla de registro
elif st.session_state.step == 'register':
    st.title("💧 Registro en H2Omiga")
    
    with st.form("registro_usuario"):
        name = st.text_input("Nombre")
        
        # Lista de ciudades de Perú
        cities = [
            "Lima", "Arequipa", "Trujillo", "Chiclayo", "Piura", 
            "Iquitos", "Cusco", "Huancayo", "Tacna", "Pucallpa",
            "Chimbote", "Juliaca", "Ica", "Cajamarca", "Sullana",
            "Ayacucho", "Huánuco", "Puno", "Tarapoto", "Tumbes"
        ]
        
        city = st.selectbox("Ciudad", cities)
        
        submitted = st.form_submit_button("Registrarme")
        
        if submitted:
            if name:
                st.session_state.user = create_or_update_user(name, city)
                st.session_state.step = 'welcome'
                st.rerun()
            else:
                st.error("Por favor, ingresa tu nombre para continuar.")

# Pantalla de bienvenida
elif st.session_state.step == 'welcome':
    user_data = load_user_data()[st.session_state.user]
    
    st.title(f"Bienvenido/a a H2Omiga, {st.session_state.user}!")
    st.write(f"Tu ciudad: {user_data['city']}")
    
    st.markdown("""
    ### ¿Qué puedes hacer en H2Omiga?
    
    * 📝 Registrar tu consumo diario de agua
    * 📊 Visualizar tu consumo semanal
    * 🚨 Recibir alertas cuando superes el límite recomendado
    * 💡 Obtener consejos personalizados para ahorrar agua
    * 💰 Calcular tu ahorro potencial
    
    ¡Comencemos a cuidar juntos este recurso vital!
    """)
    
    if st.button("Continuar a mi panel", type="primary"):
        st.session_state.step = 'dashboard'
        st.rerun()

# Panel principal
elif st.session_state.step == 'dashboard':
    st.title(f"💧 H2Omiga - Panel de {st.session_state.user}")
    
    # Crear pestañas
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📝 Registrar consumo", 
        "📊 Visualizar datos",
        "🔍 Comparativa",
        "👣 Huella hídrica",
        "🎯 Desafíos",
        "🧠 Quiz del agua",
        "🛠️ Herramientas"
    ])
    
    with tab1:
        st.header("Registra tu consumo de agua diario")
        
        st.write("Selecciona las actividades que has realizado hoy y la cantidad de veces:")
        
        with st.form("registro_consumo"):
            activities_input = {}
            
            # Dividir actividades en columnas
            col1, col2 = st.columns(2)
            
            items = list(water_activities.items())
            half = len(items) // 2
            
            with col1:
                for activity, details in items[:half]:
                    activities_input[activity] = st.number_input(
                        f"{details['name']} ({details['liters']} litros por uso)",
                        min_value=0,
                        step=1,
                        value=0
                    )
            
            with col2:
                for activity, details in items[half:]:
                    activities_input[activity] = st.number_input(
                        f"{details['name']} ({details['liters']} litros por uso)",
                        min_value=0,
                        step=1,
                        value=0
                    )
            
            submitted = st.form_submit_button("Registrar consumo")
            
            if submitted:
                if sum(activities_input.values()) > 0:
                    total = register_consumption(st.session_state.user, activities_input)
                    
                    st.success(f"¡Consumo registrado! Total: {total:.1f} litros")
                    
                    if total > 100:
                        st.warning("⚠️ **¡Alerta!** Has superado el límite recomendado de 100 litros diarios.")
                    
                    # Mostrar consejo después del registro
                    show_tips(st.session_state.user, total)
                    
                    # Recargar gráficos
                    st.rerun()
                else:
                    st.warning("Debes seleccionar al menos una actividad para registrar.")
    
    with tab2:
        st.header("Visualización de tu consumo de agua")
        
        # Mostrar gráfico semanal
        show_weekly_chart(st.session_state.user)
        
        # Mostrar estadísticas
        weekly_consumption = get_weekly_consumption(st.session_state.user)
        total_weekly = sum(weekly_consumption.values())
        daily_avg = total_weekly / 7 if weekly_consumption else 0
        
        # Obtener la ciudad del usuario para calcular costos
        user_data = load_user_data()
        city = user_data[st.session_state.user].get("city", "Lima")
        water_rate = water_rates.get(city, DEFAULT_WATER_RATE)
        
        # Calcular costo del agua semanal
        weekly_cost = (total_weekly / 1000) * water_rate
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Consumo semanal", f"{total_weekly:.1f} litros")
        
        with col2:
            st.metric("Promedio diario", f"{daily_avg:.1f} litros")
        
        with col3:
            # Días sobre el límite
            days_over_limit = sum(1 for value in weekly_consumption.values() if value > 100)
            st.metric("Días sobre el límite", f"{days_over_limit} de 7")
        
        # Mostrar costo en soles
        st.subheader("Costo del consumo de agua")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Costo semanal", f"S/ {weekly_cost:.2f}")
        
        with col2:
            st.metric("Costo mensual estimado", f"S/ {(weekly_cost * 4):.2f}")
        
        with col3:
            st.metric("Tarifa aplicada", f"S/ {water_rate:.2f} por m³")
        
        # Si hay datos de hoy, mostrar consejos
        today = datetime.now().strftime("%Y-%m-%d")
        user_data = load_user_data()
        
        if today in user_data.get(st.session_state.user, {}).get("consumption", {}):
            today_activities = user_data[st.session_state.user]["consumption"][today]
            today_total = sum(water_activities[activity]["liters"] * quantity 
                              for activity, quantity in today_activities.items())
            
            st.subheader("Consejos para ahorrar agua")
            show_tips(st.session_state.user, today_total)
            
    # Tab 3: Comparativa
    with tab3:
        st.header("Comparativa de consumo de agua")
        
        user_data = load_user_data()
        city = user_data[st.session_state.user].get("city", "Lima")
        
        # Cálculo de consumo promedio del usuario
        weekly_consumption = get_weekly_consumption(st.session_state.user)
        daily_avg = sum(weekly_consumption.values()) / 7 if weekly_consumption else 0
        
        # Consumo promedio de la ciudad
        city_avg = city_avg_consumption.get(city, NATIONAL_AVG_CONSUMPTION)
        
        # Comparación nacional
        st.subheader("Tu consumo comparado con el promedio")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            
            # Añadir barras
            fig.add_trace(go.Bar(
                x=['Tu consumo', f'Promedio en {city}', 'Promedio nacional'],
                y=[daily_avg, city_avg, NATIONAL_AVG_CONSUMPTION],
                marker_color=['#1E88E5', '#FFA726', '#66BB6A']
            ))
            
            # Añadir línea de límite recomendado
            fig.add_shape(
                type="line",
                x0=-0.5,
                y0=100,
                x1=2.5,
                y1=100,
                line=dict(
                    color="Red",
                    width=2,
                    dash="dash",
                ),
                name="Límite recomendado"
            )
            
            fig.add_annotation(
                x=2,
                y=105,
                text="Límite recomendado (100L)",
                showarrow=False,
                font=dict(color="red")
            )
            
            fig.update_layout(
                title="Consumo diario promedio (litros)",
                xaxis_title="",
                yaxis_title="Litros por día",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Calcular porcentajes
            vs_city = (daily_avg / city_avg) * 100 - 100
            vs_national = (daily_avg / NATIONAL_AVG_CONSUMPTION) * 100 - 100
            vs_recommended = (daily_avg / 100) * 100 - 100
            
            st.markdown(f"""
            ### Tu posición relativa
            
            #### Respecto a tu ciudad ({city}):
            """)
            
            if vs_city > 0:
                st.error(f"⚠️ **Consumes {abs(vs_city):.1f}% más** que el promedio de habitantes en {city}.")
            elif vs_city < 0:
                st.success(f"✅ **Consumes {abs(vs_city):.1f}% menos** que el promedio de habitantes en {city}.")
            else:
                st.info(f"📊 Tu consumo es igual al promedio de habitantes en {city}.")
            
            st.markdown("#### Respecto al promedio nacional:")
            
            if vs_national > 0:
                st.error(f"⚠️ **Consumes {abs(vs_national):.1f}% más** que el promedio nacional.")
            elif vs_national < 0:
                st.success(f"✅ **Consumes {abs(vs_national):.1f}% menos** que el promedio nacional.")
            else:
                st.info(f"📊 Tu consumo es igual al promedio nacional.")
            
            st.markdown("#### Respecto al límite recomendado (100L):")
            
            if vs_recommended > 0:
                st.error(f"⚠️ **Consumes {abs(vs_recommended):.1f}% más** que el límite recomendado.")
            elif vs_recommended < 0:
                st.success(f"✅ **Consumes {abs(vs_recommended):.1f}% menos** que el límite recomendado.")
            else:
                st.info(f"📊 Tu consumo es igual al límite recomendado.")
        
        # Ranking por ciudades
        st.subheader("Ranking de consumo por ciudades")
        
        cities_ranking = sorted(city_avg_consumption.items(), key=lambda x: x[1])
        
        df_ranking = pd.DataFrame(cities_ranking, columns=['Ciudad', 'Consumo diario (litros)'])
        
        # Resaltar la ciudad del usuario
        def highlight_city(row):
            if row.Ciudad == city:
                return ['background-color: rgba(30, 136, 229, 0.2)'] * len(row)
            return [''] * len(row)
        
        st.dataframe(
            df_ranking.style.apply(highlight_city, axis=1),
            use_container_width=True,
            height=400
        )
        
        st.info(f"💡 **Dato interesante:** Lima es la segunda ciudad más grande del mundo ubicada en un desierto, después de El Cairo. Por eso, la conservación del agua es especialmente crucial.")
    
    # Tab 4: Huella Hídrica
    with tab4:
        st.header("Calculadora de Huella Hídrica")
        
        st.markdown("""
        La huella hídrica representa la cantidad total de agua dulce utilizada para producir los bienes y servicios que consumimos.
        Incluye el agua consumida directamente (ducha, cocina, etc.) y el "agua virtual" usada para producir alimentos, productos y energía.
        """)
        
        st.subheader("Calculadora de huella hídrica de alimentos")
        
        st.write("Selecciona las cantidades aproximadas de alimentos que consumes en una semana:")
        
        # Crear tabs para categorías de alimentos
        food_cat1, food_cat2, food_cat3, food_cat4 = st.tabs([
            "Carnes y lácteos", "Granos y vegetales", "Frutas", "Bebidas y otros"
        ])
        
        food_inputs = {}
        
        with food_cat1:
            col1, col2 = st.columns(2)
            with col1:
                food_inputs["carne_res"] = st.number_input(
                    f"Carne de res (kg/semana)", 
                    min_value=0.0, 
                    value=0.5, 
                    step=0.1,
                    format="%.1f"
                )
                food_inputs["carne_pollo"] = st.number_input(
                    f"Carne de pollo (kg/semana)", 
                    min_value=0.0, 
                    value=1.0, 
                    step=0.1,
                    format="%.1f"
                )
                food_inputs["carne_cerdo"] = st.number_input(
                    f"Carne de cerdo (kg/semana)", 
                    min_value=0.0, 
                    value=0.3, 
                    step=0.1,
                    format="%.1f"
                )
            with col2:
                food_inputs["leche"] = st.number_input(
                    f"Leche (litros/semana)", 
                    min_value=0.0, 
                    value=2.0, 
                    step=0.5,
                    format="%.1f"
                )
                food_inputs["queso"] = st.number_input(
                    f"Queso (kg/semana)", 
                    min_value=0.0, 
                    value=0.2, 
                    step=0.1,
                    format="%.1f"
                )
                food_inputs["huevos"] = st.number_input(
                    f"Huevos (kg/semana - approx 1kg = 16 huevos)", 
                    min_value=0.0, 
                    value=0.5, 
                    step=0.1,
                    format="%.1f"
                )
        
        with food_cat2:
            col1, col2 = st.columns(2)
            with col1:
                food_inputs["arroz"] = st.number_input(
                    f"Arroz (kg/semana)", 
                    min_value=0.0, 
                    value=1.0, 
                    step=0.1,
                    format="%.1f"
                )
                food_inputs["papa"] = st.number_input(
                    f"Papa (kg/semana)", 
                    min_value=0.0, 
                    value=1.0, 
                    step=0.5,
                    format="%.1f"
                )
                food_inputs["trigo"] = st.number_input(
                    f"Pan/Trigo (kg/semana)", 
                    min_value=0.0, 
                    value=0.7, 
                    step=0.1,
                    format="%.1f"
                )
            with col2:
                food_inputs["tomate"] = st.number_input(
                    f"Tomate (kg/semana)", 
                    min_value=0.0, 
                    value=0.5, 
                    step=0.1,
                    format="%.1f"
                )
                food_inputs["lechuga"] = st.number_input(
                    f"Lechuga (kg/semana)", 
                    min_value=0.0, 
                    value=0.3, 
                    step=0.1,
                    format="%.1f"
                )
                food_inputs["maiz"] = st.number_input(
                    f"Maíz (kg/semana)", 
                    min_value=0.0, 
                    value=0.3, 
                    step=0.1,
                    format="%.1f"
                )
        
        with food_cat3:
            col1, col2 = st.columns(2)
            with col1:
                food_inputs["manzana"] = st.number_input(
                    f"Manzana (kg/semana)", 
                    min_value=0.0, 
                    value=0.5, 
                    step=0.1,
                    format="%.1f"
                )
                food_inputs["platano"] = st.number_input(
                    f"Plátano/Banana (kg/semana)", 
                    min_value=0.0, 
                    value=0.5, 
                    step=0.1,
                    format="%.1f"
                )
            with col2:
                # Espacio para futuras frutas
                pass
        
        with food_cat4:
            col1, col2 = st.columns(2)
            with col1:
                food_inputs["cafe"] = st.number_input(
                    f"Café (kg/semana, ~60g = 10 tazas)", 
                    min_value=0.0, 
                    value=0.1, 
                    step=0.05,
                    format="%.2f"
                )
                food_inputs["chocolate"] = st.number_input(
                    f"Chocolate (kg/semana)", 
                    min_value=0.0, 
                    value=0.1, 
                    step=0.05,
                    format="%.2f"
                )
                food_inputs["azucar"] = st.number_input(
                    f"Azúcar (kg/semana)", 
                    min_value=0.0, 
                    value=0.3, 
                    step=0.1,
                    format="%.1f"
                )
            with col2:
                food_inputs["aceite_oliva"] = st.number_input(
                    f"Aceite de oliva (litros/semana)", 
                    min_value=0.0, 
                    value=0.1, 
                    step=0.05,
                    format="%.2f"
                )
                food_inputs["cerveza"] = st.number_input(
                    f"Cerveza (litros/semana)", 
                    min_value=0.0, 
                    value=0.5, 
                    step=0.5,
                    format="%.1f"
                )
                food_inputs["vino"] = st.number_input(
                    f"Vino (litros/semana)", 
                    min_value=0.0, 
                    value=0.2, 
                    step=0.1,
                    format="%.1f"
                )
        
        # Calcular huella hídrica de alimentos
        total_food_footprint = 0
        footprint_by_category = {
            "Carnes": 0,
            "Lácteos y huevos": 0,
            "Cereales": 0,
            "Vegetales": 0,
            "Frutas": 0,
            "Bebidas": 0,
            "Otros": 0
        }
        
        for food_key, amount in food_inputs.items():
            if food_key in food_water_footprint:
                food_fp = amount * food_water_footprint[food_key]["water_footprint"]
                total_food_footprint += food_fp
                
                # Categorizar para el gráfico
                if food_key in ["carne_res", "carne_pollo", "carne_cerdo"]:
                    footprint_by_category["Carnes"] += food_fp
                elif food_key in ["leche", "queso", "huevos"]:
                    footprint_by_category["Lácteos y huevos"] += food_fp
                elif food_key in ["arroz", "trigo", "maiz"]:
                    footprint_by_category["Cereales"] += food_fp
                elif food_key in ["papa", "tomate", "lechuga"]:
                    footprint_by_category["Vegetales"] += food_fp
                elif food_key in ["manzana", "platano"]:
                    footprint_by_category["Frutas"] += food_fp
                elif food_key in ["cafe", "cerveza", "vino"]:
                    footprint_by_category["Bebidas"] += food_fp
                else:
                    footprint_by_category["Otros"] += food_fp
        
        # Calcular promedios diarios
        daily_food_footprint = total_food_footprint / 7
        
        st.subheader("Huella hídrica de productos de consumo")
        st.write("Indica la cantidad de productos que adquieres al mes:")
        
        product_inputs = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            product_inputs["camiseta_algodon"] = st.number_input(
                f"Camisetas de algodón (unidades/mes)", 
                min_value=0.0, 
                value=0.5, 
                step=0.5,
                format="%.1f"
            )
            product_inputs["jeans"] = st.number_input(
                f"Jeans/pantalones (unidades/mes)", 
                min_value=0.0, 
                value=0.2, 
                step=0.1,
                format="%.1f"
            )
            product_inputs["zapatos_cuero"] = st.number_input(
                f"Zapatos de cuero (pares/mes)", 
                min_value=0.0, 
                value=0.1, 
                step=0.1,
                format="%.1f"
            )
            
        with col2:
            product_inputs["papel"] = st.number_input(
                f"Papel (hojas/día)", 
                min_value=0.0, 
                value=5.0, 
                step=1.0,
                format="%.0f"
            )
            product_inputs["smartphone"] = st.number_input(
                f"Smartphone (unidades/año)", 
                min_value=0.0, 
                value=0.5, 
                step=0.5,
                format="%.1f"
            )
            product_inputs["computadora"] = st.number_input(
                f"Computadora/Laptop (unidades/año)", 
                min_value=0.0, 
                value=0.3, 
                step=0.1,
                format="%.1f"
            )
        
        # Calcular huella hídrica de productos
        total_product_footprint = 0
        
        for product_key, amount in product_inputs.items():
            if product_key in product_water_footprint:
                # Ajustar a base diaria
                if product_key in ["camiseta_algodon", "jeans", "zapatos_cuero"]:
                    # Productos mensuales a diarios
                    daily_amount = amount / 30
                elif product_key in ["smartphone", "computadora"]:
                    # Productos anuales a diarios
                    daily_amount = amount / 365
                else:
                    # Productos que ya están en base diaria
                    daily_amount = amount
                
                # Acumular huella hídrica
                product_fp = daily_amount * product_water_footprint[product_key]["water_footprint"]
                total_product_footprint += product_fp
        
        # Mostrar resultados de huella hídrica
        st.subheader("Resultados de tu huella hídrica")
        
        # Obtener consumo directo de agua (según datos registrados)
        weekly_consumption = get_weekly_consumption(st.session_state.user)
        direct_water_use = sum(weekly_consumption.values()) / 7 if weekly_consumption else NATIONAL_AVG_CONSUMPTION
        
        # Calcular huella hídrica total
        total_water_footprint = direct_water_use + daily_food_footprint + total_product_footprint
        
        # Mostrar resultados
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Huella hídrica total", f"{total_water_footprint:.0f} litros/día")
            
            fig = go.Figure()
            
            # Preparar datos para el gráfico de pie
            labels = ["Uso directo", "Alimentos", "Productos"]
            values = [direct_water_use, daily_food_footprint, total_product_footprint]
            colors = ["#1E88E5", "#FFA726", "#66BB6A"]
            
            fig.add_trace(go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                textinfo="percent+label",
                hole=0.3,
            ))
            
            fig.update_layout(
                title="Distribución de tu huella hídrica diaria",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Mostrar desglose por categorías
            st.subheader("Detalle de tu huella hídrica")
            
            st.write(f"**Uso directo de agua:** {direct_water_use:.0f} litros/día")
            st.write(f"**Huella hídrica de alimentos:** {daily_food_footprint:.0f} litros/día")
            st.write(f"**Huella hídrica de productos:** {total_product_footprint:.0f} litros/día")
            
            # Mostrar gráfico de barras por categorías de alimentos
            fig = go.Figure()
            
            categories = list(footprint_by_category.keys())
            values = list(footprint_by_category.values())
            
            # Dividir por 7 para obtener valores diarios
            daily_values = [v/7 for v in values]
            
            fig.add_trace(go.Bar(
                x=categories,
                y=daily_values,
                marker_color="#FFA726"
            ))
            
            fig.update_layout(
                title="Huella hídrica diaria por categoría de alimentos (litros/día)",
                xaxis_title="",
                yaxis_title="Litros por día",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Consejos para reducir la huella hídrica
        st.subheader("Consejos para reducir tu huella hídrica")
        
        # Identificar las categorías de mayor consumo
        if footprint_by_category["Carnes"] > daily_food_footprint * 0.3:
            st.info("💡 **Reduce el consumo de carne**: La producción de carne, especialmente de res, requiere enormes cantidades de agua. Intenta tener un día a la semana sin carne.")
        
        if daily_food_footprint > total_product_footprint * 2:
            st.info("💡 **Evita el desperdicio de alimentos**: Aproximadamente un tercio de los alimentos producidos se desperdician. Planifica tus comidas y compras para evitar tirar comida.")
        
        if total_product_footprint > 100:
            st.info("💡 **Extiende la vida útil de tus productos**: Reparar y mantener tus dispositivos electrónicos, ropa y calzado en lugar de reemplazarlos reduce significativamente tu huella hídrica.")
            
        st.info("💡 **Consume local y de temporada**: Los alimentos locales y de temporada generalmente requieren menos agua para su producción y transporte.")
            
    # Tab 5: Desafíos
    with tab5:
        st.header("Desafíos para ahorrar agua")
        
        st.markdown("""
        ¡Demuestra tu compromiso con la conservación del agua aceptando estos desafíos!
        Cada desafío te ayudará a reducir tu consumo de agua y desarrollar hábitos más sostenibles.
        """)
        
        # Inicializar estado para los desafíos en la sesión
        if 'active_challenges' not in st.session_state:
            st.session_state.active_challenges = []
        
        if 'completed_challenges' not in st.session_state:
            st.session_state.completed_challenges = []
        
        # Espacio para desafíos activos
        if st.session_state.active_challenges:
            st.subheader("Tus desafíos activos")
            
            for challenge_id in st.session_state.active_challenges:
                # Encontrar el desafío correspondiente
                challenge = next((c for c in water_challenges if c["id"] == challenge_id), None)
                
                if challenge:
                    with st.expander(f"{challenge['name']} ({challenge['difficulty']})"):
                        st.write(challenge["description"])
                        st.progress(0.5)  # Progreso ficticio por ahora
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"Meta: Ahorrar {challenge['target']} litros")
                            st.write(f"Duración: {challenge['duration']} días")
                        
                        with col2:
                            if st.button("Completado", key=f"complete_{challenge_id}"):
                                st.session_state.active_challenges.remove(challenge_id)
                                st.session_state.completed_challenges.append(challenge_id)
                                st.rerun()
        
        # Mostrar desafíos disponibles
        st.subheader("Desafíos disponibles")
        
        # Filtrar desafíos que no están activos ni completados
        available_challenges = [c for c in water_challenges 
                               if c["id"] not in st.session_state.active_challenges 
                               and c["id"] not in st.session_state.completed_challenges]
        
        # Agrupar por dificultad
        easy_challenges = [c for c in available_challenges if c["difficulty"] == "fácil"]
        medium_challenges = [c for c in available_challenges if c["difficulty"] == "medio"]
        hard_challenges = [c for c in available_challenges if c["difficulty"] == "difícil"]
        extreme_challenges = [c for c in available_challenges if c["difficulty"] == "extremo"]
        
        # Crear tabs para diferentes niveles de dificultad
        if available_challenges:
            diff_tab1, diff_tab2, diff_tab3, diff_tab4 = st.tabs(["Fácil", "Medio", "Difícil", "Extremo"])
            
            with diff_tab1:
                if easy_challenges:
                    for challenge in easy_challenges:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{challenge['name']}**")
                            st.write(challenge["description"])
                            st.write(f"Meta: Ahorrar {challenge['target']} litros en {challenge['duration']} días")
                        with col2:
                            if st.button("Aceptar", key=f"accept_{challenge['id']}"):
                                st.session_state.active_challenges.append(challenge["id"])
                                st.rerun()
                else:
                    st.write("No hay desafíos disponibles de nivel fácil.")
            
            with diff_tab2:
                if medium_challenges:
                    for challenge in medium_challenges:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{challenge['name']}**")
                            st.write(challenge["description"])
                            st.write(f"Meta: Ahorrar {challenge['target']} litros en {challenge['duration']} días")
                        with col2:
                            if st.button("Aceptar", key=f"accept_{challenge['id']}"):
                                st.session_state.active_challenges.append(challenge["id"])
                                st.rerun()
                else:
                    st.write("No hay desafíos disponibles de nivel medio.")
            
            with diff_tab3:
                if hard_challenges:
                    for challenge in hard_challenges:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{challenge['name']}**")
                            st.write(challenge["description"])
                            st.write(f"Meta: Ahorrar {challenge['target']} litros en {challenge['duration']} días")
                        with col2:
                            if st.button("Aceptar", key=f"accept_{challenge['id']}"):
                                st.session_state.active_challenges.append(challenge["id"])
                                st.rerun()
                else:
                    st.write("No hay desafíos disponibles de nivel difícil.")
            
            with diff_tab4:
                if extreme_challenges:
                    for challenge in extreme_challenges:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{challenge['name']}**")
                            st.write(challenge["description"])
                            st.write(f"Meta: Ahorrar {challenge['target']} litros en {challenge['duration']} días")
                        with col2:
                            if st.button("Aceptar", key=f"accept_{challenge['id']}"):
                                st.session_state.active_challenges.append(challenge["id"])
                                st.rerun()
                else:
                    st.write("No hay desafíos disponibles de nivel extremo.")
        else:
            st.info("¡Felicidades! Has aceptado todos los desafíos disponibles.")
        
        # Desafíos completados
        if st.session_state.completed_challenges:
            st.subheader("Desafíos completados")
            
            for challenge_id in st.session_state.completed_challenges:
                challenge = next((c for c in water_challenges if c["id"] == challenge_id), None)
                if challenge:
                    st.success(f"✅ {challenge['name']} - Ahorraste aproximadamente {challenge['target']} litros de agua")
    
    # Tab 6: Quiz del agua
    with tab6:
        st.header("Quiz del agua: ¿Cuánto sabes sobre el agua?")
        
        st.markdown("""
        Pon a prueba tus conocimientos sobre el agua y su conservación.
        Este quiz te ayudará a aprender datos interesantes sobre este recurso vital.
        """)
        
        # Inicializar el estado del quiz en la sesión
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
            
        if 'current_question' not in st.session_state:
            st.session_state.current_question = 0
            
        if 'correct_answers' not in st.session_state:
            st.session_state.correct_answers = 0
            
        if 'quiz_finished' not in st.session_state:
            st.session_state.quiz_finished = False
        
        # Pantalla inicial del quiz
        if not st.session_state.quiz_started and not st.session_state.quiz_finished:
            st.subheader("¿Listo para demostrar tus conocimientos?")
            
            st.write("Este quiz consta de 10 preguntas sobre el agua, su uso y conservación.")
            st.write("Cada respuesta correcta suma un punto. ¿Cuántos puntos puedes conseguir?")
            
            if st.button("Comenzar Quiz", type="primary"):
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.correct_answers = 0
                st.rerun()
        
        # Quiz en progreso
        elif st.session_state.quiz_started and not st.session_state.quiz_finished:
            # Mostrar la pregunta actual
            question_data = water_quiz[st.session_state.current_question]
            
            st.subheader(f"Pregunta {st.session_state.current_question + 1} de {len(water_quiz)}")
            st.markdown(f"### {question_data['question']}")
            
            # Permitir al usuario seleccionar una respuesta
            answer = st.radio("Selecciona tu respuesta:", question_data['options'], key="quiz_answer")
            
            # Botón para confirmar respuesta
            if st.button("Confirmar respuesta"):
                if answer == question_data['correct_answer']:
                    st.success("¡Correcto! 🎉")
                    st.session_state.correct_answers += 1
                else:
                    st.error(f"Incorrecto. La respuesta correcta es: {question_data['correct_answer']}")
                
                st.info(f"**Explicación:** {question_data['explanation']}")
                
                # Progreso
                st.progress((st.session_state.current_question + 1) / len(water_quiz))
                
                # Botón para continuar
                if st.session_state.current_question < len(water_quiz) - 1:
                    if st.button("Siguiente pregunta"):
                        st.session_state.current_question += 1
                        st.rerun()
                else:
                    if st.button("Ver resultados"):
                        st.session_state.quiz_finished = True
                        st.session_state.quiz_started = False
                        st.rerun()
        
        # Quiz finalizado - mostrar resultados
        elif st.session_state.quiz_finished:
            st.subheader("¡Quiz completado!")
            
            # Mostrar puntuación
            st.markdown(f"### Tu puntuación: {st.session_state.correct_answers} de {len(water_quiz)}")
            
            # Interpretar la puntuación
            if st.session_state.correct_answers >= 8:
                st.success("¡Excelente! 🌊 Eres un experto en el tema del agua.")
            elif st.session_state.correct_answers >= 6:
                st.info("¡Buen trabajo! 💧 Tienes buenos conocimientos sobre el agua.")
            elif st.session_state.correct_answers >= 4:
                st.warning("No está mal. 🚿 Aún puedes aprender más sobre el agua.")
            else:
                st.error("Aún hay espacio para mejorar. 🌱 Sigue aprendiendo sobre este recurso vital.")
            
            # Botón para reiniciar el quiz
            if st.button("Reiniciar Quiz"):
                st.session_state.quiz_finished = False
                st.rerun()
    
    # Tab 7: Herramientas
    with tab7:
        st.header("Herramientas adicionales")
        
        # Subtabs para diferentes herramientas
        tool_tab1, tool_tab2, tool_tab3 = st.tabs([
            "Exportar datos", 
            "Convertidor de unidades", 
            "Fuentes de agua"
        ])
        
        with tool_tab1:
            st.subheader("Exportar tus datos de consumo")
            
            # Obtener datos del usuario
            user_data = load_user_data()
            if st.session_state.user in user_data:
                consumption_data = user_data[st.session_state.user].get("consumption", {})
                
                if consumption_data:
                    # Crear DataFrame para exportar
                    export_data = []
                    
                    for date, activities in consumption_data.items():
                        total_liters = 0
                        
                        for activity, quantity in activities.items():
                            liters = water_activities[activity]["liters"] * quantity
                            total_liters += liters
                            
                            export_data.append({
                                "Fecha": date,
                                "Actividad": water_activities[activity]["name"],
                                "Cantidad": quantity,
                                "Litros": liters
                            })
                    
                    df_export = pd.DataFrame(export_data)
                    
                    # Crear archivo CSV
                    csv_buffer = io.StringIO()
                    df_export.to_csv(csv_buffer, index=False)
                    
                    # Botón de descarga
                    st.download_button(
                        label="Descargar datos (CSV)",
                        data=csv_buffer.getvalue(),
                        file_name=f"h2omiga_datos_{st.session_state.user}.csv",
                        mime="text/csv",
                    )
                    
                    # Vista previa de los datos
                    st.subheader("Vista previa de tus datos")
                    st.dataframe(df_export)
                else:
                    st.info("Aún no tienes datos de consumo registrados.")
        
        with tool_tab2:
            st.subheader("Convertidor de unidades de agua")
            
            col1, col2 = st.columns(2)
            
            with col1:
                quantity = st.number_input("Cantidad", min_value=0.0, value=100.0, step=10.0)
                from_unit = st.selectbox("De:", [
                    "Litros", "Metros cúbicos", "Galones (US)", "Botellas (500ml)", 
                    "Duchas (70L)", "Descargas inodoro (9L)"
                ])
            
            with col2:
                to_unit = st.selectbox("A:", [
                    "Litros", "Metros cúbicos", "Galones (US)", "Botellas (500ml)", 
                    "Duchas (70L)", "Descargas inodoro (9L)"
                ])
                
                # Factores de conversión a litros
                to_liters = {
                    "Litros": 1,
                    "Metros cúbicos": 1000,
                    "Galones (US)": 3.78541,
                    "Botellas (500ml)": 0.5,
                    "Duchas (70L)": 70,
                    "Descargas inodoro (9L)": 9
                }
                
                # Realizar la conversión
                litros = quantity * to_liters[from_unit]
                result = litros / to_liters[to_unit]
                
                st.metric("Resultado", f"{result:.2f} {to_unit}")
                
            # Información adicional sobre equivalencias
            if st.checkbox("Mostrar equivalencias visuales"):
                # Convertir la cantidad a litros para las equivalencias
                liters = quantity * to_liters[from_unit]
                
                impact = calculate_visual_impact(liters)
                
                st.subheader("Equivalencias visuales")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Botellas de agua (500ml)", f"{impact['bottles']}")
                    st.metric("Duchas típicas", f"{impact['showers']}")
                
                with col2:
                    st.metric("Descargas de inodoro", f"{impact['toilets']}")
                    st.metric("Riego de plantas", f"{impact['plants']}")
                
                with col3:
                    st.metric("% de piscina estándar", f"{impact['swimming_pools']*100:.4f}%")
                    st.metric("Consumo diario (personas)", f"{impact['days_for_person']:.1f}")
        
        with tool_tab3:
            st.subheader("Fuentes de agua accesibles")
            
            # Obtener la ciudad del usuario
            user_data = load_user_data()
            city = user_data[st.session_state.user].get("city", "Lima")
            
            st.write(f"Fuentes de agua gratuitas o económicas en {city}:")
            
            if city in water_sources:
                for source in water_sources[city]:
                    with st.expander(f"{source['name']} ({source['type']})"):
                        st.write(f"**Dirección:** {source['address']}")
                        st.write(f"**Tipo:** {source['type']}")
            else:
                st.info(f"Actualmente no tenemos información sobre fuentes de agua en {city}. Estamos trabajando para añadir más ciudades.")
                
                # Mostrar algunas fuentes generales
                st.write("Sin embargo, puedes considerar estas opciones generales:")
                st.write("1. **Oficinas municipales de agua**: Suelen ofrecer agua a bajo costo.")
                st.write("2. **Piletas públicas**: En plazas y parques principales.")
                st.write("3. **Comunícate con tu empresa de agua local**: Pueden tener programas especiales.")

# Botón para cerrar sesión
if st.session_state.step not in ['intro', 'register']:
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.step = 'intro'
        st.session_state.user = None
        st.rerun()
