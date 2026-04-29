import streamlit as st
from fpdf import FPDF

# Configuration de la page
st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches Pédagogiques APC")

# --- FORMULAIRE AU CENTRE ---
st.markdown("### 1. Informations de la fiche")
niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])

# Sous-disciplines précises
discipline = st.selectbox("Discipline / Sous-Discipline", [
    "Grammaire", "Conjugaison", "Orthographe", "Vocabulaire", "Lecture", 
    "Exploitation de texte", "Expression Orale", "Science et Technologie", 
    "Mathématiques", "EDHC", "Histoire-Géographie", "Arts Plastiques", "AEC"
])

lecon = st.text_input("Titre de la Leçon (Ex: Les mélanges)")
seance = st.text_input("Titre de la Séance (Ex: Eau et Sable)")

# --- BOUTON DE GÉNÉRATION ---
if st.button("🚀 GÉNÉRER LA FICHE MAINTENANT"):
    if lecon and seance:
        st.divider()
        
        # I. PRÉSENTATION
        st.markdown("### I. PRÉSENTATION")
        st.write(f"**Rappel / Mise en situation :** Activité de rappel sur la séance précédente et situation de vie pour introduire {lecon}.")

        # II. DÉVELOPPEMENT
        st.markdown("### II. DÉVELOPPEMENT")
        st.markdown(f"""
        | Étapes | Activités Maître (Questions) | Stratégies | Activités Élèves |
        | :--- | :--- | :--- | :--- |
        | **Manipulation** | Questions d'observation sur {seance}. | Travail de Groupe | Manipulent et répondent. |
        | **Synthèse** | "Que peut-on dire de ces résultats ?" | Travail Collectif | Concluent avec le maître. |
        | **Résumé** | **A RETENIR :** [Trace écrite détaillée] | Travail Collectif | Recopient le résumé. |
        """)

        # III. ÉVALUATION
        st.markdown("### III. ÉVALUATION")
        st.write(f"**Exercice :** Activité individuelle pour vérifier les acquis sur {seance}.")

        # --- PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, f"FICHE : {niveau}", ln=True, align='C')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Discipline : {discipline} | Lecon : {lecon}", ln=True)
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("⬇️ TÉLÉCHARGER LE PDF", data=pdf_output, file_name=f"Fiche_{lecon}.pdf")
    else:
        st.warning("⚠️ Remplis le titre de la leçon et de la séance.")
