import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="PrépaClasse CI", layout="wide")

st.title("📝 PrépaClasse CI")
st.subheader("Générateur de Fiches Pédagogiques (Version Officielle)")

# --- FORMULAIRE AVEC LES VRAIES DISCIPLINES ---
with st.sidebar:
    st.header("Paramètres")
    niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
    
    # Liste précise selon nos échanges
    discipline = st.selectbox("Sous-Discipline", [
        "Grammaire", "Conjugaison", "Orthographe", "Vocabulaire", "Lecture", 
        "Exploitation de texte", "Expression Orale", "Science et Technologie", 
        "Mathématiques", "EDHC", "Histoire-Géographie", "Arts Plastiques", "AEC"
    ])
    
    lecon = st.text_input("Titre de la Leçon")
    seance = st.text_input("Titre de la Séance")

if st.button("🚀 GÉNÉRER LA FICHE DÉTAILLÉE"):
    if lecon and seance:
        # Ici on simule le contenu riche que l'IA doit produire
        st.success("Génération en cours...")

        # --- STRUCTURE DES 3 PHASES ---
        
        # I. PRÉSENTATION
        st.markdown("### I. PRÉSENTATION")
        st.write("**Rappel / Mise en situation :** [Contenu détaillé à venir]")

        # II. DÉVELOPPEMENT (Tableau avec Stratégie AVANT Activités Élèves)
        st.markdown("### II. DÉVELOPPEMENT")
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
