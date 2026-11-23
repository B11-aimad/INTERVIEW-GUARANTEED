from pathlib import Path
import streamlit as st

from services.api_client import (
    check_health,
    delete_my_account,
    delete_my_profile,
    get_me,
    get_my_profile,
    login_user,
    register_user,
    update_me,
    update_my_profile,
    update_my_subscription,
    validate_my_profile,
)

st.set_page_config(
    page_title="GARANT.AI — Analyse CV & Matching",
    layout="wide",
)

CSS_PATH = Path(__file__).parent / "assets" / "styles.css"
if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

if "active_view" not in st.session_state:
    st.session_state.active_view = "home"
if "auth_redirect_after" not in st.session_state:
    st.session_state.auth_redirect_after = "home"
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None
if "profile_menu_open" not in st.session_state:
    st.session_state.profile_menu_open = False
if "dashboard_tab_hint" not in st.session_state:
    st.session_state.dashboard_tab_hint = "account"
if "agent_state" not in st.session_state:
    st.session_state.agent_state = "ACTIF"
if "show_cv_text" not in st.session_state:
    st.session_state.show_cv_text = False
if "cv_payload" not in st.session_state:
    st.session_state.cv_payload = None

_ = check_health()

# Actions via query params sans effacer jwt_token
nav_param = st.query_params.get("go")
if nav_param:
    st.query_params.clear()
    if nav_param == "home":
        st.session_state.profile_menu_open = False
        st.session_state.active_view = "home"
    elif nav_param == "upload":
        st.session_state.profile_menu_open = False
        if st.session_state.jwt_token:
            st.session_state.active_view = "home"
        else:
            st.session_state.auth_redirect_after = "home"
            st.session_state.active_view = "auth"
    elif nav_param == "dashboard":
        st.session_state.profile_menu_open = False
        st.session_state.dashboard_tab_hint = "account"
        if st.session_state.jwt_token:
            st.session_state.active_view = "dashboard"
        else:
            st.session_state.auth_redirect_after = "dashboard"
            st.session_state.active_view = "auth"
    elif nav_param == "toggle_profile_menu":
        if st.session_state.jwt_token:
            st.session_state.profile_menu_open = not st.session_state.profile_menu_open
        else:
            st.session_state.auth_redirect_after = "dashboard"
            st.session_state.active_view = "auth"
    elif nav_param == "view_profile":
        st.session_state.profile_menu_open = False
        st.session_state.dashboard_tab_hint = "profile"
        if st.session_state.jwt_token:
            st.session_state.active_view = "dashboard"
        else:
            st.session_state.auth_redirect_after = "dashboard"
            st.session_state.active_view = "auth"
    elif nav_param == "logout":
        st.session_state.profile_menu_open = False
        st.session_state.jwt_token = None
        st.session_state.active_view = "auth"

is_logged_in = bool(st.session_state.jwt_token)

right_actions_html = (
    """
    <div class="eg-right-actions">
        <a href="?go=dashboard" target="_self" class="eg-btn-dashboard-nav">
            <svg class="eg-nav-icon" viewBox="0 0 24 24">
                <rect x="3" y="3" width="7" height="9" rx="1"/>
                <rect x="14" y="3" width="7" height="5" rx="1"/>
                <rect x="14" y="12" width="7" height="9" rx="1"/>
                <rect x="3" y="16" width="7" height="5" rx="1"/>
            </svg>
            <span>Dashboard</span>
        </a>
        <a href="?go=toggle_profile_menu" target="_self" class="eg-profile-icon-btn" title="Profil &amp; Session">
            <svg class="eg-nav-icon" viewBox="0 0 24 24">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
            </svg>
        </a>
    </div>
    """
    if is_logged_in
    else """
    <div class="eg-right-actions">
        <a href="?go=dashboard" target="_self" class="eg-btn-dashboard-nav">
            <svg class="eg-nav-icon" viewBox="0 0 24 24">
                <rect x="3" y="3" width="7" height="9" rx="1"/>
                <rect x="14" y="3" width="7" height="5" rx="1"/>
                <rect x="14" y="12" width="7" height="9" rx="1"/>
                <rect x="3" y="16" width="7" height="5" rx="1"/>
            </svg>
            <span>Dashboard</span>
        </a>
    </div>
    """
)

