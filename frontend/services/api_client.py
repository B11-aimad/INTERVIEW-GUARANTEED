import os
import requests

API_BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000")


def _headers(token: str | None = None) -> dict[str, str]:
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def register_user(full_name: str, email: str, password: str, plan: str, consent: dict) -> dict:
    resp = requests.post(
        f"{API_BASE_URL}/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": password,
            "plan": plan,
            "consent": consent,
        },
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def login_user(email: str, password: str) -> str:
    resp = requests.post(
        f"{API_BASE_URL}/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_current_user_profile(token: str) -> dict:
    resp = requests.get(f"{API_BASE_URL}/auth/me", headers=_headers(token), timeout=10)
    resp.raise_for_status()
    return resp.json()


def update_user_profile(token: str, full_name: str | None = None, email: str | None = None, password: str | None = None) -> dict:
    payload = {k: v for k, v in {"full_name": full_name, "email": email, "password": password}.items() if v}
    resp = requests.patch(f"{API_BASE_URL}/auth/me", json=payload, headers=_headers(token), timeout=10)
    resp.raise_for_status()
    return resp.json()


def update_user_plan(token: str, plan: str) -> dict:
    resp = requests.patch(
        f"{API_BASE_URL}/auth/me/subscription",
        json={"plan": plan},
        headers=_headers(token),
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def delete_user_account(token: str) -> dict:
    resp = requests.delete(f"{API_BASE_URL}/auth/me", headers=_headers(token), timeout=10)
    resp.raise_for_status()
    return resp.json()