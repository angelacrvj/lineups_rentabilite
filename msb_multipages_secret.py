import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random
import os
from st_aggrid import AgGrid, GridOptionsBuilder


# Chargement des données
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "lineups_rentabilite (2).csv")
data = pd.read_csv(file_path)
data["minutes_filtre"] = pd.to_timedelta(data["minutes_filtre"])
data["minutes_filtre_num"] = data["minutes_filtre"].dt.total_seconds() / 60

# Stats 
offensive_stats = ["Rentabilite_possessions_equipe", "Rentabilite_temps_equipe", "True_Shooting_%_equipe"]
defensive_stats = ["Rentabilite_possessions_opp", "Rentabilite_temps_opp", "True_Shooting_%_opp"]
all_stats = offensive_stats + defensive_stats

stat_rename = {
    "Rentabilite_possessions_equipe": "Points par poss. (offense)",
    "Rentabilite_temps_equipe": "Poss par match (offense)",
    "True_Shooting_%_equipe": "TS% (offense)",
    "Rentabilite_possessions_opp": "Points par poss. (defense)",
    "Rentabilite_temps_opp": "Poss par match (defense)",
    "True_Shooting_%_opp": "TS% (defense)"
}

# logos équpipes
team_logos = {
    'Le Mans': "logos_equipes/Le_Mans.png",
    'Ligue': "logos_equipes/Logo_Betclic_Elite_Pro_A.png",
    'JL Bourg-en-Bresse': "logos_equipes/JL_Bourg_en_Bresse.png",
    'Chalon Saone': "logos_equipes/Chalon_Saone.png",
    'Cholet Basket': "logos_equipes/Cholet_Basket.png",
    'BCM Gravelines-Dunkerque': "logos_equipes/BCM_Gravelines_Dunkerque.png",
    'JDA Dijon Basket': "logos_equipes/JDA_Dijon_Basket.png",
    'La Rochelle Rupella': "logos_equipes/La_Rochelle_Rupella.png",
    'CSP Limoges': "logos_equipes/CSP_Limoges.png",
    'ESSM Le Portel': "logos_equipes/ESSM_Le_Portel.png",
    'ASVEL Lyon-Villeurbanne': "logos_equipes/ASVEL_Lyon_Villeurbanne.png",
    'AS Monaco Basket': "logos_equipes/AS_Monaco_Basket.png",
    'SLUC Nancy Basket': "logos_equipes/SLUC_Nancy_Basket.png",
    'Nanterre 92': "logos_equipes/Nanterre_92.png",
    'Paris Basketball': "logos_equipes/Paris_Basketball.png",
    'Saint-Quentin': "logos_equipes/Saint-Quentin.png",
    'SIG Strasbourg': "logos_equipes/SIG_Strasbourg.png"
}

# --------------------- Calculs comparaisons de matchups --------------------- #
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

# ---------------------- Fonction heatmap pete sa mère ---------------------- #

def plot_heatmap(df, title, ax):
    """
    Plot two heatmaps: one for offensive stats and one for defensive stats.
    Offensive stats have a blue-to-red colormap, while defensive stats have a red-to-blue colormap.
    """
    # Renommer les colonnes et définir l'index
    df = df.rename(columns=stat_rename).set_index("Lineup").select_dtypes(include='number')
    
    # Séparer les données offensives et défensives
    df_offense = df[[stat_rename[stat] for stat in offensive_stats]]
    df_defense = df[[stat_rename[stat] for stat in defensive_stats]]
    
    # Créer les sous-graphes
    fig, axes = plt.subplots(1, 2, figsize=(15, 8), sharey=True, gridspec_kw={'wspace': 0.1})
    
    # Heatmap offensive
    sns.heatmap(df_offense, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5, ax=axes[0])
    axes[0].set_title("Statistiques Offensives")
    axes[0].set_ylabel("Lineup")  # Garde les ylabels ici
    axes[0].tick_params(axis='x', rotation=45)
    
    # Heatmap défensive (colormap inversée)
    sns.heatmap(df_defense, annot=True, fmt=".1f", cmap="coolwarm_r", linewidths=0.5, ax=axes[1])
    axes[1].set_title("Statistiques Défensives")
    axes[1].set_ylabel("")  # Supprime les ylabels
    axes[1].tick_params(left=False)  # Désactive les ticks à gauche
    axes[1].tick_params(axis='x', rotation=45)

    # Titre global
    fig.suptitle(title, fontsize=16)
    st.pyplot(fig)

