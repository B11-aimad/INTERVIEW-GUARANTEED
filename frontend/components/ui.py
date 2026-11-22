from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def init_design_system() -> None:
    """Charge le CSS global et monte la scène WebGL 3D en arrière-plan sans bloquer le scroll."""
    css_path = ASSETS_DIR / "styles.css"
    scene_path = ASSETS_DIR / "webgl_scene.html"

    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

    if scene_path.exists():
        components.html(scene_path.read_text(encoding="utf-8"), height=0, width=0)


def render_topbar(agent_state: str, api_online: bool) -> None:
    status_cls = "online" if api_online else "offline"
    status_txt = "API_ONLINE" if api_online else "API_OFFLINE"
    state_cls = "neon" if agent_state == "ACTIF" else "warn"

    st.markdown(
        f"""
        <div class="eg-topbar">
            <div class="eg-brand">
                <span class="eg-logo-mark">EG//01</span>
                <span class="eg-brand-name">ENTRETIEN GARANTI</span>
            </div>
            <div class="eg-status-group">
                <span class="eg-pill {state_cls}">AGENT :: {agent_state}</span>
                <span class="eg-pill {status_cls}"><span class="dot"></span>{status_txt}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="eg-hero">
            <div class="eg-eyebrow">// HUMAN-IN-THE-LOOP CAREER COMMAND CENTER</div>
            <h1 class="eg-title">
                CIBLEZ LES OFFRES.<br/>
                DÉCROCHEZ <span>L'ENTRETIEN.</span>
            </h1>
            <p class="eg-subtitle">
                Pipeline IA supervisé de bout en bout : extraction structurée de votre CV,
                matching hybride explicable (<strong>45% sémantique • 35% compétences • 20% préférences</strong>),
                génération de lettres zéro-hallucination et verrouillage automatique dès votre premier entretien.
            </p>
            <div class="eg-metrics-row">
                <div class="eg-stat">
                    <span class="eg-stat-val">45 / 35 / 20</span>
                    <span class="eg-stat-lbl">PONDÉRATION MATCHING</span>
                </div>
                <div class="eg-stat">
                    <span class="eg-stat-val">0% HALLUCINATION</span>
                    <span class="eg-stat-lbl">FIDÉLITÉ STRICTEMENT CV</span>
                </div>
                <div class="eg-stat">
                    <span class="eg-stat-val">LOI 09-08 & RGPD</span>
                    <span class="eg-stat-lbl">CONFORMITÉ & DROIT À L'OUBLI</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_strip(agent_state: str, plan: str, used: int, total: int | str) -> None:
    st.markdown(
        f"""
        <div class="eg-kpi-grid">
            <div class="eg-kpi-card">
                <div class="eg-kpi-tag">01 // STATUT AGENT</div>
                <div class="eg-kpi-num neon">{agent_state}</div>
                <div class="eg-kpi-sub">Arrêt auto sur entretien décroché</div>
            </div>
            <div class="eg-kpi-card">
                <div class="eg-kpi-tag">02 // ABONNEMENT</div>
                <div class="eg-kpi-num">{plan}</div>
                <div class="eg-kpi-sub">Simulation académique active</div>
            </div>
            <div class="eg-kpi-card">
                <div class="eg-kpi-tag">03 // QUOTA ENVOIS</div>
                <div class="eg-kpi-num">{used} <span class="muted">/ {total}</span></div>
                <div class="eg-kpi-sub">Candidatures validées humainement</div>
            </div>
            <div class="eg-kpi-card">
                <div class="eg-kpi-tag">04 // CONTRÔLE HUMAIN</div>
                <div class="eg-kpi-num neon">OBLIGATOIRE</div>
                <div class="eg-kpi-sub">Aucun envoi sans votre validation</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )