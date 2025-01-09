from flask import Flask, request, render_template
import json
import urllib.request
import ssl
import os

app = Flask(__name__)

# Function to bypass self-signed certificate verification
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True)

# Azure endpoint and API key
url = ''
api_key = ''

def make_prediction(data):
    body = json.dumps(data).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return json.loads(result.decode("utf-8"))  # Load JSON response
    except urllib.error.HTTPError as error:
        return f"Error: {error.code} - {error.read().decode('utf-8')}"

@app.route('/')
def index():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    # Collecting input data from the form
    age = request.form['age']
    job = request.form['job']
    marital = request.form['marital']
    education = request.form['education']
    default = request.form['default']
    housing = request.form['housing']
    loan = request.form['loan']
    contact = request.form['contact']
    month = request.form['month']
    day_of_week = request.form['day_of_week']
    duration = request.form['duration']
    campaign = request.form['campaign']
    pdays = request.form['pdays']
    previous = request.form['previous']
    poutcome = request.form['poutcome']
    emp_var_rate = request.form['emp_var_rate']
    cons_price_idx = request.form['cons_price_idx']
    cons_conf_idx = request.form['cons_conf_idx']
    euribor3m = request.form['euribor3m']
    nr_employed = request.form['nr_employed']

    # Constructing the input data as required by the model
    data = {
        "input_data": {
            "columns": [
                "age", "job", "marital", "education", "default", 
                "housing", "loan", "contact", "month", "day_of_week", 
                "duration", "campaign", "pdays", "previous", "poutcome", 
                "emp.var.rate", "cons.price.idx", "cons.conf.idx", 
                "euribor3m", "nr.employed"
            ],
            "data": [[
                int(age), job, marital, education, default, 
                housing, loan, contact, month, day_of_week, 
                int(duration), int(campaign), int(pdays), int(previous), 
                poutcome, float(emp_var_rate), float(cons_price_idx), 
                float(cons_conf_idx), float(euribor3m), float(nr_employed)
            ]]
        }
    }

    prediction = make_prediction(data)
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
