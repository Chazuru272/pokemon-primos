import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Panteón Pokémon de los Primos", layout="wide")
st.title("🏆 Dashboard de Entrenadores Alola")

# --- EL CEREBRO (Cargar Datos) ---
try:
    df = pd.read_csv("partida_pokemon.csv")
except:
    # Creamos la libreta con las columnas nuevas (Shiny)
    df = pd.DataFrame(columns=["Primo", "Pokemon", "Nivel", "Estado", "Shiny"])
    df.to_csv("partida_pokemon.csv", index=False)

# Si actualizaste el código pero ya tenías un archivo viejo, esto agrega la columna Shiny
if "Shiny" not in df.columns:
    df["Shiny"] = "No"

# --- REGISTRAR NUEVO POKÉMON (Sidebar) ---
with st.sidebar:
    st.header("📝 Registrar Nuevo Pokémon")
    with st.form("nuevo_pokemon"):
        nombre_primo = st.selectbox("¿Quién eres?", ["Yahir", "Carlos", "Pepe", "Angel"])
        nombre_pkmn = st.text_input("Nombre del Pokémon").lower().strip()
        nivel_pkmn = st.number_input("Nivel inicial", min_value=1, max_value=100, value=5)
        es_shiny = st.checkbox("¿Es Shiny? ✨")
        
        botón = st.form_submit_button("¡Registrar!")
        
        if botón and nombre_pkmn:
            shiny_val = "Sí" if es_shiny else "No"
            nuevo_dato = pd.DataFrame([[nombre_primo, nombre_pkmn, nivel_pkmn, "Vivo", shiny_val]], 
                                     columns=["Primo", "Pokemon", "Nivel", "Estado", "Shiny"])
            df = pd.concat([df, nuevo_dato], ignore_index=True)
            df.to_csv("partida_pokemon.csv", index=False)
            st.success(f"¡{nombre_pkmn} registrado!")
            st.rerun()

# --- MOSTRAR LOS EQUIPOS ---
st.subheader("👥 Equipos Actuales")
primos_lista = ["Yahir", "Carlos", "Pepe", "Angel"]
cols = st.columns(len(primos_lista))

for i, p in enumerate(primos_lista):
    with cols[i]:
        st.markdown(f"### 🚩 {p}")
        equipo = df[(df['Primo'] == p) & (df['Estado'] == 'Vivo')]
        
        if equipo.empty:
            st.write("No hay Pokémon vivos...")
        
        for index, row in equipo.iterrows():
            # CAJITA INTERACTIVA
            with st.container(border=True):
                # Foto: Si es shiny, busca la carpeta shiny, si no, la normal
                folder = "shiny" if row['Shiny'] == "Sí" else "normal"
                url = f"https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/{folder}/{row['Pokemon']}.png"
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(url)
                with c2:
                    st.write(f"**{row['Pokemon'].capitalize()}**")
                    st.write(f"Lvl: {row['Nivel']}")

                # BOTONES DE ACCIÓN (Picarle al Pokémon)
                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button("🆙", key=f"up_{index}", help="Subir nivel"):
                        df.at[index, 'Nivel'] += 1
                        df.to_csv("partida_pokemon.csv", index=False)
                        st.rerun()
                with b2:
                    if st.button("✨", key=f"sh_{index}", help="Volver Shiny"):
                        df.at[index, 'Shiny'] = "Sí"
                        df.to_csv("partida_pokemon.csv", index=False)
                        st.rerun()
                with b3:
                    if st.button("💀", key=f"die_{index}", help="Murió"):
                        df.at[index, 'Estado'] = "Muerto"
                        df.to_csv("partida_pokemon.csv", index=False)
                        st.rerun()

# --- CEMENTERIO ---
st.markdown("---")
st.subheader("🪦 El Cementerio (Caídos en combate)")
muertos = df[df['Estado'] == 'Muerto']
if not muertos.empty:
    filas_muertos = st.columns(6)
    for idx, (original_idx, row) in enumerate(muertos.iterrows()):
        with filas_muertos[idx % 6]:
            url_dead = f"https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/{row['Pokemon']}.png"
            st.image(url_dead, width=60)
            st.write(f"~~{row['Pokemon'].capitalize()}~~")
            st.caption(f"De: {row['Primo']}")

# --- BOTÓN DE LIMPIEZA TOTAL ---
with st.sidebar:
    st.divider()
    if st.button("⚠️ Borrar todo"):
        df_vacio = pd.DataFrame(columns=["Primo", "Pokemon", "Nivel", "Estado", "Shiny"])
        df_vacio.to_csv("partida_pokemon.csv", index=False)
        st.rerun()