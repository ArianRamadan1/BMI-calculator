import streamlit as st
from pymongo import MongoClient

# Merr MongoDB URI nga secrets.toml
MONGO_URI = st.secrets["MONGO_URI"]

# Lidhja me MongoDB
try:
    client = MongoClient(MONGO_URI)

    # Kontrollo lidhjen
    client.admin.command("ping")

    db = client["BMI_DB"]
    collection = db["users"]

except Exception as e:
    st.error(f"MongoDB Connection Error: {e}")
    st.stop()


# Titulli
st.title("🏋️ Body Mass Index Calculator")


# Inputet
name = st.text_input("Emri")
height_cm = st.text_input("Gjatesia (cm)")
weight = st.text_input("Pesha (kg)")


# Butoni per llogaritje
if st.button("Llogarit BMI"):

    try:
        # Konvertimi i inputeve
        height_cm = float(height_cm)
        weight = float(weight)

        # Kontroll i vlerave
        if height_cm <= 0 or weight <= 0:
            st.error("Gjatesia dhe pesha duhet te jene me te medha se 0.")
            st.stop()

        # Konvertimi cm ne metra
        height_m = height_cm / 100

        # Formula BMI
        bmi = weight / (height_m ** 2)


        # Kategoria e BMI
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"


        # Shfaq rezultatet
        st.success(f"BMI juaj eshte: {bmi:.2f}")
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

        st.success("Te dhenat u ruajten me sukses ne MongoDB!")


    except ValueError:
        st.error("Ju lutem vendosni vetem numra per gjatesine dhe peshen.")

        