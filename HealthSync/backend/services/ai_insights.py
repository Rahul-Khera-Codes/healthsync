import os
import json
from fastapi import APIRouter, HTTPException
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session
from .database import get_db
from .models import UserHealthData

router = APIRouter()

# Initialize OpenAI with the API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables.")

llm = OpenAI(api_key=openai_api_key)

# Define a prompt template for generating health insights
prompt_template = PromptTemplate(
    input_variables=["user_data"],
    template="Based on the following health data: {user_data}, provide personalized health insights."
)

# Create a LangChain LLMChain instance
insight_chain = LLMChain(llm=llm, prompt=prompt_template)

@router.post("/generate-insights/{user_id}")
async def generate_insights(user_id: int, db: Session = next(get_db())):
    try:
        # Fetch user health data from the database
        user_health_data = db.query(UserHealthData).filter(UserHealthData.user_id == user_id).first()
        
        if not user_health_data:
            raise HTTPException(status_code=404, detail="User health data not found.")

        # Prepare the user data for the prompt
        user_data = json.dumps(user_health_data.to_dict())  # Assuming to_dict() method exists

        # Generate insights using LangChain
        insights = insight_chain.run(user_data=user_data)

        return {"user_id": user_id, "insights": insights}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))