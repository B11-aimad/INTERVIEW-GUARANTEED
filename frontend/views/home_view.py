import streamlit as st


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