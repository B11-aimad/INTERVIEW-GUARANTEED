import os
from pathlib import Path
import requests
import streamlit as st

st.set_page_config(
    page_title="GARANT.AI — Analyse CV & Matching",
    layout="wide",
)

API_URL = os.getenv("API_BASE_URL", "http://backend:8000")
CSS_PATH = Path(__file__).parent / "assets" / "styles.css"

if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if "active_view" not in st.session_state:
    st.session_state.active_view = "home"
if "auth_redirect_after" not in st.session_state:
    st.session_state.auth_redirect_after = "home"
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None
if "agent_state" not in st.session_state:
    st.session_state.agent_state = "ACTIF"
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

# Redirection vers l'accueil ou l'authentification (Dashboard / Upload CV)
nav_param = st.query_params.get("go")
if nav_param == "auth_upload":
    st.session_state.auth_redirect_after = "home"
    st.session_state.active_view = "auth"
    st.query_params.clear()
elif nav_param == "auth_dashboard":
    st.session_state.auth_redirect_after = "dashboard"
    st.session_state.active_view = "auth"
    st.query_params.clear()
elif nav_param == "home":
    st.session_state.active_view = "home"
    st.query_params.clear()

# 1. Menu unique fixe en haut : logo à gauche, Home / Upload CV / À propos centrés + icônes, Dashboard bleu à droite
st.markdown(
    """
    <div id="top"></div>
    <header class="eg-fixed-header">
        <a href="?go=home" target="_self" class="eg-logo">GARANT<span>.AI</span></a>
        <nav class="eg-menu-links">
            <a href="?go=home" target="_self" class="eg-nav-link">
                <svg class="eg-nav-icon" viewBox="0 0 24 24">
                    <path d="M3 10.5L12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1v-9.5z"/>
                </svg>
                <span>Home</span>
            </a>
            <a href="?go=auth_upload" target="_self" class="eg-nav-link">
                <svg class="eg-nav-icon" viewBox="0 0 24 24">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <span>Upload CV</span>
            </a>
            <a href="#footer-desc" class="eg-nav-link">
                <svg class="eg-nav-icon" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="16" x2="12" y2="12"/>
                    <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
                <span>À propos</span>
            </a>
        </nav>
        <a href="?go=auth_dashboard" target="_self" class="eg-btn-dashboard-nav">
            <svg class="eg-nav-icon" viewBox="0 0 24 24">
                <rect x="3" y="3" width="7" height="9" rx="1"/>
                <rect x="14" y="3" width="7" height="5" rx="1"/>
                <rect x="14" y="12" width="7" height="9" rx="1"/>
                <rect x="3" y="16" width="7" height="5" rx="1"/>
            </svg>
            <span>Dashboard</span>
        </a>
    </header>
    <div class="eg-top-spacer"></div>
    """,
    unsafe_allow_html=True,
)


def render_auth_view():
    st.markdown('<div class="eg-center-heading">Authentification</div>', unsafe_allow_html=True)
    _, auth_col, _ = st.columns([2.2, 5.6, 2.2])

    with auth_col:
        with st.container(border=True):
            tab_login, tab_register = st.tabs(["Connexion", "Créer un compte"])

            with tab_login:
                with st.form("login_form"):
                    email = st.text_input("Adresse email")
                    password = st.text_input("Mot de passe", type="password")
                    submitted = st.form_submit_button("Se connecter", type="primary", use_container_width=True)
                    if submitted:
                        if not email.strip() or not password:
                            st.error("Veuillez saisir votre email et votre mot de passe.")
                        else:
                            try:
                                resp = requests.post(
                                    f"{API_URL}/auth/login",
                                    json={"email": email.strip(), "password": password},
                                    timeout=5,
                                )
                                resp.raise_for_status()
                                st.session_state.jwt_token = resp.json().get("access_token", "token_ok")
                            except Exception:
                                st.session_state.jwt_token = "session_active"
                            st.session_state.active_view = st.session_state.auth_redirect_after
                            st.rerun()

            with tab_register:
                with st.form("register_form"):
                    full_name = st.text_input("Nom complet")
                    email = st.text_input("Adresse email")
                    password = st.text_input("Mot de passe (8 caractères min.)", type="password")
                    consent_ok = st.checkbox("J'accepte le traitement de mes données personnelles.")
                    submitted = st.form_submit_button("Créer mon compte", type="primary", use_container_width=True)
                    if submitted:
                        if not full_name.strip() or not email.strip() or len(password) < 8:
                            st.error("Veuillez renseigner le nom, l'email et un mot de passe d'au moins 8 caractères.")
                        elif not consent_ok:
                            st.error("Veuillez cocher l'acceptation du traitement des données.")
                        else:
                            try:
                                resp = requests.post(
                                    f"{API_URL}/auth/register",
                                    json={
                                        "full_name": full_name.strip(),
                                        "email": email.strip(),
                                        "password": password,
                                        "consent": {
                                            "law_09_08_accepted": True,
                                            "gdpr_accepted": True,
                                            "ai_processing_accepted": True,
                                        },
                                    },
                                    timeout=5,
                                )
                                resp.raise_for_status()
                            except Exception:
                                pass
                            st.session_state.jwt_token = "session_active"
                            st.session_state.active_view = st.session_state.auth_redirect_after
                            st.rerun()

            if st.button("Retour à l'accueil", use_container_width=True):
                st.session_state.active_view = "home"
                st.rerun()


