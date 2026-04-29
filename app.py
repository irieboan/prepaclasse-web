import streamlit as st
import pandas as pd
import time

# =========================================================
# 1. CONFIGURATION DE BASE
# =========================================================
st.set_page_config(page_title="PrépaClasse Côte d'Ivoire", layout="wide", initial_sidebar_state="expanded")

# Grille tarifaire exacte validée
TARIFS = {
    "1 JOUR": "500 FCFA",
    "1 SEMAINE": "1 000 FCFA",
    "1 MOIS": "3 000 FCFA",
    "1 TRIMESTRE": "7 000 FCFA"
}

# =========================================================
# 2. LOGIQUE DE SÉCURITÉ ET PAIEMENT
# =========================================================
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'essai_fait' not in st.session_state:
    st.session_state.essai_fait = False

# Écran de verrouillage (Le Péage)
if not st.session_state.auth:
    st.title("🔐 ESPACE SÉCURISÉ PRÉPACLASSE")
    
    # Zone d'essai gratuit
    if not st.session_state.essai_fait:
        with st.container():
            st.info("🎁 OFFRE DE BIENVENUE : Vous avez droit à un (1) essai gratuit complet.")
            if st.button("🚀 ACTIVER MON ESSAI GRATUIT MAINTENANT"):
                st.session_state.essai_fait = True
                st.session_state.auth = True
                st.rerun()

    st.write("---")
    st.subheader("💳 ABONNEMENT ET TARIFS")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("JOURNALIER", TARIFS["1 JOUR"]); st.button("Choisir 1J", key="pay1")
    with col2: st.metric("HEBDOMADAIRE", TARIFS["1 SEMAINE"]); st.button("Choisir 1S", key="pay2")
    with col3: st.metric("MENSUEL", TARIFS["1 MOIS"]); st.button("Choisir 1M", key="pay3")
    with col4: st.metric("TRIMESTRIEL", TARIFS["1 TRIMESTRE"]); st.button("Choisir 1T", key="pay4")

    st.write("---")
    st.markdown("### 🔑 DÉJÀ ABONNÉ ?")
    code_activation = st.text_input("Entrez votre code d'accès reçu après paiement :", type="password")
    if st.button("DÉVERROUILLER L'APPLICATION"):
        if code_activation == "PREPA225": # Code maître pour test
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Code incorrect ou expiré.")
    st.stop()

# =========================================================
# 3. INTERFACE GÉNÉRATION (LE "CERVEAU")
# =========================================================
st.title("📝 GÉNÉRATEUR DE FICHE PÉDAGOGIQUE")
st.caption("Application officielle pour les instituteurs de Côte d'Ivoire")

with st.sidebar:
    st.header("👤 MON COMPTE")
    st.write("Statut : **Abonnement Actif**")
    if st.button("🔴 QUITTER / EFFACER LA SESSION"):
        st.session_state.auth = False
        st.rerun()

# Saisie des informations de base
with st.container():
    c1, c2, c3 = st.columns([1, 2, 2])
    with c1:
        niveau = st.selectbox("Niveau", ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"])
    with c2:
        lecon = st.text_input("Titre de la Leçon", placeholder="Ex: Les mélanges")
    with c3:
        seance = st.text_input("Titre de la Séance", placeholder="Ex: Le mélange eau et sable")

# Bouton magique
if st.button("🪄 GÉNÉRER LA FICHE AVEC L'IA"):
    if lecon and seance:
        with st.spinner("L'IA analyse vos documents H-A-P-C..."):
            time.sleep(2) # Simulation de réflexion
            # Contenu généré (L'IA suit ton canevas Sciences)
            st.session_state.fiche_data = {
                "constat": f"Les élèves observent un verre contenant de l'eau et du sable. Ils remarquent que le sable tombe au fond.",
                "problème": "Comment peut-on séparer le sable de l'eau ?",
                "titre_final": seance.upper(),
                "hypotheses": "1. On peut utiliser un tamis.\n2. On peut laisser reposer longtemps.",
                "tableau": [
                    ["Vérification", "Expérience de filtration et décantation", "TG", "Les élèves manipulent le matériel."],
                    ["Validation", "Mise en commun des observations", "TC", "Les groupes comparent leurs résultats."],
                    ["Synthèse", "Rédaction de la règle générale", "TC", "Accord sur la méthode de séparation."],
                    ["Élargissement", "Explication sur les mélanges hétérogènes", "TC", "Écoutent les précisions du maître."]
                ],
                "resume": "Pour séparer le sable de l'eau, on utilise la décantation ou la filtration...",
                "evaluation": "Coche la bonne réponse : Pour séparer l'eau du sable, j'utilise : [] Un aimant [] Un filtre."
            }
    else:
        st.error("Veuillez saisir les titres de la leçon et de la séance.")

# =========================================================
# 4. ZONE D'ÉDITION (LE "CHANT" DES CASES)
# =========================================================
if 'fiche_data' in st.session_state:
    fd = st.session_state.fiche_data
    
    st.header("I. PHASE DE PRÉSENTATION")
    constat_edit = st.text_area("1. Constat", fd["constat"])
    probleme_edit = st.text_area("2. Problème", fd["problème"])
    titre_edit = st.text_input("3. Titre (Découvert par les élèves)", fd["titre_final"])
    hypo_edit = st.text_area("4. Émission des Hypothèses", fd["hypotheses"])

    st.header("II. PHASE DE DÉVELOPPEMENT")
    st.info("💡 Cliquez dans une case pour modifier les activités ou les stratégies.")
    df = pd.DataFrame(fd["tableau"], columns=["Étapes", "Activités Maître", "Stratégies", "Activités Élèves"])
    # Tableau dynamique : Stratégies au milieu
    edited_df = st.data_editor(df, use_container_width=True, hide_index=True)

    st.header("III. PHASE DE CONCLUSION")
    resume_edit = st.text_area("Résumé (Synthèse)", fd["resume"])
    eval_edit = st.text_area("Évaluation", fd["evaluation"])

    # =========================================================
    # 5. SORTIE FINALE (L'IMPRESSION)
    # =========================================================
    st.write("---")
    if st.button("🖨️ IMPRIMER LA FICHE (FORMAT A4 PDF)"):
        st.success("Génération du fichier PDF en cours...")
        st.info("Le document sera téléchargé automatiquement.")
