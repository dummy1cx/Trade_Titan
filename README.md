<div align="center">⚡ Agentic AI Finance Assistant</div>
<div align="center"> A production ready multi agent financial assistant that forecasts, retrieves, reasons, and answers complex financial questions with grounded evidence. <br><br> <strong>Live Demo:</strong> <a href="http://34.229.199.104:8000/web/">http://34.229.199.104:8000/web/</a> </div> <br>
🔍 Try These Prompts
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#f9f9f9;">
Loan Approval

I’m applying for a home loan. Estimate approval and confidence.
Gender=Male Married=Yes Dependents=1 Education=Graduate Self_Employed=No
ApplicantIncome=6500 CoapplicantIncome=1500 LoanAmount=180 Term=360
Credit_History=1.0 Property_Area=Urban

Stock Forecast

Predict the next closing price for Apple.
ticker=AAPL

Insurance Premium

Calculate:
age=40 weight=70 bmi=24 children=2 region=urban smoker=yes sex=male

Insurance Premium with Explanation

age=40 weight=90 bmi=54 children=7 region=southeast smoker=yes sex=male
Give a detailed explanation.

RAG Queries

From Boeing DEF 14A:
When did Alan R. Mulally join the Board?

From Alphabet 10-K:
What risks does the company cite about international operations?

Business Insight

How is Microsoft planning to increase profit next financial year?

</div> <br>
⚙️ System Overview
<div style="display:flex; gap:12px;"> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#f8f9fa;"> <h3>🧠 AI Models</h3> • LSTM → Stock forecasting • Random Forest → Loan approval • XGBoost → Insurance premium • Embedding + FAISS → SEC filing retrieval </div> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#f8f9fa;"> <h3>🔗 Agent Orchestration</h3> • LangChain agent routing • LangGraph for planning and tool selection • Autonomous reasoning + multi step execution </div> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#f8f9fa;"> <h3>🚀 Deployment</h3> • Dockerized microservices • FastAPI inference layers • Hosted on AWS EC2 (Ubuntu) • Monitored with Prometheus and Grafana • Tracked with MLflow and W&B </div> </div> <br>
🐳 Docker Images
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#eef2f7;"> <pre> docker pull abhi1199/multi_agent:latest docker pull abhi1199/finance-agent:latest docker pull abhi1199/ml_fastapi_app:latest </pre> </div> <br>
📦 Repository Links
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#f9f9f9;"> <a href="https://hub.docker.com/r/abhi1199/multi_agent">multi_agent</a><br> <a href="https://hub.docker.com/r/abhi1199/finance-agent">finance-agent</a><br> <a href="https://hub.docker.com/r/abhi1199/ml_fastapi_app">ml_fastapi_app</a> </div> <br>
🌐 Deployment Access
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#f3f5f7;"> Your full system is running live at: <strong><a href="http://34.229.199.104:8000/web/">http://34.229.199.104:8000/web/</a></strong> </div> <br>
