
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import time

st.set_page_config(page_title="Aktien Scanner PRO", layout="wide")

st.title("🚀 Aktien Scanner PRO")
st.write("Einfache Handy-Ansicht mit Kaufchance, Risiko, Einsatz und Details zum Aufklappen.")

# ---------------------------------------------------
# Aktienlisten
# ---------------------------------------------------

@st.cache_data(ttl=86400)
def lade_nasdaq100():
    try:
        url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        tabellen = pd.read_html(url)

        for tabelle in tabellen:
            if "Ticker" in tabelle.columns and "Company" in tabelle.columns:
                liste = {}
                for _, row in tabelle.iterrows():
                    name = str(row["Company"])
                    ticker = str(row["Ticker"]).replace(".", "-")
                    liste[name] = ticker
                return liste
    except:
        return {}

    return {}



# ---------------------------------------------------
# Aktienlisten
# ---------------------------------------------------

@st.cache_data(ttl=86400)
def lade_aktienuniversum():
    return {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Amazon": "AMZN",
        "Meta": "META",
        "Tesla": "TSLA",
        "Alphabet A": "GOOGL",
        "Alphabet C": "GOOG",
        "Broadcom": "AVGO",
        "AMD": "AMD",
        "Netflix": "NFLX",
        "Adobe": "ADBE",
        "Intel": "INTC",
        "Cisco": "CSCO",
        "Qualcomm": "QCOM",
        "PayPal": "PYPL",
        "Shopify": "SHOP",
        "Coinbase": "COIN",
        "Palantir": "PLTR",
        "Super Micro Computer": "SMCI",
        "Uber": "UBER",
        "Airbnb": "ABNB",
        "Booking": "BKNG",
        "CrowdStrike": "CRWD",
        "Snowflake": "SNOW",
        "Datadog": "DDOG",
        "Cloudflare": "NET",
        "ServiceNow": "NOW",
        "Palo Alto Networks": "PANW",
        "Zscaler": "ZS",
        "Micron": "MU",
        "Marvell": "MRVL",
        "ASML US": "ASML",
        "Lam Research": "LRCX",
        "Applied Materials": "AMAT",
        "KLA": "KLAC",
        "Texas Instruments": "TXN",
        "First Solar": "FSLR",
        "Enphase Energy": "ENPH",
        "Rocket Lab": "RKLB",
        "AST SpaceMobile": "ASTS",
        "Rivian": "RIVN",
        "Lucid": "LCID",
        "Ford": "F",
        "General Motors": "GM",
        "Visa": "V",
        "Mastercard": "MA",
        "American Express": "AXP",
        "JPMorgan": "JPM",
        "Bank of America": "BAC",
        "Goldman Sachs": "GS",
        "Morgan Stanley": "MS",
        "BlackRock": "BLK",
        "Berkshire Hathaway": "BRK-B",
        "Eli Lilly": "LLY",
        "Novo Nordisk": "NVO",
        "Johnson & Johnson": "JNJ",
        "UnitedHealth": "UNH",
        "Pfizer": "PFE",
        "Merck": "MRK",
        "AbbVie": "ABBV",
        "Coca-Cola": "KO",
        "PepsiCo": "PEP",
        "McDonald's": "MCD",
        "Costco": "COST",
        "Walmart": "WMT",
        "Target": "TGT",
        "Nike": "NKE",
        "Starbucks": "SBUX",
        "Home Depot": "HD",
        "Lowe's": "LOW",
        "Procter & Gamble": "PG",
        "Exxon Mobil": "XOM",
        "Chevron": "CVX",
        "Occidental Petroleum": "OXY",
        "ConocoPhillips": "COP",
        "Caterpillar": "CAT",
        "Deere": "DE",
        "Boeing": "BA",
        "Lockheed Martin": "LMT",
        "Northrop Grumman": "NOC",
        "RTX": "RTX",

        "Rheinmetall": "RHM.DE",
        "Siemens Energy": "ENR.DE",
        "SAP": "SAP.DE",
        "Allianz": "ALV.DE",
        "Deutsche Bank": "DBK.DE",
        "Volkswagen": "VOW3.DE",
        "Mercedes-Benz": "MBG.DE",
        "BMW": "BMW.DE",
        "Porsche AG": "P911.DE",
        "BASF": "BAS.DE",
        "Bayer": "BAYN.DE",
        "Deutsche Telekom": "DTE.DE",
        "Munich Re": "MUV2.DE",
        "Siemens": "SIE.DE",
        "Infineon": "IFX.DE",
        "Adidas": "ADS.DE",
        "Puma": "PUM.DE",
        "Commerzbank": "CBK.DE",
        "Heidelberg Materials": "HEI.DE",

        "ASML Europe": "ASML.AS",
        "Novo Nordisk Europe": "NOVO-B.CO",
        "LVMH": "MC.PA",
        "Hermes": "RMS.PA",
        "TotalEnergies": "TTE.PA",
        "Airbus": "AIR.PA",
        "Schneider Electric": "SU.PA",
        "Sanofi": "SAN.PA",
        "BNP Paribas": "BNP.PA",
        "ING": "INGA.AS",
        "Ferrari": "RACE.MI",
        "Stellantis": "STLAM.MI",
        "Enel": "ENEL.MI",
        "Iberdrola": "IBE.MC",
        "Banco Santander": "SAN.MC"
    }

