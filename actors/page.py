import pandas as pd
import streamlit as st
from datetime import datetime
from st_aggrid import AgGrid
from actors.service import ActorService


def show_actors():
    actor_service = ActorService()
    actors = actor_service.get_actors()

    if actors:
        st.write("Lista de Atores/Atrizes")
        actors_df = pd.json_normalize(actors)
        AgGrid(
            data=actors_df,
            reload_data=True,
            key="actors_grid",
        )
    else:
        st.warning("Nenhum ator/atriz encontrado.")

    st.title("Cadastrar novo ator")
    name = st.text_input("Nome do ator", placeholder='Insira o nome do ator')
    birthday = st.date_input(
        "Data de nascimento",
        format="DD/MM/YYYY",
        value=None,
        min_value=datetime(1800, 1, 1),
        max_value=datetime.today(),
    )
    nationality = st.selectbox(
        "Nacionalidade",
        ("BRAZIL", "USA"),
        index=None,
        placeholder="Escolha um país",
    )

    if st.button("Cadastrar"):
        new_actor = actor_service.create_actor(
            name=name,
            birthday=birthday,
            nationality=nationality,
        )
        if new_actor:
            st.rerun()
        else:
            st.error("Ocorreu um erro")
