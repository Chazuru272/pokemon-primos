import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Panteón Pokémon de los Primos", layout="wide")
st.title("🏆 Dashboard de Entrenadores Alola")

# --- EL CEREBRO (Base de datos local) ---
# Creamos un archivo para guardar los datos si no existe
try:
    df = pd.read_csv("partida_pokemon.csv")
except:
    # Si es la primera vez, creamos la libreta vacía
    df = pd.DataFrame(columns=["Primo", "Pokemon", "Nivel", "Estado"])
    df.to_csv("partida_pokemon.csv", index=False)

# --- FORMULARIO PARA AGREGAR POKÉMON ---
# Esto es como el "buzón" donde tus primos meten sus datos
with st.sidebar:
    st.header("📝 Registrar Nuevo Pokémon")
    with st.form("nuevo_pokemon"):
        nombre_primo = st.selectbox("¿Quién eres?", ["Tú", "Primo 1", "Primo 2", "Primo 3"])
        nombre_pkmn = st.text_input("Nombre del Pokémon (Ej: Pikachu)").lower().strip()
        nivel_pkmn = st.number_input("Nivel", min_value=1, max_value=100, value=5)
        estado_pkmn = st.radio("Estado", ["Vivo", "Muerto"])
        
        botón = st.form_submit_button("¡Registrar en la Web!")
        
        if botón:
            # Aquí Python escribe en la libreta
            nuevo_dato = pd.DataFrame([[nombre_primo, nombre_pkmn, nivel_pkmn, estado_pkmn]], 
                                     columns=["Primo", "Pokemon", "Nivel", "Estado"])
            df = pd.concat([df, nuevo_dato], ignore_index=True)
            df.to_csv("partida_pokemon.csv", index=False)
            st.success(f"¡{nombre_pkmn} registrado con éxito!")

# --- MOSTRAR LOS EQUIPOS ---
st.subheader("👥 Equipos Actuales")
primos_lista = ["Tú", "Primo 1", "Primo 2", "Primo 3"]
cols = st.columns(len(primos_lista))

for i, p in enumerate(primos_lista):
    with cols[i]:
        st.markdown(f"### 🚩 {p}")
        # Buscamos solo los que están vivos para el equipo actual
        equipo = df[(df['Primo'] == p) & (df['Estado'] == 'Vivo')]
        
        if equipo.empty:
            st.write("No hay Pokémon vivos aún...")
        
        for index, row in equipo.iterrows():
            # URL de la imagen (la estampa del álbum)
            url = f"https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/{row['Pokemon']}.png"
            st.image(url, width=80)
            st.write(f"**{row['Pokemon'].capitalize()}** - Lvl {row['Nivel']}")
            st.divider()

# --- EL CEMENTERIO (Los caídos) ---
st.markdown("---")
st.subheader("🪦 El Cementerio (Caídos en combate)")
muertos = df[df['Estado'] == 'Muerto']
if not muertos.empty:
    filas_muertos = st.columns(5)
    for idx, row in muertos.iterrows():
        with filas_muertos[idx % 5]:
            url = f"https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/{row['Pokemon']}.png"
            # Ponemos la imagen un poco más pequeña y el nombre tachado
            st.image(url, width=60)
            st.write(f"~~{row['Pokemon'].capitalize()}~~")
            st.caption(f"De: {row['Primo']}")