#Importing libraries
import streamlit as st
import pickle
import requests

#Function to add the movie poster
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                 '}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

#Function to find most related movies to the target movie and recommend them
def recommend(movie):
    movie_index = movies_list[movies_list['title_x'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        recommended_movies.append(movies_list.iloc[i[0]].title_x)
        #fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_list = pickle.load(open('movies.pkl','rb'))
movies_title = movies_list['title_x'].values

similarity = pickle.load(open('similarity.pkl','rb'))

st.set_page_config(
     page_title="Movie Recommendation App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
 )

st.title('Movie Recommendation System') #Displaying title of the project on the website

selected_movie_name = st.selectbox('Select the movie for recommendations',movies_title)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    st.success('Movie Recommendations Found!')

    #Creating 5 columns, one for each movie
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])   #Movie name
        st.image(posters[0])    #Movie poster

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
