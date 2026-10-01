import os

import httpx
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

import html
import re

app = FastAPI(
    title="AI Support Frontend"
)


BACKEND_URL = os.environ.get(
    "BACKEND_URL",
    "http://localhost:8001"
)

def format_result(result):

    if not result:
        return ""

    # Escape any HTML returned by the model
    safe_result = html.escape(result)

    # Convert simple Markdown bold syntax to HTML
    safe_result = re.sub(
        r"\*\*(.*?)\*\*",
        r"<strong>\1</strong>",
        safe_result
    )

    # Convert line breaks to HTML line breaks
    safe_result = safe_result.replace("\n", "<br>")

    return safe_result



def render_page(result=""):

    result_html = format_result(result)

    return f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>AI Support Ticket Analyzer</title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background:
                    linear-gradient(
                        135deg,
                        #f4f8ff 0%,
                        #eef4ff 45%,
                        #f8f9fc 100%
                    );

                color: #1f2937;
                min-height: 100vh;
            }}

            .header {{
                background:
                    linear-gradient(
                        120deg,
                        #0057b8,
                        #0078d4
                    );

                color: white;
                padding: 35px 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            }}

            .header-content {{
                max-width: 900px;
                margin: auto;
            }}

            .header h1 {{
                margin: 0;
                font-size: 34px;
                font-weight: 700;
            }}

            .header p {{
                margin-top: 10px;
                margin-bottom: 0;
                font-size: 17px;
                opacity: 0.92;
            }}

            .container {{
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
            }}

            .card {{
                background: white;
                border-radius: 16px;
                padding: 32px;

                box-shadow:
                    0 10px 30px rgba(0,0,0,0.08);

                border: 1px solid #e5e7eb;
            }}

            .section-title {{
                font-size: 20px;
                font-weight: 600;
                margin-bottom: 8px;
            }}

            .description {{
                color: #6b7280;
                margin-bottom: 22px;
                line-height: 1.6;
            }}

            textarea {{
                width: 100%;
                height: 170px;

                border: 1px solid #cbd5e1;
                border-radius: 10px;

                padding: 16px;

                font-family: Arial, Helvetica, sans-serif;
                font-size: 16px;
                line-height: 1.5;

                resize: vertical;

                transition:
                    border-color 0.2s,
                    box-shadow 0.2s;
            }}

            textarea:focus {{
                outline: none;
                border-color: #0078d4;

                box-shadow:
                    0 0 0 3px rgba(0,120,212,0.15);
            }}

            textarea::placeholder {{
                color: #9ca3af;
            }}

            .button-container {{
                margin-top: 20px;
            }}

            button {{
                border: none;
                border-radius: 8px;

                background:
                    linear-gradient(
                        120deg,
                        #0078d4,
                        #0067b8
                    );

                color: white;

                padding: 13px 25px;

                font-size: 16px;
                font-weight: 600;

                cursor: pointer;

                box-shadow:
                    0 4px 12px rgba(0,120,212,0.25);

                transition:
                    transform 0.15s,
                    box-shadow 0.15s;
            }}

            button:hover {{
                transform: translateY(-1px);

                box-shadow:
                    0 7px 18px rgba(0,120,212,0.30);
            }}

            button:active {{
                transform: translateY(0);
            }}

            .result-card {{
                margin-top: 28px;

                background:
                    linear-gradient(
                        135deg,
                        #f0f7ff,
                        #f7fbff
                    );

                border-left: 5px solid #0078d4;

                border-radius: 10px;

                padding: 24px;

                line-height: 1.7;
            }}

            .result-header {{
                display: flex;
                align-items: center;
                gap: 10px;

                margin-bottom: 15px;
            }}

            .ai-icon {{
                width: 38px;
                height: 38px;

                border-radius: 50%;

                background:
                    linear-gradient(
                        135deg,
                        #0078d4,
                        #6b5cff
                    );

                color: white;

                display: flex;
                align-items: center;
                justify-content: center;

                font-size: 18px;
                font-weight: bold;
            }}

            .result-title {{
                font-size: 21px;
                font-weight: 700;
                color: #123b69;
            }}

            .result-content {{
                color: #253858;
                font-size: 16px;
            }}

            .badge {{
                display: inline-block;

                background: #e7f3ff;
                color: #005a9e;

                border-radius: 20px;

                padding: 5px 11px;

                font-size: 12px;
                font-weight: 600;

                margin-bottom: 18px;
            }}

            .footer {{
                text-align: center;

                margin-top: 30px;

                color: #94a3b8;
                font-size: 13px;
            }}

            @media (max-width: 600px) {{

                .header h1 {{
                    font-size: 27px;
                }}

                .card {{
                    padding: 22px;
                }}

            }}

        </style>

    </head>


    <body>

        <div class="header">

            <div class="header-content">

                <h1>AI Support Ticket Analyzer</h1>

                <p>
                    Analyze customer support requests using AI
                </p>

            </div>

        </div>


        <div class="container">

            <div class="card">

                <div class="badge">
                    AI-Powered Support Analysis
                </div>

                <div class="section-title">
                    Customer Support Ticket
                </div>

                <div class="description">
                    Enter a support request below.
                    The AI service will analyze the ticket and
                    determine its category, priority, and summary.
                </div>


                <form method="post" action="/analyze">

                    <textarea
                        name="ticket"
                        placeholder="Example: I requested a password reset but the email never arrived."
                        required></textarea>

                    <div class="button-container">

                        <button type="submit">
                            Analyze Ticket
                        </button>

                    </div>

                </form>


                {
                    f'''
                    <div class="result-card">

                        <div class="result-header">

                            <div class="ai-icon">
                                AI
                            </div>

                            <div class="result-title">
                                AI Analysis
                            </div>

                        </div>

                        <div class="result-content">
                            {result_html}
                        </div>

                    </div>
                    '''
                    if result
                    else ''
                }

            </div>


            <div class="footer">
                AI Support Application • Powered by Microsoft Foundry
            </div>

        </div>

    </body>

    </html>
    """

@app.get("/", response_class=HTMLResponse)
def home():

    return render_page()


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(ticket: str = Form(...)):

    try:

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{BACKEND_URL}/analyze",
                json={
                    "ticket": ticket
                },
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            result = data["result"]

            return render_page(result)

    except Exception as ex:

        return render_page(
            f"Error communicating with AI backend: {ex}"
        )