# -------------------- Fonction radar chart pete sa mère -------------------- #
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
        values = [row[f"centile_{col}"] for col in ["Rentabilite_temps_equipe",
                                                    "Rentabilite_possessions_equipe", 
                                                    "Rentabilite_possessions_opp",
                                                    "Rentabilite_temps_opp",
                                                    "True_Shooting_%_opp",
                                                    "True_Shooting_%_equipe"]]
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
        values = [row[f"centile_{col}"] for col in ["Rentabilite_temps_equipe",
                                                    "Rentabilite_possessions_equipe", 
                                                    "Rentabilite_possessions_opp",
                                                    "Rentabilite_temps_opp",
                                                    "True_Shooting_%_opp",
                                                    "True_Shooting_%_equipe"]]
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

# --------------------- Création des filtres centralisés --------------------- #
# Filtres pour la page : Analyse Rentabilité 
def filters_analyse_rentabilite(data):
    """
    Crée les filtres pour la sélection de l'équipe, de l'équipe adverse, et des joueurs.
    
    :param data: Le DataFrame contenant toutes les données.
    :return: Les filtres appliqués et les équipes sélectionnées.
    """
    # Sélection des équipes
    team_name = st.sidebar.selectbox("Équipe de référence", data["Equipe"].unique())
    opponent_name = st.sidebar.selectbox("Équipe adverse", [team for team in data["Equipe"].unique() if team != team_name])

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

    team_players = extract_unique_players(data[data["Equipe"] == team_name])
    opponent_players = extract_unique_players(data[data["Equipe"] == opponent_name])

    # Sélection des joueurs à filtrer
    player_filter_team = st.sidebar.multiselect("Joueurs de l'équipe de référence", team_players)
    player_filter_opponent = st.sidebar.multiselect("Joueurs de l'équipe adverse", opponent_players)

    # Filtre sur la plage de minutes jouées
    min_minutes = int(data["minutes_filtre_num"].min())
    max_minutes = int(data["minutes_filtre_num"].max())
    selected_range = st.sidebar.slider("Plage de minutes jouées", min_value=0, max_value=max_minutes, value=(0, max_minutes))

    # Filtrage des données en fonction des minutes
    filtre_temporel = data[(data["minutes_filtre_num"] >= selected_range[0]) & (data["minutes_filtre_num"] <= selected_range[1])]

    return team_name, opponent_name, player_filter_team, player_filter_opponent, filtre_temporel

# Filtres pour la page : Statistiques Lineups 

def filters_stats_lineups(data):
    """
    Crée les filtres pour la page Statistiques Lineups : sélection des équipes et des joueurs.
    """
    # Sélection des équipes
    team_names = st.sidebar.multiselect("Sélectionner les équipes", data["Equipe"].unique(), default=[])

    # Filtrage des joueurs en fonction des équipes sélectionnées
    if team_names:
        players_in_selected_teams = data[data["Equipe"].isin(team_names)]
        team_players = set(
            players_in_selected_teams["Player_1_name"].tolist() +
            players_in_selected_teams["Player_2_name"].tolist() +
            players_in_selected_teams["Player_3_name"].tolist() +
            players_in_selected_teams["Player_4_name"].tolist() +
            players_in_selected_teams["Player_5_name"].tolist()
        )
    else:
        # Si aucune équipe n'est sélectionnée, on affiche tous les joueurs
        team_players = set(
            data["Player_1_name"].tolist() +
            data["Player_2_name"].tolist() +
            data["Player_3_name"].tolist() +
            data["Player_4_name"].tolist() +
            data["Player_5_name"].tolist()
        )
    
    player_filter = st.sidebar.multiselect("Sélectionner les joueurs", sorted([player for player in team_players if pd.notnull(player)]))

    # Filtre sur la plage de minutes jouées
    min_minutes = int(data["minutes_filtre_num"].min())
    max_minutes = int(data["minutes_filtre_num"].max())
    selected_range = st.sidebar.slider("Plage de minutes jouées", min_value=0, max_value=max_minutes, value=(0, max_minutes))
    
    # Filtrage des données en fonction des minutes
    filtre_temporel = data[(data["minutes_filtre_num"] >= selected_range[0]) & (data["minutes_filtre_num"] <= selected_range[1])]

    return team_names, player_filter, filtre_temporel


























