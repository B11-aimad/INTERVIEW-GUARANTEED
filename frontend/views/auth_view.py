import streamlit as st

from services.api_client import login_user, register_user


def render_auth_view(set_token_fn):
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
                                set_token_fn(token)
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
                                    set_token_fn(token)
                                    st.session_state.profile_menu_open = False
                                    st.session_state.active_view = st.session_state.auth_redirect_after
                                    st.rerun()
                                else:
                                    st.warning(f"{reg_msg} Veuillez vous connecter. ({login_msg})")

            if st.button("Retour à l'accueil", use_container_width=True):
                st.session_state.active_view = "home"
                st.rerun()