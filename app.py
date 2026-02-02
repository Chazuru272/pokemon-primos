import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Panteón Pokémon: Reto Hoenn", layout="wide")
st.title("🏆 Dashboard de Entrenadores: Rubí Omega")

# --- DEFINICIÓN DE LÍMITES (LEVEL CAPS HOENN) ---
# Ajustados con el 15% de dificultad extra para Rubí Omega
LEVEL_CAPS = {
    "1. Petra (Roca)": 17,
    "2. Marcial (Lucha)": 19,
    "3. Eriko (Eléctrico)": 25,
    "4. Candela (Fuego)": 33,
    "5. Norman (Normal)": 35,
    "6. Alana (Volador)": 40,
    "7. Vito y Leti (Psíquico)": 52,
    "8. Plubio (Agua)": 55,
    "Liga Pokémon / Máximo": 65
}

# --- EL CEREBRO (Cargar Datos) ---
try:
    df = pd.read_csv("partida_pokemon.csv")
except:
    df = pd.DataFrame(columns=["Primo", "Pokemon", "Nivel", "Estado", "Shiny"])
    df.to_csv("partida_pokemon.csv", index=False)

if "Shiny" not in df.columns:
    df["Shiny"] = "No"

# --- CONTROL DE LÍMITES EN EL SIDEBAR ---
with st.sidebar:
    st.header("🎮 Progreso en Hoenn")
    fase_actual = st.selectbox("Siguiente Medalla:", list(LEVEL_CAPS.keys()))
    limite_actual = LEVEL_CAPS[fase_actual]
    st.info(f"Nivel máximo: **{limite_actual}**")
    
    st.divider()
    st.header("📝 Registrar Pokémon")
    with st.form("nuevo_pokemon"):
        nombre_primo = st.selectbox("¿Quién eres?", ["Yahir", "Carlos", "Pepe", "Angel"])
        nombre_pkmn = st.text_input("Nombre del Pokémon").lower().strip()
        nivel_pkmn = st.number_input("Nivel actual", min_value=1, max_value=limite_actual, value=5)
        es_shiny = st.checkbox("¿Es Shiny? ✨")
        botón = st.form_submit_button("¡Registrar!")
        
        if botón and nombre_pkmn:
            shiny_val = "Sí" if es_shiny else "No"
            nuevo_dato = pd.DataFrame([[nombre_primo, nombre_pkmn, nivel_pkmn, "Vivo", shiny_val]], 
                                     columns=["Primo", "Pokemon", "Nivel", "Estado", "Shiny"])
            df = pd.concat([df, nuevo_dato], ignore_index=True)
            df.to_csv("partida_pokemon.csv", index=False)
            st.rerun()

# --- MOSTRAR LOS EQUIPOS ---
st.subheader("👥 Equipos de los Primos")
primos_lista = ["Yahir", "Carlos", "Pepe", "Angel"]
cols = st.columns(len(primos_lista))

for i, p in enumerate(primos_lista):
    with cols[i]:
        st.markdown(f"### 🚩 {p}")
        equipo = df[(df['Primo'] == p) & (df['Estado'] == 'Vivo')]
        
        for index, row in equipo.iterrows():
            with st.container(border=True):
                folder = "shiny" if row['Shiny'] == "Sí" else "normal"
                url = f"https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/{folder}/{row['Pokemon']}.png"
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(url)
                with c2:
                    st.write(f"**{row['Pokemon'].capitalize()}**")
                    if row['Nivel'] >= limite_actual:
                        st.error(f"Lvl: {row['Nivel']} (MAX)")
                    else:
                        st.write(f"Lvl: {row['Nivel']}")

                b1, b2, b3 = st.columns(3)
                with b1:
                    if row['Nivel'] < limite_actual:
                        if st.button("🆙", key=f"up_{index}"):
                            df.at[index, 'Nivel'] += 1
                            df.to_csv("partida_pokemon.csv", index=False)
                            st.rerun()
                    else:
                        st.button("🚫", key=f"max_{index}", disabled=True)
                with b2:
                    if st.button("✨", key=f"sh_{index}"):
                        df.at[index, 'Shiny'] = "Sí"
                        df.to_csv("partida_pokemon.csv", index=False)
                        st.rerun()
                with b3:
                    if st.button("💀", key=f"die_{index}"):
                        df.at[index, 'Estado'] = "Muerto"
                        df.to_csv("partida_pokemon.csv", index=False)
                        st.rerun()

# --- CEMENTERIO ---
st.divider()
st.subheader("🪦 El Cementerio de Hoenn")
muertos = df[df['Estado'] == 'Muerto']
if not muertos.empty:
    m_cols = st.columns(6)
    for idx, (original_idx, row) in enumerate(muertos.iterrows()):
        with m_cols[idx % 6]:
            st.image(f"https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/{row['Pokemon']}.png", width=60)
            st.write(f"~~{row['Pokemon'].capitalize()}~~")
            st.caption(f"De: {row['Primo']}")