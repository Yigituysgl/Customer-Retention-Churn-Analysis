# Customer-Retention-Churn-Analysis

# 📉 Customer Retention & Churn Prediction Dashboard

An end-to-end project that combines SQL analysis, machine learning, and interactive visualization to predict telecom customer churn and provide actionable business insights.

Project Overview :
This project identifies customers who are likely to leave (churn) and explains why.  
It combines:
- SQL for initial data exploration  
- Python for model training and evaluation  
- Streamlit for dashboard deployment  
- Docker for containerized, one-click execution

The dataset used is **Telco Customer Churn (9,801 rows)**.

---

# Project Workflow

1. SQL Analysis: Used to understand key business trends and calculate churn rates by region, contract, and services.  
2. Model Comparison: Compared Logistic Regression vs Random Forest — Random Forest achieved the best AUC score.  
3. Feature Selection: Focused on the 5 strongest churn drivers for clarity and performance.  
4. Streamlit App:Interactive churn prediction dashboard (single customer + batch mode).  
5. Dockerization:Packaged the whole solution into a portable container.

---

# Model Development

| Model    |  AUC Score      | Comment |
|--------|------------       |----------|
| Logistic Regression | 0.78 | Simple, interpretable baseline |
| Random Forest |  0.81      | Best balance between accuracy & explainability |

The Random Forest model was selected and saved as `rf_pipeline.joblib`.


Business Insights & Recommendations : 
-Customers with month-to-month contracts show highest churn	Low loyalty	Offer discounted annual or 2-year plans
-Short-tenure customers churn early	Onboarding problems	Introduce personalized welcome offers
-No online security → higher churn	Service gaps	Promote bundled protection services
-High monthly charges correlate with churn	Price sensitivity	Offer loyalty points or tiered pricing
-Contract type and tenure are top drivers	Predictable churn pattern	Focus retention campaigns on early-stage users

Screenhots : 

<img width="1502" height="890" alt="image" src="https://github.com/user-attachments/assets/6a36a9bd-4800-48d2-b269-4f7f5aec3d25" />
<img width="1903" height="867" alt="image" src="https://github.com/user-attachments/assets/faaf1cef-0ed8-46db-8540-cb9a54565e00" />
<img width="1415" height="817" alt="image" src="https://github.com/user-attachments/assets/7a37780a-15d3-4b60-8017-784ed8f6b0a7" />
<img width="1366" height="702" alt="image" src="https://github.com/user-attachments/assets/c626742b-d57f-4d73-b693-ffba6f87570e" />









