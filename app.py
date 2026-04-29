import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# 1. RECHERCHE AUTOMATIQUE DU MODÈLE
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    try:
        # On demande à Google la liste des modèles valides pour ta clé
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # On choisit le plus récent (1.5 flash) s'il existe, sinon le premier de la liste
        if 'models/gemini-1.5-flash' in available_models:
            selected_model = 'models/gemini-1.5-flash'
        else:
            selected_model = available_models[0]
            
        model = genai.GenerativeModel(selected_model)
    except Exception as e:
        st.error(f"Impossible de lister les modèles : {e}")
else:
    st.error("Clé API manquante dans les Secrets.")

st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur Intelligent (Mode Auto)")

# --- FORMULAIRE ---
niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
discipline = st.selectbox("Discipline", ["Grammaire", "Conjugaison", "Orthographe", "Science", "Maths", "EDHC"])
lecon = st.text_input("Titre de la Leçon")
seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE COMPLÈTE"):
    if lecon and seance:
        prompt = f"Rédige une fiche pédagogique APC (Côte d'Ivoire) complète. Niveau: {niveau}, Discipline: {discipline}, Leçon: {lecon}, Séance: {seance}. Inclus : I. Présentation, II. Développement avec un tableau (Étapes, Activités Maître, Stratégies, Activités Élèves), III. Évaluation."
        
        with st.spinner(f"Connexion au modèle {selected_model}..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
                # PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 10, txt=response.text.encode('latin-1', 'ignore').decode('latin-1'))
                st.download_button("⬇️ Télécharger", data=pdf.output(dest='S').encode('latin-1'), file_name="fiche.pdf")
            except Exception as e:
                st.error(f"Erreur de génération : {e}")
