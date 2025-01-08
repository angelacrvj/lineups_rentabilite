import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random
import os

# Chargement des données
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "lineups_rentabilite_wt_league.csv")
data = pd.read_csv(file_path)

# Configuration générale
st.set_page_config(
    page_title="Analyse Rentabilité Lineups MSB 🏀",
    page_icon="🏀",
    layout="wide",
)

# Dictionnaire des logos des équipes
team_logos = {
    'Le Mans': "logos_equipes/Le_Mans_50px.png",
    'Ligue': "logos_equipes/Logo_Betclic_Elite_Pro_A_50px.png",
    'JL Bourg-en-Bresse': "logos_equipes/JL_Bourg_en_Bresse_50px.png",
    'Chalon Saone': "logos_equipes/Chalon_Saone_50px.png",
    'Cholet Basket': "logos_equipes/Cholet_Basket_50px.png",
    'BCM Gravelines-Dunkerque': "logos_equipes/BCM_Gravelines_Dunkerque_50px.png",
    'JDA Dijon Basket': "logos_equipes/JDA_Dijon_Basket_50px.png",
    'La Rochelle Rupella': "logos_equipes/La_Rochelle_Rupella_50px.png",
    'CSP Limoges': "logos_equipes/CSP_Limoges_50px.png",
    'ESSM Le Portel': "logos_equipes/ESSM_Le_Portel_50px.png",
    'ASVEL Lyon-Villeurbanne': "logos_equipes/ASVEL_Lyon_Villeurbanne_50px.png",
    'AS Monaco Basket': "logos_equipes/AS_Monaco_Basket_50px.png",
    'SLUC Nancy Basket': "logos_equipes/SLUC_Nancy_Basket_50px.png",
    'Nanterre 92': "logos_equipes/Nanterre_92_50px.png",
    'Paris Basketball': "logos_equipes/Paris_Basketball_50px.png",
    'Saint-Quentin': "logos_equipes/Saint-Quentin_50px.png",
    'SIG Strasbourg': "logos_equipes/SIG_Strasbourg_50px.png",
}

# Fonction de calcul des matchups
def calculate_matchup(team_lineups, opponent_lineups):
    results = []
    for _, lineup in team_lineups.iterrows():
        lineup_id = f"{lineup['Lineup']} (+/- : {lineup['Plus/Minus']}, min: {lineup['Minutes']})"
        row = {"Lineup": lineup_id}

        for stat in all_stats:
            if stat in offensive_stats:
                opp_stat = stat.replace("equipe", "opp")
                opponent_stat_mean = opponent_lineups[opp_stat].mean()
                row[stat] = lineup[stat] - opponent_stat_mean
            else:
                opp_stat = stat.replace("opp", "equipe")
                opponent_stat_mean = opponent_lineups[opp_stat].mean()
                row[stat] = lineup[stat] - opponent_stat_mean

        results.append(row)
    return pd.DataFrame(results)

# Fonction pour générer la heatmap
def plot_heatmap(df, title, ax):
    fig, ax = plt.subplots()
    df = df.rename(columns=stat_rename).set_index("Lineup").select_dtypes(include='number')
    sns.heatmap(df, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5, ax=ax)

    separation_idx = len(offensive_stats)
    ax.axvline(x=separation_idx, color="black", linewidth=2)

    ax.set_title(title)
    ax.set_ylabel("Lineup")
    ax.set_xlabel("")
    st.pyplot(fig)

# Fonction pour générer le radar chart
def radar_chart(team1_lineups, team2_lineups):
    categories = ["Poss par match (offense)", "Points par poss. (offense)", "Points par poss. (defense)",
                  "Poss par match (defense)", "TS% (defense)", "TS% (offense)"]

    fig = go.Figure()
    unique_lineups = list(set(team1_lineups + team2_lineups))
    color_mapping = {lineup: f"#{random.randint(0, 0xFFFFFF):06x}" for lineup in unique_lineups}

    for lineup in team1_lineups:
        row = data[data["Lineup"] == lineup].iloc[0]
        values = [row[f"centile_{col}"] for col in ["Rentabilite_possessions_equipe", "Rentabilite_possessions_opp",
                   "Rentabilite_temps_equipe", "Rentabilite_temps_opp",
                   "True_Shooting_equipe_%", "True_Shooting_opp_%"]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name=f"{team_name} - {lineup}",
            line=dict(color=color_mapping[lineup]),
            hovertemplate="<b>%{theta}</b>: %{r:.2f}<extra></extra>"
        ))

    for lineup in team2_lineups:
        row = data[data["Lineup"] == lineup].iloc[0]
        values = [row[f"centile_{col}"] for col in ["Rentabilite_possessions_equipe", "Rentabilite_possessions_opp",
                   "Rentabilite_temps_equipe", "Rentabilite_temps_opp",
                   "True_Shooting_equipe_%", "True_Shooting_opp_%"]]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name=f"{opponent_name} - {lineup}",
            line=dict(color=color_mapping[lineup]),
            hovertemplate="<b>%{theta}</b>: %{r:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title="Graphique Radar : Comparaison des Lineups 🏀",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
        ),
        showlegend=True
    )
    st.plotly_chart(fig)

# Définir les pages
def page_accueil():
    st.title("Analyse des Lineups MSB 🏀")
    st.write("Ce site permet de visualiser et analyser la rentabilité des lineups des équipes de basket Betclic Elite.")
    st.image("easter_egg.png")

def page_analyse_rentabilite():
    st.title("Analyse de Rentabilité des Lineups 🏀")
    st.sidebar.header("Filtres")
    team_name = st.sidebar.selectbox("Équipe de référence", data["Equipe"].unique())
    opponent_name = st.sidebar.selectbox("Équipe adverse", ["Ligue"] + [team for team in data["Equipe"].unique() if team != team_name])
    team_data = data[data["Equipe"] == team_name]
    opponent_data = data[data["Equipe"] == opponent_name]

    team1_lineups = st.multiselect(f"Lineups de {team_name} :", options=team_data["Lineup"].unique())
    team2_lineups = st.multiselect(f"Lineups de {opponent_name} :", options=opponent_data["Lineup"].unique())

    radar_chart(team1_lineups, team2_lineups)

def page_statistiques_lineups():
    st.title("Statistiques des Lineups 📊")
    st.dataframe(data)

# Définir la navigation
pages = {
    "Accueil": page_accueil,
    "Analyse Rentabilité": page_analyse_rentabilite,
    "Statistiques Lineups": page_statistiques_lineups,
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Aller à :", list(pages.keys()))

# Afficher la page sélectionnée
pages[selection]()