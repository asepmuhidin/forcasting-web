from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Forecasting Web Demo</title>
        <style>
            body {
                font-family: Arial;
                background: #f1f5f9;
                text-align: center;
                padding: 100px;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                max-width: 600px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Forecasting Web Demo</h1>
            <p>Flask Application is Running!</p>
            <p>Ubuntu 24.04 LTS</p>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run()