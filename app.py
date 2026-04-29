import streamlit as st
from fpdf import FPDF

# Configuration
st.set_page_config(page_title="PrépaClasse CI", layout="centered")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches Pédagogiques APC")

# --- LE FORMULAIRE (BIEN VISIBLE AU CENTRE) ---
st.markdown("### 1. Informations de la fiche")
niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])

# Tes disciplines précises
discipline = st.selectbox("Discipline / Sous-Discipline", [
    "Grammaire", "Conjugaison", "Orthographe", "Vocabulaire", "Lecture", 
    "Exploitation de texte", "Expression Orale", "Science et Technologie", 
    "Mathématiques", "EDHC", "Histoire-Géographie", "Arts Plastiques", "AEC"
])

lecon = st.text_input("Titre de la Leçon (Ex: Les nombres de 0 à 1000)")
seance = st.text_input("Titre de la Séance (Ex: Comparer et ranger)")

# --- BOUTON DE GÉNÉRATION ---
if st.button("🚀 GÉNÉRER LA FICHE MAINTENANT"):
    if lecon and seance:
        st.divider()
        st.success(f"Fiche en cours de rédaction pour : {lecon}")

        # --- STRUCTURE OFFICIELLE ---
        
        # I. PRÉSENTATION
        st.markdown("### I. PRÉSENTATION")
        st.write(f"**Rappel / Mise en situation :** Le maître propose une activité de rappel sur la séance précédente et présente une situation de vie pour introduire la leçon sur {lecon}.")

        # II. DÉVELOPPEMENT
        st.markdown("### II. DÉVELOPPEMENT")
        st.markdown(f"""
        | Étapes | Activités Maître (Questions) | Stratégies | Activités Élèves |
        | :--- | :--- | :--- | :--- |
        | **Manipulation** | Pose des questions pour explorer {seance}. | Travail de Groupe | Manipulent et répondent aux questions. |
        | **Synthèse** | "Que peut-on conclure ?" | Travail Collectif | Établissent la règle avec le maître. |
        | **Résumé** | **A RETENIR :** [Texte du résumé ici] | Travail Collectif | Recopient la trace écrite. |
        """)

        # III. ÉVALUATION
        st.markdown("### III. ÉVALUATION")
        st.write(f"**Exercice :** Propose un exercice d'application sur {seance}.")

        # --- GÉNÉRATION DU PDF REMPLI ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, f"FICHE : {niveau}", ln=True, align='C')
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Discipline : {discipline}", ln=True)
        pdf.cell(200, 10, f"Leçon : {lecon}", ln=True)
        pdf.cell(200, 10, f"Séance : {seance}", ln=True)
        pdf.ln(10)

        # Contenu du PDF
        sections = [
            ("I. PRESENTATION", "Situation de rappel et mise en situation."),
            ("II. DEVELOPPEMENT", "Phase de recherche, de synthèse et trace écrite."),
            ("III. EVALUATION", "Exercice d'application immédiate.")
        ]
        for titre, texte in sections:
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, titre, 1, ln=True)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 10, texte)
            pdf.ln(5)

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button("⬇️ TÉLÉCHARGER LA FICHE PDF", data=pdf_output, file_name=f"Fiche_{lecon}.pdf")
    else:
        st.warning("⚠️ S'il te plaît, remplis le Titre de la leçon et de la séance avant d'appuyer sur le bouton.")

        st.markdown(f"""
        | Étapes | Activités Maître (Questions/Consignes) | Stratégies | Activités Élèves (Réponses attendues) |
        | :--- | :--- | :--- | :--- |
        | **Manipulation / Recherche** | Questions précises : 'Que voyez-vous ?' 'Comment faire pour...?' | Travail de groupe | Manipulent, observent et répondent. |
        | **Synthèse** | Questions de jonction : 'Alors, que retient-on de nos essais ?' | Travail Collectif | Concluent et valident les résultats. |
        | **Résumé** | Présentation de la trace écrite finale : 'A retenir...' | Travail Collectif | Participent et recopient le texte. |
        """)

        # III. ÉVALUATION
        st.markdown("### III. ÉVALUATION")
        st.write("**Exercice d'application :** [Exercice précis ici]")

        # --- GÉNÉRATION DU PDF RÉELLEMENT REMPLI ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, f"FICHE DE PREPARATION : {niveau}", ln=True, align='C')
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 8, f"Discipline : {discipline} | Leçon : {lecon}", ln=True)
        pdf.cell(0, 8, f"Séance : {seance}", ln=True)
        pdf.ln(5)

        # Remplissage automatique des sections pour éviter le PDF vide
        sections = [
            ("I. PRESENTATION", "Rappel et mise en situation pédagogique."),
            ("II. DEVELOPPEMENT", "Contient la manipulation, la synthèse et le résumé."),
            ("III. EVALUATION", "Exercices de vérification des acquis.")
        ]

        for titre, texte in sections:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(240, 240, 240)
            pdf.cell(0, 10, titre, ln=True, fill=True)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 8, texte)
            pdf.ln(2)

        pdf_output = pdf.output(dest='S').encode('latin-1')
        st.download_button(
            label="⬇️ TÉLÉCHARGER LA FICHE PDF",
            data=pdf_output,
            file_name=f"Fiche_{discipline}_{lecon}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Veuillez remplir les informations manquantes.")
