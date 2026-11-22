import os
from pathlib import Path
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Entretien Garanti — Pilotage Intelligent des Offres",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("API_BASE_URL", "http://backend:8000")
ASSETS_DIR = Path(__file__).parent / "assets"


def load_css(file_path: Path) -> None:
    if file_path.exists():
        css = file_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def mount_3d_background(file_path: Path) -> None:
    if file_path.exists():
        html = file_path.read_text(encoding="utf-8")
        # Force l'iframe généré par Streamlit en arrière-plan plein écran
        st.markdown(
            """
            <style>
            iframe[title="streamlit.components.v1.html"] {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                z-index: 0 !important;
                pointer-events: none !important;
                border: none !important;
            }
            .stApp > header,
            [data-testid="stAppViewContainer"],
            [data-testid="stSidebar"] {
                position: relative;
                z-index: 1;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        components.html(html, height=1, width=1)


# Chargement séparé du style et de la scène 3D
load_css(ASSETS_DIR / "styles.css")
mount_3d_background(ASSETS_DIR / "scene_3d.html")

# État initial de session
if "agent_state" not in st.session_state:
    st.session_state.agent_state = "ACTIF"
if "current_plan" not in st.session_state:
    st.session_state.current_plan = "Découverte"
if "quota_used" not in st.session_state:
    st.session_state.quota_used = (0, 5)

# ==============================================================================
# BARRE LATÉRALE : NAVIGATION & ÉTAT DU SYSTÈME
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎯 Entretien Garanti")
    st.caption("Centre de pilotage d'offres & candidatures")
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

    st.markdown(
        '<div class="hero-badge">⚡ CENTRE DE PILOTAGE IA • HUMAN-IN-THE-LOOP</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-title">Pilotez vos offres et candidatures avec précision</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-subtitle">'
        "Explorez les opportunités pertinentes, visualisez l'adéquation réelle avec votre profil "
        "et préparez des candidatures fidèles à votre parcours — avec validation humaine à chaque "
        "étape et arrêt automatique dès l'obtention d'un entretien."
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    # Indicateurs clés
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

    st.write("")
    st.markdown("#### Parcours guidé en 4 étapes")

    c1, c2, c3, c4 = st.columns(4)
    steps = [
        (c1, "ÉTAPE 01", "Compte & Conformité", "Authentification JWT, consentement explicite (Loi 09-08 / RGPD) et choix de formule."),
        (c2, "ÉTAPE 02", "Import & Validation CV", "Extraction automatique (PDF/DOCX) de vos compétences et expériences, validée par vous."),
        (c3, "ÉTAPE 03", "Matching Explicable", "Score transparent (45 % sémantique, 35 % compétences, 20 % préférences) détaillé."),
        (c4, "ÉTAPE 04", "Lettre & Règle d'arrêt", "Rédaction fidèle au CV, relecture humaine et arrêt dès le 1er entretien."),
    ]
    for col, num, title, desc in steps:
        with col:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="step-num">{num}</div>
                    <div class="card-title">{title}</div>
                    <div class="card-text">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown("#### Formules d'accompagnement")

    f1, f2, f3 = st.columns(3)
    plans = [
        (f1, "🌱 Découverte", "5 candidatures", "• Jusqu'à 5 candidatures<br>• Jusqu'à 5 générations IA<br>• Matching explicable & suivi"),
        (f2, "🚀 Accélérateur", "25 candidatures", "• Jusqu'à 25 candidatures<br>• Jusqu'à 30 générations IA<br>• Priorisation des offres"),
        (f3, "🏆 Garanti", "Illimité", "• Candidatures illimitées<br>• Générations IA illimitées<br>• Accompagnement jusqu'au 1er entretien"),
    ]
    for col, name, quota, bullets in plans:
        with col:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="card-title">{name}</div>
                    <div class="plan-price">{quota}</div>
                    <div class="card-text">{bullets}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

else:
    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-title">{page}</div>
            <div class="card-text">Module prêt à être branché sur l'API FastAPI à la prochaine étape.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )