import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

# 📌 Titre de l'application
st.title("✅ Tableau avec mise en forme conditionnelle sur AgGrid")

# 📌 Générer un DataFrame d'exemple
data = {
    "Nom": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "Centile_A": [10, 50, 90, 30, 70],
    "Centile_B": [20, 70, 30, 90, 50],
    "Score": [3, 5, 8, 2, 7],
}
df = pd.DataFrame(data)

# 📌 Configuration de la table AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# 📌 Définition des règles de mise en forme conditionnelle
for col in df.columns:
    if col.startswith("Centile"):
        gb.configure_column(
            col,
            cellClassRules={
                "cell-red": "params.value >= 50",
                "cell-blue": "params.value < 50",
            }
        )

# 📌 Construire les options de la table
grid_options = gb.build()

# 📌 Ajouter du CSS pour forcer la mise en forme
custom_css = """
<style>
    .ag-theme-streamlit .cell-red {
        background-color: red !important;
        color: white !important;
        font-weight: bold !important;
    }
    .ag-theme-streamlit .cell-blue {
        background-color: blue !important;
        color: white !important;
        font-weight: bold !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 📌 Affichage de la table avec AgGrid
st.subheader("📊 Tableau avec mise en forme conditionnelle")
AgGrid(df, gridOptions=grid_options, theme="streamlit", enable_enterprise_modules=False)
