import streamlit as st
import pandas as pd

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="War Era Industrial Command",
    page_icon="🏭",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0d1117;
    color: white;
}

.block-container {
    padding-top: 1rem;
}

.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
}

.title {
    font-size: 48px;
    font-weight: 900;
}

.subtitle {
    color: #8b949e;
    font-size: 18px;
}

.green {
    color: #00ff99;
    font-weight: bold;
    font-size: 22px;
}

.red {
    color: #ff5c7a;
    font-weight: bold;
    font-size: 22px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# ITEMS
# =====================================================

ITEMS = {

    "Piedra": {
        "img": "https://app.warera.io/images/items/limestone.png?v=32",
        "buy": 0.078,
        "sell": 0.080,
    },

    "Trigo": {
        "img": "https://app.warera.io/images/items/grain.png?v=32",
        "buy": 0.074,
        "sell": 0.076,
    },

    "Hierro": {
        "img": "https://app.warera.io/images/items/iron.png?v=32",
        "buy": 1.61,
        "sell": 1.62,
    },

    "Plomo": {
        "img": "https://app.warera.io/images/items/lead.png?v=32",
        "buy": 0.68,
        "sell": 0.71,
    },

    "Coca": {
        "img": "https://app.warera.io/images/items/coca.png?v=32",
        "buy": 0.173,
        "sell": 0.177,
    },

    "Vacas": {
        "img": "https://app.warera.io/images/items/livestock.png?v=32",
        "buy": 1.48,
        "sell": 1.54,
    },

    "Peces": {
        "img": "https://app.warera.io/images/items/fish.png?v=32",
        "buy": 0.082,
        "sell": 0.083,
    },

    "Concreto": {
        "img": "https://app.warera.io/images/items/concrete.png?v=32",
        "buy": 0.078,
        "sell": 0.080,
        "recipe": {
            "Piedra": 10
        }
    },

    "Vigas": {
        "img": "https://app.warera.io/images/items/steel.png?v=32",
        "buy": 1.65,
        "sell": 1.67,
        "recipe": {
            "Hierro": 10
        }
    },

    "Balas": {
        "img": "https://app.warera.io/images/items/lightAmmo.png?v=32",
        "buy": 0.078,
        "sell": 0.080,
        "recipe": {
            "Plomo": 1
        }
    },

    "BalasX": {
        "img": "https://app.warera.io/images/items/ammo.png?v=32",
        "buy": 2.44,
        "sell": 2.52,
        "recipe": {
            "Plomo": 4
        }
    },

    "BalasXX": {
        "img": "https://app.warera.io/images/items/heavyAmmo.png?v=32",
        "buy": 7.38,
        "sell": 7.45,
        "recipe": {
            "Plomo": 16
        }
    },

    "Pan": {
        "img": "https://app.warera.io/images/items/bread.png?v=32",
        "buy": 0.079,
        "sell": 0.080,
        "recipe": {
            "Trigo": 10
        }
    },

    "Carne": {
        "img": "https://app.warera.io/images/items/steak.png?v=32",
        "buy": 3.19,
        "sell": 3.25,
        "recipe": {
            "Vacas": 1
        }
    },

    "Pescado": {
        "img": "https://app.warera.io/images/items/cookedFish.png?v=32",
        "buy": 0.082,
        "sell": 0.083,
        "recipe": {
            "Peces": 1
        }
    },

    "Pastillas": {
        "img": "https://app.warera.io/images/items/cocain.png?v=32",
        "buy": 1.76,
        "sell": 1.80,
        "recipe": {
            "Coca": 200
        }
    }
}

TIPOS = list(ITEMS.keys())

# =====================================================
# PRODUCCIÓN
# =====================================================

def calcular_produccion(tipo, nivel, bonus):

    base = nivel * 24

    produccion = base * (1 + bonus / 100)

    factores = {

        "Concreto": 10,
        "Vigas": 10,
        "Balas": 1,
        "BalasX": 4,
        "BalasXX": 16,
        "Pan": 10,
        "Carne": 20,
        "Pescado": 40,
        "Pastillas": 200
    }

    if tipo in ["Piedra", "Trigo", "Hierro", "Plomo", "Coca"]:
        return produccion

    if tipo == "Vacas":
        return produccion / 20

    if tipo == "Peces":
        return produccion / 40

    if tipo in factores:
        return produccion / factores[tipo]

    return 0

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="title">
🏭 WAR ERA INDUSTRIAL COMMAND
</div>

<div class="subtitle">
Simulador industrial inteligente
</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================================
# MERCADO EDITABLE
# =====================================================

st.sidebar.title("📈 Mercado Editable")

for item in ITEMS:

    st.sidebar.markdown(f"### {item}")

    ITEMS[item]["buy"] = st.sidebar.number_input(
        f"Compra {item}",
        value=float(ITEMS[item]["buy"]),
        step=0.001,
        key=f"buy_{item}"
    )

    ITEMS[item]["sell"] = st.sidebar.number_input(
        f"Venta {item}",
        value=float(ITEMS[item]["sell"]),
        step=0.001,
        key=f"sell_{item}"
    )

# =====================================================
# EMPRESA FINAL
# =====================================================

st.sidebar.title("🏭 Empresa Final")

producto_final = st.sidebar.selectbox(
    "Producto Final",
    TIPOS,
    index=8
)

nivel_final = st.sidebar.slider(
    "Nivel Empresa Final",
    1,
    7,
    5
)

bonus_final = st.sidebar.number_input(
    "Bonus Empresa Final (%)",
    value=25.0,
    step=0.01
)

# =====================================================
# PRODUCCIÓN FINAL
# =====================================================

produccion_final = calcular_produccion(
    producto_final,
    nivel_final,
    bonus_final
)

# =====================================================
# MATERIA PRIMA
# =====================================================

usa_empresa_material = False
material_nombre = None

if "recipe" in ITEMS[producto_final]:

    material_nombre = list(
        ITEMS[producto_final]["recipe"].keys()
    )[0]

    st.sidebar.title("⛏️ Empresa Materia Prima")

    usa_empresa_material = st.sidebar.toggle(
        f"Producir {material_nombre}",
        value=True
    )

# =====================================================
# CONFIG MATERIA PRIMA
# =====================================================

produccion_material = 0
costo_material = 0

if usa_empresa_material and material_nombre:

    nivel_material = st.sidebar.slider(
        f"Nivel {material_nombre}",
        1,
        7,
        5
    )

    bonus_material = st.sidebar.number_input(
        f"Bonus {material_nombre} (%)",
        value=25.0,
        step=0.01
    )

    produccion_material = calcular_produccion(
        material_nombre,
        nivel_material,
        bonus_material
    )

else:

    if material_nombre:

        # COMPRAS materiales al BUY
        costo_material = ITEMS[material_nombre]["buy"]

# =====================================================
# PROFIT
# =====================================================

# VENDES producto al SELL
precio_venta = ITEMS[producto_final]["sell"]

if material_nombre:

    cantidad_material = list(
        ITEMS[producto_final]["recipe"].values()
    )[0]

else:

    cantidad_material = 0

# Si produces material tú mismo
if usa_empresa_material and material_nombre:

    costo_total = 0

else:

    costo_total = (
        costo_material *
        cantidad_material
    )

profit_unitario = (
    precio_venta -
    costo_total
)

profit_diario = (
    profit_unitario *
    produccion_final
)

# =====================================================
# SOBRANTE
# =====================================================

sobrante = 0
ganancia_sobrante = 0

if material_nombre and usa_empresa_material:

    requerido = (
        produccion_final *
        cantidad_material
    )

    sobrante = (
        produccion_material -
        requerido
    )

    # Solo si sobra suficiente
    if sobrante > 0.5:

        ganancia_sobrante = (
            sobrante *
            ITEMS[material_nombre]["sell"]
        )

        profit_diario += ganancia_sobrante

# =====================================================
# CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.image(
        ITEMS[producto_final]["img"],
        width=80
    )

    st.subheader(producto_final)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.metric(
        "Producción Final",
        round(produccion_final, 2)
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col3:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if material_nombre:

        st.metric(
            f"Producción {material_nombre}",
            round(produccion_material, 2)
        )

    else:

        st.metric(
            "Materia Prima",
            "N/A"
        )

    st.markdown('</div>', unsafe_allow_html=True)

with col4:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    color = "green" if profit_diario > 0 else "red"

    st.markdown(f'''
    <div class="{color}">
    Profit diario:<br>
    {round(profit_diario,2)}
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# ANÁLISIS
# =====================================================

st.subheader("📊 Análisis Industrial")

if material_nombre:

    requerido = (
        produccion_final *
        cantidad_material
    )

    st.write(f"🔹 Producto final: {producto_final}")

    st.write(f"🔹 Materia prima: {material_nombre}")

    st.write(
        f"🔹 Necesitas: {round(requerido,2)} de {material_nombre}"
    )

    if usa_empresa_material:

        if produccion_material >= requerido:

            st.success(
                "✅ Tu empresa cubre toda la producción"
            )

        else:

            faltante = (
                requerido -
                produccion_material
            )

            st.error(
                f"❌ Falta producir {round(faltante,2)}"
            )

        # SOBRANTE

        if sobrante > 0.5:

            st.success(
                f"💰 Sobrante vendible: "
                f"{round(sobrante,2)} "
                f"{material_nombre}"
            )

            st.success(
                f"📈 Ganancia extra: "
                f"{round(ganancia_sobrante,2)}"
            )

    else:

        st.warning(
            "⚠️ Compras materia prima del mercado"
        )

# =====================================================
# MERCADO
# =====================================================

st.subheader("📈 Mercado Global")

market_data = []

for item, data in ITEMS.items():

    spread = round(
        data["sell"] - data["buy"],
        4
    )

    market_data.append({

        "Producto": item,
        "Compra": data["buy"],
        "Venta": data["sell"],
        "Spread": spread
    })

market_df = pd.DataFrame(market_data)

st.dataframe(
    market_df,
    use_container_width=True
)

# =====================================================
# RANKING
# =====================================================

st.subheader("🔥 Ranking Profit")

ranking = []

for item, data in ITEMS.items():

    if "recipe" in data:

        costo = 0

        for material, cantidad in data["recipe"].items():

            costo += (
                ITEMS[material]["buy"] *
                cantidad
            )

        profit = (
            data["sell"] -
            costo
        )

    else:

        profit = data["sell"]

    ranking.append({

        "Producto": item,
        "Profit": round(profit, 4)
    })

ranking_df = pd.DataFrame(ranking)

ranking_df = ranking_df.sort_values(
    by="Profit",
    ascending=False
)

st.dataframe(
    ranking_df,
    use_container_width=True
)