floating_bar_html = (
    """
    <div class="eg-floating-profile-bar">
        <a href="?go=view_profile" target="_self" class="eg-floating-item profile">
            <svg class="eg-nav-icon" viewBox="0 0 24 24">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
            </svg>
            <span>Consulter profil</span>
        </a>
        <a href="?go=logout" target="_self" class="eg-floating-item logout">
            <svg class="eg-nav-icon" viewBox="0 0 24 24">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
            <span>Logout</span>
        </a>
    </div>
    """
    if (is_logged_in and st.session_state.profile_menu_open)
    else ""
)

# Menu unique fixe en haut
st.markdown(
    f"""
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
            <a href="?go=upload" target="_self" class="eg-nav-link">
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
        {right_actions_html}
    </header>
    {floating_bar_html}
    <div class="eg-top-spacer"></div>
    """,
    unsafe_allow_html=True,
)


def _parse_lines_to_experiences(raw_text: str) -> list[dict]:
    items = []
    for line in raw_text.splitlines():
        clean = line.strip()
        if not clean:
            continue
        parts = [p.strip() for p in clean.split("|")]
        items.append(
            {
                "role": parts[0] if len(parts) > 0 and parts[0] else "Poste",
                "company": parts[1] if len(parts) > 1 and parts[1] else "Entreprise",
                "start_date": parts[2] if len(parts) > 2 and parts[2] else None,
                "end_date": parts[3] if len(parts) > 3 and parts[3] else None,
                "description": parts[4] if len(parts) > 4 and parts[4] else None,
            }
        )
    return items


def _parse_lines_to_educations(raw_text: str) -> list[dict]:
    items = []
    for line in raw_text.splitlines():
        clean = line.strip()
        if not clean:
            continue
        parts = [p.strip() for p in clean.split("|")]
        items.append(
            {
                "degree": parts[0] if len(parts) > 0 and parts[0] else "Diplôme",
                "institution": parts[1] if len(parts) > 1 and parts[1] else "Établissement",
                "year": parts[2] if len(parts) > 2 and parts[2] else None,
            }
        )
    return items


def _parse_lines_to_languages(raw_text: str) -> list[dict]:
    items = []
    for line in raw_text.splitlines():
        clean = line.strip()
        if not clean:
            continue
        parts = [p.strip() for p in clean.split("|")]
        items.append(
            {
                "name": parts[0] if len(parts) > 0 and parts[0] else "Langue",
                "level": parts[1] if len(parts) > 1 and parts[1] else None,
            }
        )
    return items


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
                            ok, token, msg = login_user(email, password)
                            if ok and token:
                                st.session_state.jwt_token = token
                                st.session_state.profile_menu_open = False
                                st.session_state.active_view = st.session_state.auth_redirect_after
                                st.rerun()
                            else:
                                st.error(msg)

            with tab_register:
                with st.form("register_form"):
                    full_name = st.text_input("Nom complet")
                    email = st.text_input("Adresse email")
                    password = st.text_input("Mot de passe (8 caractères min.)", type="password")
                    plan = st.selectbox("Formule", ["Découverte", "Accélérateur", "Garanti"])
                    consent_ok = st.checkbox("J'accepte le traitement de mes données personnelles.")
                    submitted = st.form_submit_button("Créer mon compte", type="primary", use_container_width=True)
                    if submitted:
                        if not full_name.strip() or not email.strip() or len(password) < 8:
                            st.error("Veuillez renseigner le nom, l'email et un mot de passe d'au moins 8 caractères.")
                        elif not consent_ok:
                            st.error("Veuillez cocher l'acceptation du traitement des données.")
                        else:
                            reg_ok, reg_msg = register_user(full_name, email, password, plan)
                            if not reg_ok:
                                st.error(reg_msg)
                            else:
                                login_ok, token, login_msg = login_user(email, password)
                                if login_ok and token:
                                    st.session_state.jwt_token = token
                                    st.session_state.profile_menu_open = False
                                    st.session_state.active_view = st.session_state.auth_redirect_after
                                    st.rerun()
                                else:
                                    st.warning(f"{reg_msg} Veuillez vous connecter. ({login_msg})")

            if st.button("Retour à l'accueil", use_container_width=True):
                st.session_state.active_view = "home"
                st.rerun()


