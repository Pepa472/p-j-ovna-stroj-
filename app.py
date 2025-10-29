import streamlit as st
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- Data stroje ---
stroje = [
    {"nazev": "Bagr CAT 305", "cena_za_den": 2500, "dostupnost": "Ano"},
    {"nazev": "Vibrační deska Wacker", "cena_za_den": 900, "dostupnost": "Ano"},
    {"nazev": "Nůžková plošina Genie", "cena_za_den": 1800, "dostupnost": "Ano"},
    {"nazev": "Kompresor Atlas Copco", "cena_za_den": 1500, "dostupnost": "Ano"},
    {"nazev": "Míchačka Altrad", "cena_za_den": 400, "dostupnost": "Ano"},
    {"nazev": "Řezačka betonu Husqvarna", "cena_za_den": 1300, "dostupnost": "Ano"}
]

# --- Data klienti ---
klienti = [
    {"nazev": "Stavmont s.r.o.", "ico": "12345678", "adresa": "Praha 1, Ulice 1", "kontakt": "Jan Novák", "sleva": 0.10},
    {"nazev": "Betonservis a.s.", "ico": "87654321", "adresa": "Brno, Náměstí 2", "kontakt": "Petr Svoboda", "sleva": 0.05},
    {"nazev": "Kamenstav s.r.o.", "ico": "11223344", "adresa": "Ostrava, Ulice 3", "kontakt": "Lucie Králová", "sleva": 0.08}
]

st.set_page_config(page_title="Půjčovna strojů - faktura", layout="wide")
st.title("Půjčovna stavebních strojů – fakturace")

# --- Výběr klienta ---
klient_nazev = st.selectbox("Vyber klienta:", [k["nazev"] for k in klienti])
vybrany_klient = next(k for k in klienti if k["nazev"] == klient_nazev)

st.subheader("Údaje o klientovi")
st.write(f"IČO: {vybrany_klient['ico']}")
st.write(f"Adresa: {vybrany_klient['adresa']}")
st.write(f"Kontaktní osoba: {vybrany_klient['kontakt']}")

# --- Datum vystavení ---
datum = st.date_input("Datum vystavení:", value=date.today())

# --- Výběr strojů ---
st.subheader("Vyber stroje")
vybrane_stroje = st.multiselect(
    "Vyber jeden nebo více strojů:",
    options=[s["nazev"] for s in stroje]
)

# Počet dní pro každý stroj
pocet_dni_dict = {}
for stroj_nazev in vybrane_stroje:
    pocet_dni_dict[stroj_nazev] = st.number_input(f"Počet dní pro {stroj_nazev}:", min_value=1, max_value=31, value=1)

# --- Výpočet ceny ---
if vybrane_stroje:
    celkem_bez_dph = 0
    st.subheader("Faktura")
    st.write(f"Datum vystavení: {datum}")
    st.write(f"Klient: {vybrany_klient['nazev']}")
    for stroj_nazev in vybrane_stroje:
        stroj = next(s for s in stroje if s["nazev"] == stroj_nazev)
        dny = pocet_dni_dict[stroj_nazev]
        cena = stroj["cena_za_den"] * dny
        cena_po_sleve = cena * (1 - vybrany_klient["sleva"])
        celkem_bez_dph += cena_po_sleve
        st.write(f"{stroj_nazev} – {dny} dní – Cena po slevě: {cena_po_sleve:,.0f} Kč")

    dph = celkem_bez_dph * 0.21
    celkem_s_dph = celkem_bez_dph + dph
    st.markdown(f"**Celkem bez DPH:** {celkem_bez_dph:,.0f} Kč")
    st.markdown(f"**DPH 21 %:** {dph:,.0f} Kč")
    st.markdown(f"### Celkem k úhradě: {celkem_s_dph:,.0f} Kč")

    # --- Export do PDF ---
    if st.button("Vytisknout / stáhnout fakturu PDF"):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height-50, "Faktura – Půjčovna stavebních strojů")
        c.setFont("Helvetica", 12)
        c.drawString(50, height-80, f"Datum vystavení: {datum}")
        c.drawString(50, height-100, f"Klient: {vybrany_klient['nazev']}")
        c.drawString(50, height-120, f"IČO: {vybrany_klient['ico']}")
        c.drawString(50, height-140, f"Adresa: {vybrany_klient['adresa']}")
        c.drawString(50, height-160, f"Kontaktní osoba: {vybrany_klient['kontakt']}")

        y = height-200
        for stroj_nazev in vybrane_stroje:
            stroj = next(s for s in stroje if s["nazev"] == stroj_nazev)
            dny = pocet_dni_dict[stroj_nazev]
            cena = stroj["cena_za_den"] * dny
            cena_po_sleve = cena * (1 - vybrany_klient["sleva"])
            c.drawString(50, y, f"{stroj_nazev} – {dny} dní – Cena po slevě: {cena_po_sleve:,.0f} Kč")
            y -= 20

        c.drawString(50, y-20, f"Celkem bez DPH: {celkem_bez_dph:,.0f} Kč")
        c.drawString(50, y-40, f"DPH 21%: {dph:,.0f} Kč")
        c.drawString(50, y-60, f"Celkem k úhradě: {celkem_s_dph:,.0f} Kč")

        c.showPage()
        c.save()
        buffer.seek(0)

        st.download_button(
            label="Stáhnout PDF",
            data=buffer,
            file_name="faktura.pdf",
            mime="application/pdf"
        )
