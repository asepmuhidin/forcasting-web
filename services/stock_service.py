
import csv
from pathlib import Path
from datetime import datetime, timedelta

# Root directory project
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder penyimpanan CSV saham
STOCK_DATA_DIR = BASE_DIR / "data" / "raw" / "stock_prices"

TICKERS = [
    "ADRO", "ANTM", "ASII", "BBCA",
    "BBRI", "BMRI", "EMTK", "EXCL",
    "ICBP", "INDF", "INKP", "JSMR",
    "KLBF", "MLPT", "MTDL", "PGAS",
    "PTBA", "SIDO", "SMGR", "TLKM",
    "TOTO", "TSPC", "UNTR", "UNVR"
]


def to_float(value):
    """Mengubah nilai CSV menjadi float."""
    if value is None or str(value).strip() == "":
        return None

    try:
        return float(str(value).strip().replace(",", ""))
    except (ValueError, TypeError):
        return None


def load_stock_data(ticker, period="365"):
    """
    Membaca data historis satu saham berdasarkan ticker.

    period:
        90  = 90 hari kalender
        180 = 180 hari kalender
        365 = 365 hari kalender
        all = seluruh data historis
    """

    ticker = ticker.upper().strip()

    if ticker not in TICKERS:
        raise ValueError("Ticker tidak terdaftar.")

    file_path = STOCK_DATA_DIR / f"{ticker}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"File dataset {ticker}.csv tidak ditemukan."
        )

    records = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Normalisasi nama kolom
            row = {
                str(key).strip().lower(): value
                for key, value in row.items()
                if key is not None
            }

            try:
                date_value = datetime.strptime(
                    row["date"][:10], "%Y-%m-%d"
                ).strftime("%Y-%m-%d")

                record = {
                    "date": date_value,
                    "open": to_float(row.get("open")),
                    "high": to_float(row.get("high")),
                    "low": to_float(row.get("low")),
                    "close": to_float(row.get("close")),
                    "adj_close": to_float(row.get("adj close")),
                    "volume": to_float(row.get("volume")),
                }

                records.append(record)

            except (KeyError, ValueError, TypeError):
                continue

    if not records:
        raise ValueError(
            f"Tidak ada data valid untuk saham {ticker}."
        )

    # Urutkan berdasarkan tanggal
    records.sort(key=lambda x: x["date"])

    # Filter periode
    if period != "all":
        allowed_periods = {
            "90": 90,
            "180": 180,
            "365": 365
        }

        if period not in allowed_periods:
            raise ValueError("Periode tidak valid.")

        last_date = datetime.strptime(
            records[-1]["date"], "%Y-%m-%d"
        )

        start_date = last_date - timedelta(
            days=allowed_periods[period]
        )

        records = [
            item for item in records
            if datetime.strptime(
                item["date"], "%Y-%m-%d"
            ) >= start_date
        ]

    if not records:
        raise ValueError("Tidak ada data pada periode tersebut.")

    latest = records[-1]

    # Cari harga penutupan sebelumnya
    previous_close = None

    for item in reversed(records[:-1]):
        if item["close"] is not None:
            previous_close = item["close"]
            break

    latest_close = latest["close"]

    daily_change = None
    daily_change_pct = None

    if (
        latest_close is not None
        and previous_close is not None
    ):
        daily_change = latest_close - previous_close

        if previous_close != 0:
            daily_change_pct = (
                daily_change / previous_close
            ) * 100

    # Tabel menampilkan 20 data terakhir
    table_data = list(reversed(records[-20:]))

    return {
        "ticker": ticker,
        "total_records": len(records),
        "latest_date": latest["date"],
        "latest_close": latest_close,
        "latest_volume": latest["volume"],
        "previous_close": previous_close,
        "daily_change": daily_change,
        "daily_change_pct": daily_change_pct,
        "history": records,
        "table": table_data
    }