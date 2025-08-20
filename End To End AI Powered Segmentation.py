# recommendation_system.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Dense, Dropout, Concatenate
from flask import Flask, jsonify, request

def load_and_preprocess_data():
    """Load and preprocess the MovieLens dataset"""
    # Note: Update these paths to where you've stored the dataset locally
    ratings = pd.read_csv('data/u.data', sep='\t', 
                         names=['userId', 'movieId', 'rating', 'timestamp'], 
                         engine='python')
    movies = pd.read_csv('data/u.item', sep='|', 
                        names=['movieId', 'title'], 
                        usecols=[0, 1], 
                        encoding='latin-1')
    
    # Data preprocessing
    ratings = ratings.drop(columns=['timestamp'])
    
    # Encode user and movie IDs
    user_encoder = LabelEncoder()
    ratings['user'] = user_encoder.fit_transform(ratings['userId'])
    
    movie_encoder = LabelEncoder()
    ratings['movie'] = movie_encoder.fit_transform(ratings['movieId'])
    
    return ratings, movies, user_encoder, movie_encoder

def build_and_train_model(ratings):
    """Build and train the recommendation model"""
    # Prepare data
    n_users = ratings['user'].nunique()
    n_movies = ratings['movie'].nunique()
    ratings['rating'] = ratings['rating'].astype(np.float32)
    
    # Train-test split
    train, test = train_test_split(ratings, test_size=0.2, random_state=42)
    
    # Model architecture
    user_input = Input(shape=(1,))
    movie_input = Input(shape=(1,))
    
    # Embedding layers
    user_embedding = Embedding(n_users, 50)(user_input)
    movie_embedding = Embedding(n_movies, 50)(movie_input)
    
    # Flatten embeddings
    user_vec = Flatten()(user_embedding)
    movie_vec = Flatten()(movie_embedding)
    
    # Concatenate and add dense layers
    concat = Concatenate()([user_vec, movie_vec])
    dense = Dense(128, activation='relu')(concat)
    dropout = Dropout(0.3)(dense)
    dense = Dense(64, activation='relu')(dropout)
    output = Dense(1)(dense)
    
    # Compile the model
    model = Model(inputs=[user_input, movie_input], outputs=output)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    # Prepare training data
    train_user = train['user'].values
    train_movie = train['movie'].values
    train_rating = train['rating'].values
    
    test_user = test['user'].values
    test_movie = test['movie'].values
    test_rating = test['rating'].values
    
    # Train the model
    print("Training the recommendation model...")
    history = model.fit(
        [train_user, train_movie],
        train_rating,
        validation_data=([test_user, test_movie], test_rating),
        epochs=10,
        batch_size=64,
        verbose=1
    )
    
    return model, history

def create_flask_app(model, user_encoder, movie_encoder):
    """Create Flask API for recommendations"""
    app = Flask(__name__)
    
    @app.route('/recommend', methods=['POST'])
    def recommend():
        data = request.json
        try:
            user_id = user_encoder.transform([data['userId']])[0]
            movie_id = movie_encoder.transform([data['movieId']])[0]
            
            # Predict rating
            predicted_rating = model.predict([[user_id], [movie_id]])[0][0]
            return jsonify({
                'predicted_rating': float(predicted_rating),
                'status': 'success'
            })
        except Exception as e:
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 400
    
    return app

def main():
    # Step 1: Load and preprocess data
    ratings, movies, user_encoder, movie_encoder = load_and_preprocess_data()
    
    # Step 2: Build and train model
    model, history = build_and_train_model(ratings)
    
    # Save the model in modern Keras format
    model.save('models/recommendation_model.keras')
    print("Model saved successfully.")
    
    # Step 3: Create and run Flask app
    app = create_flask_app(model, user_encoder, movie_encoder)
    
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()