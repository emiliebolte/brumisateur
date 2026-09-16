(french below)
# Cool Bordeaux — Water & Misting Points

An interactive web app built with Streamlit to quickly locate active drinking fountains and water misters across the Bordeaux metropolitan area.
Try the app ! https://fontaine-brumisateur-bordeaux.streamlit.app/

---

## Key Features
- Interactive Map (Folium): Full overview of cooling points with custom icons and color coding.
- Dynamic Filters: Filter by equipment type and restrict display to active/functional points.
- Live GPS Geolocation: Automatic user location detection via browser geolocation.
- Nearest Point Finder: Great-circle distance calculation using the **Haversine formula** with instant visual highlighting on the map.
- 1-Click Walking Directions: Direct integration with Google Maps walking mode.

---

## Tech Stack & Data
- Core : Python, Streamlit, Pandas, NumPy.
- Mapping & Location : Folium, `streamlit-js-eval`.
- Data Pipeline : Preprocessed and cleaned upstream using **Dataiku DSS** (`points_fraicheur_bordeaux_clean.csv`).

-----
# FRENCH

# Fraîcheur Bordeaux — Points d'eau & Brumisateurs

Une application web interactive conçue avec Streamlit pour localiser rapidement les fontaines d'eau potable et les brumisateurs en service dans la métropole bordelaise.

Tester l'application ! https://fontaine-brumisateur-bordeaux.streamlit.app/

---

## Fonctionnalités : 
- Carte interactive (Folium) : visualisation globale des points de fraîcheur avec distinction visuelle (icônes & couleurs adaptées).
- Filtres opérationnels : affichage selon le type d'équipement et sélection stricte des équipements en service.
- Géolocalisation GPS en direct : détection automatique de la position de l'utilisateur.
- Calcul du point le plus proche : calcul de distance orthodromique via la formule de **Haversine** et surbrillance sur la carte.
- Itinéraire piéton 1-clic : redirection directe vers Google Maps en mode guidage piéton.

---

## Stack technique & Données
- Développement : Python, Streamlit, Pandas, NumPy.
- Cartographie & GPS : Folium, `streamlit-js-eval`.
- Pipeline Data : Données nettoyées et préparées en amont sous Dataiku DSS (`points_fraicheur_bordeaux_clean.csv`).


---
## Local Installation

```bash
git clone [https://github.com/emiliebolte/brumisateur](https://github.com/emiliebolte/brumisateur)
cd brumisateur
pip install -r requirements.txt
streamlit run app.py



