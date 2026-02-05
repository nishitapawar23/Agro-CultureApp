import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import requests  # For optional weather API

# Database setup
def init_db():
    conn = sqlite3.connect('agri_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS crops (id INTEGER PRIMARY KEY, user_id INTEGER, crop_name TEXT, soil_type TEXT, season TEXT, weather REAL, past_yield REAL)''')
    conn.commit()
    conn.close()

init_db()

# Hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authenticate user
def authenticate(username, password):
    conn = sqlite3.connect('agri_app.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username=? AND password=?', (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

# Register user
def register_user(username, password):
    conn = sqlite3.connect('agri_app.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Get user crops
def get_crops(user_id):
    conn = sqlite3.connect('agri_app.db')
    c = conn.cursor()
    c.execute('SELECT id, crop_name, soil_type, season, weather, past_yield FROM crops WHERE user_id=?', (user_id,))
    crops = c.fetchall()
    conn.close()
    return crops

# Add crop
def add_crop(user_id, crop_name, soil_type, season, weather, past_yield):
    conn = sqlite3.connect('agri_app.db')
    c = conn.cursor()
    c.execute('INSERT INTO crops (user_id, crop_name, soil_type, season, weather, past_yield) VALUES (?, ?, ?, ?, ?, ?)', 
              (user_id, crop_name, soil_type, season, weather, past_yield))
    conn.commit()
    conn.close()

# Delete crop
def delete_crop(crop_id):
    conn = sqlite3.connect('agri_app.db')
    c = conn.cursor()
    c.execute('DELETE FROM crops WHERE id=?', (crop_id,))
    conn.commit()
    conn.close()

# AI Model Setup (Dummy training data - replace with real data if available)
np.random.seed(42)
data = {
    'soil_type': np.random.choice(['Clay', 'Sandy', 'Loamy'], 100),
    'season': np.random.choice(['Summer', 'Winter', 'Monsoon'], 100),
    'weather': np.random.uniform(20, 40, 100),  # Temp in Celsius
    'past_yield': np.random.uniform(50, 200, 100),  # Yield in tons
    'crop': np.random.choice(['Wheat', 'Rice', 'Corn', 'Soybean'], 100)
}
df = pd.DataFrame(data)

# Encode categoricals
le_soil = LabelEncoder()
le_season = LabelEncoder()
le_crop = LabelEncoder()
df['soil_type'] = le_soil.fit_transform(df['soil_type'])
df['season'] = le_season.fit_transform(df['season'])
df['crop'] = le_crop.fit_transform(df['crop'])

X = df[['soil_type', 'season', 'weather', 'past_yield']]
y = df['crop']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predict crops
def suggest_crops(soil_type, season, weather, past_yield):
    try:
        soil_enc = le_soil.transform([soil_type])[0]
        season_enc = le_season.transform([season])[0]
        input_data = [[soil_enc, season_enc, weather, past_yield]]
        pred = model.predict_proba(input_data)[0]
        top_indices = np.argsort(pred)[-3:][::-1]  # Top 3
        suggestions = [le_crop.inverse_transform([i])[0] for i in top_indices]
        probs = [pred[i] for i in top_indices]
        return list(zip(suggestions, probs))
    except Exception as e:
        st.error(f"AI Suggestion Error: {e}. Using defaults.")
        return [("Wheat", 0.5), ("Rice", 0.4), ("Corn", 0.3)]  # Fallback

# Optional: Fetch real weather (replace with your API key)
def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Get from openweathermap.org
    if api_key == "YOUR_OPENWEATHERMAP_API_KEY":
        return 25.0  # Default if no key
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        return response['main']['temp'] if 'main' in response else 25.0
    except:
        return 25.0

# Custom CSS for creative styling (Green agricultural theme)
st.markdown("""
<style>
body { background-color: #e8f5e8; font-family: 'Arial', sans-serif; }
.stButton>button { background-color: #4caf50; color: white; border-radius: 10px; }
.stTextInput, .stNumberInput, .stSelectbox { border-radius: 5px; }
.header { text-align: center; color: #2e7d32; font-size: 2em; margin-bottom: 20px; }
.subheader { color: #388e3c; font-size: 1.5em; }
</style>
""", unsafe_allow_html=True)

# Session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# App Logic
if st.session_state.page == 'login':
    st.markdown('<div class="header">🌾 Agro Cultural App 🌾</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Login or Register to Manage Your Crops</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_id = authenticate(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")

elif st.session_state.page == 'dashboard':
    st.markdown('<div class="header">🌱 Dashboard 🌱</div>', unsafe_allow_html=True)
    st.sidebar.button("Logout", on_click=lambda: (st.session_state.update({'user_id': None, 'page': 'login'}), st.rerun()))
    
    tab1, tab2, tab3 = st.tabs(["Manage Crops", "Add Crop", "AI Suggestions"])
    
    with tab1:
        st.markdown('<div class="subheader">Your Crops</div>', unsafe_allow_html=True)
        crops = get_crops(st.session_state.user_id)
        if crops:
            for crop in crops:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{crop[1]}** - Soil: {crop[2]}, Season: {crop[3]}, Weather: {crop[4]}°C, Past Yield: {crop[5]} tons")
                with col2:
                    if st.button(f"Delete {crop[1]}", key=crop[0]):
                        delete_crop(crop[0])
                        st.rerun()
        else:
            st.write("No crops added yet.")
    
    with tab2:
        st.markdown('<div class="subheader">Add a New Crop</div>', unsafe_allow_html=True)
        crop_name = st.text_input("Crop Name")
        soil_type = st.selectbox("Soil Type", ["Clay", "Sandy", "Loamy"])
        season = st.selectbox("Season", ["Summer", "Winter", "Monsoon"])
        weather = st.number_input("Weather (Temp in °C)", min_value=0.0, max_value=50.0)
        past_yield = st.number_input("Past Yield (tons)", min_value=0.0)
        if st.button("Add Crop"):
            add_crop(st.session_state.user_id, crop_name, soil_type, season, weather, past_yield)
            st.success("Crop added!")
            st.rerun()
    
    with tab3:
        st.markdown('<div class="subheader">AI-Powered Crop Suggestions</div>', unsafe_allow_html=True)
        soil_type = st.selectbox("Soil Type", ["Clay", "Sandy", "Loamy"], key="suggest_soil")
        season = st.selectbox("Season", ["Summer", "Winter", "Monsoon"], key="suggest_season")
        weather = st.number_input("Weather (Temp in °C)", min_value=0.0, max_value=50.0, key="suggest_weather")
        past_yield = st.number_input("Past Yield (tons)", min_value=0.0, key="suggest_yield")
        if st.button("Get Suggestions"):
            suggestions = suggest_crops(soil_type, season, weather, past_yield)
            st.write("**Top Suggested Crops:**")
            for crop, prob in suggestions:
                st.write(f"- {crop} (Confidence: {prob:.2f})")
