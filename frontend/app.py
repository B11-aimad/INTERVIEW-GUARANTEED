import os
from pathlib import Path
import requests
import streamlit as st

st.set_page_config(
    page_title="GARANT.AI — Analyse CV & Matching Explicable",
    layout="wide",
)

API_URL = os.getenv("API_BASE_URL", "http://backend:8000")
CSS_PATH = Path(__file__).parent / "assets" / "styles.css"

if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if "agent_state" not in st.session_state:
    st.session_state.agent_state = "ACTIF"
if "current_plan" not in st.session_state:
    st.session_state.current_plan = "Découverte"
if "quota_used" not in st.session_state:
    st.session_state.quota_used = (0, 5)
if "show_cv_text" not in st.session_state:
    st.session_state.show_cv_text = False
if "cv_payload" not in st.session_state:
    st.session_state.cv_payload = None


def api_is_online() -> bool:
    try:
        return requests.get(f"{API_URL}/health", timeout=1.5).status_code == 200
    except Exception:
        return False


_ = api_is_online()

# 1. Menu unique fixe en haut : logo à gauche, liens centrés
st.markdown(
    """
    <div id="top"></div>
    <header class="eg-fixed-header">
        <a href="#top" class="eg-logo">GARANT<span>.AI</span></a>
        <nav class="eg-menu-links">
            <a href="#upload-cv">Upload CV</a>
            <a href="#matching">Matching 45/35/20</a>
            <a href="#formules">Formules</a>
            <a href="#footer-desc">À propos</a>
        </nav>
        <div class="eg-header-spacer"></div>
    </header>
    <div class="eg-top-spacer"></div>
    """,
    unsafe_allow_html=True,
)

_, main_col, _ = st.columns([0.2, 9.6, 0.2])

