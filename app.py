import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Dashboard Muscu & ML", layout="wide")

st.title("ML & Musculation : Suivi de Recuperation")
st.markdown("---")

# Barre laterale pour les donnees physiologiques
st.sidebar.header("Metriques du Jour")
sleep_score = st.sidebar.slider("Score de Sommeil (Garmin Vivoactive)", 0, 100, 75)
stress_level = st.sidebar.slider("Niveau de Stress moyen", 0, 100, 25)
body_battery = st.sidebar.slider("Body Battery au reveil", 0, 100, 80)

# Section centrale pour la seance de musculation
st.header("Parametres de la Seance")
muscle_group = st.selectbox("Groupe Musculaire", ["Jambes", "Dos", "Pectoraux", "Epaules", "Bras"])

st.markdown("---")

# Analyse des donnees
st.header("Analyse et Recommandation")

# Logique V1 axee uniquement sur la recuperation interne
recovery_score = (sleep_score * 0.5) + (body_battery * 0.3) - (stress_level * 0.2)

st.metric(label="Score de Recuperation Interne", value=f"{int(recovery_score)}/100")

if recovery_score < 50:
    st.warning("Attention : Le systeme nerveux n'est pas pret. Privilegie le repos ou une seance tres legere.")
elif recovery_score < 75:
    st.info("Recuperation moyenne. Maintiens la seance prevue mais garde une marge sur tes series (pas d'echec musculaire).")
else:
    st.success("Feu vert. Ton corps est pret pour une seance intense.")