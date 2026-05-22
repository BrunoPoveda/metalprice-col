import streamlit as st
from datetime import datetime
from api_metales import get_metal_prices
from calculos import calcular_precios, generar_texto_copia

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MetalPrice COL",
    page_icon="🥇",
    layout="centered"
)

st.title("🥇 MetalPrice COL")
st.caption("Monitor de precios de oro y plata — Taller de joyas Isa")

# ─────────────────────────────────────────
# OBTENER PRECIOS
# ─────────────────────────────────────────
with st.spinner("Consultando precios internacionales..."):
    metales = get_metal_prices()

if metales is None:
    st.error("Lo sentimos — no fue posible consultar los precios. Recargue la página e intente de nuevo.")
    st.stop()

st.caption(f"📡 Fuente: **{metales['fuente']}** — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

bid_oro   = metales["oro"]
bid_plata = metales["plata"]

col1, col2 = st.columns(2)
col1.metric("BID Oro (USD/oz)",   f"${bid_oro:,.0f}")
col2.metric("BID Plata (USD/oz)", f"${bid_plata:,.2f}")

# ─────────────────────────────────────────
# DÓLAR MANUAL
# ─────────────────────────────────────────
st.markdown("---")
st.markdown("### 💵 Dólar del día (COP)")
st.warning("⚠️ Consulte el valor del dólar en Google: **'dólar hoy'** e ingréselo aquí y presione **Enter**")

trm_input = st.text_input(
    "Ingrese el valor del dólar (COP)",
    placeholder="Ejemplo: 3730 — presione Enter para calcular",
    label_visibility="collapsed",
    key="trm_field"
)

if not trm_input or len(trm_input.strip()) < 4:
    st.info("👆 Ingrese el dólar del día y presione **Enter**")
    st.stop()

try:
    trm = float(trm_input.strip().replace(",", "."))
except:
    st.error("❌ Valor no válido. Use solo números, ejemplo: 3730")
    st.stop()
# ─────────────────────────────────────────
# RESULTADOS
# ─────────────────────────────────────────
precios = calcular_precios(bid_oro, bid_plata, trm)

st.markdown("---")

# ── ORO ──
st.markdown("""
<div style='background: linear-gradient(90deg, #b8860b, #ffd700);
     padding: 12px 20px; border-radius: 10px; margin-bottom: 10px;'>
    <h2 style='color: #1a1a1a; margin: 0;'>🟡 ORO — Precio por gramo (COP)</h2>
</div>
""", unsafe_allow_html=True)
st.caption(f"Gramo internacional: **${precios['gramo_oro_internacional']:,.0f} COP**")

for tipo, valor in precios["oro"].items():
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;
         background-color: #2a2a1a; border-left: 4px solid #ffd700;
         padding: 10px 16px; border-radius: 6px; margin-bottom: 6px;'>
        <span style='color: #ffd700; font-weight: bold; font-size: 15px;'>{tipo}</span>
        <span style='color: #ffffff; font-size: 20px; font-weight: bold;'>${valor:,.0f} COP</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── PLATA ──
st.markdown("""
<div style='background: linear-gradient(90deg, #708090, #c0c0c0);
     padding: 12px 20px; border-radius: 10px; margin-bottom: 10px;'>
    <h2 style='color: #1a1a1a; margin: 0;'>🔘 PLATA — Precio por gramo (COP)</h2>
</div>
""", unsafe_allow_html=True)
st.caption(f"Gramo internacional: **${precios['gramo_plata_internacional']:,.0f} COP**")

for tipo, valor in precios["plata"].items():
    st.markdown(f"""
    <div style='display: flex; justify-content: space-between; align-items: center;
         background-color: #1a1a2a; border-left: 4px solid #c0c0c0;
         padding: 10px 16px; border-radius: 6px; margin-bottom: 6px;'>
        <span style='color: #c0c0c0; font-weight: bold; font-size: 15px;'>{tipo}</span>
        <span style='color: #ffffff; font-size: 20px; font-weight: bold;'>${valor:,.0f} COP</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# BOTÓN COPIAR
# ─────────────────────────────────────────
# ─────────────────────────────────────────
# COMPARTIR EN WHATSAPP
# ─────────────────────────────────────────
# ─────────────────────────────────────────
# COMPARTIR EN WHATSAPP
# ─────────────────────────────────────────
import urllib.parse
from datetime import datetime

texto = generar_texto_copia(precios, trm, bid_oro, bid_plata)

st.markdown("### 📋 Compartir precios")

# Vista previa NO editable
st.code(texto, language=None)

# URL con saltos de línea correctos para WhatsApp
texto_url = urllib.parse.quote(texto)
whatsapp_url = f"https://api.whatsapp.com/send?text={texto_url}"

st.markdown(f"""
<a href="{whatsapp_url}" target="_blank">
<button style='
    background-color: #25D366;
    color: white;
    border: none;
    padding: 14px 24px;
    font-size: 18px;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
    margin-top: 10px;
'>
    📲 Compartir en WhatsApp
</button>
</a>
""", unsafe_allow_html=True)
