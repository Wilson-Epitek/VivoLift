import streamlit as st
import datetime
from garminconnect import Garmin

# Configuration de la page
st.set_page_config(page_title="Dashboard Muscu & ML", layout="wide")

st.title("ML & Musculation : Suivi de Recuperation")

if "sleep_val" not in st.session_state:
    st.session_state.sleep_val = 75
if "stress_val" not in st.session_state:
    st.session_state.stress_val = 25
if "bb_val" not in st.session_state:
    st.session_state.bb_val = 80

st.header("Connexion Garmin Connect")
with st.expander("Saisir les identifiants", expanded=True):
    col_email, col_pwd = st.columns(2)
    with col_email:
        garmin_email = st.text_input("Adresse Email")
    with col_pwd:
        garmin_password = st.text_input("Mot de passe", type="password")
        
    if st.button("Synchroniser les donnees"):
        if garmin_email and garmin_password:
            try:
                with st.spinner("Connexion aux serveurs Garmin en cours..."):
                    client = Garmin(garmin_email, garmin_password)
                    client.login()
                    
                    today = datetime.date.today().isoformat()
                    
                    stats = client.get_stats(today)
                    sleep_data = client.get_sleep_data(today)
                    
                    if stats:
                        st.session_state.stress_val = int(stats.get("averageStressLevel", 25))
                        st.session_state.bb_val = int(stats.get("bodyBatteryHighestValue", 80))
                        
                    if sleep_data and "dailySleepDTO" in sleep_data:
                        score = sleep_data["dailySleepDTO"].get("sleepScores", {}).get("overall", {}).get("value")
                        if score:
                            st.session_state.sleep_val = int(score)
                    
                    st.success("Extraction reussie. Tes metriques sont a jour.")
            except Exception as e:
                st.error("Erreur de connexion. Verifie tes identifiants.")
        else:
            st.error("Veuillez entrer vos identifiants.")
st.markdown("---")

# BARRE LATERALE
st.sidebar.header("Metriques du Jour")
sleep_score = st.sidebar.slider("Score de Sommeil (Garmin Vivoactive)", 0, 100, st.session_state.sleep_val)
stress_level = st.sidebar.slider("Niveau de Stress moyen", 0, 100, st.session_state.stress_val)
body_battery = st.sidebar.slider("Body Battery au reveil", 0, 100, st.session_state.bb_val)

# SECTION CENTRAL
st.header("Parametres de la Seance")
muscle_group = st.selectbox("Groupe Musculaire", ["Jambes", "Dos", "Pectoraux", "Epaules", "Bras"])

st.markdown("---")

#ANALYSE
st.header("Analyse et Recommandation")

recovery_score = (sleep_score * 0.5) + (body_battery * 0.3) - (stress_level * 0.2)

st.metric(label="Score de Recuperation Interne", value=f"{int(recovery_score)}/100")

if recovery_score < 50:
    st.warning("Attention : Le systeme nerveux n'est pas pret. Privilegie le repos ou une seance tres legere.")
elif recovery_score < 75:
    st.info("Recuperation moyenne. Maintiens la seance prevue mais garde une marge sur tes series (pas d'echec musculaire).")
else:
    st.success("Feu vert. Ton corps est pret pour une seance intense.")