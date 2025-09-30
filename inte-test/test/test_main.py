# import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


## Test two cases

def test_eligibility_pass():
    payload = {
        'income': 60000,
        'age' : 25,
        'employment_status' : 'employed'
    }
    respone = client.post('/loan-eligibility', json = payload)
    assert resposne.status_code == 200
    assert response.json() == {'eligible' : True}



