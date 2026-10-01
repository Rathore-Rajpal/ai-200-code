import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI


# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

base_url = os.environ["OPENAI_BASE_URL"]
api_key = os.environ["OPENAI_API_KEY"]
deployment_name = os.environ["MODEL_DEPLOYMENT"]


# ---------------------------------------------------
# OpenAI client
# ---------------------------------------------------

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)


# ---------------------------------------------------
# FastAPI application
# ---------------------------------------------------

app = FastAPI(
    title="AI Support Backend"
)


# ---------------------------------------------------
# Request model
# ---------------------------------------------------

class TicketRequest(BaseModel):
    ticket: str


# ---------------------------------------------------
# Health endpoint
# ---------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ---------------------------------------------------
# AI endpoint
# ---------------------------------------------------

@app.post("/analyze")
def analyze_ticket(request: TicketRequest):

    try:

        response = client.responses.create(
            model=deployment_name,

            instructions="""
            You are an AI assistant that analyzes
            customer support tickets.

            Determine:
            - the category
            - the priority
            - a short summary

            Keep the response concise.
            """,

            input=request.ticket
        )

        return {
            "result": response.output_text
        }

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )