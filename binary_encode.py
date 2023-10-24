import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

csv_file = 'alt_data.csv'

df = pd.read_csv(csv_file)
categories = {
    "Colors and Descriptions": {"blue", "light", "bright", "white", "black", "red", "orange", "yellow", "pink", "green", "color", "colorful", "shades"},
    "Spatial Directions and Positions": {"left", "right", "top", "bottom", "center", "below", "above", "up", "down", "side"},
    "Astronomical Terms": {"galaxies", "galaxy", "star", "stars", "telescope", "planet", "nebula", "rings", "dust", "gas", "core", "disk", "cluster", "sphere", "arms", "area", "field", "outer", "distant", "region", "central", "material", "thin"},
    "Visualization Elements": {"image", "graphic", "illustration", "infographic", "arrows", "key", "dots", "mirror", "lines", "shapes", "panel", "sizes", "oval", "wispy"},
    "Telescope and Instrument Names": {"webb", "nircam", "microns", "nirspec", "miri"},
    "Text and Labels": {"labeled", "titled", "showing", "shows", "points", "appear", "throughout", "representing"},
    "Measurement and Data": {"scale", "wavelength", "diffraction", "spectrum", "brightness"},
    "Direction and Movement": {"there", "out", "around", "toward", "horizontal", "vertical", "across", "between", "create", "sizes"},
    "Quantitative Terms": {"three", "more", "few", "many", "most", "some", "about", "time", "while"},
    "Other Terms": {"arrows", "key", "clock", "indicate", "field", "cloud", "clouds", "also", "hubble", "exoplanet", "used", "miri", "oval"}
}

# I empty list to store vectors
binary_vectors = []

for text in df['Alt Text']:
    #empty binary vector for the current text
    binary_vector = []

    
    for category, terms in categories.items():
       
        if any(term in text for term in terms):
            binary_vector.append(1) 
        else:
            binary_vector.append(0)  
    
    binary_vectors.append(binary_vector)

binary_vectors_array = np.array(binary_vectors)

binary_vectors_df = pd.DataFrame(binary_vectors_array, columns=categories.keys())

output_csv_file = 'binary_vectors_output.csv'

binary_vectors_df.to_csv(output_csv_file, index=False)

print(binary_vectors_array[1])
print(binary_vectors_array.shape)

n_components = 2  
pca = PCA(n_components=n_components)
reduced_vectors = pca.fit_transform(binary_vectors_array)
print(reduced_vectors.shape)


plt.figure(figsize=(8, 6))
plt.scatter(reduced_vectors[:, 0], reduced_vectors[:, 1], marker='o', s=50)
plt.title('PCA Visualization')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)

# Show the plot
plt.show()
