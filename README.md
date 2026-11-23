# ZeroWaste AI

My capstone project for SDG 12 (Responsible Consumption and Production).

Restaurants, hostel messes and caterers often cook more than they need, and the extra food gets thrown away while people nearby go hungry. This app tries to fix that in two steps: it predicts how much food will be left over, then suggests which NGOs nearby can take it.

## What it does
- Predicts leftover food (in kg) using a Random Forest model
- Finds the nearest NGOs and splits the food between them based on how much each can take
- Shows how many meals were saved and roughly how much CO2 was avoided
- Gives tips such as "cook a little less today because it is raining"
- Has a small API (`POST /api/predict`) so other apps can use it

## How to run
```
pip install -r requirements.txt
python model.py
python app.py
```
Then open http://127.0.0.1:5000

## Note
The training data is made up (see `data_gen.py`) because I did not have real restaurant data. The NGOs in `matcher.py` are sample entries. Both should be replaced with real data in future.

## Tech used
Python, Flask, scikit-learn, pandas, HTML and CSS.
