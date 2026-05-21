import requests
import streamlit as st

def get_metal_prices():
    """Intenta Kitco primero, luego Metals.dev como respaldo"""

    # Fuente 1 — Kitco
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

    return None