with main_col:
    # 2. Section Hero centrée + bouton renvoyant vers la section d'upload CV
    with st.container(border=True):
        st.markdown(
            """
            <div class="eg-hero-box">
                <h1 class="eg-hero-title">
                    Optimisez votre CV pour un <span class="eg-hero-mark">matching exact</span>
                </h1>
                <p class="eg-hero-sub">
                    GARANT.AI structure votre profil avec validation humaine obligatoire, calcule un score
                    explicable (45% sémantique, 35% compétences, 20% préférences), génère des lettres
                    fidèles à votre CV sans hallucination et arrête automatiquement l'agent dès
                    l'obtention d'un entretien.
                </p>
                <a href="#upload-cv" class="eg-hero-cta">Importer mon CV</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        p1, p2, p3, p4, p5 = st.columns(5)
        p1.markdown('<div class="eg-step-pill"><strong>Matching 45/35/20</strong><br><small>Score explicable</small></div>', unsafe_allow_html=True)
        p2.markdown('<div class="eg-step-pill"><strong>Validation Humaine</strong><br><small>Human-in-the-Loop</small></div>', unsafe_allow_html=True)
        p3.markdown('<div class="eg-step-pill"><strong>Sans Hallucination</strong><br><small>Fidèle au CV</small></div>', unsafe_allow_html=True)
        p4.markdown('<div class="eg-step-pill"><strong>Règle d\'Arrêt</strong><br><small>ACTIF / ARRETE</small></div>', unsafe_allow_html=True)
        p5.markdown('<div class="eg-step-pill"><strong>Loi 09-08 & RGPD</strong><br><small>Consentement & oubli</small></div>', unsafe_allow_html=True)

    # 3. Section Upload CV centrée en bas du Hero
    st.markdown('<div id="upload-cv"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eg-center-heading">1. Importer votre CV</div>', unsafe_allow_html=True)

    with st.container(border=True):
        s1, s2, s3 = st.columns(3)
        s1.markdown('<div class="eg-step-pill"><strong>1. Importer le CV</strong><br><small>PDF, DOCX ou texte brut</small></div>', unsafe_allow_html=True)
        s2.markdown('<div class="eg-step-pill"><strong>2. Validation humaine</strong><br><small>Profil vérifié avant génération IA</small></div>', unsafe_allow_html=True)
        s3.markdown('<div class="eg-step-pill"><strong>3. Matching & Candidature</strong><br><small>Score 45/35/20 et arrêt auto</small></div>', unsafe_allow_html=True)

        cv_file = st.file_uploader(
            "Déposez ou sélectionnez votre CV (PDF ou DOCX)",
            type=["pdf", "docx"],
        )

        b_col1, _ = st.columns([1.4, 3.6])
        with b_col1:
            if st.button("Coller le texte du CV", use_container_width=True):
                st.session_state.show_cv_text = not st.session_state.show_cv_text
                st.rerun()

        cv_text = ""
        if st.session_state.show_cv_text:
            cv_text = st.text_area(
                "Texte du CV",
                height=130,
                placeholder="Collez ici vos compétences, expériences, formations et préférences...",
            )

        if cv_file is not None:
            st.success(f"Fichier sélectionné : {cv_file.name} ({cv_file.size} octets)")

        if st.button("Préparer / Analyser le CV", type="primary", use_container_width=True):
            if st.session_state.agent_state == "ARRETE":
                st.warning("L'agent est à l'état ARRETE suite à l'obtention d'un entretien.")
            elif cv_file is None and not cv_text.strip():
                st.info("Veuillez importer un fichier PDF/DOCX ou coller le texte de votre CV.")
            else:
                st.session_state.cv_payload = {
                    "filename": cv_file.name if cv_file else "texte_colle.txt",
                    "size_bytes": cv_file.size if cv_file else len(cv_text.encode("utf-8")),
                    "has_text": bool(cv_text.strip()),
                    "human_validated": False,
                }
                st.success(
                    f"CV préparé ({st.session_state.cv_payload['filename']}) — "
                    "Prêt pour l'envoi vers l'endpoint backend de parsing et validation humaine."
                )

    # Matching explicable (45 / 35 / 20)
    st.markdown('<div id="matching"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eg-center-heading">Pondération du matching explicable</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Similarité sémantique", "45 %")
    m2.metric("Compétences", "35 %")
    m3.metric("Préférences", "20 %")
    m4.metric("État de l'agent", st.session_state.agent_state)

    # Formules
    st.markdown('<div id="formules"></div>', unsafe_allow_html=True)
    st.markdown('<div class="eg-center-heading">Formules</div>', unsafe_allow_html=True)

    used, total = st.session_state.quota_used
    f1, f2, f3 = st.columns(3)
    with f1:
        with st.container(border=True):
            st.markdown("### Découverte")
            st.write("5 candidatures • 5 générations IA")
            if st.button("Choisir Découverte", use_container_width=True):
                st.session_state.current_plan = "Découverte"
                st.session_state.quota_used = (used, 5)
                st.rerun()
    with f2:
        with st.container(border=True):
            st.markdown("### Accélérateur")
            st.write("25 candidatures • 30 générations IA")
            if st.button("Choisir Accélérateur", use_container_width=True):
                st.session_state.current_plan = "Accélérateur"
                st.session_state.quota_used = (used, 25)
                st.rerun()
    with f3:
        with st.container(border=True):
            st.markdown("### Garanti")
            st.write("Candidatures et générations IA illimitées")
            if st.button("Choisir Garanti", use_container_width=True):
                st.session_state.current_plan = "Garanti"
                st.session_state.quota_used = (used, "Illimité")
                st.rerun()

    # 4. Footer descriptif
    st.markdown('<div id="footer-desc"></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown(
        f"""
        <div class="eg-footer-box">
            <div class="eg-logo">GARANT<span>.AI</span></div>
            <p class="eg-footer-text" style="margin-top: 8px; margin-bottom: 10px;">
                GARANT.AI est une plateforme intelligente de gestion de recherche d'emploi et de candidatures
                fondée sur une approche Human-in-the-Loop. Elle analyse et structure le CV, calcule un score
                de matching explicable (45% sémantique, 35% compétences, 20% préférences), génère des lettres
                fidèles au parcours sans hallucination et arrête automatiquement l'agent dès l'obtention d'un entretien.
            </p>
            <small>
                Conformité Loi 09-08 &amp; RGPD • Formule active : {st.session_state.current_plan} • Quotas : {used}/{total}
            </small>
        </div>
        """,
        unsafe_allow_html=True,
    )