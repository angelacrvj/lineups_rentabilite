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

# Stats 
offensive_stats = ["Rentabilite_possessions_equipe", "Rentabilite_temps_equipe", "True_Shooting_equipe_%"]
defensive_stats = ["Rentabilite_possessions_opp", "Rentabilite_temps_opp", "True_Shooting_opp_%"]
all_stats = offensive_stats + defensive_stats

stat_rename = {
    "Rentabilite_possessions_equipe": "Points par poss. (offense)",
    "Rentabilite_temps_equipe": "Poss par match (offense)",
    "True_Shooting_equipe_%": "TS% (offense)",
    "Rentabilite_possessions_opp": "Points par poss. (defense)",
    "Rentabilite_temps_opp": "Poss par match (defense)",
    "True_Shooting_opp_%": "TS% (defense)"
}

# logos équpipes
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

# Calculs comparaisons de matchups
def calculate_matchup(team_lineups, opponent_lineups):
    results = []
    for _, lineup in team_lineups.iterrows():
        lineup_id = f"{lineup['Lineup']} (+/- : {round(lineup['Plus/Minus'],2)}, min: {lineup['Minutes']})"  
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

# Fonction heatmap pete sa mère
####def plot_heatmap(df, title, ax):
def plot_heatmap(df, title, ax, figsize=(10, 8)):  # ajout de figsize
    fig, ax = plt.subplots(figsize=figsize)
    df = df.rename(columns=stat_rename).set_index("Lineup").select_dtypes(include='number')
    sns.heatmap(df, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5, ax=ax)

    # Ligne de séparation des stats offensives et défensives
    separation_idx = len(offensive_stats)  # position
    ax.axvline(x=separation_idx, color="black", linewidth=2)

    ax.set_title(title)
    ax.set_ylabel("Lineup")
    ax.set_xlabel("")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    st.pyplot(fig)

# Fonction radar chart pete sa mère
def radar_chart(team1_lineups, team2_lineups, team_name, opponent_name):    
    categories = ["Poss par match (offense)", 
                  "Points par poss. (offense)", 
                  "Points par poss. (defense)", 
                  "Poss par match (defense)", 
                  "TS% (defense)", 
                  "TS% (offense)"] 

    fig = go.Figure()
    unique_lineups = list(set(team1_lineups + team2_lineups))
    color_mapping = {lineup: f"#{random.randint(0, 0xFFFFFF):06x}" for lineup in unique_lineups}

    # Lineups équipe 1
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
            hovertemplate="<b>%{theta}</b>: %{r:.2f}<extra></extra>" #génération d'info-bulle
        ))

    # Lineups équipe 2
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
            hovertemplate="<b>%{theta}</b>: %{r:.2f}<extra></extra>" #info-bulle
        ))

    # mise en page bg 
    fig.update_layout(
        title="Graphique Radar : Comparaison des Lineups 🏀",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#1E2D24")  # Changer la couleur des ticks radiaux
            ),
            angularaxis=dict(
                tickvals=[0, 1, 2, 3, 4, 5],
                ticktext=categories
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",  
            yanchor="bottom", 
            y=-0.5,  
            xanchor="center", 
            x=0.5  
        )
    )
    st.plotly_chart(fig)
#|-----------------------------------------------------------------------------|
#|------------------------------- Création Site -------------------------------|
#|-----------------------------------------------------------------------------|

# Configuration générale
st.set_page_config(
    page_title="Analyse Rentabilité Lineups MSB 🏀",
    page_icon="🏀",
    layout="wide",
)
#|-----------------------------------------------------------------------------|
# Définition des pages
    #|---------------------------- Page d'acceuil ----------------------------|
def page_accueil():
    st.title("Analyse des Lineups MSB 🏀")
    st.write("Ce site trop waow va te permettre de visualiser et analyser la rentabilité des lineups des équipes de basket Betclic Elite 😍​🤯.")
    st.markdown("""
    **Fonctionnalités principales :**
    - **Analyse Rentabilité** : Compare les performances des équipes/lineups grâce à mes viz trop waow.
    - **Statistiques des Lineups** : Explorez les statistiques détaillées des lineups dans des tables trop waow.
    """)
