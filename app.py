from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CloudXeus Customer Portal</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f7fb;
                margin: 0;
                padding: 0;
            }

            .container {
                width: 700px;
                margin: 80px auto;
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                text-align: center;
            }

            h1 {
                color: #0078d4;
            }

            p {
                font-size: 18px;
                color: #444;
            }

            .status {
                margin-top: 30px;
                padding: 15px;
                background-color: #e8f5e9;
                border-radius: 8px;
                color: #2e7d32;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>CloudXeus Customer Portal</h1>

            <p>
                Welcome to our sample Python application running with FastAPI.
            </p>

            <p>
                This application will be packaged as a container image
                and deployed to Azure. This is the new line added.
            </p>

            <div class="status">
                Application Status: Running
            </div>
        </div>
    </body>
    </html>
    """