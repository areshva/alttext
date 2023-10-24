import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
data = pd.read_csv('binary_vectors_output.csv')

# store the sum of squared distances (WCSS)
wcss = []

# different values of k+compute WCSS for each
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(data)
    wcss.append(kmeans.inertia_)

# Plot the elbow method graph
# plt.plot(range(1, 11), wcss)
# plt.title('Elbow Method')
# plt.xlabel('Number of Clusters')
# plt.ylabel('WCSS')
# plt.show()

#elbow at 4/5

kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
cluster_labels = kmeans.fit_predict(data)
print(cluster_labels)
data = np.array(data)  
cluster_labels = np.array(cluster_labels)
centroids = kmeans.cluster_centers_


colors = ['red', 'green', 'blue', 'purple']

plt.figure(figsize=(10, 6))
for i in range(len(colors)):
    plt.scatter(data[cluster_labels == i, 0], data[cluster_labels == i, 1], s=50, c=colors[i], label=f'Cluster {i+1}')

# Plot cluster centroids
plt.scatter(centroids[:, 0], centroids[:, 1], s=100, c='black', label='Centroids', marker='X')

plt.title('K-Means Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

#LLM- bert.
#bert returns a vector for the text (not anything of meaning but captures the semantic menaing)
#tune prompts to gpt to hopefully find the best set of questins to create the vectors in a useful way


#finetune for classification
#get a rating (regression problem)
#need some alt text description + score
#dimensions that account for negative traits (poetry?)
#find a point in space where you can say 'these texts are good'
#binary for encoding?


#powerpoint alt text
#azure ai visual studio
#old chandra/webb
#+ add dimension for simile? 

#img + text pair
#source, category, who got it?
