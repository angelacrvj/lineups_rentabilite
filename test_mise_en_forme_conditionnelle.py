import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

# 📌 Titre de l'application
st.title("Test de mise en forme conditionnelle avec AgGrid 🎨")

# 📌 Générer un DataFrame d'exemple
data = {
    "Nom": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "Centile_A": [10, 50, 90, 30, 70],
    "Centile_B": [20, 70, 30, 90, 50],
    "Score": [3, 5, 8, 2, 7],  # Une colonne normale pour comparaison
}
df = pd.DataFrame(data)

# 📌 Configuration de la table AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# 📌 Appliquer la mise en forme conditionnelle avec cellClassRules
for col in df.columns:
    if col.startswith("Centile"):  
        gb.configure_column(
            col, 
            cellClassRules={
                "red-cell": "params.value >= 50",
                "blue-cell": "params.value < 50"
            }
        )

# 📌 Construire les options de la table
grid_options = gb.build()

# 📌 Ajout de styles CSS personnalisés pour les couleurs
custom_css = """
<style>
    .ag-theme-streamlit .red-cell {
        background-color: red !important;
        color: white !important;
    }
    .ag-theme-streamlit .blue-cell {
        background-color: blue !important;
        color: white !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 📌 Affichage de la table avec AgGrid
st.subheader("📊 Tableau avec mise en forme conditionnelle simple")
AgGrid(df, gridOptions=grid_options, theme="streamlit")
