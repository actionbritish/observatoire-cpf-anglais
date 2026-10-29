#!/usr/bin/env python3
"""Génère le paquet de données à partir du JSON source (stdlib seule, rejouable)."""
import csv
import json
import os
import shutil

SRC = os.environ.get(
    "OBS_SRC",
    r"C:\Users\treso\Downloads\facpf-deploy\data\observatoire-cpf-anglais.json",
)
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

with open(SRC, encoding="utf-8") as f:
    d = json.load(f)

cat = d["catalogue"]
tables = {
    "serie_mensuelle.csv": (None, d["serie_mensuelle"]),
    "certifications_achetees.csv": (None, d["certifications_achetees"]),
    "departements.csv": (None, d["departements"]),
    "catalogue_offres.csv": (cat["colonnes"], cat["offres"]),
}
DESC = {
    "serie_mensuelle.csv": "Série mensuelle des dossiers CPF anglais engagés",
    "certifications_achetees.csv": "Certifications achetées",
    "departements.csv": "Dossiers par département",
    "catalogue_offres.csv": "Offres du catalogue (groupes d'offres identiques)",
}


def ftype(vals):
    vals = [v for v in vals if v not in ("", None)]
    if vals and all(isinstance(v, int) and not isinstance(v, bool) for v in vals):
        return "integer"
    if vals and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in vals):
        return "number"
    return "string"


counts, fields = {}, {}
for name, (cols, rows) in tables.items():
    if cols is None:
        cols = list(rows[0].keys())
        matrix = [[r[c] for c in cols] for r in rows]
    else:
        matrix = rows
    with open(os.path.join(DATA, name), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        w.writerows(matrix)
    counts[name] = len(matrix)
    fields[name] = [
        {"name": c, "type": ftype([r[i] for r in matrix])} for i, c in enumerate(cols)
    ]

shutil.copyfile(SRC, os.path.join(DATA, "observatoire-cpf-anglais.json"))

lic = d["licence"]
srcs = d["sources"]
ed = d["editeur"]

# datapackage.json
dp = {
    "name": "observatoire-cpf-anglais",
    "title": d["titre"],
    "licenses": [{"name": "etalab-2.0", "path": lic["url"]}],
    "sources": [
        {"title": s["titre"], "path": s["page_caisse_des_depots"], "producteur": s["producteur"]}
        for s in srcs
    ],
    "resources": [
        {
            "name": n[:-4].replace("_", "-"),
            "path": "data/" + n,
            "format": "csv",
            "mediatype": "text/csv",
            "encoding": "utf-8",
            "description": DESC[n],
            "schema": {"fields": fields[n]},
        }
        for n in tables
    ],
}
with open(os.path.join(HERE, "datapackage.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(dp, f, ensure_ascii=False, indent=2)
    f.write("\n")

# CITATION.cff
cff = f"""cff-version: 1.2.0
message: "Merci de citer ce jeu de données."
title: "{d['titre']}"
type: dataset
authors:
  - name: "SARL ACTION (ActionBRITISH)"
version: "2026-10-27"
date-released: "2026-10-29"
license: Etalab-2.0
"""
with open(os.path.join(HERE, "CITATION.cff"), "w", encoding="utf-8", newline="\n") as f:
    f.write(cff)

# LICENSE
prod = "\n".join(
    f"- {s['titre']} : {s['producteur']} ({s['page_caisse_des_depots']})" for s in srcs
)
lic_txt = f"""{lic['nom']}

Texte de la licence : {lic['url']}

Les données sont réutilisables dans les conditions de cette licence, avec mention de la paternité des producteurs :
{prod}
"""
with open(os.path.join(HERE, "LICENSE"), "w", encoding="utf-8", newline="\n") as f:
    f.write(lic_txt)


# README.md
def fmt(v):
    if isinstance(v, float):
        i, _, fr = repr(v).partition(".")
        i = f"{int(i):,}".replace(",", " ")
        return i if fr == "0" else i + "," + fr
    if isinstance(v, int):
        return f"{v:,}".replace(",", " ")
    return str(v)


def fr_date(s):
    y, m, dd = s[:10].split("-")
    return f"{dd}/{m}/{y}"


rows_src = []
for s in srcs:
    last = s.get("dernier_mois_publie")
    load = s.get("date_chargement") or s.get("date_extract")
    info = fr_date(load) if load else ""
    if last:
        info += f" ; dernier mois publié : {last}"
    rows_src.append(
        f"| {s['titre']} | {s['producteur']} | [{s['page_caisse_des_depots']}]({s['page_caisse_des_depots']}) "
        f"| [{s['page_data_gouv']}]({s['page_data_gouv']}) | {s['licence']} | {info} |"
    )

rows_cle = []
for c in d["chiffres_cles"]:
    unit = " €" if c["id"].endswith("_eur") else " %" if c["id"].endswith("_pct") else ""
    val = fmt(c["valeur"]) + unit
    if "comparaison" in c:
        val += f" (contre {fmt(c['comparaison']['valeur'])}{unit}, {c['comparaison']['periode']})"
    rows_cle.append(f"| {c['libelle']} | {val} | {fr_date(c['date'])} |")

files = "\n".join(
    f"- `data/{n}` : {DESC[n]} ({counts[n]} lignes)" for n in tables
)
S1 = "https://formation-anglais-cpf.com/observatoire-cpf-anglais-caisse-des-depots.html"
S2 = "https://formation-anglais-cpf.com/blog/formation-anglais-cpf-prix.html"
S3 = "https://formation-anglais-cpf.com/"

readme = f"""# {d['titre']}

Ce paquet reprend, sous forme de fichiers CSV, les données ouvertes de {srcs[0]['producteur']} sur les formations d'anglais engagées et proposées via le compte personnel de formation (CPF) : série mensuelle, certifications achetées, départements et catalogue d'offres. Les données sont publiées sous {lic['nom']}.

## Sources

| Jeu de données | Producteur | Page Caisse des Dépôts | Page data.gouv | Licence | Date de chargement |
|---|---|---|---|---|---|
{chr(10).join(rows_src)}

## Méthode

Dossiers engagés : filtre `{d['definition']['engagees']}`.
Catalogue : filtre `{d['definition']['catalogue']}`.

Chaque chiffre clé porte sa requête dans le champ `requetes` du fichier `data/observatoire-cpf-anglais.json`.

## Chiffres clés

| Libellé | Valeur | Date |
|---|---|---|
{chr(10).join(rows_cle)}

## Fichiers

{files}
- `data/observatoire-cpf-anglais.json` : fichier source complet
- `datapackage.json` : description Frictionless
- `CITATION.cff` : référence de citation
- `LICENSE` : licence
- `build.py` : génère les fichiers de `data/` à partir du JSON source

## Éditeur

{ed['nom']} (marque {ed['marque']}), SIRET {ed['siret']}. {ed['conflit_interets']}

## Liens

[{S1}]({S1})

[{S2}]({S2})

[{S3}]({S3})
"""
with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write(readme)

for n in tables:
    print(n, counts[n], "lignes (source:", len(tables[n][1]), ")")
