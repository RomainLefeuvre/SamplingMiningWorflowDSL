import pandas as pd
from rapidfuzz import fuzz, process

# Charger les fichiers
csv1 = pd.read_csv("MSR_24.csv")
csv2 = pd.read_csv("../DBLP/msr.csv")

# Nettoyer les DOIs dans csv2
csv2["doi_clean"] = csv2["doi"].str.replace("https://doi.org/", "", regex=False)
# Créer dictionnaire titre → DOI (nettoyé)
title_to_doi = dict(zip(csv2["title"], csv2["doi_clean"]))

# Initialiser listes de log
fuzzy_matched = []
non_trouves = []


# Fonction de correspondance
def trouver_doi(titre_csv1, seuil=95):
    # Cherche d'abord une correspondance exacte
    if titre_csv1 in title_to_doi:
        return title_to_doi[titre_csv1], "exact"

    # Sinon fuzzy matching
    match, score, _ = process.extractOne(
        titre_csv1, title_to_doi.keys(), scorer=fuzz.token_sort_ratio
    )
    if score >= seuil:
        fuzzy_matched.append((titre_csv1, match, score))
        return title_to_doi[match], "fuzzy"

    # Aucun match
    non_trouves.append(titre_csv1)
    return None, "none"


# Appliquer correspondance à chaque ligne
dois = []
for titre in csv1["Document Title"]:
    doi, status = trouver_doi(titre)
    dois.append(doi)

csv1["DOI"] = dois

# Sauvegarder le fichier mis à jour
csv1.to_csv("csv1_mis_a_jour.csv", index=False)

# Afficher les résultats
print(f"\n🔍 Correspondances via fuzzy matching ({len(fuzzy_matched)} titres) :")
for titre1, titre2, score in fuzzy_matched:
    print(f"- '{titre1}' ≈ '{titre2}' (score: {score})")

print(f"\n❌ Titres sans aucun DOI trouvé ({len(non_trouves)}) :")
for titre in non_trouves:
    print(f"- {titre}")
