import requests
import pandas as pd

# 1. Data recovery : fountains
url_fontaines = "https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/bor_fontaines_eau_potable/records"
offset = 0
all_fontaines = []

while True:
    res = requests.get(url_fontaines, params={"limit": 100, "offset": offset}).json()
    records = res.get("results", [])
    if not records:
        break
    all_fontaines.extend(records)
    offset += 100

df_fontaines_raw = pd.json_normalize(all_fontaines)
df_fontaines = pd.DataFrame({
    "id": df_fontaines_raw["id"],
    "nom": df_fontaines_raw["nom_fontaine"],
    "type": df_fontaines_raw["modele_fontaine"],
    "etat": df_fontaines_raw["etat"],
    "commune": df_fontaines_raw["code_insee"],
    "lon": df_fontaines_raw["geom.lon"],
    "lat": df_fontaines_raw["geom.lat"],
    "categorie": "Fontaine"
})

# 2. Data recovery : water misters
url_brumi = "https://geo.bordeaux-metropole.fr/adws/app/33cebc9f-cd8e-11ed-ad24-9bf3b515cd35/services/aas/v1/infoSheets/getData"
sheet_id = "9c7e1e2e-fbd5-11ed-860c-4b9f9d2d7221"
brumisateurs = []

for gid in range(1, 60):
    params = {"centroid": "true", "id": sheet_id, "idValue": gid, "srs": "EPSG:4326"}
    res = requests.get(url_brumi, params=params)
    if res.status_code == 200:
        data = res.json()
        props = data.get("properties", {})
        coords = data.get("geometry", {}).get("coordinates", [None, None])
        if props and coords[0] is not None:
            brumisateurs.append({
                "id": props.get("GID"),
                "nom": props.get("NOM"),
                "type": props.get("TYPE"),
                "etat": props.get("ETAT"),
                "commune": props.get("INSEE"),
                "lon": coords[0],
                "lat": coords[1],
                "categorie": "Brumisateur"
            })

df_brumi = pd.DataFrame(brumisateurs)

# 3. Concatenate & save
df_final = pd.concat([df_brumi, df_fontaines], ignore_index=True)
df_final.to_csv("points_fraicheur_bordeaux_clean.csv", index=False)
