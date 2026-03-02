import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Load dataset
movies = pd.read_csv("movies.csv")  # Movie metadata
ratings = pd.read_csv("ratings.csv")  # User ratings

# Merge datasets
movie_ratings = pd.merge(ratings, movies, on="movieId")

# Create pivot table (users as rows, movies as columns)
user_movie_matrix = movie_ratings.pivot_table(index="userId", columns="title", values="rating")

# Fill missing values with 0 (or use mean imputation)
user_movie_matrix = user_movie_matrix.fillna(0)

# Fit KNN model
model = NearestNeighbors(metric="cosine", algorithm="brute")
model.fit(user_movie_matrix.values)

# Function to recommend movies
def recommend_movies(movie_name, num_recommendations=5):
    if movie_name not in user_movie_matrix.columns:
        return f"Movie '{movie_name}' not found in database."
    
    # Get movie index
    movie_index = user_movie_matrix.columns.get_loc(movie_name)
    
    # Find similar movies
    distances, indices = model.kneighbors(user_movie_matrix.values[:, movie_index].reshape(1, -1), n_neighbors=num_recommendations + 1)
    
    # Get recommended movie titles
    recommended_movies = [user_movie_matrix.columns[i] for i in indices.flatten()][1:]
    
    return recommended_movies

# Example Usage
movie_input = "Toy Story (1995)"  # Change to any movie in dataset
recommendations = recommend_movies(movie_input)
print(f"Movies similar to '{movie_input}':\n", recommendations)
