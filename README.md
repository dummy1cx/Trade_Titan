<div align="center">
<img src="https://raw.githubusercontent.com/rickstaa/readme-generator/main/templates/banner.png" width="100%">
⚡ Agentic AI Finance Assistant

A production ready multi agent financial system that forecasts, retrieves, reasons, and answers domain specific questions with grounded citations.

<br>










<br>
Live Demo

🚀 http://34.229.199.104:8000/web/

</div>
🎯 Overview

This system blends tool using agents, predictive models, and a RAG engine over SEC filings to deliver finance domain intelligence.
It can forecast stock prices, evaluate loans, estimate insurance premiums, search 10-K filings, and analyze business strategy.

The interface lets users submit questions in natural language while agents autonomously plan, select tools, verify outputs, and answer with citations where needed.

<br>
🔍 Try These Prompts (Showcase)
<div style="border:1px solid #ccc; padding:18px; border-radius:10px; background:#f9f9f9; line-height:1.6;">
Loan Approval

I’m applying for a home loan. Estimate approval and confidence.
Gender=Male Married=Yes Dependents=1 Education=Graduate Self_Employed=No
ApplicantIncome=6500 CoapplicantIncome=1500 LoanAmount=180 Term=360
Credit_History=1.0 Property_Area=Urban

Stock Forecast

Predict the next closing price for Apple.
ticker=AAPL

Insurance Premium

age=40 weight=70 bmi=24 children=2 region=urban smoker=yes sex=male

Insurance with Explanation

age=40 weight=90 bmi=54 children=7 region=southeast smoker=yes sex=male
Give a detailed explanation.

RAG: Governance Query

From Boeing's DEF 14A
When did Alan R. Mulally join the Board?

RAG: Risk Disclosure

From Alphabet's 10-K
What risks are cited about international operations?

Business Insight

How is Microsoft planning to increase profit next financial year?

</div> <br>
⚙️ System Architecture
<div align="center"> <img src="https://raw.githubusercontent.com/rickstaa/readme-generator/main/templates/diagram.png" width="80%"> </div> <br>
🧠 Core Components
<div style="display:flex; gap:12px;"> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#eef2f7;"> <h3>AI Models</h3> LSTM for stock forecasting Random Forest for loan approval XGBoost for insurance premium Embedding + FAISS for SEC filings retrieval </div> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#eef2f7;"> <h3>Agent Stack</h3> LangChain tool routing LangGraph planning Autonomous decision making Self verification loop </div> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#eef2f7;"> <h3>Deployment</h3> FastAPI microservices Docker containers AWS EC2 hosting Prometheus and Grafana monitoring MLflow and W and B tracking </div> </div> <br>
🐳 Docker Images
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#f8f9fa;"> <pre> docker pull abhi1199/multi_agent:latest docker pull abhi1199/finance-agent:latest docker pull abhi1199/ml_fastapi_app:latest </pre> </div> <br>
📦 Docker Hub Repositories
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#fff;"> <a href="https://hub.docker.com/r/abhi1199/multi_agent">multi_agent</a><br> <a href="https://hub.docker.com/r/abhi1199/finance-agent">finance-agent</a><br> <a href="https://hub.docker.com/r/abhi1199/ml_fastapi_app">ml_fastapi_app</a> </div> <br>
🌐 Deployment Access
<div style="border:1px solid #ccc; padding:18px; border-radius:10px; background:#f3f5f7;"> Your system is live at: <strong><a href="http://34.229.199.104:8000/web/">http://34.229.199.104:8000/web/</a></strong> </div> <br>
