"""
Export every live control set of an AmpliFlow tenant as LLM-friendly,
machine-readable YAML: one file per set with the set and its items (every API
field, in API order) plus inlined display values for people/dropdown ids, and
reference-data.json with id -> display-value maps for users, teams, roles and
the control-item dropdown sources (processes, risks, pages, legislation,
equipment).

Configuration: copy .env.example to .env and set AF_TENANT, AF_USERNAME and
AF_PASSWORD (see .env.example). Requires: pip install -r requirements.txt
"""

import json
import os
import re
import sys
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
TENANT, USER, PASSWORD = (os.environ[k] for k in ("AF_TENANT", "AF_USERNAME", "AF_PASSWORD"))
BASE, OUT = f"https://{TENANT}".rstrip("/"), Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)


def check(response):
    response.raise_for_status()
    return response.json()


token = check(
    requests.post(
        f"{BASE}/api/Auth/login",
        json={"email": USER, "password": PASSWORD},
        timeout=60,
    )
)
if token.get("status") not in (0, "IsValid"):
    sys.exit(f"Login failed: {token.get('status')}")
token = token["data"]["token"]


def api(path):
    """GET a JSON endpoint with the bearer token."""
    return check(requests.get(f"{BASE}{path}", headers={"Authorization": f"Bearer {token}"}, timeout=60))


sets = api("/api/control-set")  # live sets only: the API filters soft-deleted sets
print(f"{TENANT}: {len(sets)} live control set(s)")

# id -> display-value maps for every dropdown/linked field, from the API's
# published options. users/teams/roles use {value, label}; the control-item
# options use {id, name}.
maps = {}
for kind, path in [
    ("users", "/api/user/published-extended"),
    ("teams", "/api/team/published"),
    ("roles", "/api/role/published"),
    ("processes", "/api/control-item/options/processes"),
    ("risks", "/api/control-item/options/risks"),
    ("pages", "/api/control-item/options/pages"),
    ("legislation", "/api/control-item/options/legislation"),
    ("equipment", "/api/control-item/options/equipment"),
]:
    try:
        entries = api(path) or []
        maps[kind] = {e.get("value", e.get("id")): e.get("label", e.get("name")) for e in entries}
    except requests.HTTPError as error:  # lookups are an enhancement, not a requirement
        print(f"  note: {kind} display values unavailable ({error})")
        maps[kind] = {}
(OUT / "reference-data.json").write_text(json.dumps(maps, ensure_ascii=False), encoding="utf-8")


def add_display_values(obj):
    """For every `*Ids` list field, add a sibling `...Names` field with display values."""
    for key, value in list(obj.items()):
        if key.endswith("Ids") and isinstance(value, list):
            kind = next((k for k in ("user", "team", "role") if k in key.lower()), None)
            lookup = maps.get(kind + "s", {})
            obj[key[:-3] + "Names"] = [lookup.get(i, f"unknown id {i}") for i in value]

for control_set in sets:
    data = api(f"/api/control-set/{control_set['id']}/items")
    items = data if isinstance(data, list) else [data["values"][i] for i in data["ids"]]
    page = 2
    while isinstance(data, dict) and len(items) < data["totalCount"]:  # page-size cap safety
        data = api(f"/api/control-set/{control_set['id']}/items?Page={page}&PageSize=100")
        if not data.get("ids"):
            break
        items += [data["values"][i] for i in data["ids"]]
        page += 1
    for item in items:  # inline display values for people/dropdown ids
        add_display_values(item)
        for task in item.get("tasks") or []:
            add_display_values(task)

    slug = re.sub(r"\W+", "-", f"{control_set.get('standardCode')} {control_set.get('versionName')} {control_set['id'][:8]}".lower()).strip("-")
    (OUT / f"{slug}.yaml").write_text(
        yaml.safe_dump({"controlSet": control_set, "items": items}, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    print(f"  {slug}: {len(items)} items")
