from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
DATA_FILE = "results/variants_annotated.tsv"

@app.route("/variants", methods=["GET"])
def get_variants():
    min_af = request.args.get("min_af", 0.0, type=float)
    max_af = request.args.get("max_af", 1.0, type=float)
    min_dp = request.args.get("min_dp", 0, type=int)

    df = pd.read_csv(DATA_FILE, sep="\t")

    filtered = df[
        (df["AF"].astype(float) >= min_af) &
        (df["AF"].astype(float) <= max_af) &
        (df["DP"].astype(float) >= min_dp)
    ]

    return filtered.to_json(orient="records")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
