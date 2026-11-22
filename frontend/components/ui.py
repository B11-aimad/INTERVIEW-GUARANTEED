from pathlib import Path
import streamlit as st

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def init_design_system() -> None:
    css_path = ASSETS_DIR / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_sidebar_nav(modules: list[str], user_email: str | None = None) -> str:
    if "compact_info" not in st.session_state:
        st.session_state.compact_info = False

    with st.sidebar:
        st.markdown("### 🎯 Entretien Garanti")
        if not st.session_state.compact_info:
            st.caption("Agent IA supervisé • Human-in-the-Loop")

        toggle_label = "Mode détaillé" if st.session_state.compact_info else "Mode compact"
        if st.button(toggle_label, use_container_width=True):
            st.session_state.compact_info = not st.session_state.compact_info
            st.rerun()

        st.divider()
        selected = st.radio("Navigation", modules, label_visibility="collapsed")

        if not st.session_state.compact_info:
            st.divider()
            compte = user_email if user_email else "Invité"
            st.caption(f"Compte : {compte}")
            st.caption("Conformité : Loi 09-08 & RGPD")
            st.caption("Stack : FastAPI • PostgreSQL 16")

    return selected


def render_sticky_bar(active_page: str, agent_state: str, api_online: bool) -> None:
    api_cls = "ok" if api_online else "err"
    api_txt = "API Connectée" if api_online else "API Hors ligne"
    agent_cls = "ok" if agent_state == "ACTIF" else "info"

    st.markdown(
        f"""
        <div class="eg-sticky-bar">
            <div class="eg-sticky-title">{active_page}</div>
            <div class="eg-badges">
                <span class="eg-badge {agent_cls}">Agent : {agent_state}</span>
                <span class="eg-badge {api_cls}">{api_txt}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <div class="eg-hero">
            <div class="eg-kicker">HUMAN-IN-THE-LOOP • PILOTAGE INTELLIGENT DES CANDIDATURES</div>
            <h1>Pilotez vos offres et décrochez <span>votre entretien.</span></h1>
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


def render_kpis(agent_state: str, plan: str, used: int, total: int | str) -> None:
    st.markdown(
        f"""
        <div class="eg-grid-4">
            <div class="eg-box">
                <div class="eg-box-tag">ÉTAT AGENT IA</div>
                <div class="eg-box-val em">{agent_state}</div>
                <div class="eg-box-desc">Arrêt auto dès le 1er entretien</div>
            </div>
            <div class="eg-box">
                <div class="eg-box-tag">FORMULE ACTIVE</div>
                <div class="eg-box-val">{plan}</div>
                <div class="eg-box-desc">Simulation académique</div>
            </div>
            <div class="eg-box">
                <div class="eg-box-tag">QUOTAS CANDIDATURES</div>
                <div class="eg-box-val">{used} / {total}</div>
                <div class="eg-box-desc">Envois validés par vous</div>
            </div>
            <div class="eg-box">
                <div class="eg-box-tag">RÈGLE D'ARRÊT</div>
                <div class="eg-box-val em">ACTIF</div>
                <div class="eg-box-desc">Verrouillage auto sur entretien</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )