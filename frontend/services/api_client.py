import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://backend:8000")


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def check_health() -> bool:
    try:
        return requests.get(f"{API_BASE_URL}/health", timeout=2.0).status_code == 200
    except requests.RequestException:
        return False


def register_user(full_name: str, email: str, password: str, plan: str = "Découverte") -> tuple[bool, str]:
    try:
        resp = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={
                "full_name": full_name.strip(),
                "email": email.strip().lower(),
                "password": password,
                "plan": plan,
                "consent": {
                    "law_09_08_accepted": True,
                    "gdpr_accepted": True,
                    "ai_processing_accepted": True,
                },
            },
            timeout=10,
        )
        if resp.status_code == 201:
            return True, "Compte créé avec succès."
        detail = resp.json().get("detail", "Erreur lors de l'inscription.")
        return False, str(detail)
    except requests.RequestException as exc:
        return False, f"Erreur de communication avec le backend : {exc}"


def login_user(email: str, password: str) -> tuple[bool, str | None, str]:
    try:
        resp = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email.strip().lower(), "password": password},
            timeout=10,
        )
        if resp.status_code == 200:
            token = resp.json().get("access_token")
            return True, token, "Connexion réussie."
        detail = resp.json().get("detail", "Identifiants invalides.")
        return False, None, str(detail)
    except requests.RequestException as exc:
        return False, None, f"Erreur de communication avec le backend : {exc}"


def get_me(token: str) -> tuple[bool, dict | None, str]:
    try:
        resp = requests.get(f"{API_BASE_URL}/auth/me", headers=_auth_headers(token), timeout=10)
        if resp.status_code == 200:
            return True, resp.json(), "OK"
        return False, None, "Session expirée ou invalide."
    except requests.RequestException as exc:
        return False, None, f"Erreur réseau : {exc}"


def update_me(
    token: str,
    full_name: str | None = None,
    email: str | None = None,
    password: str | None = None,
) -> tuple[bool, dict | None, str]:
    payload = {
        k: v
        for k, v in {
            "full_name": full_name.strip() if full_name is not None else None,
            "email": email.strip().lower() if email is not None else None,
            "password": password if password else None,
        }.items()
        if v is not None
    }
    try:
        resp = requests.patch(f"{API_BASE_URL}/auth/me", json=payload, headers=_auth_headers(token), timeout=10)
        if resp.status_code == 200:
            return True, resp.json(), "Compte mis à jour."
        detail = resp.json().get("detail", "Impossible de mettre à jour le compte.")
        return False, None, str(detail)
    except requests.RequestException as exc:
        return False, None, f"Erreur réseau : {exc}"


def update_my_subscription(token: str, plan: str) -> tuple[bool, dict | None, str]:
    try:
        resp = requests.patch(
            f"{API_BASE_URL}/auth/me/subscription",
            json={"plan": plan},
            headers=_auth_headers(token),
            timeout=10,
        )
        if resp.status_code == 200:
            return True, resp.json(), "Formule mise à jour."
        detail = resp.json().get("detail", "Impossible de mettre à jour la formule.")
        return False, None, str(detail)
    except requests.RequestException as exc:
        return False, None, f"Erreur réseau : {exc}"


def delete_my_account(token: str) -> tuple[bool, str]:
    try:
        resp = requests.delete(f"{API_BASE_URL}/auth/me", headers=_auth_headers(token), timeout=10)
        if resp.status_code == 200:
            return True, "Compte supprimé."
        detail = resp.json().get("detail", "Impossible de supprimer le compte.")
        return False, str(detail)
    except requests.RequestException as exc:
        return False, f"Erreur réseau : {exc}"
def get_my_profile(token: str) -> tuple[bool, dict | None, str]:
    try:
        resp = requests.get(f"{API_BASE_URL}/profile/me", headers=_auth_headers(token), timeout=10)
        if resp.status_code == 200:
            return True, resp.json(), "OK"
        detail = resp.json().get("detail", "Impossible de charger le profil.")
        return False, None, str(detail)
    except requests.RequestException as exc:
        return False, None, f"Erreur réseau : {exc}"


def update_my_profile(token: str, payload: dict) -> tuple[bool, dict | None, str]:
    try:
        resp = requests.put(
            f"{API_BASE_URL}/profile/me",
            json=payload,
            headers=_auth_headers(token),
            timeout=10,
        )
        if resp.status_code == 200:
            return True, resp.json(), "Profil enregistré."
        detail = resp.json().get("detail", "Erreur lors de l'enregistrement du profil.")
        return False, None, str(detail)
    except requests.RequestException as exc:
        return False, None, f"Erreur réseau : {exc}"


def validate_my_profile(token: str, is_validated: bool = True) -> tuple[bool, dict | None, str]:
    try:
        resp = requests.post(
            f"{API_BASE_URL}/profile/me/validate",
            json={"is_validated": is_validated},
            headers=_auth_headers(token),
            timeout=10,
        )
        if resp.status_code == 200:
            return True, resp.json(), "Validation du profil mise à jour."
        detail = resp.json().get("detail", "Erreur lors de la validation du profil.")
        return False, None, str(detail)
    except requests.RequestException as exc:
        return False, None, f"Erreur réseau : {exc}"


def delete_my_profile(token: str) -> tuple[bool, str]:
    try:
        resp = requests.delete(f"{API_BASE_URL}/profile/me", headers=_auth_headers(token), timeout=10)
        if resp.status_code == 200:
            return True, "Profil réinitialisé."
        detail = resp.json().get("detail", "Impossible de supprimer le profil.")
        return False, str(detail)
    except requests.RequestException as exc:
        return False, f"Erreur réseau : {exc}"