def render_profile_tab(token: str):
    p_ok, profile_data, p_msg = get_my_profile(token)
    if not p_ok or not profile_data:
        st.error(p_msg)
        return

    status_badge = "Validé" if profile_data.get("is_validated") else "Non validé (validation requise)"
    st.write(f"**Statut du profil :** {status_badge}")

    exp_default = "\n".join(
        " | ".join(
            filter(None, [e.get("role"), e.get("company"), e.get("start_date"), e.get("end_date"), e.get("description")])
        )
        for e in profile_data.get("experiences", [])
    )
    edu_default = "\n".join(
        " | ".join(filter(None, [ed.get("degree"), ed.get("institution"), ed.get("year")]))
        for ed in profile_data.get("educations", [])
    )
    lang_default = "\n".join(
        " | ".join(filter(None, [lg.get("name"), lg.get("level")]))
        for lg in profile_data.get("languages", [])
    )
    prefs = profile_data.get("preferences") or {}

    with st.form("candidate_profile_form"):
        headline = st.text_input("Titre du profil", value=profile_data.get("headline") or "")
        summary = st.text_area("Résumé professionnel", value=profile_data.get("summary") or "", height=100)
        skills_str = st.text_input(
            "Compétences (séparées par des virgules)",
            value=", ".join(profile_data.get("skills") or []),
        )

        st.markdown("**Préférences de recherche**")
        pr1, pr2 = st.columns(2)
        with pr1:
            pref_role = st.text_input("Poste recherché", value=prefs.get("target_role") or "")
            pref_contract = st.text_input("Type de contrat (CDI, Stage, Freelance...)", value=prefs.get("contract_type") or "")
        with pr2:
            pref_city = st.text_input("Ville souhaitée", value=prefs.get("city") or "")
            pref_remote = st.checkbox("Télétravail accepté", value=bool(prefs.get("remote_allowed", False)))

        exp_raw = st.text_area(
            "Expériences (une par ligne : Poste | Entreprise | Début | Fin | Description)",
            value=exp_default,
            height=100,
        )
        edu_raw = st.text_area(
            "Formations (une par ligne : Diplôme | Établissement | Année)",
            value=edu_default,
            height=90,
        )
        lang_raw = st.text_area(
            "Langues (une par ligne : Langue | Niveau)",
            value=lang_default,
            height=80,
        )

        if st.form_submit_button("Enregistrer le profil", type="primary", use_container_width=True):
            skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]
            payload = {
                "headline": headline,
                "summary": summary,
                "skills": skills_list,
                "experiences": _parse_lines_to_experiences(exp_raw),
                "educations": _parse_lines_to_educations(edu_raw),
                "languages": _parse_lines_to_languages(lang_raw),
                "preferences": {
                    "target_role": pref_role.strip() or None,
                    "city": pref_city.strip() or None,
                    "contract_type": pref_contract.strip() or None,
                    "remote_allowed": pref_remote,
                },
            }
            u_ok, _, u_msg = update_my_profile(token, payload)
            if u_ok:
                st.success(u_msg)
                st.rerun()
            else:
                st.error(u_msg)

    v_col1, v_col2 = st.columns(2)
    with v_col1:
        if st.button("Valider mon profil", type="primary", use_container_width=True):
            v_ok, _, v_msg = validate_my_profile(token, True)
            if v_ok:
                st.success(v_msg)
                st.rerun()
            else:
                st.error(v_msg)
    with v_col2:
        if st.button("Réinitialiser le profil", use_container_width=True):
            d_ok, d_msg = delete_my_profile(token)
            if d_ok:
                st.success(d_msg)
                st.rerun()
            else:
                st.error(d_msg)


