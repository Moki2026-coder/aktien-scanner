import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import time

st.set_page_config(page_title="Aktien Scanner PRO 2.0", layout="wide")

st.title("🚀 Aktien Scanner PRO 2.0")
st.write("Fokus: frühere Kaufchancen, bessere Einstiegspunkte und weniger verspätete Kaufsignale.")

@st.cache_data(ttl=86400)
def lade_aktienuniversum():
    return {
        "Apple": "AAPL", "Microsoft": "MSFT", "NVIDIA": "NVDA", "Amazon": "AMZN",
        "Meta": "META", "Tesla": "TSLA", "Alphabet A": "GOOGL", "Broadcom": "AVGO",
        "AMD": "AMD", "Netflix": "NFLX", "Adobe": "ADBE", "Intel": "INTC",
        "Cisco": "CSCO", "Qualcomm": "QCOM", "PayPal": "PYPL", "Shopify": "SHOP",
        "Coinbase": "COIN", "Palantir": "PLTR", "Super Micro Computer": "SMCI",
        "Uber": "UBER", "Airbnb": "ABNB", "Booking": "BKNG", "CrowdStrike": "CRWD",
        "Snowflake": "SNOW", "Datadog": "DDOG", "Cloudflare": "NET",
        "ServiceNow": "NOW", "Palo Alto Networks": "PANW", "Zscaler": "ZS",
        "Micron": "MU", "Marvell": "MRVL", "ASML US": "ASML",
        "Lam Research": "LRCX", "Applied Materials": "AMAT", "KLA": "KLAC",
        "Texas Instruments": "TXN", "First Solar": "FSLR", "Enphase Energy": "ENPH",
        "Rocket Lab": "RKLB", "AST SpaceMobile": "ASTS", "Rivian": "RIVN",
        "Lucid": "LCID", "Ford": "F", "General Motors": "GM", "Visa": "V",
        "Mastercard": "MA", "American Express": "AXP", "JPMorgan": "JPM",
        "Bank of America": "BAC", "Goldman Sachs": "GS", "Morgan Stanley": "MS",
        "BlackRock": "BLK", "Berkshire Hathaway": "BRK-B", "Eli Lilly": "LLY",
        "Novo Nordisk": "NVO", "Johnson & Johnson": "JNJ", "UnitedHealth": "UNH",
        "Pfizer": "PFE", "Merck": "MRK", "AbbVie": "ABBV", "Coca-Cola": "KO",
        "PepsiCo": "PEP", "McDonald's": "MCD", "Costco": "COST", "Walmart": "WMT",
        "Target": "TGT", "Nike": "NKE", "Starbucks": "SBUX", "Home Depot": "HD",
        "Lowe's": "LOW", "Procter & Gamble": "PG", "Exxon Mobil": "XOM",
        "Chevron": "CVX", "Occidental Petroleum": "OXY", "ConocoPhillips": "COP",
        "Caterpillar": "CAT", "Deere": "DE", "Boeing": "BA", "Lockheed Martin": "LMT",
        "Northrop Grumman": "NOC", "RTX": "RTX",

        "Rheinmetall": "RHM.DE", "Siemens Energy": "ENR.DE", "SAP": "SAP.DE",
        "Allianz": "ALV.DE", "Deutsche Bank": "DBK.DE", "Volkswagen": "VOW3.DE",
        "Mercedes-Benz": "MBG.DE", "BMW": "BMW.DE", "Porsche AG": "P911.DE",
        "BASF": "BAS.DE", "Bayer": "BAYN.DE", "Deutsche Telekom": "DTE.DE",
        "Munich Re": "MUV2.DE", "Siemens": "SIE.DE", "Infineon": "IFX.DE",
        "Adidas": "ADS.DE", "Puma": "PUM.DE", "Commerzbank": "CBK.DE",
        "Heidelberg Materials": "HEI.DE",

        "ASML Europe": "ASML.AS", "Novo Nordisk Europe": "NOVO-B.CO",
        "LVMH": "MC.PA", "Hermes": "RMS.PA", "TotalEnergies": "TTE.PA",
        "Airbus": "AIR.PA", "Schneider Electric": "SU.PA", "Sanofi": "SAN.PA",
        "BNP Paribas": "BNP.PA", "ING": "INGA.AS", "Ferrari": "RACE.MI",
        "Stellantis": "STLAM.MI", "Enel": "ENEL.MI", "Iberdrola": "IBE.MC",
        "Banco Santander": "SAN.MC"
    }

