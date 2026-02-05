# Agro Culture App

## About
Agro Culture App is a web-based application developed to provide agriculture-related information and basic digital support for farmers. The project focuses on creating a simple, user-friendly interface to explore agricultural content and services.

## Features
- Informational pages related to agriculture and farming
- Simple and clean user interface
- Responsive design for different screen sizes
- Easy navigation for users

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Tools: VS Code, Git

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/nishitapawar23/Agro-CultureApp.git


📁 Project Structure
backend/
│-- index.js
│-- routes/
│   ├── cropRoute.js
│   ├── soilRoute.js
│   ├── weatherRoute.js
│   ├── priceRoute.js
│-- controllers/
│-- models/
│-- config/
│-- package.json

⚙️ Installation & Setup
1. Clone the repository
git clone <your-repo-link>
cd backend

2. Install dependencies
npm install

3. Start the server
node index.js


Server runs at:

http://localhost:5000

📡 API Endpoints
1️⃣ Crop Recommendation

POST /api/crop

{
  "soilType": "clay",
  "rainfall": 220,
  "temperature": 28,
  "humidity": 70
}

2️⃣ Soil Nutrient Analysis
POST /api/soil

{
  "N": 90,
  "P": 40,
  "K": 35
}

3️⃣ Weather Information
GET /api/weather?city=Pune

4️⃣ Market Price
GET /api/prices?crop=wheat

🤖 ML Model (Optional)

If you trained a crop prediction model on Kaggle:

Download the .pkl model

Add it to your Flask/Node backend

Use via:

POST /api/predict

🌐 Deployment Options

Render (recommended)
Railway.app
Vercel (serverless functions)
Firebase Cloud Functions

📜 License

This project is for educational and academic use.
Feel free to modify or extend.