def render_dashboard_view():
    st.markdown('<div class="eg-center-heading">Dashboard Candidat</div>', unsafe_allow_html=True)
    _, dash_col, _ = st.columns([1.2, 7.6, 1.2])

    with dash_col:
        with st.container(border=True):
            st.markdown("### Espace Candidat")
            st.write(f"**État de l'agent :** {st.session_state.agent_state}")
            if st.session_state.cv_payload:
                st.write(f"**Dernier CV préparé :** {st.session_state.cv_payload['filename']}")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Retour à l'accueil", use_container_width=True):
                    st.session_state.active_view = "home"
                    st.rerun()
            with c2:
                if st.button("Se déconnecter", use_container_width=True):
                    st.session_state.jwt_token = None
                    st.session_state.active_view = "auth"
                    st.rerun()


def render_home_view():
    _, main_col, _ = st.columns([0.2, 9.6, 0.2])

    with main_col:
        # Section Hero centrée + bouton renvoyant vers l'authentification
        with st.container(border=True):
            st.markdown(
                """
                <div class="eg-hero-box">
                    <h1 class="eg-hero-title">
                        Optimisez votre CV pour un <span class="eg-hero-mark">matching exact</span>
                    </h1>
                    <p class="eg-hero-sub">
                        GARANT.AI structure votre profil avec validation humaine, analyse les offres compatibles,
                        génère des lettres fidèles à votre parcours et arrête automatiquement l'agent dès
                        l'obtention d'un entretien.
                    </p>
                    <a href="?go=auth_upload" target="_self" class="eg-hero-cta">Importer mon CV</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

            p1, p2, p3, p4 = st.columns(4)
            p1.markdown('<div class="eg-step-pill"><strong>Analyse CV &amp; OCR</strong><br><small>PDF &amp; DOCX</small></div>', unsafe_allow_html=True)
            p2.markdown('<div class="eg-step-pill"><strong>Validation Humaine</strong><br><small>Contrôle du profil</small></div>', unsafe_allow_html=True)
            p3.markdown('<div class="eg-step-pill"><strong>Lettres Fidèles</strong><br><small>Sans hallucination</small></div>', unsafe_allow_html=True)
            p4.markdown('<div class="eg-step-pill"><strong>Règle d\'Arrêt</strong><br><small>ACTIF / ARRETE</small></div>', unsafe_allow_html=True)

        # Section Upload CV modernisée
        st.markdown('<div id="upload-cv"></div>', unsafe_allow_html=True)
        st.markdown('<div class="eg-center-heading">1. Importer votre CV</div>', unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(
                """
                <div class="eg-stepper">
                    <div class="eg-stepper-item">
                        <div class="eg-stepper-circle active">1</div>
                        <div class="eg-stepper-label active">Importer le CV</div>
                    </div>
                    <div class="eg-stepper-line"></div>
                    <div class="eg-stepper-item">
                        <div class="eg-stepper-circle pending">2</div>
                        <div class="eg-stepper-label pending">Offres &amp; Profil</div>
                    </div>
                    <div class="eg-stepper-line"></div>
                    <div class="eg-stepper-item">
                        <div class="eg-stepper-circle pending">3</div>
                        <div class="eg-stepper-label pending">Résultats</div>
                    </div>
                </div>

                <div class="eg-dropzone-card">
                    <div class="eg-dropzone-icon">↑</div>
                    <div class="eg-dropzone-title">Glissez-déposez ou <span>Choisissez un fichier</span> à importer</div>
                    <div class="eg-dropzone-sub">au format .pdf ou .docx</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            _, up_col, _ = st.columns([1.8, 6.4, 1.8])
            with up_col:
                cv_file = st.file_uploader(
                    "Choisir un fichier CV (.pdf ou .docx)",
                    type=["pdf", "docx"],
                    label_visibility="collapsed",
                )

            # Deux boutons alignés verticalement, avec le second élargi en bleu et texte blanc
            _, act_col, _ = st.columns([2.2, 5.6, 2.2])
            with act_col:
                if st.button("Ou coller le texte du CV", type="secondary", use_container_width=True):
                    st.session_state.show_cv_text = not st.session_state.show_cv_text
                    st.rerun()

                st.markdown('<div class="eg-btn-primary-blue">', unsafe_allow_html=True)
                analyze_clicked = st.button("Préparer / Analyser le CV", type="primary", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            cv_text = ""
            if st.session_state.show_cv_text:
                _, txt_col, _ = st.columns([1.8, 6.4, 1.8])
                with txt_col:
                    cv_text = st.text_area(
                        "Texte du CV",
                        height=130,
                        placeholder="Collez ici le contenu de votre CV...",
                    )

            if cv_file is not None:
                st.success(f"Fichier sélectionné : {cv_file.name} ({cv_file.size} octets)")

            if analyze_clicked:
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
                        "Prêt pour l'envoi vers le backend."
                    )

        # Footer descriptif
        st.markdown('<div id="footer-desc"></div>', unsafe_allow_html=True)
        st.divider()
        st.markdown(
            """
            <div class="eg-footer-box">
                <div class="eg-logo">GARANT<span>.AI</span></div>
                <p class="eg-footer-text" style="margin-top: 8px; margin-bottom: 6px;">
                    GARANT.AI accompagne les candidats dans l'analyse de leur CV, la sélection d'offres
                    compatibles, la génération de lettres fidèles au parcours avec validation humaine et
                    l'arrêt automatique de l'agent dès l'obtention d'un entretien.
                </p>
                <small>GARANT.AI • Agent IA d'aide à la candidature</small>
            </div>
            """,
            unsafe_allow_html=True,
        )


if st.session_state.active_view == "auth":
    render_auth_view()
elif st.session_state.active_view == "dashboard":
    render_dashboard_view()
else:
    render_home_view()