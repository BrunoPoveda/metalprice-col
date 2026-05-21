import streamlit as st
import requests
from datetime import datetime

# ─────────────────────────────────────────
# CONFIGURACIÓN DE LA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MetalPrice COL",
    page_icon="🥇",
    layout="centered"
)

st.title("🥇 MetalPrice COL - Taller de joyas Isa")
st.caption("Monitor de precios de oro y plata en pesos colombianos")

# ─────────────────────────────────────────
# FUNCIONES PARA OBTENER DATOS
# ─────────────────────────────────────────


def get_metal_prices():
    """Intenta Kitco primero, luego Metals.dev como respaldo"""

    # Fuente 1 — Kitco (directo, sin API key)
    try:
        url = "https://api.kitco.com/api/v1/precious-metals"
        response = requests.get(url, headers={"Accept": "application/json"}, timeout=10)
        data = response.json()
        metales = {}
        for metal in data["PreciousMetals"]["PM"]:
            if metal["Symbol"] == "AU":
                metales["oro"] = float(metal["current_bid"])
            if metal["Symbol"] == "AG":
                metales["plata"] = float(metal["current_bid"])
        if "oro" in metales and "plata" in metales:
            metales["fuente"] = "Kitco"
            return metales
    except:
        pass

    # Fuente 2 — Metals.dev (respaldo)
    try:
        API_KEY = st.secrets["METALS_API_KEY"]
        url = f"https://api.metals.dev/v1/latest?api_key={API_KEY}&currency=USD&unit=toz"
        response = requests.get(url, timeout=10)
        data = response.json()
        return {
            "oro":    data["metals"]["gold"],
            "plata":  data["metals"]["silver"],
            "fuente": "Metals.dev"
        }
    except:
        pass

    # Si ambas fallan
    return None

# ─────────────────────────────────────────
# CÁLCULOS
# ─────────────────────────────────────────

def calcular_precios(bid_oro, bid_plata, trm):
    onza = 31.1

    bid_oro_redondeado = round(bid_oro)

    gramo_oro   = (bid_oro_redondeado * trm) / onza
    gramo_plata = (bid_plata * trm) / onza

    base_24k = gramo_oro * 0.88

    return {
        "gramo_oro_internacional": gramo_oro,
        "gramo_plata_internacional": gramo_plata,
        "oro": {
            "24k":            base_24k,
            "18k - Italiano": base_24k * 0.74,
            "18k - Nacional": base_24k * 0.71,
            "16k":            base_24k * 0.66,
            "14k":            base_24k * 0.58,
            "10k":            base_24k * 0.41,
            "8k":             base_24k * 0.33,
        },
        "plata": {
            "Plata": gramo_plata * 0.85,
        }
    }

# ─────────────────────────────────────────
# OBTENER PRECIOS DEL ORO Y PLATA
# ─────────────────────────────────────────

with st.spinner("Consultando precios internacionales..."):
    metales = get_metal_prices()

if metales is None:
    st.error("Lo sentimos — los servidores no pueden consultar ni Kitco ni la fuente global de precios. Intente más tarde.")
    st.stop()

# Mostrar fuente
st.caption(f"📡 Fuente de precios: **{metales['fuente']}**")

# Botón actualizar
if st.button("🔄 Actualizar precios"):
    st.cache_data.clear()
    st.rerun()

# ─────────────────────────────────────────
# DÓLAR MANUAL
# ─────────────────────────────────────────

st.markdown("---")
st.markdown("### 💵 Dólar del día (COP)")
st.warning("⚠️ Por favor ingrese el valor del dólar de hoy antes de continuar. Consúltelo en Google: **'dólar hoy'**")

trm = st.number_input(
    "Ingrese el valor del dólar (COP)",
    min_value=0.0,
    max_value=10000.0,
    value=0.0,
    step=1.0,
    format="%.2f"
)

if trm == 0:
    st.stop()

# ─────────────────────────────────────────
# MOSTRAR RESULTADOS
# ─────────────────────────────────────────

bid_oro   = metales["oro"]
bid_plata = metales["plata"]
precios   = calcular_precios(bid_oro, bid_plata, trm)

col1, col2 = st.columns(2)
col1.metric("BID Oro (USD/oz)",   f"${bid_oro:,.0f}")
col2.metric("BID Plata (USD/oz)", f"${bid_plata:,.2f}")

st.markdown("---")

# Tabla ORO
st.subheader("🥇 Oro — Precio por gramo (COP)")
st.caption(f"Gramo internacional: ${precios['gramo_oro_internacional']:,.0f} COP")

for tipo, valor in precios["oro"].items():
    st.metric(label=tipo, value=f"${valor:,.0f} COP")

st.markdown("---")

# Tabla PLATA
st.subheader("🥈 Plata — Precio por gramo (COP)")
st.caption(f"Gramo internacional: ${precios['gramo_plata_internacional']:,.0f} COP")

for tipo, valor in precios["plata"].items():
    st.metric(label=tipo, value=f"${valor:,.0f} COP")

st.markdown("---")
st.caption(f"🕐 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")