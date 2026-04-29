import streamlit as st
from fpdf import FPDF

# Configuration
st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches Pédagogiques APC")

# --- FORMULAIRE ---
with st.container():
    niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
    matiere = st.selectbox("Discipline", ["Français", "Mathématiques", "Éveil Scientifique", "EDHC", "AEC"])
    lecon = st.text_input("Titre de la Leçon")
    seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE DÉTAILLÉE"):
    if lecon and seance:
        # Simulation de la rédaction détaillée par l'IA
        st.success("Fiche rédigée avec succès !")
        
        # --- AFFICHAGE ÉCRAN ---
        st.markdown("### I. PRÉSENTATION")
        st.write("**Rappel / Mise en situation :** Le maître présente une situation pour susciter l'intérêt.")

        st.markdown("### II. DÉVELOPPEMENT")
        # Tableau avec l'ordre : Étapes > Activités Maître > Stratégies > Activités Élèves
        st.markdown("""
        | Étapes | Activités Maître (Questions) | Stratégies | Activités Élèves |
        | :--- | :--- | :--- | :--- |
        | **Manipulation** | Pose des questions précises sur l'expérience... | Travail de groupe | Observent et manipulent |
        | **Synthèse** | "Que peut-on dire de... ?" | Travail Collectif | Concluent avec le maître |
        | **Résumé** | Présente la trace écrite au tableau | Travail Collectif | Recopient dans le cahier |
        """)

        st.markdown("### III. ÉVALUATION")
        st.write("**Exercice :** Propose une activité pour vérifier les acquis.")

        # --- GÉNÉRATION DU VRAI PDF ---
        pdf = FPDF()
        pdf.add_page()
        
        # En-tête
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, f"FICHE PEDAGOGIQUE : {lecon.upper()}", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"Niveau : {niveau} | Discipline : {matiere}", ln=True, align='C')
        pdf.ln(10)

        # Contenu
        sections = [
            ("I. PRESENTATION", "Rappel et mise en situation de la leçon."),
            ("II. DEVELOPPEMENT", "Phase de manipulation, synthèse des résultats et trace écrite (Résumé)."),
            ("III. EVALUATION", "Exercices d'application et de vérification.")
        ]

        for titre, corps in sections:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, titre, ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 8, corps)
            pdf.ln(5)

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("⬇️ TÉLÉCHARGER LA FICHE COMPLÈTE (PDF)", data=pdf_output, file_name=f"Fiche_{lecon}.pdf")
    else:
        st.error("Veuillez remplir le titre de la leçon.")
