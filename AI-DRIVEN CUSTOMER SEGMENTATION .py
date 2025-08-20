# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA

# # Load the dataset
# data = pd.read_csv('Mall_Customers.csv')  # Update the path to your local file location

# # Display the first few rows
# print(data.head())

# # Plot distributions
# plt.figure(figsize=(15, 5))

# plt.subplot(1, 3, 1)
# sns.histplot(data['Age'], kde=True)
# plt.title('Age Distribution')

# plt.subplot(1, 3, 2)
# sns.histplot(data['Annual Income (k$)'], kde=True)
# plt.title('Annual Income Distribution')

# plt.subplot(1, 3, 3)
# sns.histplot(data['Spending Score (1-100)'], kde=True)
# plt.title('Spending Score Distribution')

# plt.tight_layout()
# plt.show()

# # Data preprocessing
# data.rename(columns={'Genre': 'Gender'}, inplace=True)
# print(data.info())
# data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})

# # Feature selection and scaling
# features = data[['Annual Income (k$)', 'Spending Score (1-100)']]
# scaler = StandardScaler()
# features_scaled = scaler.fit_transform(features)

# # Elbow Method to identify the best number of clusters
# inertia = []
# K = range(1, 11)
# for k in K:
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(features_scaled)
#     inertia.append(kmeans.inertia_)

# # Plot the Elbow Curve
# plt.figure(figsize=(8, 5))
# plt.plot(K, inertia, 'bo-')
# plt.xlabel('Number of Clusters')
# plt.ylabel('Inertia')
# plt.title('Elbow Method for Optimal k')
# plt.show()

# # KMeans clustering
# kmeans = KMeans(n_clusters=5, random_state=42)
# data['Cluster'] = kmeans.fit_predict(features_scaled)

# # Scatter plot for clusters
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x=features_scaled[:, 0], y=features_scaled[:, 1], hue=data['Cluster'], palette='viridis')
# plt.xlabel('Annual Income (scaled)')
# plt.ylabel('Spending Score (scaled)')
# plt.title('Customer Segmentation')
# plt.legend(title='Cluster')
# plt.show()

# # Cluster summary
# cluster_summary = data.groupby('Cluster')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
# print("\nCluster Summary:")
# print(cluster_summary)

# # PCA for dimensionality reduction
# pca = PCA(n_components=2)
# pca_features = pca.fit_transform(features_scaled)

# # Apply KMeans on PCA components
# kmeans_pca = KMeans(n_clusters=5, random_state=42)
# data['Cluster_PCA'] = kmeans_pca.fit_predict(pca_features)

# # Plot clusters based on PCA
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x=pca_features[:, 0], y=pca_features[:, 1], hue=data['Cluster_PCA'], palette='viridis')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')
# plt.title('Customer Segmentation with PCA')
# plt.legend(title='Cluster')
# plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load the dataset
data = pd.read_csv('Mall_Customers.csv')  # Update the path to your local file location

# Display the first few rows
print(data.head())

# Figure 1: Plot distributions
plt.figure(1, figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.histplot(data['Age'], kde=True)
plt.title('Age Distribution')

plt.subplot(1, 3, 2)
sns.histplot(data['Annual Income (k$)'], kde=True)
plt.title('Annual Income Distribution')

plt.subplot(1, 3, 3)
sns.histplot(data['Spending Score (1-100)'], kde=True)
plt.title('Spending Score Distribution')

plt.tight_layout()
plt.show()

# Data preprocessing
data.rename(columns={'Genre': 'Gender'}, inplace=True)
print(data.info())
data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})

# Feature selection and scaling
features = data[['Annual Income (k$)', 'Spending Score (1-100)']]
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Elbow Method to identify the best number of clusters
inertia = []
K = range(1, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features_scaled)
    inertia.append(kmeans.inertia_)

# Figure 2: Plot the Elbow Curve
plt.figure(2, figsize=(8, 5))
plt.plot(K, inertia, 'bo-')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

# KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=42)
data['Cluster'] = kmeans.fit_predict(features_scaled)

# Figure 3: Scatter plot for clusters
plt.figure(3, figsize=(10, 6))
sns.scatterplot(x=features_scaled[:, 0], y=features_scaled[:, 1], hue=data['Cluster'], palette='viridis')
plt.xlabel('Annual Income (scaled)')
plt.ylabel('Spending Score (scaled)')
plt.title('Customer Segmentation')
plt.legend(title='Cluster')
plt.show()

# Cluster summary
cluster_summary = data.groupby('Cluster')[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].mean()
print("\nCluster Summary:")
print(cluster_summary)

# PCA for dimensionality reduction
pca = PCA(n_components=2)
pca_features = pca.fit_transform(features_scaled)

# Apply KMeans on PCA components
kmeans_pca = KMeans(n_clusters=5, random_state=42)
data['Cluster_PCA'] = kmeans_pca.fit_predict(pca_features)

# Figure 4: Plot clusters based on PCA
plt.figure(4, figsize=(10, 6))
sns.scatterplot(x=pca_features[:, 0], y=pca_features[:, 1], hue=data['Cluster_PCA'], palette='viridis')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.title('Customer Segmentation with PCA')
plt.legend(title='Cluster')
plt.show()