#    st.image("Easter egg\01.png")

    #|----------------------------- Renta lineups -----------------------------|
def page_analyse_rentabilite():
    # Interface Streamlit
    st.title("Analyse de Rentabilité des Lineups 🏀📊")
    st.sidebar.header("Filtres")

    # Sélection des équipes
    team_name = st.sidebar.selectbox("Équipe de référence", data["Equipe"].unique())
    opponent_name = st.sidebar.selectbox("Équipe adverse", ["Ligue"] + [team for team in data["Equipe"].unique() if team != team_name])
    
    # Filtrage des joueurs en fonction de l'équipe sélectionnée
    team_data = data[data["Equipe"] == team_name]
    opponent_data = data[data["Equipe"] == opponent_name]

    # Récupérer la liste des joueurs pour chaque équipe
    def extract_unique_players(df):
        players = set(
            df["Player_1_name"].tolist() +
            df["Player_2_name"].tolist() +
            df["Player_3_name"].tolist() +
            df["Player_4_name"].tolist() +
            df["Player_5_name"].tolist()
        )
        return sorted([player for player in players if pd.notnull(player)])

    team_players = extract_unique_players(team_data)
    opponent_players = extract_unique_players(opponent_data)
    
    # Filtre des joueurs
    player_filter_team = st.sidebar.multiselect("Joueurs de l'équipe de référence", team_players)
    player_filter_opponent = st.sidebar.multiselect("Joueurs de l'équipe adverse", opponent_players)

    # Filtrage des données des joueurs sélectionnés (que pour les heatmap)
    if player_filter_team:
        team_data_filtered = team_data[team_data["Player_1_name"].isin(player_filter_team) |
                            team_data["Player_2_name"].isin(player_filter_team) |
                            team_data["Player_3_name"].isin(player_filter_team) |
                            team_data["Player_4_name"].isin(player_filter_team) |
                            team_data["Player_5_name"].isin(player_filter_team)]
    else:
        team_data_filtered = team_data  # on prévoit les cas où monsieur basket ne filtre pas les joueurs 

    if player_filter_opponent:
        opponent_data_filtered = opponent_data[opponent_data["Player_1_name"].isin(player_filter_opponent) |
                                    opponent_data["Player_2_name"].isin(player_filter_opponent) |
                                    opponent_data["Player_3_name"].isin(player_filter_opponent) |
                                    opponent_data["Player_4_name"].isin(player_filter_opponent) |
                                    opponent_data["Player_5_name"].isin(player_filter_opponent)]
    else:
        opponent_data_filtered = opponent_data  # on prévoit les cas où monsieur basket ne filtre pas les joueurs 

    # Dimensionnement de la heatmap si "Ligue" sélectionné 
    ####if opponent_name == "Ligue":
        # Taille personnalisée pour "Ligue"
    ####    fig, ax = plt.subplots(figsize=(10, 2))  # Ajuste selon la taille souhaitée pour "Ligue"
    ####else:
        # Pas de figsize spécifié ici, matplotlib ajustera automatiquement la taille
    ####    fig, ax = plt.subplots()
    # Dimensionnement de la heatmap si "Ligue" sélectionné 
    if opponent_name == "Ligue":
        # Taille personnalisée pour "Ligue"
        plot_heatmap(matchup_df_opponent, f"Heatmap pour {team_name} contre {opponent_name}", ax, figsize=(10, 2))  # petite taille
    else:
        plot_heatmap(matchup_df_opponent, f"Heatmap pour {team_name} contre {opponent_name}", ax)


    # Affichage Heatmap : Équipe de référence vs Équipe adverse
    st.subheader(f"Heatmap : {team_name} vs {opponent_name}")
    col1, col2 = st.columns([0.5, 5])  
    with col1:
        if team_name in team_logos:
            st.image(team_logos[team_name])
    with col2:
        matchup_df = calculate_matchup(team_data_filtered, opponent_data_filtered)
        plot_heatmap(matchup_df, f"Heatmap pour {team_name} contre {opponent_name}", ax)

    # Affichage Heatmap : Équipe adverse vs Équipe de référence
    st.subheader(f"Heatmap : {opponent_name} vs {team_name}")
    col1, col2 = st.columns([0.5, 5])
    with col1:
        if opponent_name in team_logos:
            st.image(team_logos[opponent_name])
    with col2:
        matchup_df_opponent = calculate_matchup(opponent_data_filtered, team_data_filtered)
        plot_heatmap(matchup_df_opponent, f"Heatmap pour {opponent_name} contre {team_name}", plt.gca())
        

    # Affichage Radar Chart
    st.subheader("Radar Chart")
    team1_lineups = st.multiselect(f"Lineups de {team_name} :", options=team_data["Lineup"].unique())
    team2_lineups = st.multiselect(f"Lineups de {opponent_name} :", options=opponent_data["Lineup"].unique())
    radar_chart(team1_lineups, team2_lineups, team_name, opponent_name)

    #|----------------------------- Stats tableau -----------------------------|