@st.cache_data(ttl=900)
def lade_daten(ticker):
    return yf.Ticker(ticker).history(period="1y")

@st.cache_data(ttl=900)
def lade_usd_eur():
    daten = yf.Ticker("EURUSD=X").history(period="5d")
    return 1 / daten["Close"].iloc[-1]

@st.cache_data(ttl=900)
def lade_markt():
    return yf.Ticker("^GSPC").history(period="1y")

def rsi(daten, periode=14):
    delta = daten["Close"].diff()
    gewinne = delta.where(delta > 0, 0)
    verluste = -delta.where(delta < 0, 0)
    avg_gain = gewinne.rolling(window=periode).mean()
    avg_loss = verluste.rolling(window=periode).mean()
    rs = avg_gain / avg_loss
    return (100 - (100 / (1 + rs))).iloc[-1]

def analyse_aktie(name, ticker, daten, markt, usd_eur):
    close = daten["Close"]
    volumen = daten["Volume"]

    kurs = close.iloc[-1]
    kurs_3 = close.iloc[-3]
    kurs_5 = close.iloc[-5]
    kurs_20 = close.iloc[-20]
    kurs_60 = close.iloc[-60]

    trend_3 = (kurs - kurs_3) / kurs_3 * 100
    trend_5 = (kurs - kurs_5) / kurs_5 * 100
    trend_20 = (kurs - kurs_20) / kurs_20 * 100
    trend_60 = (kurs - kurs_60) / kurs_60 * 100

    ema20 = close.ewm(span=20).mean().iloc[-1]
    ema50 = close.ewm(span=50).mean().iloc[-1]
    ema200 = close.ewm(span=200).mean().iloc[-1]

    abstand_ema50 = (kurs - ema50) / ema50 * 100
    abstand_ema200 = (kurs - ema200) / ema200 * 100

    aktueller_rsi = rsi(daten)

    volumen_heute = volumen.iloc[-1]
    volumen_avg = volumen.tail(30).mean()

    renditen = close.pct_change().dropna()
    vola = renditen.tail(30).std() * 100

    hoch_52w = close.max()
    abstand_hoch = (kurs - hoch_52w) / hoch_52w * 100

    markt_start = markt["Close"].iloc[-60]
    markt_ende = markt["Close"].iloc[-1]
    markt_perf = (markt_ende - markt_start) / markt_start * 100
    relative_staerke = trend_60 - markt_perf

    score = 50
    gruende = []

    # 1. Früher Einstieg statt zu spät
    if 0 < trend_5 < 6 and trend_20 > 0 and 40 <= aktueller_rsi <= 65:
        score += 25
        gruende.append("🚀 Frühe Bewegung erkannt")

    if trend_5 > 10:
        score -= 25
        gruende.append("⚠️ Schon stark gelaufen")

    if trend_20 > 20:
        score -= 15
        gruende.append("⚠️ 20-Tage-Anstieg sehr hoch")

    # 2. EMA-Regeln deutlich härter
    if kurs > ema50:
        score += 15
        gruende.append("✅ Über EMA50")
    else:
        score -= 25
        gruende.append("❌ Unter EMA50")

    if kurs > ema200:
        score += 15
        gruende.append("✅ Über EMA200")
    else:
        score -= 35
        gruende.append("❌ Unter EMA200")

    if ema20 > ema50 > ema200:
        score += 20
        gruende.append("🟢 Sauberer Aufwärtstrend")

    # 3. Nicht kaufen, wenn zu weit von EMA50 entfernt
    if abstand_ema50 > 10:
        score -= 25
        gruende.append("⚠️ Zu weit über EMA50")
    elif -2 <= abstand_ema50 <= 6 and kurs > ema200:
        score += 20
        gruende.append("✅ Gute Nähe zur EMA50")

    # 4. RSI
    if 45 <= aktueller_rsi <= 65:
        score += 15
        gruende.append("✅ RSI gesund")
    elif aktueller_rsi > 72:
        score -= 30
        gruende.append("🔥 Überhitzt")
    elif aktueller_rsi < 35:
        score -= 10
        gruende.append("🔵 Sehr schwach / überverkauft")

    # 5. Relative Stärke
    if relative_staerke > 8:
        score += 15
        gruende.append("✅ Stärker als Markt")
    elif relative_staerke < -5:
        score -= 15
        gruende.append("❌ Schwächer als Markt")

    # 6. Stabilität belohnen
    if vola < 2.5 and kurs > ema50:
        score += 15
        risiko = "🟢 Niedrig"
        gruende.append("🟢 Stabiler Trend")
    elif vola < 4:
        risiko = "🟡 Mittel"
    else:
        score -= 10
        risiko = "🔴 Hoch"
        gruende.append("🔴 Hohe Schwankung")

    # 7. Trendverlust erkennen
    if trend_3 < -2 and trend_5 < 0:
        score -= 25
        trendstatus = "🔴 Trend verliert Stärke"
        gruende.append("🔴 Kurzfristiger Trendverlust")
    elif trend_3 > 0 and trend_5 > 0:
        score += 10
        trendstatus = "🟢 Trend zieht an"
    else:
        trendstatus = "🟡 Trend neutral"

    # 8. Breakout aber nicht zu spät
    if -5 <= abstand_hoch <= 0 and trend_5 < 8 and aktueller_rsi < 70:
        score += 15
        breakout = "🟢 Früher Breakout möglich"
    elif abstand_hoch > -3 and trend_5 >= 8:
        score -= 10
        breakout = "⚠️ Breakout spät"
    else:
        breakout = "➖ Kein frischer Breakout"

    score = max(0, min(120, score))

    if ticker.endswith((".DE", ".PA", ".AS", ".MI", ".MC", ".CO")):
        kurs_euro = kurs
    else:
        kurs_euro = kurs * usd_eur

    if score >= 90 and 45 <= aktueller_rsi <= 68 and kurs > ema50 and kurs > ema200 and trend_5 < 8:
        kaufempfehlung = "✅ Kaufen"
        kaufchance = "🟢 Hoch"
    elif score >= 75 and kurs > ema50 and kurs > ema200:
        kaufempfehlung = "👀 Beobachten"
        kaufchance = "🟡 Mittel"
    elif aktueller_rsi > 72 or trend_5 > 10 or abstand_ema50 > 10:
        kaufempfehlung = "⏳ Zu spät / warten"
        kaufchance = "🟠 Spät"
    else:
        kaufempfehlung = "❌ Nicht kaufen"
        kaufchance = "🔴 Niedrig"

    if kaufempfehlung == "✅ Kaufen" and risiko == "🟢 Niedrig":
        einsatz = "💰 Groß"
    elif kaufempfehlung == "✅ Kaufen":
        einsatz = "💰 Mittel"
    elif kaufempfehlung == "👀 Beobachten":
        einsatz = "💰 Klein"
    else:
        einsatz = "—"

    return {
        "Aktie": name,
        "Ticker": ticker,
        "Kaufempfehlung": kaufempfehlung,
        "Kaufchance": kaufchance,
        "Risiko": risiko,
        "Einsatz": einsatz,
        "Score": round(score, 1),
        "Kurs €": round(kurs_euro, 2),
        "Trendstatus": trendstatus,
        "Trend 3T %": round(trend_3, 2),
        "Trend 5T %": round(trend_5, 2),
        "Trend 20T %": round(trend_20, 2),
        "RSI": round(aktueller_rsi, 2),
        "EMA50 Abstand %": round(abstand_ema50, 2),
        "EMA200 Abstand %": round(abstand_ema200, 2),
        "Relative Stärke %": round(relative_staerke, 2),
        "Breakout": breakout,
        "Abstand Hoch %": round(abstand_hoch, 2),
        "Volatilität": round(vola, 2),
        "Volumen": int(volumen_heute),
        "Ø Volumen": int(volumen_avg),
        "Gründe": " | ".join(gruende[:6])
    }

