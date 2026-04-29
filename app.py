import streamlit as st
from fpdf import FPDF

# Configuration de la page
st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches Pédagogiques APC")

# --- FORMULAIRE ---
with st.container():
    niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
    matiere = st.selectbox("Discipline", ["Français", "Mathématiques", "Éveil Scientifique", "EDHC", "AEC"])
    lecon = st.text_input("Titre de la Leçon")
    seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE OFFICIELLE"):
    if lecon and seance:
        st.success("Fiche générée selon la structure APC !")
        
        # --- PHASE I : PRÉSENTATION ---
        st.markdown("### I. PRÉSENTATION")
        st.info("Rappel / Mise en situation")

        # --- PHASE II : DÉVELOPPEMENT ---
        st.markdown("### II. DÉVELOPPEMENT")
        st.write("*(Inclut : Manipulation, Synthèse et Résumé)*")
        
        # Le tableau avec l'ordre : Étapes > Activités Maître > Stratégies > Activités Élèves
        col1, col2, col3, col4 = st.columns([1, 2, 1, 2])
        col1.write("**Étapes**")
        col2.write("**Activités Maître**")
        col3.write("**Stratégies**")
        col4.write("**Activités Élèves**")
        st.divider()

        # --- PHASE III : ÉVALUATION ---
        st.markdown("### III. ÉVALUATION")
        st.write("Exercices d'application immédiate.")

        # --- BOUTON PDF ---
        # Note : Assure-toi d'avoir créé le fichier requirements.txt avec 'fpdf' dedans
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, f"FICHE PEDAGOGIQUE : {lecon}", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "I. PRESENTATION", ln=True)
        pdf.cell(200, 10, "II. DEVELOPPEMENT", ln=True)
        pdf.cell(200, 10, "III. EVALUATION", ln=True)

        try:
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("⬇️ TÉLÉCHARGER LA FICHE (PDF)", data=pdf_output, file_name=f"Fiche_{lecon}.pdf")
        except:
            st.warning("Pour activer le téléchargement PDF, n'oublie pas d'ajouter le fichier requirements.txt sur GitHub.")
    else:
        st.error("Veuillez remplir les champs.")
