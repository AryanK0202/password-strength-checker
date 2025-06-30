import streamlit as st
import joblib
import pandas as pd
from checker import calculate_score, suggestions, extract_features

model = joblib.load("password_model.pkl")

st.set_page_config(page_title="Password Strength Checker", page_icon="🔐")
st.title("🔐 Hybrid Password Strength Checker")

password = st.text_input("Enter your password: ", type="password")

if password:
    math_score = calculate_score(password)

    features = pd.DataFrame([extract_features(password)])
    ml_label = int(model.predict(features)[0])
    ml_score = (ml_label + 1) * (5 / 3) 

    final_score = round((0.6 * math_score + 0.4 * ml_score), 1)

    st.subheader("Results")
    st.metric("Final Strength Score", f"{final_score} / 5")
    st.text(f"Math Model Score: {math_score} / 5")
    st.text(f"ML model Rating: {ml_label} (0=Weak, 1=Medium, 2=Strong)")

    suggestion_list =suggestions(password, math_score)
    if suggestion_list:
        st.warning("Suggestions to improve password: ")
        for s in suggestion_list:
            st.markdown(f" - {s}")
        else:
            st.success("Your password is strong")
