import os
from pathlib import Path
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Entretien Garanti",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("API_BASE_URL", "http://backend:8000")
ASSETS_DIR = Path(__file__).parent / "assets"
CSS_PATH = ASSETS_DIR / "styles.css"
MOTION_PATH = ASSETS_DIR / "ambient_motion.html"

if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if MOTION_PATH.exists():
    components.html(MOTION_PATH.read_text(encoding="utf-8"), height=0, width=0)

# État initial de session
if "agent_state" not in st.session_state:
    st.session_state.agent_state = "ACTIF"
if "current_plan" not in st.session_state:
    st.session_state.current_plan = "Découverte"
if "quota_used" not in st.session_state:
    st.session_state.quota_used = (0, 5)
if "compact_sidebar" not in st.session_state:
    st.session_state.compact_sidebar = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None


def api_is_online() -> bool:
    try:
        return requests.get(f"{API_URL}/health", timeout=1.5).status_code == 200
    except Exception:
        return False


online = api_is_online()

# ==============================================================================
# SIDEBAR CLAIRE AVEC OPTION COMPACT / DÉTAILLÉ
# ==============================================================================
with st.sidebar:
    st.markdown("## Entretien Garanti")
    if not st.session_state.compact_sidebar:
        st.caption("Agent IA supervisé • Human-in-the-Loop")

    btn_txt = "Afficher détails" if st.session_state.compact_sidebar else "Mode compact"
    if st.button(btn_txt, use_container_width=True):
        st.session_state.compact_sidebar = not st.session_state.compact_sidebar
        st.rerun()

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Accueil (Home)",
            "Compte & Consentement",
            "Mon CV & Profil",
            "Offres recommandées",
            "Mes candidatures",
        ],
    )

    if not st.session_state.compact_sidebar:
        st.divider()
        compte_lbl = st.session_state.user_email or "Invité"
        st.caption(f"Compte : {compte_lbl}")
        st.caption("Conformité : Loi 09-08 & RGPD")
        st.caption("Backend : FastAPI • PostgreSQL 16")

# ==============================================================================
# BARRE SUPÉRIEURE FIXE LORS DU SCROLL
# ==============================================================================
api_badge_cls = "eg-badge-ok" if online else "eg-badge-err"
api_badge_txt = "API Connectée" if online else "API Hors ligne"
agent_badge_cls = "eg-badge-ok" if st.session_state.agent_state == "ACTIF" else "eg-badge-info"

st.markdown(
    f"""
    <div class="eg-topbar">
        <div class="eg-topbar-title">{page}</div>
        <div>
            <span class="eg-badge {agent_badge_cls}">Agent : {st.session_state.agent_state}</span>
            <span class="eg-badge {api_badge_cls}">{api_badge_txt}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# VUE PRINCIPALE : ACCUEIL (HOME)
# ==============================================================================
if page == "Accueil (Home)":
    if st.session_state.agent_state == "ARRETE":
        st.success(
            "Entretien obtenu — Candidatures arrêtées. "
            "Conformément à la règle d'arrêt, l'agent IA est verrouillé sur l'état ARRETE."
        )

    st.markdown(
        """
        <div class="eg-hero">
            <div class="eg-kicker">Human-in-the-Loop • Pilotage intelligent des candidatures</div>
            <h1>Pilotez vos candidatures, décrochez <span>votre entretien.</span></h1>
            <p>
                Extraction structurée de votre CV, score de matching explicable
                (<strong>45% sémantique • 35% compétences • 20% préférences</strong>),
                génération de lettres fidèles à votre profil sans hallucination et arrêt automatique
                dès l'obtention d'un entretien.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    used, total = st.session_state.quota_used
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.metric("État de l'Agent IA", st.session_state.agent_state)
    with m2:
        with st.container(border=True):
            st.metric("Formule active", st.session_state.current_plan)
    with m3:
        with st.container(border=True):
            st.metric("Quotas candidatures", f"{used} / {total}")
    with m4:
        with st.container(border=True):
            st.metric("Règle d'arrêt", "Auto sur Entretien")

    st.subheader("Parcours en 4 étapes")
    s1, s2, s3, s4 = st.columns(4)
    steps = [
        (s1, "Étape 01", "Compte & Conformité", "Authentification sécurisée, consentement explicite (Loi 09-08 / RGPD) et choix de formule."),
        (s2, "Étape 02", "Import & Validation CV", "Extraction PDF/DOCX des compétences, expériences et diplômes avec validation humaine."),
        (s3, "Étape 03", "Matching Explicable", "Score transparent (45% sémantique, 35% compétences, 20% préférences) détaillé."),
        (s4, "Étape 04", "Lettre & Règle d'arrêt", "Lettre fidèle au CV, relecture avant envoi et arrêt auto dès le 1er entretien."),
    ]
    for col, tag, title, desc in steps:
        with col:
            with st.container(border=True):
                st.caption(tag)
                st.markdown(f"**{title}**")
                st.write(desc)

    st.subheader("Formules d'abonnement")
    p1, p2, p3 = st.columns(3)
    with p1:
        with st.container(border=True):
            st.caption("FORMULE 01")
            st.markdown("### Découverte")
            st.markdown("**Jusqu'à 5 candidatures**")
            st.write("• Jusqu'à 5 candidatures")
            st.write("• Jusqu'à 5 générations IA")
            st.write("• Matching explicable & suivi")
    with p2:
        with st.container(border=True):
            st.caption("FORMULE 02")
            st.markdown("### Accélérateur")
            st.markdown("**Jusqu'à 25 candidatures**")
            st.write("• Jusqu'à 25 candidatures")
            st.write("• Jusqu'à 30 générations IA")
            st.write("• Priorisation des offres")
    with p3:
        with st.container(border=True):
            st.caption("FORMULE 03 • RECOMMANDÉE")
            st.markdown("### Garanti")
            st.markdown("**Candidatures illimitées**")
            st.write("• Candidatures illimitées")
            st.write("• Générations IA illimitées")
            st.write("• Accompagnement jusqu'au 1er entretien")

else:
    with st.container(border=True):
        st.subheader(page)
        st.info("Module prêt — prochainement connecté à PostgreSQL 16 et FastAPI.")