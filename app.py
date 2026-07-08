import streamlit as st
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["BMI_DB"]
collection = db["users"]

st.title("🏋️ Body Mass Index Calculator")

# Inputet
name = st.text_input("Emri")
height_cm = st.text_input("Gjatesia (cm)")
weight = st.text_input("Pesha (kg)")

if st.button("Llogarit BMI"):
    try:
        # Konvertimi në numra
        height_cm = float(height_cm)
        weight = float(weight)

        # Konverto cm -> m
        height = height_cm / 100

        # Llogaritja e BMI
        bmi = weight / (height ** 2)

        # Kategoria
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        # Shfaq rezultatin
        st.success(f"BMI: {bmi:.2f}")
        st.info(f"Kategoria: {category}")

        # Ruaj në MongoDB
        data = {
            "name": name,
            "height_cm": height_cm,
            "weight": weight,
            "BMI": round(bmi, 2),
            "category": category
        }

        collection.insert_one(data)

        st.success("Te dhenat u ruajten ne MongoDB.")

    except ValueError:
        st.error("Ju lutem shkruani vlera numerike te sakta per gjatesine dhe peshen.")