import pandas as pd
import streamlit as st
from datetime import datetime
from st_aggrid import AgGrid
from actors.service import ActorService
from genres.service import GenreService
from movies.service import MovieService


def show_movies():
    movie_service = MovieService()
    movies = movie_service.get_movies()

    if movies:
        st.write("Lista de Filmes")
        movies_df = pd.json_normalize(movies)
        movies_df = movies_df.drop(columns=["actors", "genre.id"])

        AgGrid(
            data=(movies_df),
            reload_data=True,
            key="movies_grid",
        )
    else:
        st.warning("Nenhum filme encontrado.")

    st.title("Cadastrar novo filme",)
    title = st.text_input("Título do filme", placeholder='Título')
    release_date = st.date_input(
        "Data de lançamento",
        format="DD/MM/YYYY",
        value=None,
        min_value=datetime(1800, 1, 1),
        max_value=datetime.today(),
    )
    genre_service = GenreService()
    genres = genre_service.get_genres()
    genres_name = {genre["name"]: genre["id"] for genre in genres}
    selected_genre_name = st.selectbox(
        "Genero",
        list(genres_name.keys()),
        placeholder="Escolher gênero",
        index=None
    )

    actor_service = ActorService()
    actors = actor_service.get_actors()
    actors_name = {actor["name"]: actor["id"] for actor in actors}
    selected_actors_names = st.multiselect(
        "Atores", list(actors_name.keys()), placeholder="Escolher atores"
    )
    selected_actors_ids = [actors_name[name] for name in selected_actors_names]

    resume = st.text_area(
        "Resumo", placeholder="Escreva um breve resumo sobre o filme"
    )

    if st.button("Cadastrar"):
        new_movie = movie_service.create_movie(
            title=title,
            release_date=release_date,
            genre=genres_name[selected_genre_name],
            actors=selected_actors_ids,
            resume=resume,
        )
        if new_movie:
            st.rerun()
        else:
            st.error("Ocorreu um erro")
