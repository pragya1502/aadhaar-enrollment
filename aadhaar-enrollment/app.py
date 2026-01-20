from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
import re  # for pincode cleaning

app = Flask(__name__)

# ----------------------------
# LOAD DATA
# ----------------------------
CSV_PATH = os.path.join("data", "processed", "final_risk_scores.csv")

try:
    ml_data = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    print(f"CSV file not found at {CSV_PATH}")
    ml_data = pd.DataFrame()  # prevent crash

# Normalize CSV columns
if not ml_data.empty:
    ml_data['state'] = ml_data['state'].astype(str).str.strip().str.lower()
    ml_data['district'] = ml_data['district'].astype(str).str.strip().str.lower()
    ml_data['pincode'] = ml_data['pincode'].astype(int)


# ----------------------------
# ROUTES
# ----------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-risk', methods=['POST'])
def get_risk():
    try:
        # ----------------------------
        # READ JSON from frontend fetch
        # ----------------------------
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        state = data.get("state", "").strip().lower()
        district = data.get("district", "").strip().lower()
        pincode_raw = str(data.get("pincode", "")).strip()

        # ----------------------------
        # CLEAN PINCODE
        # ----------------------------
        pincode_clean = re.sub(r'\D', '', pincode_raw)
        if pincode_clean == "":
            return jsonify({"error": "Invalid pincode. Please enter only numbers."}), 400

        pincode = int(pincode_clean)

        # ----------------------------
        # DEBUG PRINTS (optional)
        # ----------------------------
        print(f"Input -> STATE: '{state}', DISTRICT: '{district}', PINCODE: {pincode}")
        print("Available pincodes for this district:",
              ml_data[ml_data['district'] == district]['pincode'].tolist()[:20])

        # ----------------------------
        # FILTER CSV
        # ----------------------------
        row = ml_data[
            (ml_data['state'] == state) &
            (ml_data['district'] == district) &
            (ml_data['pincode'] == pincode)
        ]

        if not row.empty:
            risk_score = float(row['risk_score_5_17'].values[0])
            risk_level = row['risk_level_5_17'].values[0]

            return jsonify({
                "risk_score": risk_score,
                "score_text": risk_score,  # optional text, can adjust
                "risk_level": risk_level
            })
        else:
            return jsonify({"error": "No data found for given inputs"}), 404

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# ----------------------------
# RUN FLASK APP
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)