# Daten laden
# ---------------------------------------------------

@st.cache_data(ttl=900)
def lade_daten(ticker):
    return yf.Ticker(ticker).history(period="1y")


@st.cache_data(ttl=900)
def lade_usd_eur():
    daten = yf.Ticker("EURUSD=X").history(period="5d")
    kurs = daten["Close"].iloc[-1]
    return 1 / kurs


@st.cache_data(ttl=900)
def lade_markt():
    return yf.Ticker("^GSPC").history(period="1y")


# ---------------------------------------------------
# Analysefunktionen
# ---------------------------------------------------

def berechne_rsi(daten, periode=14):
    delta = daten["Close"].diff()
    gewinne = delta.where(delta > 0, 0)
    verluste = -delta.where(delta < 0, 0)

    avg_gain = gewinne.rolling(window=periode).mean()
    avg_loss = verluste.rolling(window=periode).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]


def berechne_risiko(daten):
    renditen = daten["Close"].pct_change().dropna()
    vola = renditen.std() * 100

    if vola < 2:
        return "🟢 Niedrig", 20
    elif vola < 4:
        return "🟡 Mittel", 10
    else:
        return "🔴 Hoch", 0


def berechne_trendqualitaet(daten):
    close = daten["Close"]

    kurs = close.iloc[-1]
    ema50 = close.ewm(span=50).mean().iloc[-1]
    ema200 = close.ewm(span=200).mean().iloc[-1]

    punkte = 0

    if kurs > ema50:
        punkte += 15

    if kurs > ema200:
        punkte += 15

    if ema50 > ema200:
        punkte += 10

    if punkte >= 35:
        text = "🟢 Stark"
    elif punkte >= 20:
        text = "🟡 Mittel"
    else:
        text = "🔴 Schwach"

    return text, punkte, ema50, ema200


def berechne_breakout(daten):
    close = daten["Close"]
    kurs = close.iloc[-1]

    hoch_52w = close.max()
    vorheriges_hoch = close.iloc[:-1].max()

    abstand_hoch = ((kurs - hoch_52w) / hoch_52w) * 100

    if kurs >= vorheriges_hoch * 0.995:
        return "🟢 Breakout möglich", 15, hoch_52w, abstand_hoch
    elif kurs >= hoch_52w * 0.95:
        return "🟡 Nah am Hoch", 8, hoch_52w, abstand_hoch
    else:
        return "🔴 Kein Breakout", 0, hoch_52w, abstand_hoch


