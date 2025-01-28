import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Exemple de DataFrame avec des colonnes "Centile"
data = {
    "Nom": ["Alice", "Bob", "Charlie"],
    "Centile_A": [10, 50, 90],
    "Centile_B": [20, 70, 30],
    "Autre_Colonne": [1, 2, 3],
}
df = pd.DataFrame(data)

# Générer une fonction pour obtenir une couleur CSS en fonction de la valeur
def get_color_class(value):
    if value <= 20:
        return "low"
    elif value <= 40:
        return "mid-low"
    elif value <= 60:
        return "mid"
    elif value <= 80:
        return "mid-high"
    else:
        return "high"

# Appliquer des classes CSS aux colonnes "Centile"
for col in df.columns:
    if col.startswith("Centile"):
        df[f"{col}_class"] = df[col].apply(get_color_class)

# Configurer AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Ajouter les règles CSS aux colonnes "Centile"
for col in df.columns:
    if col.startswith("Centile"):
        gb.configure_column(
            col,
            cellClassRules={
                "low": f"params.data.{col}_class === 'low'",
                "mid-low": f"params.data.{col}_class === 'mid-low'",
                "mid": f"params.data.{col}_class === 'mid'",
                "mid-high": f"params.data.{col}_class === 'mid-high'",
                "high": f"params.data.{col}_class === 'high'",
            },
        )

# Construire les options de la grille
grid_options = gb.build()

# Supprimer les colonnes "_class" de l'affichage
df = df[[col for col in df.columns if not col.endswith("_class")]]

# Ajouter le CSS pour les styles
custom_css = """
<style>
    .ag-theme-streamlit .low {
        background-color: #3b4cc0 !important; /* Coolwarm (bleu pour valeurs faibles) */
        color: white !important;
    }
    .ag-theme-streamlit .mid-low {
        background-color: #7ba6dd !important;
        color: black !important;
    }
    .ag-theme-streamlit .mid {
        background-color: #f0f0f0 !important; /* Neutre */
        color: black !important;
    }
    .ag-theme-streamlit .mid-high {
        background-color: #f4978e !important;
        color: black !important;
    }
    .ag-theme-streamlit .high {
        background-color: #a50026 !important; /* Coolwarm (rouge pour valeurs élevées) */
        color: white !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Afficher la table dans Streamlit
AgGrid(df, gridOptions=grid_options)
