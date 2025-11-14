AI Productivity Dashboard

Python • Power BI • Machine Learning

This project analyzes how AI tools (ChatGPT, Copilot, Notion AI, etc.) impact work productivity across different job roles.
The dataset contains 1,000 synthetic, realistic entries covering AI usage patterns, time saved, performance improvement, and satisfaction.

Tech Stack

Python (pandas, matplotlib, seaborn, scikit-learn)

Power BI

Key Features

End-to-end data pipeline: CSV→ Python EDA → ML → Power BI dashboard

Regression model to predict time_saved_per_week

R² = 0.80, MAE ≈ 0.75

Power BI dashboard with:

1. Productivity by role
2. Tool usage comparison
3. Satisfaction vs performance trends


📁 Project Structure

/data           → dataset
/notebook      → full EDA + ML notebook
/sql           → database + queries
/powerbi       → .pbix dashboard file
/images        → screenshots for README


Model Performance

R² Score: 0.80  
MAE: 0.75  

📂 How to Use

1. Clone repo
2. Install requirements
3. Open notebook → run EDA + ML
4. Load Power BI .pbix to view dashboard
5. Browse SQL folder for DB operations

📌 Insights

AI usage increases weekly productivity by 18–22%

Data & content roles show maximum gains

Higher satisfaction strongly correlates with performance improvement

Remote workers saved more time than office workers (on avg.)

📄 Future Work

Add Random Forest model

Build an API version

Deploy dashboard online
