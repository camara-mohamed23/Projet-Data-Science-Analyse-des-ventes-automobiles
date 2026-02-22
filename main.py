# ===============================
# Analyse des ventes automobiles
# Interface Tkinter Scrollable
# ===============================

import matplotlib
matplotlib.use("TkAgg")  # IMPORTANT pour Tkinter

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ===============================
# Configuration graphique
# ===============================
sns.set(style='whitegrid', palette='muted', font_scale=0.9)

# ===============================
# Chargement des données
# ===============================
df = pd.read_csv('voiture.csv')

numerical_cols = [
    'price_usd','marketing_spend_usd','dealership_count',
    'fuel_price_usd','gdp_growth_percent','interest_rate_percent',
    'competition_index','units_sold'
]

# ===============================
# Création de la figure Matplotlib
# ===============================
fig, axes = plt.subplots(5, 2, figsize=(14, 28))
fig.tight_layout(pad=5)

# 1️⃣ Ventes par pays
df.groupby('country')['units_sold'].sum().sort_values(ascending=False).plot(
    kind='bar', ax=axes[0,0]
)
axes[0,0].set_title('Ventes totales par pays')

# 2️⃣ Ventes par segment
df.groupby('segment')['units_sold'].sum().plot(
    kind='pie', autopct='%1.1f%%', ax=axes[0,1], ylabel=''
)
axes[0,1].set_title('Répartition des ventes par segment')

# 3️⃣ Ventes par année
df.groupby('year')['units_sold'].sum().plot(
    kind='line', marker='o', ax=axes[1,0]
)
axes[1,0].set_title('Ventes totales par année')

# 4️⃣ Prix moyen par année
df.groupby('year')['price_usd'].mean().plot(
    kind='line', marker='x', ax=axes[1,1]
)
axes[1,1].set_title('Prix moyen par année')

# 5️⃣ Corrélation
sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', ax=axes[2,0])
axes[2,0].set_title('Corrélations')
axes[2,1].axis('off')

# 6️⃣ Marketing vs ventes
sns.scatterplot(
    x='marketing_spend_usd',
    y='units_sold',
    data=df,
    ax=axes[3,0]
)
axes[3,0].set_title('Marketing vs Ventes')

# 7️⃣ Ventes par moteur
df.groupby('engine_type')['units_sold'].sum().plot(
    kind='bar', ax=axes[3,1]
)
axes[3,1].set_title('Ventes par type de moteur')

# 8️⃣ Segment vs pays
sns.barplot(
    x='segment',
    y='units_sold',
    hue='country',
    data=df,
    ax=axes[4,0]
)
axes[4,0].set_title('Ventes par segment et pays')
axes[4,1].axis('off')

# ===============================
# Tkinter Scrollable Window
# ===============================

root = tk.Tk()
root.title("Analyse des ventes automobiles")
root.geometry("1000x700")

# Canvas principal
main_canvas = tk.Canvas(root)
main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar verticale
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=main_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

main_canvas.configure(yscrollcommand=scrollbar.set)
main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

# Frame interne
frame = tk.Frame(main_canvas)
main_canvas.create_window((0, 0), window=frame, anchor="nw")

# Ajouter la figure matplotlib dans le frame
canvas_fig = FigureCanvasTkAgg(fig, master=frame)
canvas_fig.draw()
canvas_fig.get_tk_widget().pack()

# Scroll avec la molette souris
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root.bind_all("<MouseWheel>", _on_mousewheel)

root.mainloop()