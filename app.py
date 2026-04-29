import streamlit as st
from fpdf import FPDF
import io

# Configuration
st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches Pédagogiques")

# Formulaire
with st.expander("Configuration de la fiche", expanded=True):
    niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
    matiere = st.selectbox("Discipline / Matière", ["Français", "Mathématiques", "Éveil Scientifique", "EDHC", "Arts Plastiques", "EPS", "AEC"])
    lecon = st.text_input("Titre de la Leçon")
    seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE DÉTAILLÉE"):
    if lecon and seance:
        with st.spinner("L'IA rédige votre scénario pédagogique (Questions/Réponses/Résumé)..."):
            
            # --- STRUCTURE DE LA FICHE ---
            st.success("Fiche générée !")
            
            # Affichage écran pour vérification
            st.markdown(f"**Discipline :** {matiere} | **Niveau :** {niveau}")
            st.markdown(f"**Leçon :** {lecon}")
            st.markdown(f"**Séance :** {seance}")

            # Création du PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(200, 10, f"FICHE DE PREPARATION - {niveau}", ln=True, align='C')
            
            pdf.set_font("Arial", '', 11)
            pdf.cell(100, 8, f"Discipline : {matiere}", ln=False)
            pdf.cell(100, 8, f"Leçon : {lecon}", ln=True)
            pdf.cell(100, 8, f"Séance : {seance}", ln=True)
            pdf.ln(5)

            # ENTÊTE DU TABLEAU (Ordre corrigé)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(35, 10, "Etapes", 1)
            pdf.cell(75, 10, "Activites Maitre (Questions)", 1)
            pdf.cell(30, 10, "Strategies", 1) # Stratégie AVANT
            pdf.cell(50, 10, "Activites Eleves", 1) # Élèves APRÈS
            pdf.ln()

            # Exemple de contenu riche (Ce que l'IA produira)
            pdf.set_font("Arial", '', 9)
            
            # Ligne de développement avec Synthèse et Résumé inclus
            etapes = ["Dév: Manipulation", "Dév: Synthèse", "Dév: Résumé", "Conclusion: Eval"]
            contenu_maitre = [
                "Pose des questions d'observation : 'Que se passe-t-il si...?'",
                "Amène les élèves à confronter les résultats aux hypothèses.",
                "Dicte et écrit le résumé au tableau.",
                "Propose un exercice d'application."
            ]
            strategies = ["T. Collectif", "T. Groupe", "T. Collectif", "T. Individuel"]
            contenu_eleves = [
                "Répondent aux questions précisément.",
                "Valident ou rejettent les hypothèses.",
                "Recopient le résumé dans les cahiers.",
                "Traitent l'exercice."
            ]

            for i in range(len(etapes)):
                pdf.cell(35, 15, etapes[i], 1)
                pdf.multi_cell(75, 5, contenu_maitre[i], 1)
                # On revient à la position pour les colonnes suivantes
                curr_y = pdf.get_y()
                pdf.set_xy(120, curr_y - 15)
                pdf.cell(30, 15, strategies[i], 1)
                pdf.cell(50, 15, contenu_eleves[i], 1)
                pdf.ln()

            # BOUTON DE TÉLÉCHARGEMENT
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="⬇️ TÉLÉCHARGER LA FICHE EN PDF",
                data=pdf_output,
                file_name=f"Fiche_{lecon}.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Veuillez remplir les champs manquants.")
