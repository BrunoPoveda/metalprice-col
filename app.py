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

st.title("🥇 MetalPrice COL")
st.caption("Monitor de precios de oro y plata en pesos colombianos")

# ─────────────────────────────────────────
# FUNCIONES PARA OBTENER DATOS
# ─────────────────────────────────────────

def get_metal_prices():
    """Obtiene BID del oro y plata desde Metals.dev"""
    try:
        API_KEY = "URMX9HHCI64KACLYHCKP865LYHCKP"
        url = f"https://api.metals.dev/v1/latest?api_key={API_KEY}&currency=USD&unit=toz"
        response = requests.get(url, timeout=10)
        data = response.json()
        return {
            "oro":   data["metals"]["gold"],
            "plata": data["metals"]["silver"]
        }
    except Exception as e:
        st.warning(f"Error al obtener metales: {e}")
        return {
            "oro":   4542.40,
            "plata": 32.50
        }

def get_trm():
    """Obtiene tasa de cambio USD/COP desde ExchangeRate-API"""
    try:
        API_KEY = "7685e9a2a2575e25cc0b992f"
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["conversion_rates"]["COP"])
    except Exception as e:
        st.warning(f"Error TRM: {e}")
        return 3730.49  # valor de respaldo

# ─────────────────────────────────────────
# CÁLCULOS
# ─────────────────────────────────────────

def calcular_precios(bid_oro, bid_plata, trm):
    onza = 31.1035

    # Gramo internacional
    gramo_oro   = (bid_oro * trm) / onza
    gramo_plata = (bid_plata * trm) / onza

    return {
        "gramo_oro_internacional": gramo_oro,
        "gramo_plata_internacional": gramo_plata,
        "oro": {
            "24k":      gramo_oro * 0.88,
            "Italiano": gramo_oro * 0.74,
            "18k":      gramo_oro * 0.70,
            "16k":      gramo_oro * 0.66,
        },
        "plata": {
            "Plata": gramo_plata * 0.85,
        }
    }

# ─────────────────────────────────────────
# INTERFAZ
# ─────────────────────────────────────────

if st.button("🔄 Actualizar precios"):
    st.rerun()

with st.spinner("Consultando precios..."):
    metales = get_metal_prices()
    trm_auto = get_trm()

# TRM editable por el usuario
trm = st.number_input(
    "💵 Dólar (COP) — puedes editarlo con el valor de Google",
    min_value=1000.0,
    max_value=10000.0,
    value=float(trm_auto),
    step=1.0,
    format="%.2f"
)

if metales:
    bid_oro   = metales["oro"]
    bid_plata = metales["plata"]
    precios   = calcular_precios(bid_oro, bid_plata, trm)

    # Mostrar datos base
    col1, col2 = st.columns(2)
    col1.metric("BID Oro (USD/oz)",   f"${bid_oro:,.2f}")
    col2.metric("BID Plata (USD/oz)", f"${bid_plata:,.2f}")
    st.divider()

    # Tabla ORO
    st.subheader("🥇 Oro — Precio por gramo (COP)")
    st.caption(f"Gramo internacional: ${precios['gramo_oro_internacional']:,.0f} COP")

    for tipo, valor in precios["oro"].items():
        st.metric(label=tipo, value=f"${valor:,.0f} COP")

    st.divider()

    # Tabla PLATA
    st.subheader("🥈 Plata — Precio por gramo (COP)")
    st.caption(f"Gramo internacional: ${precios['gramo_plata_internacional']:,.0f} COP")

    for tipo, valor in precios["plata"].items():
        st.metric(label=tipo, value=f"${valor:,.0f} COP")

    st.divider()
    st.caption(f"🕐 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

else:
    st.error("No se pudo obtener el precio de los metales.")