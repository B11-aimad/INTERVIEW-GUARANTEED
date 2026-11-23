import streamlit as st

from services.api_client import (
    delete_my_account,
    delete_my_profile,
    get_me,
    get_my_profile,
    update_me,
    update_my_profile,
    update_my_subscription,
    validate_my_profile,
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


def render_profile_section(token: str):
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


def render_dashboard_view(set_token_fn, logout_fn):
    st.markdown('<div class="eg-center-heading">Dashboard Candidat</div>', unsafe_allow_html=True)

    token = st.session_state.jwt_token
    if not token:
        st.session_state.active_view = "auth"
        st.rerun()
        return

    ok, user_data, msg = get_me(token)
    if not ok or not user_data:
        st.warning(msg)
        set_token_fn(None)
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
                    logout_fn()
                    st.rerun()

            st.divider()
            st.markdown("### Profil Candidat")
            render_profile_section(token)

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
                        set_token_fn(None)
                        st.session_state.profile_menu_open = False
                        st.session_state.active_view = "home"
                        st.rerun()
                    else:
                        st.error(d_msg)