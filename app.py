import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np

# Database Setup
engine = create_engine('sqlite:///agro_cultural.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

class Crop(Base):
    __tablename__ = 'crops'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    soil_type = Column(String, nullable=False)
    season = Column(String, nullable=False)
    weather = Column(String, nullable=False)
    past_yield = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User')

Base.metadata.create_all(engine)

# AI Model Setup (Simple Random Forest for Crop Suggestion)
# Dummy data for training (expand with real data)
data = {
    'soil_type': ['clay', 'sandy', 'loam', 'clay', 'sandy'],
    'season': ['summer', 'winter', 'monsoon', 'summer', 'winter'],
    'weather': ['dry', 'rainy', 'humid', 'dry', 'rainy'],
    'past_yield': [50, 30, 70, 60, 40],
    'crop': ['wheat', 'rice', 'corn', 'wheat', 'rice']
}
df = pd.DataFrame(data)
df['soil_type'] = df['soil_type'].map({'clay': 0, 'sandy': 1, 'loam': 2})
df['season'] = df['season'].map({'summer': 0, 'winter': 1, 'monsoon': 2})
df['weather'] = df['weather'].map({'dry': 0, 'rainy': 1, 'humid': 2})
X = df[['soil_type', 'season', 'weather', 'past_yield']]
y = df['crop']
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X, y)

# Streamlit App
st.set_page_config(page_title="Agro Cultural App", page_icon="🌾", layout="wide")

# Custom CSS for Creative Styling
st.markdown("""
    <style>
    .main { background-color: #f0f8e7; color: #2e7d32; }
    .sidebar .sidebar-content { background-color: #e8f5e8; }
    .stButton>button { background-color: #4caf50; color: white; border-radius: 10px; }
    .stTextInput, .stSelectbox, .stNumberInput { border-radius: 5px; }
    h1, h2 { color: #1b5e20; text-align: center; }
    .card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 10px; }
    </style>
""", unsafe_allow_html=True)

# Session State for User Management
if 'user' not in st.session_state:
    st.session_state.user = None

# Helper Functions
def hash_password(password):
    return generate_password_hash(password)

def check_password(hashed, password):
    return check_password_hash(hashed, password)

def login_user(username, password):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and check_password(user.password_hash, password):
        st.session_state.user = user
        return True
    return False

def register_user(username, password):
    session = Session()
    if session.query(User).filter_by(username=username).first():
        session.close()
        return False  # Username exists
    new_user = User(username=username, password_hash=hash_password(password))
    session.add(new_user)
    session.commit()
    session.close()
    return True

def add_crop(name, soil_type, season, weather, past_yield, user_id):
    session = Session()
    new_crop = Crop(name=name, soil_type=soil_type, season=season, weather=weather, past_yield=past_yield, user_id=user_id)
    session.add(new_crop)
    session.commit()
    session.close()

def delete_crop(crop_id, user_id):
    session = Session()
    crop = session.query(Crop).filter_by(id=crop_id, user_id=user_id).first()
    if crop:
        session.delete(crop)
        session.commit()
    session.close()

def get_user_crops(user_id):
    session = Session()
    crops = session.query(Crop).filter_by(user_id=user_id).all()
    session.close()
    return crops

def suggest_crop(soil_type, season, weather, past_yield):
    soil_map = {'clay': 0, 'sandy': 1, 'loam': 2}
    season_map = {'summer': 0, 'winter': 1, 'monsoon': 2}
    weather_map = {'dry': 0, 'rainy': 1, 'humid': 2}
    input_data = [[soil_map[soil_type], season_map[season], weather_map[weather], past_yield]]
    prediction = model.predict(input_data)[0]
    return prediction

# Sidebar Navigation
st.sidebar.title("🌾 Agro Cultural App")
if st.session_state.user:
    st.sidebar.write(f"Logged in as: {st.session_state.user.username}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
    page = st.sidebar.radio("Navigate", ["Dashboard", "Add Crop", "Delete Crop", "Crop Suggestions"])
else:
    page = st.sidebar.radio("Navigate", ["Login", "Register"])

# Pages
if page == "Login":
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

elif page == "Register":
    st.title("📝 Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Registered successfully! Please login.")
        else:
            st.error("Username already exists.")

elif page == "Dashboard":
    if not st.session_state.user:
        st.error("Please login first.")
    else:
        st.title("🏠 Dashboard")
        crops = get_user_crops(st.session_state.user.id)
        if crops:
            st.subheader("Your Crops")
            for crop in crops:
                st.markdown(f"""
                <div class="card">
                <h3>{crop.name}</h3>
                <p>Soil: {crop.soil_type} | Season: {crop.season} | Weather: {crop.weather} | Past Yield: {crop.past_yield}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No crops added yet.")

elif page == "Add Crop":
    if not st.session_state.user:
        st.error("Please login first.")
    else:
        st.title("➕ Add Crop")
        name = st.text_input("Crop Name")
        soil_type = st.selectbox("Soil Type", ["clay", "sandy", "loam"])
        season = st.selectbox("Season", ["summer", "winter", "monsoon"])
        weather = st.selectbox("Weather", ["dry", "rainy", "humid"])
        past_yield = st.number_input("Past Yield (tons)", min_value=0.0)
        if st.button("Add Crop"):
            add_crop(name, soil_type, season, weather, past_yield, st.session_state.user.id)
            st.success("Crop added!")

elif page == "Delete Crop":
    if not st.session_state.user:
        st.error("Please login first.")
    else:
        st.title("🗑️ Delete Crop")
        crops = get_user_crops(st.session_state.user.id)
        if crops:
            crop_options = {crop.id: f"{crop.name} (ID: {crop.id})" for crop in crops}
            selected_crop = st.selectbox("Select Crop to Delete", list(crop_options.values()))
            crop_id = [k for k, v in crop_options.items() if v == selected_crop][0]
            if st.button("Delete"):
                delete_crop(crop_id, st.session_state.user.id)
                st.success("Crop deleted!")
                st.rerun()
        else:
            st.info("No crops to delete.")

elif page == "Crop Suggestions":
    if not st.session_state.user:
        st.error("Please login first.")
    else:
        st.title("🤖 AI-Powered Crop Suggestions")
        soil_type = st.selectbox("Soil Type", ["clay", "sandy", "loam"])
        season = st.selectbox("Season", ["summer", "winter", "monsoon"])
        weather = st.selectbox("Weather", ["dry", "rainy", "humid"])
        past_yield = st.number_input("Past Yield (tons)", min_value=0.0)
        if st.button("Get Suggestion"):
            suggestion = suggest_crop(soil_type, season, weather, past_yield)
            st.success(f"Suggested Crop: {suggestion}")
            st.info("This is based on a simple AI model. For accuracy, use real data.")
