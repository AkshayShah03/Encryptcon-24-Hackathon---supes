from flask import Flask,request,render_template,flash,redirect,url_for,session,Response
from flask_session import Session
import os
import db
from datetime import datetime, timedelta
import model
import threading
import time

app = Flask(__name__)
tickers = {
    'Adani Green Energy': 'ADANIGREEN.BO',
    'Reliance Industries': 'RELIANCE.BO',
    'GAIL (India)': 'GAIL.BO',
    'ONGC (Oil and Natural Gas Corporation)': 'ONGC.BO',
    'Indian Oil Corporation (IOCL)': 'IOC.BO',
    'Tata Power': 'TATAPOWER.BO',
    'JSW Energy': 'JSWENERGY.BO',
    'Sterling and Wilson': 'SWPL.BO',
    'KP Energy': 'KPEL.BO',
    'Borosil Renewables': 'BORORENEW.BO',
    'Websol Energy Systems': 'WEBELSOLAR.BO',
    'NTPC (National Thermal Power Corporation)': 'NTPC.BO',
}

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/tech")
def tech():
    return render_template("tech.html")

@app.route('/loan')
def loan():
    return render_template('loan.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    goal = request.form['goal']
    budget = request.form['budget']
    coll = request.form['collateral']
    assets = request.form['assets']
    location = request.form['location']
    income = request.form['income']
    selected_options = request.form.getlist('selectOptions')

    # Include extra inputs if 'Agriculture' is selected
    extra_answer1 = None
    extra_answer2 = None
    if 'option3' in selected_options:
        extra_answer1 = request.form.get('extraAnswer1', '')
        extra_answer2 = request.form.get('extraAnswer2', '')
    
    db.new_customer(goal, budget, coll, assets, location, income, selected_options[0], extra_answer1, extra_answer2)
    print("database updated!")
    return render_template('add_data.html')
    
@app.route("/invest")
def invest():
    tech_list = list(tickers.values())
    start_date = "2023-01-01"
    end_date = datetime.today().strftime('%Y-%m-%d')
    company_list = model.download_stock_data(tech_list, start_date, end_date)
    img1 = model.plot_moving_averages(company_list, tech_list)
    img2 = model.plot_daily_returns(company_list, tech_list)
    imgs = []
    for i in tech_list:
        try:
            imgs.append(model.get_arima_predictions(i))
        except: pass
    return render_template('invest.html', img1=img1, img2=img2, imgs=imgs)
    
def simulate_long_running_process():
    time.sleep(10)  # Simulate a 10-second process
@app.route('/start_process')
def start_process():
    threading.Thread(target=simulate_long_running_process).start()
    return "Process started"
if __name__=="__main__":
    app.run(host='localhost',port=5000)