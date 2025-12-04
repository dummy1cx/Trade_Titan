<div align="center">
<img src="https://raw.githubusercontent.com/dummy1cx/Trade_Titan/main/preview.png" width="40%">



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

<div style="
  border:1px solid #ccc; 
  padding:22px; 
  border-radius:14px; 
  background:#f9f9f9; 
  line-height:1.55;
  font-size:15px;
">

<h3>01. Loan Approval Estimate</h3>
I’m applying for a home loan—can you estimate whether I’d be approved and the confidence?<br>
Gender=Male Married=Yes Dependents=1 Education=Graduate Self_Employed=No ApplicantIncome=6500 CoapplicantIncome=1500 LoanAmount=180 Loan_Amount_Term=360 Credit_History=1.0 Property_Area=Urban

<hr>

<h3>02. Stock Forecasting</h3>
Could you predict the next closing price for Apple?<br>
ticker=AAPL

<hr>

<h3>03. Insurance Premium</h3>
How much should I pay for insurance? calculate from tool_insurance.<br>
age = 40 weight = 70 bmi = 24 children = 2 region = urban smoker = yes sex = male

<hr>

<h3>04. Insurance with Explanation</h3>
age = 40 weight = 90 bmi = 54 children = 7 region = southeast smoker = yes sex = male<br>
Give a detailed explanation.

<hr>

<h3>05. RAG: Corporate Governance Query</h3>
From Boeing’s DEF 14A, since when has Alan R. Mulally served on the company’s Board of Directors?

<hr>

<h3>06. RAG: International Risk Exposure</h3>
From Alphabet’s 10-K, what risks does the company cite related to operating internationally and to financial exposures?  
Keep it concise and include citations.

<hr>

<h3>07. Metrics</h3>
WandB Loggers
<img src="https://raw.githubusercontent.com/dummy1cx/Trade_Titan/main/preview.png" width="40%">

</div>


</div> <br>
⚙️ System Architecture
<div align="center"> <img src="https://raw.githubusercontent.com/rickstaa/readme-generator/main/templates/diagram.png" width="80%"> </div> <br>
🧠 Core Components
<div style="display:flex; gap:12px;"> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#eef2f7;"> <h3>AI Models</h3> LSTM for stock forecasting Random Forest for loan approval XGBoost for insurance premium Embedding + FAISS for SEC filings retrieval </div> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#eef2f7;"> <h3>Agent Stack</h3> LangChain tool routing LangGraph planning Autonomous decision making Self verification loop </div> <div style="flex:1; border:1px solid #ddd; padding:18px; border-radius:10px; background:#eef2f7;"> <h3>Deployment</h3> FastAPI microservices Docker containers AWS EC2 hosting Prometheus and Grafana monitoring MLflow and W and B tracking </div> </div> <br>
🐳 Docker Images
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#f8f9fa;"> <pre> docker pull abhi1199/multi_agent:latest docker pull abhi1199/finance-agent:latest docker pull abhi1199/ml_fastapi_app:latest </pre> </div> <br>
<div style="border:1px solid #ddd; padding:18px; border-radius:10px; background:#fff;">
  <a href="https://hub.docker.com/r/abhi1199/multi_agent">multi_agent</a><br><br>
  <a href="https://hub.docker.com/r/abhi1199/finance-agent">finance-agent</a><br><br>
  <a href="https://hub.docker.com/r/abhi1199/ml_fastapi_app">ml_fastapi_app</a>
</div>

🌐 Deployment Access
<div style="border:1px solid #ccc; padding:18px; border-radius:10px; background:#f3f5f7;">  system is live at: <strong><a href="http://34.229.199.104:8000/web/">http://34.229.199.104:8000/web/</a></strong> </div> <br>
