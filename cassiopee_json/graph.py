import matplotlib.pyplot as plt

# Créer une liste de rectangles avec des noms
rectangles = [((1, 1), (1, 4), (4, 4), (4, 1), "Rectangle 1"), 
              ((2, 2), (2, 6), (6, 6), (6, 2), "Rectangle 2")]

# Créer la figure et les axes
fig, ax = plt.subplots()

# Tracer les rectangles
for rect in rectangles:
    ax.add_patch(plt.Polygon(rect[:4], fill=None, edgecolor="black", linewidth=2))
    ax.text(rect[0][0], rect[0][1], rect[4], ha="center", va="center")

# Ajouter une légende
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc="center left", bbox_to_anchor=(1.05, 0.5))

# Ajuster la taille de la figure
fig.subplots_adjust(left=0.1, right=0.8)

# Afficher le graphique
plt.show()

