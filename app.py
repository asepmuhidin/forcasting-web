
from flask import Flask, render_template, jsonify, request

from services.stock_service import (
    TICKERS,
    load_stock_data
)

app = Flask(__name__)


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

app.config["JSON_SORT_KEYS"] = False


# =========================================================
# MAIN DASHBOARD
# =========================================================

@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        tickers=TICKERS
    )


# =========================================================
# STOCK EXPLORER PAGE
# =========================================================

@app.route("/stock-explorer")
def stock_explorer():
    return render_template(
        "stock_explorer.html",
        tickers=TICKERS
    )


# =========================================================
# STOCK DATA API
# =========================================================

@app.route("/api/stocks/<ticker>", methods=["GET"])
def stock_api(ticker):

    period = request.args.get("period", "365")

    try:

        # Load historical stock data
        data = load_stock_data(
            ticker=ticker,
            period=period
        )

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except FileNotFoundError as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 404

    except ValueError as error:

        return jsonify({
            "success": False,
            "message": str(error)
        }), 400

    except Exception:

        app.logger.exception(
            "Unexpected error while loading stock data"
        )

        return jsonify({
            "success": False,
            "message": "Internal server error."
        }), 500


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health_check():

    return jsonify({
        "status": "ok",
        "application": "Forecasting Web Demo",
        "version": "1.0.0"
    }), 200


# =========================================================
# ERROR HANDLERS
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({
        "success": False,
        "message": "Page not found."
    }), 404


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "message": "Internal server error."
    }), 500


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )