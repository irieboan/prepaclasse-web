import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# CONFIGURATION CORRIGÉE
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # On utilise cette syntaxe précise pour éviter l'erreur 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erreur de configuration : {e}")


st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches APC")

# --- FORMULAIRE ---
niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
discipline = st.selectbox("Discipline", ["Grammaire", "Conjugaison", "Orthographe", "Science et Technologie", "Mathématiques", "EDHC"])
lecon = st.text_input("Titre de la Leçon")
seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE COMPLÈTE"):
    if lecon and seance:
        # Le "Prompt" pour forcer l'IA à remplir les cases
        prompt = f"Rédige une fiche pédagogique APC (Côte d'Ivoire) pour le niveau {niveau}. Discipline: {discipline}. Leçon: {lecon}. Séance: {seance}. Inclus : I. Présentation (Rappel/Situation), II. Développement (Tableau avec Étapes, Activités Maître, Stratégies, Activités Élèves), III. Évaluation."
        
        with st.spinner("Rédaction en cours..."):
            try:
                response = model.generate_content(prompt)
                contenu = response.text
                st.markdown(contenu)
                
                # Option de téléchargement
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=contenu.encode('latin-1', 'ignore').decode('latin-1'))
                st.download_button("⬇️ Télécharger le PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="fiche.pdf")
            except Exception as e:
                st.error(f"L'IA n'a pas pu répondre : {e}")