# Nouvelle fonction pour afficher les tableaux avec AgGrid (Hagrid)
def display_aggrid_table(dataframe, fixed_column="Lineup"):

    # Création des options de configuration
    gb = GridOptionsBuilder.from_dataframe(dataframe)
    
    # Fixe la colonne spécifiée
    gb.configure_column(fixed_column, pinned="left")
    
    # Applique la classe CSS personnalisée à chaque colonne
    columns = dataframe.columns.tolist()  # Liste des noms de colonnes
    for col in columns:
        gb.configure_column(col, headerClass='custom-header')  # Applique à chaque colonne

    # Génère les options de tableau avec les colonnes configurées
    grid_options = gb.build()

    # CSS personnalisé pour les en-têtes
    custom_css = {
        ".custom-header": {
            "font-size": "14px",  # Taille du texte des en-têtes
            "font-weight": "bold"  # Gras pour les intitulés
        }
    }

    # Affiche le tableau avec les options configurées
    AgGrid(
        dataframe,
        gridOptions=grid_options,
        height=400,
        fit_columns_on_grid_load=False,  # Ajuste automatiquement les colonnes
        custom_css=custom_css,  # Injecte le CSS personnalisé
        enable_enterprise_modules=False
    )

































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
    #|----------------------------- Page d'acceuil ----------------------------|
def page_accueil():
    #st.title("Analyse des Lineups MSB 🏀")

    st.markdown("""
    <h1 style="text-align: center; margin-bottom: 30px; ">Analyse des Lineups MSB 🏀</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style="text-align: center; font-size: 22px;">Les chiffres ne mentent pas : analysez pour gagner !</h2>
    <br><br><br>
    """, unsafe_allow_html=True)

    st.write("Ce site trop waow va te permettre de visualiser et analyser la rentabilité des lineups des équipes de basket Betclic Elite 😍​🤯.")

    st.markdown("""
    **Fonctionnalités principales :**
    - **Analyse Rentabilité** : Compare les performances des équipes/lineups grâce à mes viz trop waow.
    - **Statistiques des Lineups** : Explorez les statistiques détaillées des lineups dans des tables trop waow.
    
    Pas folichon pour le moment mais bon je n'ai pas reçu la prose de la frappe de Chicagre 😢
                
    """)

    st.image(r"Easter egg/GIF/crying.gif")

    st.title("Du coup on va se contenter des vannes de cette dame 👇")
    st.image("Easter egg/09.png")

    st.title("Désolé pour le contre-temps bg : ma bouille en contre-partie")
    st.image("Easter egg/08.png")
    st.text("tu as le droit à un bonus pour le délai de maj et pour essayer de te changer les idées en espérant que tu ailles mieux 🤍")
    st.image("Easter egg/03.jpg")
    #|----------------------------- Renta lineups -----------------------------|