def page_statistiques_lineups():
    st.title("Statistiques des Lineups 🎯")
    st.write("Cette page contient **4 tableaux** avec les statistiques clés des lineups. "
             "Vous pouvez cliquer sur les liens ci-dessous pour naviguer directement vers chaque tableau.")
    
    # Liste des tableaux avec liens cliquables
    st.markdown("""
    **Tableaux disponibles :**
    - [Offense](#offense)
    - [Offense/Shooting](#offense-shooting)
    - [Defense / Overall](#defense-overall)
    - [Defense / Shooting](#defense-shooting)
    """)

    # Table 1 : Offense
    st.markdown("### Offense", unsafe_allow_html=True)
    st.write("Ce tableau présente les statistiques offensives générales des lineups.")
    offense_columns = {
        "Lineup": "Lineup",
        "Plus/Minus": "Plus/Minus",
        "Minutes": "Minutes",
        "Possessions Equipe": "Possessions Equipe",
        "Points Equipe": "Points Equipe",
        "Rentabilite_possessions_equipe": "Points par 100 possessions",
        "centile_Rentabilite_possessions_equipe": "Centile Points par 100 possessions",
        "Rentabilite_temps_equipe": "Possessions par 40 minutes",
        "centile_Rentabilite_temps_equipe": "Centile Possessions par 40 minutes",
        "Pts_Tirs_Tentes_equipe": "Point par tir tenté",
        "centile_Pts_Tirs_Tentes_opp": "Centile Point par tir tenté",
        "Rebounds Equipe": "Rebounds Equipe",
        "Offensive rebounds Equipe": "Offensive rebounds Equipe",
        "Defensive rebounds Equipe": "Defensive rebounds Equipe",
        "Assists Equipe": "Assists Equipe",
        "Steals Equipe": "Steals Equipe",
        "Turnovers Equipe": "Turnovers Equipe",
        "Fouls Equipe": "Fouls Equipe"
    }
    st.dataframe(data[offense_columns.keys()].rename(columns=offense_columns))

    # Table 2 : Offense/Shooting
    st.markdown("### Offense/Shooting", unsafe_allow_html=True)
    st.write("Ce tableau montre les statistiques offensives liées au tir, comme le True Shooting %.")
    offense_shooting_columns = {
        "True_Shooting_equipe_%": "True Shooting%",
        "centile_True_Shooting_equipe_%": "Centile True Shooting%",
        "Field goals attempted Equipe": "Field goals attempted Equipe",
        "Field goals made Equipe": "Field goals made Equipe",
        "2-pt field goals attempted Equipe": "2-pt field goals attempted Equipe",
        "2-pt field goals made Equipe": "2-pt field goals made Equipe",
        "2-pt field goals, % Equipe": "2-pt field goals, % Equipe",
        "centile_2-pt field goals, % Equipe": "Centile 2-pt field goals, % Equipe",
        "3-pt field goals attempted Equipe": "3-pt field goals attempted Equipe",
        "3-pt field goals made Equipe": "3-pt field goals made Equipe",
        "3-pt field goals, % Equipe": "3-pt field goals, % Equipe",
        "centile_3-pt field goals, % Equipe": "Centile 3-pt field goals, % Equipe",
        "Free throws attempted Equipe": "Free throws attempted Equipe",
        "Free throws made Equipe": "Free throws made Equipe",
        "Free throws, % Equipe": "Free throws, % Equipe",
        "Rebounds Equipe": "Rebounds Equipe",
        "Offensive rebounds Equipe": "Offensive rebounds Equipe",
        "Defensive rebounds Equipe": "Defensive rebounds Equipe",
        "Assists Equipe": "Assists Equipe",
        "Steals Equipe": "Steals Equipe",
        "Turnovers Equipe": "Turnovers Equipe",
        "Fouls Equipe": "Fouls Equipe"
    }
    st.dataframe(data[offense_shooting_columns.keys()].rename(columns=offense_shooting_columns))

    # Table 3 : Defense / Overall
    st.markdown("### Defense / Overall", unsafe_allow_html=True)
    st.write("Ce tableau résume les statistiques globales défensives des lineups.")
    defense_overall_columns = {
        "Lineup": "Lineup",
        "Plus/Minus": "Plus/Minus",
        "Minutes": "Minutes",
        "Possessions Opposant": "Possessions Opposant",
        "Points Opposant": "Points Opposant",
        "Rentabilite_possessions_opp": "Points par 100 possessions",
        "centile_Rentabilite_possessions_opp": "Centile Points par 100 possessions",
        "Rentabilite_temps_opp": "Possessions par 40 minutes",
        "centile_Rentabilite_temps_opp": "Centile Possessions par 40 minutes",
        "Pts_Tirs_Tentes_equipe": "Point par tir tenté",
        "centile_Pts_Tirs_Tentes_opp": "Centile Point par tir tenté",
        "Rebounds Opposant": "Rebounds Opposant",
        "Offensive rebounds Opposant": "Offensive rebounds Opposant",
        "Defensive rebounds Opposant": "Defensive rebounds Opposant",
        "Assists Opposant": "Assists Opposant",
        "Steals Opposant": "Steals Opposant",
        "Turnovers Opposant": "Turnovers Opposant",
        "Fouls Opposant": "Fouls Opposant"
    }
    st.dataframe(data[defense_overall_columns.keys()].rename(columns=defense_overall_columns))

    # Table 4 : Défense / Shooting
    st.markdown("### Defense / Shooting", unsafe_allow_html=True)
    st.write("Ce tableau met en avant les statistiques défensives liées au tir.")
    defense_shooting_columns = {
        "True_Shooting_equipe_%": "True Shooting%",
        "centile_True_Shooting_equipe_%": "Centile True Shooting%",
        "Field goals attempted Opposant": "Field goals attempted Opposant",
        "Field goals made Opposant": "Field goals made Opposant",
        "2-pt field goals attempted Opposant": "2-pt field goals attempted Opposant",
        "2-pt field goals made Opposant": "2-pt field goals made Opposant",
        "2-pt field goals, % Opposant": "2-pt field goals, % Opposant",
        "centile_2-pt field goals, % Opposant": "Centile 2-pt field goals, % Opposant",
        "3-pt field goals attempted Opposant": "3-pt field goals attempted Opposant",
        "3-pt field goals made Opposant": "3-pt field goals made Opposant",
        "3-pt field goals, % Opposant": "3-pt field goals, % Opposant",
        "centile_3-pt field goals, % Opposant": "Centile 3-pt field goals, % Opposant",
        "Free throws attempted Opposant": "Free throws attempted Opposant",
        "Free throws made Opposant": "Free throws made Opposant",
        "Free throws, % Opposant": "Free throws, % Opposant",
        "Assists Opposant": "Assists Opposant",
        "Steals Opposant": "Steals Opposant",
        "Turnovers Opposant": "Turnovers Opposant",
        "Fouls Opposant": "Fouls Opposant"
    }
    st.dataframe(data[defense_shooting_columns.keys()].rename(columns=defense_shooting_columns))

    
#|-----------------------------------------------------------------------------|

# Définir la navigation
pages = {
    "Accueil": page_accueil,
    "Analyse Rentabilité": page_analyse_rentabilite,
    "Statistiques Lineups": page_statistiques_lineups
}

st.sidebar.title("Menu")
selection = st.sidebar.radio("Aller à :", list(pages.keys()))

# Afficher la page sélectionnée
pages[selection]()