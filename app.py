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
texto = generar_texto_copia(precios, trm, bid_oro, bid_plata)

st.markdown("### 📋 Copiar para WhatsApp")

copy_html = f"""
<style>
.copy-box {{
    background-color: #1a1a2e;
    border: 1px solid #444;
    border-radius: 10px;
    padding: 20px;
    font-family: monospace;
    font-size: 14px;
    color: #e0e0e0;
    white-space: pre-line;
    margin-bottom: 12px;
}}
.copy-btn {{
    background-color: #25D366;
    color: white;
    border: none;
    padding: 10px 24px;
    font-size: 16px;
    border-radius: 8px;
    cursor: pointer;
    width: 100%;
}}
.copy-btn:hover {{
    background-color: #1ebe5d;
}}
.copy-btn.copiado {{
    background-color: #555;
}}
</style>

<div class="copy-box" id="textoCopia">{texto}</div>
<button class="copy-btn" onclick="copiarTexto()" id="btnCopiar">
    📋 Copiar todo para WhatsApp
</button>

<script>
function copiarTexto() {{
    const el = document.getElementById('textoCopia');
    const texto = el.innerText;
    const textarea = document.createElement('textarea');
    textarea.value = texto;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    const btn = document.getElementById('btnCopiar');
    btn.innerText = '✅ ¡Copiado!';
    btn.classList.add('copiado');
    setTimeout(() => {{
        btn.innerText = '📋 Copiar todo para WhatsApp';
        btn.classList.remove('copiado');
    }}, 2000);
}}
</script>
"""

st.components.v1.html(copy_html, height=600)