def berechne_relative_staerke(daten, markt):
    try:
        aktie_start = daten["Close"].iloc[-60]
        aktie_ende = daten["Close"].iloc[-1]

        markt_start = markt["Close"].iloc[-60]
        markt_ende = markt["Close"].iloc[-1]

        aktie_perf = (aktie_ende - aktie_start) / aktie_start * 100
        markt_perf = (markt_ende - markt_start) / markt_start * 100

        rel = aktie_perf - markt_perf

        if rel > 10:
            return "🟢 Sehr stark", 20, rel
        elif rel > 3:
            return "🟡 Stark", 10, rel
        else:
            return "🔴 Schwach", 0, rel
    except:
        return "⚪ Keine Daten", 0, 0


def berechne_einsatz(kaufchance, risiko):
    if "Hoch" in kaufchance and "Niedrig" in risiko:
        return "💰 Groß"
    elif "Hoch" in kaufchance and "Mittel" in risiko:
        return "💰 Mittel"
    elif "Mittel" in kaufchance:
        return "💰 Klein bis Mittel"
    else:
        return "💰 Klein"


# ---------------------------------------------------
# Scanner
# ---------------------------------------------------

def scanner_starten():
    startzeit = time.time()

    aktien = lade_aktienuniversum()
    usd_eur = lade_usd_eur()
    markt = lade_markt()

    ergebnisse = []
    gescannt = 0
    fehler = 0

    for name, ticker in aktien.items():
        try:
            daten = lade_daten(ticker)

            if daten.empty or len(daten) < 220:
                fehler += 1
                continue

            gescannt += 1

            kurs = daten["Close"].iloc[-1]
            kurs_5 = daten["Close"].iloc[-5]
            trend_5 = (kurs - kurs_5) / kurs_5 * 100

            volumen = daten["Volume"].iloc[-1]
            volumen_avg = daten["Volume"].tail(30).mean()

            rsi = berechne_rsi(daten)
            risiko_text, risiko_punkte = berechne_risiko(daten)
            trend_text, trend_punkte, ema50, ema200 = berechne_trendqualitaet(daten)
            breakout_text, breakout_punkte, hoch_52w, abstand_hoch = berechne_breakout(daten)
            rel_text, rel_punkte, rel_wert = berechne_relative_staerke(daten, markt)

            score = 0

            # Kurzfristiger Trend
            if trend_5 > 10:
                score += 25
            elif trend_5 > 5:
                score += 18
            elif trend_5 > 0:
                score += 10

            # Volumen
            if volumen > volumen_avg * 1.5:
                score += 15
            elif volumen > volumen_avg:
                score += 8

            # Profi-Faktoren
            score += risiko_punkte
            score += trend_punkte
            score += breakout_punkte
            score += rel_punkte

            # RSI Einstiegschance
            if 40 <= rsi <= 70:
                score += 15
            elif rsi > 70:
                score -= 10
            elif rsi < 30:
                score += 5

            # Euro-Kurs
            if ticker.endswith(".DE") or ticker.endswith(".PA") or ticker.endswith(".AS") or ticker.endswith(".MI") or ticker.endswith(".MC"):
                kurs_euro = kurs
            else:
                kurs_euro = kurs * usd_eur

            # Kaufchance
            if score >= 85 and 40 <= rsi <= 70:
                kaufchance = "🟢 Hoch"
                signal = "✅ Kaufen möglich"
            elif score >= 70 and rsi <= 75:
                kaufchance = "🟡 Mittel"
                signal = "👀 Beobachten"
            elif score >= 70 and rsi > 75:
                kaufchance = "🟡 Mittel"
                signal = "⚠️ Stark, aber heiß"
            else:
                kaufchance = "🔴 Niedrig"
                signal = "❌ Warten"

            einsatz = berechne_einsatz(kaufchance, risiko_text)

            ergebnisse.append({
                "Aktie": name,
                "Ticker": ticker,
                "Kaufchance": kaufchance,
                "Risiko": risiko_text,
                "Einsatz": einsatz,
                "Signal": signal,
                "Score": round(score, 1),
                "Kurs €": round(kurs_euro, 2),
                "Trend 5T %": round(trend_5, 2),
                "RSI": round(rsi, 2),
                "Relative Stärke": rel_text,
                "Relative Stärke %": round(rel_wert, 2),
                "Trendqualität": trend_text,
                "EMA50": round(ema50, 2),
                "EMA200": round(ema200, 2),
                "Breakout": breakout_text,
                "52W Hoch": round(hoch_52w, 2),
                "Abstand Hoch %": round(abstand_hoch, 2),
                "Volumen": int(volumen),
                "Ø Volumen": int(volumen_avg),
            })

        except:
            fehler += 1
            continue

    df = pd.DataFrame(ergebnisse)

    if df.empty:
        return df, gescannt, fehler, 0

    df = df.sort_values(by="Score", ascending=False).head(20)
    df.insert(0, "Platz", range(1, len(df) + 1))

    dauer = round(time.time() - startzeit, 1)

    return df, gescannt, fehler, dauer


