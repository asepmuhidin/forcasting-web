
from flask import Flask, render_template

app = Flask(__name__)

# Daftar saham yang digunakan dalam penelitian
TICKERS = [
    "ADRO", "ANTM", "ASII", "BBCA",
    "BBRI", "BMRI", "EMTK", "EXCL",
    "ICBP", "INDF", "INKP", "JSMR",
    "KLBF", "MLPT", "MTDL", "PGAS",
    "PTBA", "SIDO", "SMGR", "TLKM",
    "TOTO", "TSPC", "UNTR", "UNVR"
]

@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        tickers=TICKERS
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)