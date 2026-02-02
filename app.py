import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Panteón Pokémon: Hoenn Admin", layout="wide")
st.title("🏆 Dashboard de Entrenadores: Rubí Omega")

# --- LEVEL CAPS ---
LEVEL_CAPS = {
    "1. Petra (Roca)": 16, "2. Marcial (Lucha)": 19, "3. Eriko (Eléctrico)": 25,
    "4. Candela (Fuego)": 33, "5. Norman (Normal)": 35, "6. Alana (Volador)": 40,
    "7. Vito y Leti (Psíquico)": 52, "8. Plubio (Agua)": 55, "Liga Pokémon / Máximo": 65
}

# --- CARGAR DATOS ---
try:
    df = pd.read_csv("partida_pokemon.csv")
except:
    df = pd.DataFrame(columns=["Primo", "Pokemon", "Nivel", "Estado", "Shiny"])
    df.to_csv("partida_pokemon.csv", index=False)

if "Shiny" not in df.columns:
    df["Shiny"] = "No"

# --- SIDEBAR (IDENTIFICACIÓN Y ADMIN) ---
with st.sidebar:
    st.header("👤 ¿Quién eres hoy?")
    # Agregamos Yahir (Admin) a la lista
    usuario_actual = st.selectbox("Identifícate:", ["Invitado", "Yahir (Admin)", "Yahir", "Carlos", "Pepe", "Angel"])
    
    es_admin = (usuario_actual == "Yahir (Admin)")
    
    st.divider()
    st.header("🎮 Progreso")
    fase_actual = st.selectbox("Siguiente Medalla:", list(LEVEL_CAPS.keys()))
    limite_actual = LEVEL_CAPS[fase_actual]
    st.info(f"Nivel máximo: **{limite_actual}**")
    
    if es_admin:
        st.warning("⚡ MODO ADMINISTRADOR ACTIVO")
        if st.button("⚠️ BORRAR TODA LA BASE DE DATOS"):
            df_vacio = pd.DataFrame(columns=["Primo", "Pokemon", "Nivel", "Estado", "Shiny"])
            df_vacio.to_csv("partida_pokemon.csv", index=False)
            st.rerun()

    st.divider()
    st.header("📝 Registrar Pokémon")
    with st.form("nuevo_pokemon"):
        # Si eres admin, puedes elegir a nombre de quién registrar
        propietario = st.selectbox("Registrar para:", ["Yahir", "Carlos", "Pepe", "Angel"]) if es_admin else usuario_actual
        nombre_pkmn = st.text_input("Nombre del Pokémon").lower().strip()
        nivel_pkmn = st.number_input("Nivel", min_value=1, max_value=limite_actual, value=5)
        es_shiny = st.checkbox("¿Es Shiny? ✨")
        botón = st.form_submit_button("¡Registrar!")
        
        if botón and nombre_pkmn:
            if usuario_actual == "Invitado":
                st.error("Identifícate primero.")
            else:
                s_val = "Sí" if es_shiny else "No"
                nuevo = pd.DataFrame([[propietario, nombre_pkmn, nivel_pkmn, "Vivo", s_val]], columns=df.columns)
                df = pd.concat([df, nuevo], ignore_index=True)
                df.to_csv("partida_pokemon.csv", index=False)
                st.success(f"{nombre_pkmn} registrado.")
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
                    st.write(f"Lvl: {row['Nivel']}")

                # BOTONES: Aparecen si eres el dueño O si eres Yahir (Admin)
                if usuario_actual == p or (es_admin and usuario_actual != "Invitado"):
                    b1, b2, b3, b4 = st.columns(4)
                    with b1:
                        if st.button("🆙", key=f"up_{index}"):
                            df.at[index, 'Nivel'] += 1
                            df.to_csv("partida_pokemon.csv", index=False)
                            st.rerun()
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
                    with b4:
                        # Botón especial para borrar solo este Pokémon por error de dedo
                        if st.button("❌", key=f"del_{index}", help="Borrar por error"):
                            df = df.drop(index)
                            df.to_csv("partida_pokemon.csv", index=False)
                            st.rerun()

# --- CEMENTERIO ---
st.divider()
st.subheader("🪦 El Cementerio")
muertos = df[df['Estado'] == 'Muerto']
if not muertos.empty:
    m_cols = st.columns(6)
    for idx, (orig_idx, row) in enumerate(muertos.iterrows()):
        with m_cols[idx % 6]:
            st.image(f"https://img.pokemondb.net/sprites/omega-ruby-alpha-sapphire/dex/normal/{row['Pokemon']}.png", width=60)
            st.write(f"~~{row['Pokemon'].capitalize()}~~")
            if es_admin:
                if st.button("Revivir", key=f"rev_{orig_idx}"):
                    df.at[orig_idx, 'Estado'] = 'Vivo'
                    df.to_csv("partida_pokemon.csv", index=False)
                    st.rerun()