def page_analyse_rentabilite():
    # Interface Streamlit
    st.title("Analyse de Rentabilité des Lineups 🏀📊")
    st.sidebar.header("Filtres")

    # ajout des filtres centralisés 
    team_name, opponent_name,  player_filter_team, player_filter_opponent, filtre_temporel = filters_analyse_rentabilite(data)
    

    # Filtrage des joueurs en fonction de l'équipe sélectionnée
    team_data = filtre_temporel[filtre_temporel["Equipe"] == team_name]
    opponent_data = filtre_temporel[filtre_temporel["Equipe"] == opponent_name]

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


    # Affichage Heatmap : Équipe de référence vs Équipe adverse
    st.subheader(f"Heatmap : {team_name} vs {opponent_name}")
    col1, col2 = st.columns([0.5, 5])  
    with col1:
        if team_name in team_logos:
            st.image(team_logos[team_name], use_container_width=True, output_format="auto")
    with col2:
        matchup_df = calculate_matchup(team_data_filtered, opponent_data_filtered)
        plot_heatmap(matchup_df, f"Heatmap pour {team_name} contre {opponent_name}", plt.gca())

    # Affichage Heatmap : Équipe adverse vs Équipe de référence
    st.subheader(f"Heatmap : {opponent_name} vs {team_name}")
    col1, col2 = st.columns([0.5, 5])
    with col1:
        if opponent_name in team_logos:
            st.image(team_logos[opponent_name], use_container_width=True, output_format="auto")
    with col2:
        matchup_df_opponent = calculate_matchup(opponent_data_filtered, team_data_filtered)
        plot_heatmap(matchup_df_opponent, f"Heatmap pour {opponent_name} contre {team_name}", plt.gca())
        

    # Affichage Radar Chart
    st.subheader("Radar Chart")

    if st.button(" "):
        if not st.session_state["secret_unlocked"]:
            st.session_state["secret_unlocked"] = True
            st.sidebar.title("Menu")
            st.success("Beau travail, je crois que tu viens de trouver quelque chose 😏. (je te conseille de clicker à nouveau au même endroit)")
            st.stop()

    team1_lineups = st.multiselect(f"Lineups de {team_name} :", options=team_data["Lineup"].unique())
    team2_lineups = st.multiselect(f"Lineups de {opponent_name} :", options=opponent_data["Lineup"].unique())
    radar_chart(team1_lineups, team2_lineups, team_name, opponent_name)

    #|----------------------------- Stats tableau -----------------------------|

def page_statistiques_lineups():

    st.sidebar.header("Filtres")

    # ajout des filtres centralisés 
    team_names, player_filter, filtre_temporel = filters_stats_lineups(data)

    # Filtrage des données en fonction des équipes et des joueurs sélectionnés
    if team_names:
        filtered_data = filtre_temporel[filtre_temporel["Equipe"].isin(team_names)]
    else:
        filtered_data = filtre_temporel  # Si aucune équipe n'est sélectionnée, on garde toutes les équipes
    
    if player_filter:
        filtered_data = filtered_data[filtered_data["Player_1_name"].isin(player_filter) |
                                      filtered_data["Player_2_name"].isin(player_filter) |
                                      filtered_data["Player_3_name"].isin(player_filter) |
                                      filtered_data["Player_4_name"].isin(player_filter) |
                                      filtered_data["Player_5_name"].isin(player_filter)]
    

    st.title("Statistiques des Lineups 🎯")
    st.write("Cette page contient **4 tableaux** avec les statistiques clés des lineups. "
             "Vous pouvez cliquer sur les liens ci-dessous pour naviguer directement vers chaque tableau.")
    
    # Liste des tableaux avec liens cliquables