# ---------------------------------------------------
# Oberfläche
# ---------------------------------------------------

if st.button("🔄 Scanner aktualisieren"):
    with st.spinner("Scanner läuft... bitte warten."):
        df, gescannt, fehler, dauer = scanner_starten()

    if df.empty:
        st.error("Keine Daten gefunden.")
    else:
        st.success("Scanner fertig ✅")

        jetzt = datetime.now(ZoneInfo("Europe/Berlin")).strftime("%d.%m.%Y %H:%M:%S")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🌍 Aktien gescannt", gescannt)

        with col2:
            st.metric("🏆 Kandidaten", len(df))

        with col3:
            st.metric("⏱️ Scan-Dauer", f"{dauer} Sek.")

        with col4:
            st.metric("🕒 Uhrzeit", jetzt)

        st.subheader("🥇 Top 3")

        top3 = df.head(3)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("🥇 Platz 1", top3.iloc[0]["Aktie"], top3.iloc[0]["Kaufchance"])

        with c2:
            st.metric("🥈 Platz 2", top3.iloc[1]["Aktie"], top3.iloc[1]["Kaufchance"])

        with c3:
            st.metric("🥉 Platz 3", top3.iloc[2]["Aktie"], top3.iloc[2]["Kaufchance"])

        st.subheader("📱 Einfache Übersicht")

        hauptansicht = df[[
            "Platz",
            "Aktie",
            "Kaufchance",
            "Risiko",
            "Einsatz",
            "Signal"
        ]]

        st.dataframe(
            hauptansicht,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🔎 Details anzeigen")

        for _, row in df.iterrows():
            with st.expander(f"{row['Platz']}. {row['Aktie']} – {row['Signal']}"):
                st.write("**Ticker:**", row["Ticker"])
                st.write("**Kurs in Euro:**", row["Kurs €"])
                st.write("**Score:**", row["Score"])
                st.write("**Trend 5 Tage:**", str(row["Trend 5T %"]) + "%")
                st.write("**RSI:**", row["RSI"])
                st.write("**Relative Stärke:**", row["Relative Stärke"], f"({row['Relative Stärke %']}%)")
                st.write("**Trendqualität:**", row["Trendqualität"])
                st.write("**EMA50:**", row["EMA50"])
                st.write("**EMA200:**", row["EMA200"])
                st.write("**Breakout:**", row["Breakout"])
                st.write("**52-Wochen-Hoch:**", row["52W Hoch"])
                st.write("**Abstand zum Hoch:**", str(row["Abstand Hoch %"]) + "%")
                st.write("**Volumen:**", row["Volumen"])
                st.write("**Durchschnittsvolumen:**", row["Ø Volumen"])

        st.caption("Hinweis: Dieser Scanner liefert Analyse-Signale, keine garantierte Anlageberatung.")

else:
    st.info("Klicke auf „Scanner aktualisieren“, um aktuelle Daten zu laden.")
