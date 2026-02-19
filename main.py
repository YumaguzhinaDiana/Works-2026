import time
import json
import logging
import requests
import pandas as pd
import streamlit as st
import re
import numpy as np


tones_dict = {0:"Обычный",1:"Токсичный"}


@st.cache_data(ttl=60)
def get_all_comments():
    response = requests.get(
                "http://localhost:8000/get_all_comments",
                json={}, timeout=150
            )
    if response.status_code == 200:
        comments = response.json()
        return  comments
    else:
        st.write("Ошибка загрузки данных")


def get_predict(input):
    data = {"comment": input}
    response = requests.post(
        "http://localhost:8000/predict_tonality_comment",
        json=data, timeout=100
    )
    if response.status_code == 200:
        preds = response.json()
        return  preds
    else:
        st.write("Ошибка загрузки данных")


def save_comment(comment, tone):
    data = {"comment": comment, "tone":tone}
    response = requests.post(
        "http://localhost:8000/save_comment",
        json=data, timeout=100
    )
    if response.status_code == 200:
        preds = response.json()
        return preds
    else:
        st.write("Ошибка загрузки данных")


st.title("💬 Анализатор тональности комментариев")


col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Введите комментарий")

    user_input = st.text_area(
        "Текст комментария:",
        height=150,
        placeholder="Напишите ваш комментарий здесь..."
    )

    if st.button("🔍 Предсказать тональность", type="primary"):
        if user_input:
            prediction = get_predict(user_input)

            save_comment(user_input, prediction['tone'])

            st.success(f" Комментарий сохранен!")

            st.info(f"Тональность: **{tones_dict.get(prediction['tone'])} - {prediction['probs']}**")

            st.cache_data.clear()
        else:
            st.warning("Введите текст комментария")

with col2:
    st.subheader("📋 Все комментарии из БД")

    with st.spinner("Загрузка комментариев..."):
        comments_df = get_all_comments()
    print(comments_df)
    if not len(comments_df) == 0:
        for row in comments_df:
            with st.container():
                col_text, col_sent = st.columns([2, 1])
                with col_text:
                    st.write(row[0])
                    st.write(row[1])
                with col_sent:
                    sentiment = row[2]
                    st.markdown(f"{tones_dict.get( sentiment)}")
                st.divider()
    else:
        st.info("📭 В базе данных пока нет комментариев")

