import streamlit as st

# Data stroje
stroje = [
    {"nazev": "Bagr CAT 305", "cena_za_den": 2500, "dostupnost": "Ano"},
    {"nazev": "Vibrační deska Wacker", "cena_za_den": 900, "dostupnost": "Ne"},
    {"nazev": "Nůžková plošina Genie", "cena_za_den": 1800, "dostupnost": "Ano"},
    {"nazev": "Kompresor Atlas Copco", "cena_za_den": 1500, "dostupnost": "Ano"},
    {"nazev": "Míchačka Altrad", "cena_za_den": 400, "dostupnost": "Ne"},
    {"nazev": "Řezačka betonu Husqvarna", "cena_za_den": 1300, "dostupnost": "Ano"}
]

# Data klienti
klienti = [
    {"nazev": "Stavmont s.r.o.", "sleva": 0.10},
    {"nazev": "Betonservis a.s.", "sleva": 0.05},
    {"nazev": "Kamenstav s.r.o.", "sleva": 0.08}
]

st.set_page_config(page_title="Půjčovna strojů", layout="centered")
st.title("Půjčovna stavebních strojů")

# Výběr klienta
klient_nazev = st.selectbox("Vyber klienta:", [k["nazev"] for k in klienti])
sleva = next(k["sleva"] for k in klienti if k["nazev"] == klient_nazev)

# Výběr stroje
stroj_nazev = st.selectbox("Vyber stroj:", [s["nazev"] for s in stroje])
vybrany_stroj = next(s for s in stroje if s["nazev"] == stroj_nazev)

# Počet dní
pocet_dni = st.slider("Počet dní:", min_value=1, max_value=31, value=1)

# Výpočet ceny
if vybrany_stroj["dostupnost"] != "Ano":
    st.warning("Tento stroj není momentálně dostupný.")
else:
    cena_celkem = vybrany_stroj["cena_za_den"] * pocet_dni * (1 - sleva)
    st.success(f"Cena celkem: {cena_celkem:,.0f} Kč")
