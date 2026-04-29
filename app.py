import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# Configuration de l'IA avec ta clé secrète
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches Pédagogiques (IA)")

# Formulaire
niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
discipline = st.selectbox("Discipline", ["Grammaire", "Conjugaison", "Orthographe", "Science et Technologie", "Mathématiques", "EDHC"])
lecon = st.text_input("Titre de la Leçon")
seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE DÉTAILLÉE"):
    if lecon and seance:
        prompt = f"Rédige une fiche pédagogique APC pour le niveau {niveau} en {discipline}. Leçon: {lecon}. Séance: {seance}. Respecte les 3 phases : I. Présentation, II. Développement (avec tableau Étapes, Activités Maître, Stratégies, Activités Élèves incluant Manipulation et Résumé), III. Évaluation."
        
        with st.spinner("L'IA prépare votre fiche..."):
            response = model.generate_content(prompt)
            texte_fiche = response.text
            
            st.markdown(texte_fiche)
            
            # Export PDF simple
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=texte_fiche.encode('latin-1', 'ignore').decode('latin-1'))
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("⬇️ Télécharger le PDF", data=pdf_output, file_name=f"Fiche_{lecon}.pdf")
    else:
        st.error("Remplis le titre de la leçon !")
