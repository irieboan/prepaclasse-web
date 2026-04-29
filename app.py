import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# Configuration simplifiée pour éviter l'erreur 404
try:
    # On utilise le nom direct du modèle sans préfixe
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # On ajoute cette ligne pour forcer la version de l'API si besoin
    # Mais normalement Gemini 1.5 s'en charge seul
except Exception as e:
    st.error(f"Erreur de configuration : {e}")
    
st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches APC Intelligent")

# --- FORMULAIRE ---
st.markdown("### 📋 Détails de la séance")
niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
discipline = st.selectbox("Discipline", [
    "Grammaire", "Conjugaison", "Orthographe", "Vocabulaire", "Lecture", 
    "Science et Technologie", "Mathématiques", "EDHC", "AEC"
])
lecon = st.text_input("Titre de la Leçon")
seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE COMPLÈTE"):
    if lecon and seance:
        # L'ordre précis pour l'IA (le Prompt)
        prompt = f"""
        Rédige une fiche pédagogique APC pour la Côte d'Ivoire.
        Niveau: {niveau}. Discipline: {discipline}.
        Leçon: {lecon}. Séance: {seance}.
        
        STRUCTURE OBLIGATOIRE :
        I. PRÉSENTATION : Propose un rappel et une situation de vie motivante.
        II. DÉVELOPPEMENT : Crée un tableau avec les colonnes suivantes :
        - Étapes (Manipulation, Synthèse, Résumé)
        - Activités Maître (Questions précises et consignes)
        - Stratégies (Travail de groupe ou collectif)
        - Activités Élèves (Réponses attendues)
        III. ÉVALUATION : Propose un exercice d'application concret.
        
        Rédige le contenu complet de chaque partie, surtout le résumé (trace écrite).
        """
        
        with st.spinner("L'IA rédige votre fiche complète..."):
            try:
                response = model.generate_content(prompt)
                texte_fiche = response.text
                
                # Affichage à l'écran
                st.markdown("---")
                st.markdown(texte_fiche)
                
                # Création du PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, f"FICHE PEDAGOGIQUE : {niveau}", ln=True, align='C')
                pdf.set_font("Arial", size=11)
                # Nettoyage du texte pour le PDF
                pdf_text = texte_fiche.encode('latin-1', 'ignore').decode('latin-1')
                pdf.multi_cell(0, 10, txt=pdf_text)
                
                pdf_output = pdf.output(dest='S').encode('latin-1')
                st.download_button("⬇️ TÉLÉCHARGER LA FICHE (PDF)", data=pdf_output, file_name=f"Fiche_{lecon}.pdf")
            except Exception as e:
                st.error(f"Une erreur est survenue : {e}")
    else:
        st.warning("Veuillez remplir le titre de la leçon et de la séance.")
