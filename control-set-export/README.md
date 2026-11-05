# Control set export example

Exports every live control set of a tenant (sets that are not archived or
deleted) as one YAML file per set, plus `reference-data.json` mapping ids to
display values. Each file contains the control set and every control item
with **every field the API returns**, in API order (new fields are picked up
automatically), readable by humans, LLMs and `yaml.safe_load`. Nothing is
filtered or omitted: statuses, all texts, tasks, evidence files, links, review
data and AI metadata are all included.

Display values are inlined for every id-bearing field: each `*Ids` field
(people, tasks) is followed by a sibling `...Names` field with resolved names.
`reference-data.json` also contains the id -> display-value maps for every
dropdown source - users, teams, roles, processes, risks, pages, legislation
and equipment (fetched from the control-item options endpoints). Linked
processes, risks, pages, legislation and equipment already carry their names
inside each item; evidence files carry their file names.

Output is written to `output/`, which is gitignored. Exports may contain
licensed standard texts (e.g. ISO via [SIS](https://www.sis.se)) - keep them
inside your tenant and local files; never commit or publish them.

## Configuration

Copy `.env.example` to `.env` and fill in your tenant domain, username and
password (the script logs in with `POST /api/Auth/login` and uses the returned
JWT bearer token - no API key needed):

```ini
AF_TENANT='yourtenant.ampliflow.com'
AF_USERNAME='you@yourcompany.com'
AF_PASSWORD='your_password'
```

## Running

```bash
pip install -r control-set-export/requirements.txt
python control-set-export/control_set_export.py
```

| Endpoint | Purpose |
| --- | --- |
| `POST /api/Auth/login` | Exchange username + password for a bearer token |
| `GET /api/control-set` | List the tenant's control sets (soft-deleted sets are filtered server-side) |
| `GET /api/control-set/{id}/items` | All control items of a set (`{ids, values, totalCount}` shape; pagination handled if needed) |
| `GET /api/user/published-extended`, `/api/team/published`, `/api/role/published` | People/team/role display values |
| `GET /api/control-item/options/{processes,risks,pages,legislation,equipment}` | Dropdown display values for linked entities |

See the [Swagger definition](https://app.ampliflow.com/swagger/index.html) for full request/response shapes.