#    st.markdown("""
#    **Tableaux disponibles :**
#    - [Offense  / Overall](#offense)
#    - [Offense / Shooting](#offense-shooting)
#    - [Defense / Overall](#defense-overall)
#    - [Defense / Shooting](#defense-shooting)
#    """)



    # Liste des tableaux avec liens cliquables et descriptions à côté
    st.markdown("""
    **Tableaux disponibles :**
    - [Offense / Overall](#offense) : Ce tableau présente les statistiques offensives générales des lineups.
    - [Offense / Shooting](#offense-shooting) : Ce tableau montre les statistiques offensives liées au tir, comme le True Shooting %.
    - [Defense / Overall](#defense-overall) : Ce tableau résume les statistiques globales défensives des lineups.
    - [Defense / Shooting](#defense-shooting) : Ce tableau met en avant les statistiques défensives liées au tir.
    """)




    # Table 1 : Offense  / Overall
    st.markdown("### Offense / Overall", unsafe_allow_html=True)
    st.write("Ce tableau présente les statistiques offensives générales des lineups.")
    offense_columns = {
        "Equipe" :  "Equipe",
        "Lineup": "Lineup",
        "Plus/Minus": "Plus/Minus",
        "Minutes": "Minutes",
        "Possessions Equipe": "Possessions attaque",
        "Points Equipe": "Points marqués",
        "Rentabilite_possessions_equipe": "Points par 100 possessions",
        "centile_Rentabilite_possessions_equipe": "Centile Points par 100 possessions",
        "Rentabilite_temps_equipe": "Possessions par 40 minutes",
        "centile_Rentabilite_temps_equipe": "Centile Possessions par 40 minutes",
        "Pts_Tirs_Tentes_equipe": "Point par tir tenté",
        "centile_Pts_Tirs_Tentes_opp": "Centile Point par tir tenté",
        "Rebounds Equipe": "Rebounds Equipe",
        "Offensive rebounds Equipe": "Offensive rebounds Equipe",
        "Assists Equipe": "Assists Equipe",
        "Turnovers Equipe": "Turnovers Equipe"
    }
    #st.dataframe(filtered_data[offense_columns.keys()].rename(columns=offense_columns).round(1))

    df1 = filtered_data[offense_columns.keys()].rename(columns=offense_columns).round(1)
    display_aggrid_table(df1)


    # Table 2 : Offense / Shooting
    st.markdown("### Offense / Shooting", unsafe_allow_html=True)
    st.write("Ce tableau montre les statistiques offensives liées au tir, comme le True Shooting %.")
    offense_shooting_columns = {
        "Equipe" :  "Equipe",
        "Lineup": "Lineup",
        "Plus/Minus": "Plus/Minus",
        "Minutes": "Minutes",
        "True_Shooting_%_equipe": "True Shooting%",
        "centile_True_Shooting_%_equipe": "Centile True Shooting%",
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
    #st.dataframe(filtered_data[offense_shooting_columns.keys()].rename(columns=offense_shooting_columns).round(1))

    df2 = filtered_data[offense_shooting_columns.keys()].rename(columns=offense_shooting_columns).round(1)
    display_aggrid_table(df2)



    # Table 3 : Defense / Overall
    st.markdown("### Defense / Overall", unsafe_allow_html=True)
    st.write("Ce tableau résume les statistiques globales défensives des lineups.")
    defense_overall_columns = {
        "Equipe" :  "Equipe",
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
        "Assists Opposant": "Assists Opposant",
        "Turnovers Opposant": "Turnovers Opposant"
    }
    #st.dataframe(filtered_data[defense_overall_columns.keys()].rename(columns=defense_overall_columns).round(1))

    df3 = filtered_data[defense_overall_columns.keys()].rename(columns=defense_overall_columns).round(1)
    display_aggrid_table(df3)


    # Table 4 : Défense / Shooting
    st.markdown("### Defense / Shooting", unsafe_allow_html=True)
    st.write("Ce tableau met en avant les statistiques défensives liées au tir.")
    defense_shooting_columns = {
        "Equipe" :  "Equipe",
        "Lineup": "Lineup",
        "Plus/Minus": "Plus/Minus",
        "Minutes": "Minutes",
        "True_Shooting_%_equipe": "True Shooting%",
        "centile_True_Shooting_%_equipe": "Centile True Shooting%",
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
    #st.dataframe(filtered_data[defense_shooting_columns.keys()].rename(columns=defense_shooting_columns).round(1))


    df4 = filtered_data[defense_shooting_columns.keys()].rename(columns=defense_shooting_columns).round(1)
    display_aggrid_table(df4)












def page_secret():
    st.markdown("""
    <h1 style="text-align: center; margin-bottom: 30px; ">🎉 Bravo Azouloulou 🎉</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style="text-align: center; font-size: 22px;">Tes efforts ont payé, tu as trouvé la page secrète ! 🕵️</h2>
    <br><br><br>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center;font-size: 22px;">
            🌷🌸🌹🌺🌻🌼
        <br><br><br>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.image("Easter egg/06.jpg")  # Ajoute une image secrète, si tu le souhaites.



















    
#|-----------------------------------------------------------------------------|
# Initialisation de l'état de session pour la page secrète
if "secret_unlocked" not in st.session_state:
    st.session_state["secret_unlocked"] = False

# Définir la navigation
pages = {
    "Accueil": page_accueil,
    "Analyse Rentabilité": page_analyse_rentabilite,
    "Statistiques Lineups": page_statistiques_lineups
}

#st.sidebar.title("Menu")
#selection = st.sidebar.radio("Aller à :", list(pages.keys()))

# Afficher la page sélectionnée
#pages[selection]()



# Ajouter dynamiquement la page secrète si elle est débloquée
if st.session_state["secret_unlocked"]:
    pages["🕵️"] = page_secret

st.sidebar.title("Menu")
selection = st.sidebar.radio("Aller à :", list(pages.keys()))
pages[selection]()