def scanner_starten():
    start = time.time()
    aktien = lade_aktienuniversum()
    usd_eur = lade_usd_eur()
    markt = lade_markt()

    ergebnisse = []
    fehler = 0

    for name, ticker in aktien.items():
        try:
            daten = lade_daten(ticker)
            if daten.empty or len(daten) < 220:
                fehler += 1
                continue

            ergebnisse.append(analyse_aktie(name, ticker, daten, markt, usd_eur))

        except Exception:
            fehler += 1
            continue

    df = pd.DataFrame(ergebnisse)

    if df.empty:
        return df, 0, fehler, 0

    df = df.sort_values(by="Score", ascending=False).head(20)
    df.insert(0, "Platz", range(1, len(df) + 1))

    dauer = round(time.time() - start, 1)
    return df, len(ergebnisse), fehler, dauer

if st.button("🔄 Scanner aktualisieren"):
    with st.spinner("Scanner läuft... bitte warten."):
        df, gescannt, fehler, dauer = scanner_starten()

    if df.empty:
        st.error("Keine Daten gefunden.")
    else:
        jetzt = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%d.%m.%Y %H:%M:%S")

        st.success("Scanner fertig ✅")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌍 Aktien gescannt", gescannt)
        c2.metric("🏆 Kandidaten", len(df))
        c3.metric("⏱️ Scan-Dauer", f"{dauer} Sek.")
        c4.metric("🕒 Uhrzeit", jetzt)

        st.subheader("📱 Einfache Übersicht")

        hauptansicht = df[[
            "Platz",
            "Aktie",
            "Kaufempfehlung",
            "Kaufchance",
            "Risiko",
            "Einsatz"
        ]]

        st.dataframe(hauptansicht, use_container_width=True, hide_index=True)

        st.subheader("🔎 Details anzeigen")

        for _, row in df.iterrows():
            with st.expander(f"{row['Platz']}. {row['Aktie']} – {row['Kaufempfehlung']}"):
                st.write("**Ticker:**", row["Ticker"])
                st.write("**Kurs €:**", row["Kurs €"])
                st.write("**Score:**", row["Score"])
                st.write("**Trendstatus:**", row["Trendstatus"])
                st.write("**Trend 3 Tage:**", str(row["Trend 3T %"]) + "%")
                st.write("**Trend 5 Tage:**", str(row["Trend 5T %"]) + "%")
                st.write("**Trend 20 Tage:**", str(row["Trend 20T %"]) + "%")
                st.write("**RSI:**", row["RSI"])
                st.write("**EMA50 Abstand:**", str(row["EMA50 Abstand %"]) + "%")
                st.write("**EMA200 Abstand:**", str(row["EMA200 Abstand %"]) + "%")
                st.write("**Relative Stärke:**", str(row["Relative Stärke %"]) + "%")
                st.write("**Breakout:**", row["Breakout"])
                st.write("**Abstand zum Hoch:**", str(row["Abstand Hoch %"]) + "%")
                st.write("**Volatilität:**", row["Volatilität"])
                st.write("**Volumen:**", row["Volumen"])
                st.write("**Durchschnittsvolumen:**", row["Ø Volumen"])
                st.write("**Warum diese Bewertung?**", row["Gründe"])

        st.caption("Hinweis: Das ist ein Analyse-Scanner, keine garantierte Anlageberatung.")

else:
    st.info("Klicke auf „Scanner aktualisieren“, um aktuelle Daten zu laden.")
    
