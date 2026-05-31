import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mein Aktien Scanner", layout="wide")

st.title("🚀 Mein Aktien Scanner")
st.write("Top 20 Aktien nach Trend, Volumen, RSI und Chance-Bewertung.")

aktien = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Meta": "META",
    "Tesla": "TSLA",
    "Palantir": "PLTR",
    "AMD": "AMD",
    "Google": "GOOGL",
    "Netflix": "NFLX",
    "Broadcom": "AVGO",
    "Super Micro Computer": "SMCI",
    "First Solar": "FSLR",
    "Rocket Lab": "RKLB",
    "AST SpaceMobile": "ASTS",
    "Coinbase": "COIN",
    "Shopify": "SHOP",
    "Uber": "UBER",
    "PayPal": "PYPL",
    "Rivian": "RIVN",
    "Rheinmetall": "RHM.DE",
    "Siemens Energy": "ENR.DE",
    "SAP": "SAP.DE",
    "Allianz": "ALV.DE",
    "Deutsche Bank": "DBK.DE",
    "Volkswagen": "VOW3.DE",
    "Mercedes-Benz": "MBG.DE"
}

def berechne_rsi(daten, periode=14):
    veraenderung = daten["Close"].diff()
    gewinne = veraenderung.where(veraenderung > 0, 0)
    verluste = -veraenderung.where(veraenderung < 0, 0)

    durchschnitt_gewinn = gewinne.rolling(window=periode).mean()
    durchschnitt_verlust = verluste.rolling(window=periode).mean()

    rs = durchschnitt_gewinn / durchschnitt_verlust
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]

def get_usd_eur():
    daten = yf.Ticker("EURUSD=X").history(period="5d")
    kurs = daten["Close"].iloc[-1]
    return 1 / kurs

def scanner_starten():
    ergebnisse = []
    usd_eur = get_usd_eur()

    for name, ticker in aktien.items():
        daten = yf.Ticker(ticker).history(period="60d")

        if daten.empty:
            continue

        letzter_kurs = daten["Close"].iloc[-1]
        kurs_vor_5_tagen = daten["Close"].iloc[-5]
        trend = (letzter_kurs - kurs_vor_5_tagen) / kurs_vor_5_tagen * 100

        volumen = daten["Volume"].iloc[-1]
        durchschnitt_volumen = daten["Volume"].mean()
        durchschnitt_20_tage = daten["Close"].tail(20).mean()
        rsi = berechne_rsi(daten)

        if ticker.endswith(".DE"):
            kurs_euro = letzter_kurs
            waehrung = "EUR"
        else:
            kurs_euro = letzter_kurs * usd_eur
            waehrung = "USD → EUR"

        score = 0

        if trend > 10:
            score += 40
        elif trend > 5:
            score += 30
        elif trend > 0:
            score += 20

        if volumen > durchschnitt_volumen * 1.5:
            score += 30
        elif volumen > durchschnitt_volumen:
            score += 20

        if letzter_kurs > durchschnitt_20_tage:
            score += 30

        if rsi > 70:
            rsi_signal = "⚠️ Überhitzt"
        elif rsi < 30:
            rsi_signal = "🔵 Überverkauft"
        else:
            rsi_signal = "✅ Normal"

        if score >= 85 and 40 <= rsi <= 70:
            scanner_signal = "✅ Beobachten / möglicher Kaufkandidat"
            chance_score = score + 20
        elif score >= 85 and rsi > 70:
            scanner_signal = "🟡 Stark, aber heiß"
            chance_score = score - 10
        elif score >= 60 and rsi <= 70:
            scanner_signal = "🟡 Interessant / warten"
            chance_score = score
        else:
            scanner_signal = "❌ Aktuell nicht spannend"
            chance_score = score

        ergebnisse.append({
            "Aktie": name,
            "Ticker": ticker,
            "Kurs €": round(kurs_euro, 2),
            "Trend %": round(trend, 2),
            "Score": score,
            "RSI": round(rsi, 2),
            "RSI Signal": rsi_signal,
            "Scanner Signal": scanner_signal,
            "Chance Score": chance_score
        })

    df = pd.DataFrame(ergebnisse)
    df = df.sort_values(by="Chance Score", ascending=False).head(20)
    df.insert(0, "Platz", range(1, len(df) + 1))

    return df

if st.button("🔄 Scanner aktualisieren"):
    with st.spinner("Scanner läuft... bitte warten."):
        df = scanner_starten()

    st.success("Scanner fertig ✅")
    st.write("Letzte Aktualisierung:", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    top3 = df.head(3)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🥇 Platz 1", top3.iloc[0]["Aktie"], top3.iloc[0]["Chance Score"])

    with col2:
        st.metric("🥈 Platz 2", top3.iloc[1]["Aktie"], top3.iloc[1]["Chance Score"])

    with col3:
        st.metric("🥉 Platz 3", top3.iloc[2]["Aktie"], top3.iloc[2]["Chance Score"])

    st.subheader("🏆 Top 20 spannendste Aktien")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Klicke auf „Scanner aktualisieren“, um aktuelle Daten zu laden.")