import streamlit as st
import folium
import streamlit.components.v1 as components
from folium.plugins import LocateControl
from streamlit_js_eval import get_geolocation
import numpy as np
import pandas as pd


st.set_page_config(page_title="Fraîcheur Bordeaux", layout="wide")
st.title("Points d'eau et brumisateurs — Bordeaux Métropole")

# 1. Chargement et nettoyage des données
@st.cache_data
def load_data():
    df_raw = pd.read_csv("points_fraicheur_bordeaux_clean.csv", sep=None, engine="python")
    return df_raw.dropna(subset=["lat", "lon"])

df = load_data()

# 2. Fonction de calcul de distance (Haversine)
def calcul_distance_m(lat1, lon1, lat2, lon2):
    r = 6371000.0
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2)**2
    return 2 * r * np.arcsin(np.sqrt(a))

st.sidebar.header("Filtres d'affichage")
uniquement_actifs = st.sidebar.checkbox("Uniquement en service", value=True)
if uniquement_actifs:
    etats_actifs = ["en_service", "fonctionnelle"]
    df = df[df["etat"].astype(str).str.strip().str.lower().isin(etats_actifs)]
    
categories = st.sidebar.multiselect(
    "Type d'équipement :",
    options=df["categorie"].unique(),
    default=list(df["categorie"].unique())
)
df_filtre = df[df["categorie"].isin(categories)]
st.sidebar.metric("Points affichés", len(df_filtre))

# 4. Points cibles
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Trouver le plus proche")
besoin = st.sidebar.radio(
    "Quel est votre besoin ?",
    options=["💧 Fontaine (Boire)", "🌫️ Brumisateur (Se rafraîchir)", "🌟 N'importe quel point"]
)

if "Fontaine" in besoin:
    df_cible = df[df["categorie"] == "Fontaine"].copy()
elif "Brumisateur" in besoin:
    df_cible = df[df["categorie"] == "Brumisateur"].copy()
else:
    df_cible = df.copy()

# 5. Géolocalisation sécurisée
plus_proche = None
loc = get_geolocation()
if loc and isinstance(loc, dict) and "coords" in loc:
    user_lat, user_lon = loc["coords"]["latitude"], loc["coords"]["longitude"]
    if not df_cible.empty:
        df_cible["distance_m"] = calcul_distance_m(user_lat, user_lon, df_cible["lat"], df_cible["lon"])
        plus_proche = df_cible.sort_values("distance_m").iloc[0]
        st.sidebar.success(f"📍 Trouvé à **{int(plus_proche['distance_m'])} m** !")
        st.sidebar.markdown(f"**Nom :** {plus_proche['nom']}")
        st.sidebar.markdown(f"**État :** {plus_proche['etat']}")
        # Génération du lien piéton Google Maps
        dest_lat, dest_lon = plus_proche["lat"], plus_proche["lon"]
        gmaps_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={dest_lat},{dest_lon}&travelmode=walking"
        st.sidebar.link_button("🚶 Lancer l'itinéraire (Google Maps)", gmaps_url)
       
    else:
        st.sidebar.warning("Aucun équipement en service pour ce choix.")
else:
    st.sidebar.info("En attente de l'autorisation GPS du navigateur...")
    
        
   
    
    
# 6. Carte interactive
m = folium.Map(location=[44.837789, -0.57918], zoom_start=13)

for _, r in df_filtre.iterrows():
    is_brumi = r["categorie"] == "Brumisateur"
    icon = folium.Icon(
        icon="cloud" if is_brumi else "tint",
        color="green" if is_brumi else "blue",
        icon_color="white"
    )
    folium.Marker(
        location=[float(r["lat"]), float(r["lon"])],
        icon=icon,
        tooltip=str(r["nom"]),
        popup=f"<b>{r['nom']}</b><br>Type: {r['type']}<br>État: {r['etat']}"
    ).add_to(m)

LocateControl(
    auto_start=False,
    position="topleft",
    icon="fa fa-crosshairs",
    strings={"title": "Me localiser"}
).add_to(m)

# Surbrillance du point le plus proche
if plus_proche is not None:
    # 1. Halo / bulle rouge autour du point
    folium.Circle(
        location=[float(plus_proche["lat"]), float(plus_proche["lon"])],
        radius=40,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.35,
    ).add_to(m)

    # 2. Picto cible rouge vif
    folium.Marker(
        location=[float(plus_proche["lat"]), float(plus_proche["lon"])],
        icon=folium.Icon(icon="bullseye", prefix="fa", color="red", icon_color="white"),
        tooltip=f"🎯 LE PLUS PROCHE : {plus_proche['nom']} ({int(plus_proche['distance_m'])} m)",
        popup=f"<b>🎯 Équipement le plus proche !</b><br>{plus_proche['nom']}<br>À {int(plus_proche['distance_m'])} m"
    ).add_to(m)

map_html = m.get_root().render()
components.html(map_html, height=600, scrolling=False)
