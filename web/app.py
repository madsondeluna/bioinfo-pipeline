from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "http://localhost:5000/variants"

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/filter", methods=["GET"])
def filter_variants():
    min_af = request.args.get("min_af", 0.0)
    max_af = request.args.get("max_af", 1.0)
    min_dp = request.args.get("min_dp", 0)

    response = requests.get(API_URL, params={
        "min_af": min_af,
        "max_af": max_af,
        "min_dp": min_dp,
    })

    if response.status_code == 200:
        variants = response.json()
        return render_template("index.html", variants=variants)
    else:
        return render_template("index.html", error="Erro ao buscar dados da API.")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
