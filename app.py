import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Configuration avec forçage de version
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # On utilise une méthode de sélection plus simple
    model = genai.GenerativeModel('gemini-pro') 
except Exception as e:
    st.error(f"Erreur de configuration : {e}")

st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches APC")

niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
discipline = st.selectbox("Discipline", ["Grammaire", "Conjugaison", "Orthographe", "Science", "Maths", "EDHC"])
lecon = st.text_input("Titre de la Leçon")
seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE COMPLÈTE"):
    if lecon and seance:
        prompt = f"Rédige une fiche pédagogique APC pour la Côte d'Ivoire. Niveau: {niveau}. Discipline: {discipline}. Leçon: {lecon}. Séance: {seance}. Structure: I. Présentation, II. Développement (avec tableau), III. Évaluation."
        
        # On ajoute un conteneur pour voir si l'IA répond
        placeholder = st.empty()
        placeholder.info("Connexion au cerveau de l'IA en cours...")
        
        try:
            response = model.generate_content(prompt)
            placeholder.empty()
            st.markdown(response.text)
            
            # Export PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
            st.download_button("⬇️ Télécharger PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="fiche.pdf")
        except Exception as e:
            placeholder.empty()
            st.error(f"L'IA est indisponible pour le moment : {e}")
    else:
        st.warning("Veuillez remplir tous les champs.")
