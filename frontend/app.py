from pathlib import Path
import streamlit as st

from services.api_client import check_health
from views.auth_view import render_auth_view
from views.dashboard_view import render_dashboard_view
from views.home_view import render_home_view

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

# Restaure le token depuis l'URL si la session Streamlit est rechargée
url_token = st.query_params.get("token")
if not st.session_state.jwt_token and url_token:
    st.session_state.jwt_token = url_token

_ = check_health()


def set_token(token: str | None):
    st.session_state.jwt_token = token
    if token:
        st.query_params["token"] = token
    else:
        st.query_params.pop("token", None)


def logout_user():
    st.session_state.profile_menu_open = False
    set_token(None)
    st.session_state.active_view = "auth"


# Actions via query params en conservant ?token=... quand connecté
nav_param = st.query_params.get("go")
if nav_param:
    st.query_params.pop("go", None)
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
        logout_user()

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

if st.session_state.active_view == "auth":
    render_auth_view(set_token)
elif st.session_state.active_view == "dashboard":
    render_dashboard_view(set_token, logout_user)
else:
    render_home_view()