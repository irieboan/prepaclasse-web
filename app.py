import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="PrépaClasse CI", layout="wide")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur Automatique de Fiches (Canevas Officiel)")

# --- FORMULAIRE ---
st.markdown("### 📋 Informations de la leçon")
col1, col2 = st.columns(2)
with col1:
    niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
    discipline = st.selectbox("Discipline", ["Science et Technologie", "Mathématiques", "Grammaire", "Conjugaison", "Orthographe", "EDHC"])
with col2:
    lecon = st.text_input("Titre de la Leçon")
    seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE COMPLÈTE"):
    if lecon and seance:
        # Simulation d'un contenu riche (en attendant la clé API)
        st.success("Fiche générée selon le modèle APC ivoirien !")
        
        # --- AFFICHAGE DES 3 PHASES ---
        st.markdown("---")
        st.markdown(f"## I. PRÉSENTATION")
        st.write(f"**Rappel :** Le maître interroge les élèves sur la séance précédente.")
        st.write(f"**Situation :** Une situation de vie réelle introduisant '{lecon}'.")

        st.markdown("## II. DÉVELOPPEMENT")
        st.markdown(f"""
        | Étapes | Activités Maître (Questions) | Stratégies | Activités Élèves |
        | :--- | :--- | :--- | :--- |
        | **Manipulation** | Pose des questions d'observation sur {seance}. | Travail de Groupe | Manipulent et répondent. |
        | **Synthèse** | "Que peut-on dire après nos essais ?" | Travail Collectif | Concluent avec le maître. |
        | **Résumé** | **A RETENIR :** Le maître écrit la trace écrite. | Travail Collectif | Recopient le résumé. |
        """)

        st.markdown("## III. ÉVALUATION")
        st.write(f"**Exercice d'application :** Un exercice pratique sur {seance}.")

        # --- GÉNÉRATION DU PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"FICHE PEDAGOGIQUE : {niveau}", ln=True, align='C')
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 10, f"Discipline : {discipline} | Leçon : {lecon}", ln=True)
        pdf.cell(0, 10, f"Séance : {seance}", ln=True)
        pdf.ln(5)

        # Contenu détaillé dans le PDF
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "I. PRESENTATION", 1, ln=True, fill=False)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 8, f"Rappel et mise en situation sur {lecon}.")
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "II. DEVELOPPEMENT", 1, ln=True)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 8, "1. Manipulation : Recherche et observation.\n2. Synthèse : Mise en commun.\n3. Résumé : Trace écrite élaborée avec les élèves.")
        
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "III. EVALUATION", 1, ln=True)
        pdf.multi_cell(0, 8, f"Exercice d'application sur {seance}.")

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("⬇️ TÉLÉCHARGER LA FICHE PDF", data=pdf_output, file_name=f"Fiche_{lecon}.pdf")
    else:
        st.error("⚠️ S'il te plaît, écris le titre de la leçon.")
