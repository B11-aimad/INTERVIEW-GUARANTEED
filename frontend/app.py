import os
import requests
import streamlit as st
from components.ui import init_design_system, render_hero, render_kpi_strip, render_topbar

st.set_page_config(
    page_title="ENTRETIEN GARANTI // AI CAREER COMMAND",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto",
)

API_URL = os.getenv("API_BASE_URL", "http://backend:8000")

# Initialise le Design System 1337 + Scène 3D Three.js (sans bloquer le scroll)
init_design_system()

# État de session
if "agent_state" not in st.session_state:
    st.session_state.agent_state = "ACTIF"
if "current_plan" not in st.session_state:
    st.session_state.current_plan = "DÉCOUVERTE"
if "quota_used" not in st.session_state:
    st.session_state.quota_used = (0, 5)


def check_api_health() -> bool:
    try:
        return requests.get(f"{API_URL}/health", timeout=1.5).status_code == 200
    except Exception:
        return False


api_online = check_api_health()

# ==============================================================================
# NAVIGATION LATÉRALE
# ==============================================================================
with st.sidebar:
    st.markdown("### `// NAVIGATION`")
    page = st.radio(
        "Modules",
        [
            "00 // ACCUEIL",
            "01 // COMPTE & LOI 09-08",
            "02 // MON CV & PROFIL",
            "03 // OFFRES SCORÉES",
            "04 // CANDIDATURES & SUIVI",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("STACK :: FASTAPI + POSTGRES 16 + STREAMLIT")

# Barre d'état supérieure
render_topbar(st.session_state.agent_state, api_online)

# ==============================================================================
# ROUTAGE DES VUES
# ==============================================================================
if page == "00 // ACCUEIL":
    if st.session_state.agent_state == "ARRETE":
        st.success(
            "ENTRETIEN OBTENU — CANDIDATURES ARRÊTÉES. "
            "L'agent IA est verrouillé à l'état ARRETE conformément à la règle d'arrêt."
        )

    render_hero()

    used, total = st.session_state.quota_used
    render_kpi_strip(st.session_state.agent_state, st.session_state.current_plan, used, total)

    st.markdown('<div class="eg-sec-title">// ARCHITECTURE DU PIPELINE CANDIDAT</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="eg-grid">
            <div class="eg-card">
                <div class="eg-card-code">[MODULE_01] AUTH & RGPD</div>
                <div class="eg-card-title">Compte & Loi 09-08</div>
                <div class="eg-card-desc">Création de compte JWT, consentement explicite tracé en base et gestion du droit à l'oubli.</div>
            </div>
            <div class="eg-card">
                <div class="eg-card-code">[MODULE_02] NLP PARSER</div>
                <div class="eg-card-title">Extraction & Validation CV</div>
                <div class="eg-card-desc">Analyse PDF/DOCX de vos compétences et expériences avec validation humaine obligatoire.</div>
            </div>
            <div class="eg-card">
                <div class="eg-card-code">[MODULE_03] HYBRID MATCH</div>
                <div class="eg-card-title">Scoring Explicable</div>
                <div class="eg-card-desc">Score transparent (45% sémantique, 35% compétences, 20% préférences) et justifications détaillées.</div>
            </div>
            <div class="eg-card">
                <div class="eg-card-code">[MODULE_04] STOP-RULE</div>
                <div class="eg-card-title">Lettre & Arrêt Auto</div>
                <div class="eg-card-desc">Génération fidèle à votre CV, relecture avant envoi et verrouillage automatique au 1er entretien.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="eg-sec-title">// FORMULES & QUOTAS D\'EXÉCUTION</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="eg-grid">
            <div class="eg-card">
                <div class="eg-card-code">TIER_01 // STARTER</div>
                <div class="eg-card-title">Découverte</div>
                <div class="eg-price">5 CANDIDATURES</div>
                <div class="eg-card-desc">• 5 candidatures max<br/>• 5 générations IA max<br/>• Scoring explicable complet</div>
            </div>
            <div class="eg-card">
                <div class="eg-card-code">TIER_02 // BOOST</div>
                <div class="eg-card-title">Accélérateur</div>
                <div class="eg-price">25 CANDIDATURES</div>
                <div class="eg-card-desc">• 25 candidatures max<br/>• 30 générations IA max<br/>• Priorisation des opportunités</div>
            </div>
            <div class="eg-card highlight">
                <div class="eg-card-code">TIER_03 // FULL ACCESS</div>
                <div class="eg-card-title">Garanti</div>
                <div class="eg-price">ILLIMITÉ</div>
                <div class="eg-card-desc">• Candidatures illimitées<br/>• Générations IA illimitées<br/>• Accompagnement jusqu'au 1er entretien</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        f"""
        <div class="eg-card">
            <div class="eg-card-code">// ACTIVE_VIEW</div>
            <div class="eg-card-title">{page}</div>
            <div class="eg-card-desc">Interface prête — nous allons maintenant connecter ce module à PostgreSQL 16 et FastAPI.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )