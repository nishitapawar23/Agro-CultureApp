🌾 Smart Crop Recommendation & Agriculture App – Backend

This repository contains the backend for the Smart Agriculture Application, designed to help farmers and students with crop suggestions, soil analysis, weather information, and market price tracking.
The backend provides clean REST APIs that connect with your frontend.

🚀 Features

🌱 Crop Recommendation API

🧪 Soil Nutrient Analysis API

🌧️ Weather Information

📊 Market Price Lookup

🤖 Optional: Machine Learning Model Integration

🗄️ Database support (MongoDB / Firebase)

🔌 Easy-to-use REST APIs

🔐 CORS Enabled

🛠 Tech Stack

Backend: Node.js + Express
(If using Flask, update here — but Node.js preferred for students)

Database: MongoDB / Firebase

ML Model (optional): Python (.pkl model)

Frontend: Your existing UI (HTML/CSS/JS or React)

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
