Agentic AI Finance Assistant

A fully containerized, production-ready agentic system that blends prediction models, retrieval, and reasoning to answer real financial questions with grounded citations.

Live Demo

Web Interface:
http://34.229.199.104:8000/web/

Try These Prompts

01. Loan Approval Estimate
I’m applying for a home loan—can you estimate whether I’d be approved and the confidence?
Gender=Male Married=Yes Dependents=1 Education=Graduate Self_Employed=No ApplicantIncome=6500 CoapplicantIncome=1500 LoanAmount=180 Loan_Amount_Term=360 Credit_History=1.0 Property_Area=Urban

02. Stock Forecasting
Could you predict the next closing price for Apple?
ticker=AAPL

03. Insurance Premium
How much should I pay for insurance? calculate from tool_insurance.
age = 40 weight = 70 bmi = 24 children = 2 region = urban smoker = yes sex = male

04. Insurance with Explanation
age = 40 weight = 90 bmi = 54 children = 7 region = southeast smoker = yes sex = male
Give a detailed explanation.

05. RAG: Corporate Governance Query
From Boeing’s DEF 14A, since when has Alan R. Mulally served on the company’s Board of Directors?

06. RAG: International Risk Exposure
From Alphabet’s 10-K, what risks does the company cite related to operating internationally and to financial exposures? Keep it concise and include citations.

07. Business Insight
How is Microsoft planning to increase their profit for the next financial year?

What This System Does

This project creates a multi-agent financial assistant that thinks, retrieves, predicts, and explains. The system can plan its own steps, call the right tools, validate information, and respond with evidence.

Here’s what powers it underneath:

Core Features

• Built a finance assistant that handles analytical Q&A, forecasts, approvals, and grounded citations.
• Integrated three production models
 • LSTM for stock price forecasting
 • Random Forest for home loan approval
 • XGBoost for insurance premium estimation
• Constructed a retrieval engine over SEC 10-K filings using embedding models and FAISS.
• Deployed across AWS EC2 using Docker with continuous monitoring through Prometheus and Grafana.
• Experiment tracking and model lifecycle managed with MLflow and W&B.
• Routing logic and tool orchestration handled through LangChain and LangGraph, giving agents autonomy to pick the right workflow for each question.

Docker Images

You can pull the production containers directly:

docker pull abhi1199/multi_agent:latest
docker pull abhi1199/finance-agent:latest
docker pull abhi1199/ml_fastapi_app:latest


These containers include the web interface, the agent layer, and all ML inference endpoints.

Deployment

The full stack is running on an Ubuntu EC2 instance at:

http://34.229.199.104:8000/web/

The system boots through Docker and exposes the agent interface via FastAPI.