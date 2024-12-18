import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random

data = pd.read_csv("lineups_rentabilite.csv")

offensive_stats = ["Rentabilite_possessions_equipe", "Rentabilite_temps_equipe", "True_Shooting_equipe_%"]
defensive_stats = ["Rentabilite_possessions_opp", "Rentabilite_temps_opp", "True_Shooting_opp_%"]

def calculate_matchup(team_lineups, opponent_lineups):
    results = []
    for _, lineup in team_lineups.iterrows():
        row = {"Lineup": lineup['Lineup']}
        for stat in offensive_stats + defensive_stats:
            if stat in offensive_stats:
                opp_stat = stat.replace("equipe", "opp")
                opponent_mean = opponent_lineups[opp_stat].mean()
                row[stat] = lineup[stat] - opponent_mean
            else:
                opp_stat = stat.replace("opp", "equipe")
                opponent_mean = opponent_lineups[opp_stat].mean()
                row[stat] = lineup[stat] - opponent_mean
        results.append(row)
    return pd.DataFrame(results)

def plot_heatmap(df, title):
    fig, ax = plt.subplots()
    df = df.set_index("Lineup").select_dtypes(include='number')
    sns.heatmap(df, annot=True, fmt=".1f", cmap="coolwarm", linewidths=0.5, ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

def radar_chart(team1_lineups, team2_lineups):
    categories = ["Pts per poss (offense)", "Pts per poss (defense)", "Poss per game (offense)",
                  "Poss per game (defense)", "TS% (offense)", "TS% (defense)"]

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
            line=dict(color=color_mapping[lineup])
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
            line=dict(color=color_mapping[lineup])
        ))

    # mise en page bg 
    fig.update_layout(
        title="Graphique Radar : Comparaison des Lineups 🏀",
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100]),
            angularaxis=dict(tickvals=[0, 1, 2, 3, 4, 5], ticktext=categories)  
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

# Titre page
st.title("Analyse de Rentabilité des Lineups 🏀📊")

# mise en page filtres coté 
st.sidebar.header("Filtres")
team_name = st.sidebar.selectbox("Équipe de référence", options=data["Equipe"].unique())
opponent_name = st.sidebar.selectbox("Équipe adverse", options=[team for team in data["Equipe"].unique() if team != team_name])

# set up des filtres d'équipes
team_data = data[data["Equipe"] == team_name]
opponent_data = data[data["Equipe"] == opponent_name]

st.subheader(f"Analyse des Lineups : {team_name} vs {opponent_name}")
matchup_df = calculate_matchup(team_data, opponent_data)
plot_heatmap(matchup_df, f"Heatmap pour {team_name} contre {opponent_name}")

# Set up choix de lineups pour radar chart, j'en ai fait deux bcs c'est plus smart 
st.subheader("Analyse des lineups via un graphique Radar")
team1_lineups = st.multiselect(f"Lineups de {team_name} :", options=team_data["Lineup"].unique())
team2_lineups = st.multiselect(f"Lineups de {opponent_name} :", options=opponent_data["Lineup"].unique())

radar_chart(team1_lineups, team2_lineups)
