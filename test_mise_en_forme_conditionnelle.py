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
    norm = mcolors.Normalize(vmin=0, vmax=100)  # Normaliser l'échelle entre 0 et 100
    cmap = plt.get_cmap("coolwarm")  # Dégradé coolwarm
    color = mcolors.rgb2hex(cmap(norm(value)))  # Convertir en code hexadécimal
    return color

# 📌 Fonction de style conditionnel appliqué aux colonnes "Centile"
def cell_style(params):
    if "Centile" in params["colDef"]["field"]:  # Vérifier si la colonne commence par "Centile"
        color = get_color(params["value"])  # Obtenir la couleur associée à la valeur
        return {"backgroundColor": color, "color": "black"}  # Appliquer la couleur
    return None

# 📌 Configuration de la table AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Appliquer la mise en forme conditionnelle aux colonnes "Centile"
gb.configure_columns(
    [col for col in df.columns if col.startswith("Centile")],  # Colonnes ciblées
    cellStyle=cell_style,  # Fonction de style
)

# 📌 Construire les options de la table
grid_options = gb.build()

# 📌 Affichage de la table avec AgGrid
st.subheader("📊 Tableau avec mise en forme conditionnelle")
AgGrid(df, gridOptions=grid_options)

# 📌 Explication de la mise en forme
st.markdown("""
🔹 **Explication :**  
- Les cellules des colonnes "Centile" ont une couleur de fond selon leur valeur.  
- **Bleu** = Valeurs faibles (~0)  
- **Blanc** = Valeurs moyennes (~50)  
- **Rouge** = Valeurs élevées (~100)  
- Les autres colonnes restent neutres.
""")

# 📌 Ajout d'une légende avec une barre de couleur
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
