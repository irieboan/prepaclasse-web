import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# CONFIGURATION AUTO-ADAPTATIVE
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # On cherche le premier modèle disponible qui permet de générer du texte
    models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if models:
        # On prend le premier modèle trouvé (souvent gemini-1.5-flash ou pro)
        model_name = models[0].name
        model = genai.GenerativeModel(model_name)
    else:
        st.error("Aucun modèle n'a été trouvé pour cette clé API.")
except Exception as e:
    st.error(f"Erreur de connexion : {e}")


st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches APC")

# --- FORMULAIRE ---
niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
discipline = st.selectbox("Discipline", ["Grammaire", "Conjugaison", "Orthographe", "Science", "Maths", "EDHC"])
lecon = st.text_input("Titre de la Leçon")
seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE COMPLÈTE"):
    if lecon and seance:
        prompt = f"Rédige une fiche pédagogique APC pour la Côte d'Ivoire. Niveau: {niveau}. Discipline: {discipline}. Leçon: {lecon}. Séance: {seance}. Structure: I. Présentation, II. Développement (avec tableau détaillé), III. Évaluation."
        
        with st.spinner("Rédaction en cours..."):
            try:
                # Appel direct à la génération
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
                # Bouton PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
                st.download_button("⬇️ Télécharger PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="fiche.pdf")
            except Exception as e:
                st.error(f"Désolé, l'IA a rencontré une erreur : {e}")
    else:
        st.warning("Veuillez remplir tous les champs.")
