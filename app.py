"""ZeroWaste AI - my Flask web app for SDG 12 (Responsible Consumption)."""
from flask import Flask, render_template, request, jsonify
import model, matcher
from data_gen import VENDOR_TYPES

app = Flask(__name__)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
HISTORY = []   # keeps recent predictions to show on the page (resets when the app restarts)

@app.route("/")
def index():
    _, _, metrics = model.load()
    total = sum(h["surplus"] for h in HISTORY)
    stats = {"runs": len(HISTORY), "kg": round(total, 1),
             "meals": sum(h["meals"] for h in HISTORY),
             "co2": round(total * 2.5, 1)}   # rough estimate: 1 kg food saved = about 2.5 kg CO2 not released
    return render_template("index.html", vendors=VENDOR_TYPES, days=DAYS, metrics=metrics,
                           stats=stats, history=HISTORY[-5:][::-1], result=None, form={})

@app.route("/predict", methods=["POST"])
def predict():
    f = request.form
    vt, day = f["vendor_type"], int(f["day_of_week"])
    prepared, foot = int(f["meals_prepared"]), int(f["expected_footfall"])
    fest, rain = int("festival" in f), int("rain" in f)
    lat, lon = float(f.get("lat", 28.6139)), float(f.get("lon", 77.2090))
    surplus = model.predict(vt, day, prepared, foot, fest, rain)
    plan, unplaced = matcher.allocate(surplus, lat, lon)
    meals = sum(p["meals"] for p in plan)
    advice = []
    if surplus > 0.15 * prepared * 0.5:
        advice.append("Reduce today's preparation by about %d%% to cut waste at the source." % min(30, int(surplus / max(prepared*0.5,1) * 40)))
    if fest: advice.append("Festival days raise surplus - prepare in smaller batches.")
    if rain: advice.append("Rain lowers footfall - cook to order where possible.")
    advice.append("Pack surplus in food-safe containers and hand over within 2 hours.")
    HISTORY.append({"vendor": vt, "day": DAYS[day], "surplus": surplus, "meals": meals})
    _, _, metrics = model.load()
    total = sum(h["surplus"] for h in HISTORY)
    stats = {"runs": len(HISTORY), "kg": round(total, 1), "meals": sum(h["meals"] for h in HISTORY),
             "co2": round(total * 2.5, 1)}
    result = dict(surplus=surplus, plan=plan, unplaced=unplaced, meals=meals, advice=advice)
    return render_template("index.html", vendors=VENDOR_TYPES, days=DAYS, metrics=metrics, stats=stats,
                           history=HISTORY[-5:][::-1], result=result, form=dict(f.items()) | {"festival": fest, "rain": rain})

@app.route("/api/predict", methods=["POST"])
def api_predict():
    d = request.get_json(force=True)
    s = model.predict(d["vendor_type"], d["day_of_week"], d["meals_prepared"],
                      d["expected_footfall"], d.get("festival", 0), d.get("rain", 0))
    plan, left = matcher.allocate(s, d.get("lat", 28.6139), d.get("lon", 77.2090))
    return jsonify(surplus_kg=s, plan=plan, unplaced_kg=left)

if __name__ == "__main__":
    model.load()
    app.run(debug=True)
