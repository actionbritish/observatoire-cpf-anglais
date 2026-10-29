# Observatoire CPF anglais : données de la Caisse des Dépôts

Ce paquet reprend, sous forme de fichiers CSV, les données ouvertes de CDC et DGEFP sur les formations d'anglais engagées et proposées via le compte personnel de formation (CPF) : série mensuelle, certifications achetées, départements et catalogue d'offres. Les données sont publiées sous Licence Ouverte v2.0 (Etalab).

## Sources

| Jeu de données | Producteur | Page Caisse des Dépôts | Page data.gouv | Licence | Date de chargement |
|---|---|---|---|---|---|
| Moncompteformation - Les formations engagées | CDC et DGEFP | [https://opendata.caissedesdepots.fr/explore/dataset/moncompteformation_formations_engagees/](https://opendata.caissedesdepots.fr/explore/dataset/moncompteformation_formations_engagees/) | [https://www.data.gouv.fr/datasets/moncompteformation-les-formations-engagees](https://www.data.gouv.fr/datasets/moncompteformation-les-formations-engagees) | Licence Ouverte v2.0 (Etalab) | 01/10/2026 ; dernier mois publié : 2026-09 |
| Moncompteformation - L'offre de formation | CDC et DGEFP | [https://opendata.caissedesdepots.fr/explore/dataset/moncompteformation_catalogueformation/](https://opendata.caissedesdepots.fr/explore/dataset/moncompteformation_catalogueformation/) | [https://www.data.gouv.fr/datasets/moncompteformation-loffre-de-formation](https://www.data.gouv.fr/datasets/moncompteformation-loffre-de-formation) | Licence Ouverte v2.0 (Etalab) | 27/10/2026 |

## Méthode

Dossiers engagés : filtre `libelle_formacode_principal like "%anglais%"`.
Catalogue : filtre `libelle_code_formacode_principal like "%anglais%"`.

Chaque chiffre clé porte sa requête dans le champ `requetes` du fichier `data/observatoire-cpf-anglais.json`.

## Chiffres clés

| Libellé | Valeur | Date |
|---|---|---|
| dossiers CPF anglais engagés, janvier à septembre 2026 | 79 296 (contre 68 269, janvier à septembre 2025) | 01/10/2026 |
| montant engagé, janvier à septembre 2026 | 137 246 162 € (contre 158 572 454 €, janvier à septembre 2025) | 01/10/2026 |
| prix moyen pondéré d'un dossier, septembre 2026 | 1 478,79 € (contre 2 395,04 €, septembre 2025) | 01/10/2026 |
| part des dossiers suivis à distance, janvier à septembre 2026 | 51,9 % | 01/10/2026 |
| offres anglais au catalogue | 21 894 | 27/10/2026 |
| prix médian TTC d'une offre au catalogue | 1 650 € | 27/10/2026 |

## Fichiers

- `data/serie_mensuelle.csv` : Série mensuelle des dossiers CPF anglais engagés (81 lignes)
- `data/certifications_achetees.csv` : Certifications achetées (30 lignes)
- `data/departements.csv` : Dossiers par département (101 lignes)
- `data/catalogue_offres.csv` : Offres du catalogue (groupes d'offres identiques) (16025 lignes)
- `data/observatoire-cpf-anglais.json` : fichier source complet
- `CITATION.cff` : référence de citation
- `LICENSE` : licence
- `build.py` : génère les fichiers de `data/` à partir du JSON source

## Éditeur

SARL ACTION (marque ActionBRITISH), SIRET 53418175500016. L'éditeur propose des formations d'anglais finançables par le CPF (8 offres au catalogue extrait le 27/10/2026). Aucun organisme n'est classé ni mis en avant.

## Liens

[https://formation-anglais-cpf.com/observatoire-cpf-anglais-caisse-des-depots.html](https://formation-anglais-cpf.com/observatoire-cpf-anglais-caisse-des-depots.html)

[https://formation-anglais-cpf.com/blog/formation-anglais-cpf-prix.html](https://formation-anglais-cpf.com/blog/formation-anglais-cpf-prix.html)

[https://formation-anglais-cpf.com/](https://formation-anglais-cpf.com/)