def render_dashboard_view():
    st.markdown('<div class="eg-center-heading">Dashboard Candidat</div>', unsafe_allow_html=True)

    token = st.session_state.jwt_token
    if not token:
        st.session_state.active_view = "auth"
        st.rerun()
        return

    ok, user_data, msg = get_me(token)
    if not ok or not user_data:
        st.warning(msg)
        st.session_state.jwt_token = None
        st.session_state.active_view = "auth"
        st.rerun()
        return

    st.session_state.agent_state = user_data.get("agent_status", "ACTIF")
    sub = user_data.get("subscription") or {}

    _, dash_col, _ = st.columns([1.2, 7.6, 1.2])
    with dash_col:
        with st.container(border=True):
            st.markdown(f"### {user_data['full_name']}")
            st.write(f"**Email :** {user_data['email']}")
            st.write(f"**État de l'agent :** {user_data['agent_status']}")
            st.write(f"**Formule active :** {sub.get('plan', 'Découverte')}")
            st.write(f"**Candidatures :** {sub.get('applications_used', 0)} / {sub.get('max_applications') or 'Illimité'}")
            st.write(f"**Générations IA :** {sub.get('ai_generations_used', 0)} / {sub.get('max_ai_generations') or 'Illimité'}")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Retour à l'accueil", use_container_width=True):
                    st.session_state.active_view = "home"
                    st.rerun()
            with c2:
                if st.button("Se déconnecter", use_container_width=True):
                    st.session_state.jwt_token = None
                    st.session_state.profile_menu_open = False
                    st.session_state.active_view = "auth"
                    st.rerun()

            st.divider()
            st.markdown("### Profil Candidat")
            render_profile_tab(token)

            st.divider()
            with st.expander("Modifier le compte / Formule / Supprimer"):
                with st.form("update_user_form"):
                    upd_name = st.text_input("Nom complet", value=user_data["full_name"])
                    upd_email = st.text_input("Adresse email", value=user_data["email"])
                    upd_password = st.text_input("Nouveau mot de passe (optionnel)", type="password")
                    if st.form_submit_button("Enregistrer les modifications", type="primary", use_container_width=True):
                        u_ok, _, u_msg = update_me(token, full_name=upd_name, email=upd_email, password=upd_password or None)
                        if u_ok:
                            st.success(u_msg)
                            st.rerun()
                        else:
                            st.error(u_msg)

                plans = ["Découverte", "Accélérateur", "Garanti"]
                current_plan = sub.get("plan", "Découverte")
                idx = plans.index(current_plan) if current_plan in plans else 0
                chosen_plan = st.selectbox("Formule", plans, index=idx)
                if st.button("Mettre à jour la formule", use_container_width=True):
                    s_ok, _, s_msg = update_my_subscription(token, chosen_plan)
                    if s_ok:
                        st.success(s_msg)
                        st.rerun()
                    else:
                        st.error(s_msg)

                if st.button("Confirmer la suppression définitive du compte", use_container_width=True):
                    d_ok, d_msg = delete_my_account(token)
                    if d_ok:
                        st.session_state.jwt_token = None
                        st.session_state.profile_menu_open = False
                        st.session_state.active_view = "home"
                        st.rerun()
                    else:
                        st.error(d_msg)


def render_home_view():
    _, main_col, _ = st.columns([0.2, 9.6, 0.2])

    with main_col:
        with st.container(border=True):
            cta_href = "?go=upload#upload-cv" if st.session_state.jwt_token else "?go=upload"
            st.markdown(
                f"""
                <div class="eg-hero-box">
                    <h1 class="eg-hero-title">
                        Optimisez votre CV pour un <span class="eg-hero-mark">matching exact</span>
                    </h1>
                    <p class="eg-hero-sub">
                        GARANT.AI structure votre profil avec validation humaine, analyse les offres compatibles,
                        génère des lettres fidèles à votre parcours et arrête automatiquement l'agent dès
                        l'obtention d'un entretien.
                    </p>
                    <a href="{cta_href}" target="_self" class="eg-hero-cta">Importer mon CV</a>
                </div>
                """,
                unsafe_allow_html=True,
            )

            p1, p2, p3, p4 = st.columns(4)
            p1.markdown('<div class="eg-step-pill"><strong>Analyse CV &amp; OCR</strong><br><small>PDF &amp; DOCX</small></div>', unsafe_allow_html=True)
            p2.markdown('<div class="eg-step-pill"><strong>Validation Humaine</strong><br><small>Contrôle du profil</small></div>', unsafe_allow_html=True)
            p3.markdown('<div class="eg-step-pill"><strong>Lettres Fidèles</strong><br><small>Sans hallucination</small></div>', unsafe_allow_html=True)
            p4.markdown('<div class="eg-step-pill"><strong>Règle d\'Arrêt</strong><br><small>ACTIF / ARRETE</small></div>', unsafe_allow_html=True)

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