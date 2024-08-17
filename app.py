import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDb API
def fetch_movie_poster(movie_id):
    api_key = "283f3adfc9246ea265b18b24d60d99f3"  # Replace with your actual TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    response = requests.get(url)
    data = response.json()
    
    # Check if the poster_path exists in the response
    if 'poster_path' in data:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return None  # Return None if no poster is found

# Load movie data and similarity matrix
movies_list = pickle.load(open('data/movies.pkl', 'rb'))
movies_df = pd.DataFrame(movies_list)  # Ensure this DataFrame contains 'title' and 'movie_id'
similarity = pickle.load(open('data/similarity.pkl', 'rb'))

def recommend(movie):
    # Find the index of the movie that matches the title
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    
    # Get the similarity scores for the selected movie
    distances = similarity[movie_index]
    
    # Get the indices of the 5 most similar movies
    movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    # Create a list of recommended movie titles and their posters
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies:
        movie_id = movies_df.iloc[i[0]]['movie_id']  # Access movie_id correctly
        recommended_movies.append(movies_df.iloc[i[0]]['title'])  # Append the title of the recommended movie
        
        # Fetch poster from API        
        recommended_movies_posters.append(fetch_movie_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

# Streamlit UI
st.title('Movie Recommendation System')

# Create a selectbox for movie selection
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies_df['title'].values  # Pass the movie titles as options
)

# Button to get recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    
    # Create columns for displaying the recommended movies and their posters
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])