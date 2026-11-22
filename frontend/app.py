import os
import requests
import streamlit as st

st.set_page_config(
    page_title="Entretien Garanti — Accueil",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("API_BASE_URL", "http://backend:8000")

# Initialisation de l'état de session
if "agent_state" not in st.session_state:
    st.session_state.agent_state = "ACTIF"
if "current_plan" not in st.session_state:
    st.session_state.current_plan = "Découverte"
if "quota_used" not in st.session_state:
    st.session_state.quota_used = (0, 5)

# ==============================================================================
# BARRE LATÉRALE : NAVIGATION & ÉTAT SYSTÈME
# ==============================================================================
with st.sidebar:
    st.title("🎯 Entretien Garanti")
    st.caption("Agent IA supervisé de candidature")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Accueil (Home)",
            "👤 Compte & Consentement",
            "📄 Mon CV & Profil",
            "🔍 Offres recommandées",
            "✉️ Mes candidatures",
        ],
        index=0,
    )

    st.divider()
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            st.success("API Backend : Connectée")
        else:
            st.warning(f"API Backend : Code {response.status_code}")
    except Exception:
        st.error("API Backend : Hors ligne")

# ==============================================================================
# VUE PRINCIPALE : HOME
# ==============================================================================
if page == "🏠 Accueil (Home)":
    if st.session_state.agent_state == "ARRETE":
        st.success(
            "🎉 **Entretien obtenu — Candidatures arrêtées.** "
            "Conformément à la règle d'arrêt, l'agent IA est verrouillé à l'état ARRETE."
        )

    st.title("Bienvenue sur Entretien Garanti")
    st.markdown(
        "Plateforme intelligente d'aide à la recherche d'emploi fondée sur une approche "
        "**Human-in-the-Loop** : l'IA structure votre CV, sélectionne les offres les plus "
        "pertinentes via un **score explicable** et prépare vos lettres sans inventer "
        "d'expérience, tandis que **vous gardez le contrôle à chaque étape**."
    )

    # Indicateurs clés du candidat
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("État de l'Agent IA", st.session_state.agent_state)
    with col2:
        st.metric("Formule active", st.session_state.current_plan)
    with col3:
        used, total = st.session_state.quota_used
        st.metric("Quotas candidatures", f"{used} / {total}")
    with col4:
        st.metric("Règle d'arrêt", "Auto sur Entretien")

    st.divider()

    # Parcours en 4 étapes
    st.subheader("Parcours d'accompagnement en 4 étapes")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info(
            "**1. Compte & Conformité**\n\n"
            "Authentification sécurisée (JWT), consentement explicite (Loi 09-08 / RGPD) "
            "et choix de votre formule."
        )
    with c2:
        st.info(
            "**2. Import & Validation CV**\n\n"
            "Extraction NLP depuis PDF/DOCX (compétences, expériences, diplômes) "
            "avec validation humaine obligatoire."
        )
    with c3:
        st.info(
            "**3. Matching Explicable**\n\n"
            "Score transparent (**45 %** sémantique, **35 %** compétences, **20 %** préférences) "
            "avec détails des critères."
        )
    with c4:
        st.info(
            "**4. Lettre & Règle d'arrêt**\n\n"
            "Génération fidèle au CV, relecture avant envoi, et arrêt automatique "
            "dès l'obtention d'un entretien."
        )

    st.divider()

    # Comparatif des 3 formules
    st.subheader("Formules d'abonnement (Simulation académique)")
    f1, f2, f3 = st.columns(3)

    with f1:
        with st.container(border=True):
            st.markdown("### 🌱 Découverte")
            st.write("• Jusqu'à **5 candidatures**")
            st.write("• Jusqu'à **5 générations IA**")
            st.write("• Matching explicable & suivi des statuts")

    with f2:
        with st.container(border=True):
            st.markdown("### 🚀 Accélérateur")
            st.write("• Jusqu'à **25 candidatures**")
            st.write("• Jusqu'à **30 générations IA**")
            st.write("• Priorisation des offres & relances")

    with f3:
        with st.container(border=True):
            st.markdown("### 🏆 Garanti")
            st.write("• **Candidatures illimitées**")
            st.write("• **Générations IA illimitées**")
            st.write("• Accompagnement jusqu'au **1er entretien**")

else:
    st.title(page)
    st.info("Module en cours de développement — disponible à la prochaine étape.")