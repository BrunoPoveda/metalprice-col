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
            "ORO 24K":           base_24k,
            "ORO ITALIANO":      base_24k * 0.74,
            "ORO 18K NACIONAL":  base_24k * 0.71,
            "ORO 16K":           base_24k * 0.66,
            "ORO 14K":           base_24k * 0.58,
            "ORO 10K":           base_24k * 0.38,
            "ORO 8K":            base_24k * 0.28,
        },
        "plata": {
            "PRECIO PLATA COLOMBIA PURA": gramo_plata * 0.85,
        }
    }


def generar_texto_copia(precios, trm, bid_oro, bid_plata):
    from datetime import datetime
    hora = datetime.now().strftime('%d/%m/%Y %H:%M')

    lineas = [
        f"Precios {hora}",
        f"Dólar: ${trm:,.0f}",
        "",
        "── ORO ──",
    ]

    for tipo, valor in precios["oro"].items():
        nombre = tipo.replace("ORO ", "")
        lineas.append(f"{nombre} = ${valor:,.0f}")

    lineas.append("")
    lineas.append("── PLATA ──")
    lineas.append(f"PLATA PURA = ${list(precios['plata'].values())[0]:,.0f}")

    return "\n".join(lineas)