import streamlit as st
import datetime
import pandas as pd
import os
from garminconnect import Garmin

# Configuration de la page
st.set_page_config(page_title="Dashboard Muscu & ML", layout="wide")

st.title("ML & Musculation : Constitution du Dataset")
st.markdown("---")

# Securite : creation du dossier data
os.makedirs("data", exist_ok=True)
DATASET_FILE = "data/dataset_vivolift.csv"

st.header("Connexion et Extraction Garmin (30 derniers jours)")
with st.expander("Saisir les identifiants", expanded=True):
    col_email, col_pwd = st.columns(2)
    with col_email:
        garmin_email = st.text_input("Adresse Email")
    with col_pwd:
        garmin_password = st.text_input("Mot de passe", type="password")
        
    if st.button("Lancer l'extraction du dernier mois"):
        if garmin_email and garmin_password:
            try:
                st.info("Connexion aux serveurs Garmin...")
                client = Garmin(garmin_email, garmin_password)
                client.login()
                
                # Preparation de la boucle sur 30 jours
                today = datetime.date.today()
                historique_data = []
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(30):
                    # On remonte le temps jour par jour
                    current_date = today - datetime.timedelta(days=i)
                    date_str = current_date.isoformat()
                    
                    status_text.text(f"Extraction des donnees pour le {date_str}...")
                    
                    # Interrogation des APIs
                    stats = client.get_stats(date_str)
                    sleep_data = client.get_sleep_data(date_str)
                    
                    # Variables par defaut (Sommeil)
                    sommeil_profond_min = 0
                    sommeil_leger_min = 0
                    sommeil_rem_min = 0
                    sommeil_eveil_min = 0
                    
                    # Variables par defaut (Stress)
                    stress_moyen_score = None
                    stress_repos_min = 0
                    stress_bas_min = 0
                    stress_moyen_min = 0
                    stress_haut_min = 0
                    
                    # Extraction des durees de stress
                    if stats:
                        stress_moyen_score = stats.get("averageStressLevel")
                        stress_repos_min = (stats.get("restStressDuration") or 0) // 60
                        stress_bas_min = (stats.get("lowStressDuration") or 0) // 60
                        stress_moyen_min = (stats.get("mediumStressDuration") or 0) // 60
                        stress_haut_min = (stats.get("highStressDuration") or 0) // 60
                        
                    # Extraction des phases de sommeil
                    if sleep_data and "dailySleepDTO" in sleep_data:
                        sleep_dto = sleep_data["dailySleepDTO"]
                        sommeil_profond_min = sleep_dto.get("deepSleepSeconds", 0) // 60
                        sommeil_leger_min = sleep_dto.get("lightSleepSeconds", 0) // 60
                        sommeil_rem_min = sleep_dto.get("remSleepSeconds", 0) // 60
                        sommeil_eveil_min = sleep_dto.get("awakeSleepSeconds", 0) // 60

                    # Ajout a notre liste
                    historique_data.append({
                        "Date": date_str,
                        "Stress_Score_Moyen": stress_moyen_score,
                        "Stress_Repos_min": stress_repos_min,
                        "Stress_Bas_min": stress_bas_min,
                        "Stress_ZoneMoyenne_min": stress_moyen_min,
                        "Stress_Haut_min": stress_haut_min,
                        "Sommeil_Profond_min": sommeil_profond_min,
                        "Sommeil_Leger_min": sommeil_leger_min,
                        "Sommeil_Paradoxal_min": sommeil_rem_min,
                        "Sommeil_Eveil_min": sommeil_eveil_min
                    })
                    
                    # Mise a jour de la barre de progression
                    progress_bar.progress((i + 1) / 30)
                
                status_text.text("Extraction terminee !")
                
                # Conversion en base de donnees Pandas
                df_new = pd.DataFrame(historique_data)
                
                # Sauvegarde dans le dossier data
                df_new.to_csv(DATASET_FILE, index=False)
                st.success(f"Historique recupere avec succes ! {len(df_new)} jours enregistres.")
                
            except Exception as e:
                st.error(f"Erreur lors de l'extraction : {e}")
        else:
            st.error("Veuillez entrer vos identifiants.")

st.markdown("---")

st.header("Apercu de la Base de Donnees (ML)")

if os.path.exists(DATASET_FILE):
    df_dataset = pd.read_csv(DATASET_FILE)
    
    if not df_dataset.empty:
        st.dataframe(df_dataset)
        
        # Formatage pour les graphiques
        df_chart = df_dataset.set_index("Date").sort_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Phases de sommeil (Min)")
            colonnes_sommeil = ["Sommeil_Profond_min", "Sommeil_Leger_min", "Sommeil_Paradoxal_min"]
            st.bar_chart(df_chart[colonnes_sommeil])
            
        with col2:
            st.subheader("Zones de stress (Min)")
            colonnes_stress = ["Stress_Bas_min", "Stress_ZoneMoyenne_min", "Stress_Haut_min"]
            st.bar_chart(df_chart[colonnes_stress])
            
else:
    st.info("Aucun historique disponible. Lance l'extraction ci-dessus.")