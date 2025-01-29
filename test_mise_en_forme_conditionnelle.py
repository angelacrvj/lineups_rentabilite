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

# 📌 Fonction de style conditionnel avec `cellStyle`
def cell_style(params):
    """Applique un fond rouge si la valeur est ≥ 50, sinon bleu."""
    try:
        value = params["value"]
        if value is None:
            return {}
        elif value >= 50:
            return {"backgroundColor": "red", "color": "white"}
        else:
            return {"backgroundColor": "blue", "color": "white"}
    except Exception:
        return {}

# 📌 Configuration de la table AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# 📌 Appliquer la mise en forme conditionnelle sur les colonnes "Centile"
for col in df.columns:
    if col.startswith("Centile"):
        gb.configure_column(col, cellStyle=cell_style)

# 📌 Construire les options de la table
grid_options = gb.build()

# 📌 Affichage de la table avec AgGrid
st.subheader("📊 Tableau avec mise en forme conditionnelle")
AgGrid(df, gridOptions=grid_options, theme="alpine", enable_enterprise_modules=False)
