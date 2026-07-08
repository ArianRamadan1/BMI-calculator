import streamlit as st
from pymongo import MongoClient

# MongoDB Atlas Connection


try:
    client = MongoClient(MONGO_URI)
    client.admin.command("ping")

    db = client["BMI_DB"]
    collection = db["users"]

except Exception as e:
    st.error(f"MongoDB Connection Error: {e}")


st.title("Body Mass Index Calculator")

# Inputet
name = st.text_input("Emri")
height_cm = st.text_input("Gjatesia (cm)")
weight = st.text_input("Pesha (kg)")


if st.button("Llogarit BMI"):
    try:
        # Konvertimi i inputeve
        height_cm = float(height_cm)
        weight = float(weight)

        # Kontroll
        if height_cm <= 0 or weight <= 0:
            st.error("Gjatesia dhe pesha duhet te jene me te medha se 0.")
        else:
            # Cm ne meter
            height = height_cm / 100

            # Llogaritja BMI
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

            # Ruajtja ne MongoDB
            data = {
                "name": name,
                "height_cm": height_cm,
                "weight_kg": weight,
                "BMI": round(bmi, 2),
                "category": category
            }

            collection.insert_one(data)

            st.success("Te dhenat u ruajten ne MongoDB.")


    except ValueError:
        st.error("Ju lutem shkruani vlera numerike te sakta per gjatesine dhe peshen.")