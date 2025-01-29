import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

# 📌 Fonction pour récupérer une couleur du dégradé "coolwarm"
def get_color(value):
    """Renvoie un code hexadécimal pour une valeur entre 0 et 100 en utilisant le cmap coolwarm."""
    norm = mcolors.Normalize(vmin=0, vmax=100)  # Normalisation des valeurs
    cmap = plt.get_cmap("coolwarm")  # Dégradé coolwarm
    color = mcolors.rgb2hex(cmap(norm(value)))  # Convertir en code hexadécimal
    return color

# 📌 Fonction de style conditionnel pour les colonnes "Centile"
def cell_style(params):
    """Applique une couleur en fonction de la valeur dans les colonnes Centile."""
    if "Centile" in params["colDef"]["field"]:  # Vérifier si la colonne commence par "Centile"
        color = get_color(params["value"])
        return {"backgroundColor": color, "color": "black"}  # Appliquer la couleur
    return None  # Pas de modification sur les autres colonnes

# 📌 Configuration de la table AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Appliquer la mise en forme conditionnelle aux colonnes "Centile"
for col in df.columns:
    if col.startswith("Centile"):  
        gb.configure_column(col, cellStyle=cell_style)  # Application du style

# 📌 Construire les options de la table
grid_options = gb.build()

# 📌 Affichage de la table avec AgGrid
st.subheader("📊 Tableau avec mise en forme conditionnelle")
AgGrid(df, gridOptions=grid_options, theme="streamlit")

# 📌 Légende du dégradé coolwarm
st.subheader("🎨 Légende du dégradé coolwarm")
gradient = plt.figure(figsize=(6, 1))
ax = gradient.add_axes([0, 0, 1, 0.3])

# Création d'un dégradé horizontal
cmap = plt.get_cmap("coolwarm")
norm = mcolors.Normalize(vmin=0, vmax=100)
cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='horizontal')
cb.set_label("Valeurs des centiles (0 à 100)")

# Afficher la légende sous forme d'image
st.pyplot(gradient)
