import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Panteón Pokémon: Hoenn Admin", layout="wide")
st.title("🏆 Dashboard de Entrenadores: Rubí Omega")

# --- LEVEL CAPS ---
LEVEL_CAPS = {
    "1. Petra (Roca)": 17, "2. Marcial (Lucha)": 20, "3. Eriko (Eléctrico)": 25,
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

# --- SIDEBAR (IDENTIFICACIÓN Y SEGURIDAD) ---
with st.sidebar:
    st.header("👤 ¿Quién eres hoy?")
    usuario_actual = st.selectbox("Identifícate:", ["Invitado", "Carlos (Admin)", "Yahir", "Carlos", "Pepe", "Angel"])
    
    es_admin = False
    
    # Si elige ser Admin, le pedimos la palabra secreta
    if usuario_actual == "Carlos (Admin)":
        password = st.text_input("Introduce la palabra secreta:", type="password")
        if password == "1234": # <--- CAMBIA "1234" POR TU CONTRASEÑA
            es_admin = True
            st.success("Acceso de Administrador concedido")
        else:
            if password != "":
                st.error("Contraseña incorrecta")
    
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
                    
# --- CALCULADORA DE TIPOS ---
st.markdown("---")
st.header("🧮 Calculadora de Debilidades")

# Definimos la tabla de tipos (Atacante -> Defensor)
tablas_tipos = {
    "Normal": {"Roca": 0.5, "Fantasma": 0, "Acero": 0.5},
    "Fuego": {"Fuego": 0.5, "Agua": 0.5, "Planta": 2, "Hielo": 2, "Bicho": 2, "Roca": 0.5, "Dragón": 0.5, "Acero": 2},
    "Agua": {"Fuego": 2, "Agua": 0.5, "Planta": 0.5, "Tierra": 2, "Roca": 2, "Dragón": 0.5},
    "Planta": {"Fuego": 0.5, "Agua": 2, "Planta": 0.5, "Veneno": 0.5, "Tierra": 2, "Volador": 0.5, "Bicho": 0.5, "Roca": 2, "Dragón": 0.5, "Acero": 0.5},
    "Eléctrico": {"Agua": 2, "Planta": 0.5, "Eléctrico": 0.5, "Tierra": 0, "Volador": 2, "Dragón": 0.5},
    "Hielo": {"Fuego": 0.5, "Agua": 0.5, "Planta": 2, "Hielo": 0.5, "Tierra": 2, "Volador": 2, "Dragón": 2, "Acero": 0.5},
    "Lucha": {"Normal": 2, "Hielo": 2, "Veneno": 0.5, "Volador": 0.5, "Psíquico": 0.5, "Bicho": 0.5, "Roca": 2, "Fantasma": 0, "Oscuro": 2, "Acero": 2, "Hada": 0.5},
    "Veneno": {"Planta": 2, "Veneno": 0.5, "Tierra": 0.5, "Roca": 0.5, "Fantasma": 0.5, "Acero": 0, "Hada": 2},
    "Tierra": {"Fuego": 2, "Planta": 0.5, "Eléctrico": 2, "Veneno": 2, "Volador": 0, "Bicho": 0.5, "Acero": 2},
    "Volador": {"Planta": 2, "Eléctrico": 0.5, "Lucha": 2, "Bicho": 2, "Roca": 0.5, "Acero": 0.5},
    "Psíquico": {"Lucha": 2, "Veneno": 2, "Psíquico": 0.5, "Oscuro": 0, "Acero": 0.5},
    "Bicho": {"Fuego": 0.5, "Planta": 2, "Lucha": 0.5, "Veneno": 0.5, "Volador": 0.5, "Psíquico": 2, "Fantasma": 0.5, "Oscuro": 2, "Acero": 0.5, "Hada": 0.5},
    "Roca": {"Fuego": 2, "Hielo": 2, "Lucha": 0.5, "Tierra": 0.5, "Volador": 2, "Bicho": 2, "Acero": 0.5},
    "Fantasma": {"Normal": 0, "Psíquico": 2, "Fantasma": 2, "Oscuro": 0.5},
    "Dragón": {"Dragón": 2, "Acero": 0.5, "Hada": 0},
    "Oscuro": {"Lucha": 0.5, "Psíquico": 2, "Fantasma": 2, "Oscuro": 0.5, "Hada": 0.5},
    "Acero": {"Fuego": 0.5, "Agua": 0.5, "Eléctrico": 0.5, "Hielo": 2, "Roca": 2, "Acero": 0.5, "Hada": 2},
    "Hada": {"Fuego": 0.5, "Lucha": 2, "Veneno": 0.5, "Dragón": 2, "Oscuro": 2, "Acero": 0.5}
}

lista_tipos = sorted(list(tablas_tipos.keys()))

c1, c2 = st.columns(2)
with c1:
    t1 = st.selectbox("Tipo 1", lista_tipos)
with c2:
    t2 = st.selectbox("Tipo 2 (Opcional)", ["Ninguno"] + lista_tipos)

# Lógica para calcular multiplicadores
defensas = {tipo: 1.0 for tipo in lista_tipos}

for atacante in lista_tipos:
    # Daño contra el primer tipo
    mod1 = tablas_tipos[atacante].get(t1, 1.0)
    # Daño contra el segundo tipo (si existe)
    mod2 = 1.0
    if t2 != "Ninguno":
        mod2 = tablas_tipos[atacante].get(t2, 1.0)
    
    defensas[atacante] = mod1 * mod2

# Mostrar resultados ordenados
st.write(f"Resultados para: **{t1}**" + (f" / **{t2}**" if t2 != "Ninguno" else ""))

debiles_x4 = [t for t, v in defensas.items() if v == 4]
debiles_x2 = [t for t, v in defensas.items() if v == 2]
resistentes_x05 = [t for t, v in defensas.items() if v == 0.5]
resistentes_x025 = [t for t, v in defensas.items() if v == 0.25]
inmunes = [t for t, v in defensas.items() if v == 0]

# Usamos columnas de colores para que se vea profesional
res_cols = st.columns(3)
with res_cols[0]:
    if debiles_x4: st.error(f"❌ Super Débil (x4): {', '.join(debiles_x4)}")
    if debiles_x2: st.warning(f"⚠️ Débil (x2): {', '.join(debiles_x2)}")
with res_cols[1]:
    if resistentes_x05: st.success(f"🛡️ Resistente (x0.5): {', '.join(resistentes_x05)}")
    if resistentes_x025: st.info(f"💎 Muy Resistente (x0.25): {', '.join(resistentes_x025)}")
with res_cols[2]:
    if inmunes: st.markdown(f"🚫 Inmune (x0): {', '.join(inmunes)}")         