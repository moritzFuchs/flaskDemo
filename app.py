'''
Created on 24.05.2017

@author: Moritz Fuchs
'''
import quandl
from quandl.errors.quandl_error import NotFoundError
from bokeh.charts import TimeSeries
from bokeh.embed import components
from flask import Flask, render_template, request, jsonify
from pandas import DataFrame
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
# Set Quandl API key
quandl.ApiConfig.api_key = "ahDPSmt3RPsTSSo5PT3_"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

def format_date_for_quandl(date):
    return date.strftime("%Y-%m-%d")

@app.route('/get_stock_plot', methods=['GET'])
def get_stock_plot():

    # Get Data for stock the user requests 
    stock_keys = request.args.get("stock_names").split(",")
    if len(stock_keys) == 0 :
        return jsonify({"error": "Please enter a valid stock token."})
    
    stock_data = DataFrame()
    error_list = []
    plots = 0
    for stock_key in stock_keys:
        try:
            data = quandl.get("WIKI/" + stock_key, start_date=format_date_for_quandl(date.today() + relativedelta(months=-1)), end_date=format_date_for_quandl(date.today()))
        except NotFoundError:
            error_list.append(stock_key)
            continue

        plots+=1
        opening_data = data[["Open"]]
        if opening_data.empty:
            error_list.append(stock_key)
            continue
        opening_data = opening_data.rename(columns={"Date":"Date", "Open": stock_key})
        
        if stock_data.empty:
            stock_data = opening_data
        else:
            stock_data = pd.concat([stock_data, opening_data], axis=1)
            
    if not stock_data.empty and plots > 0:
        p = TimeSeries(stock_data, y=list(stock_data), title=", ".join(stock_keys), xlabel="", ylabel="Dollar")
        p.legend.click_policy="hide"
    
        script, div = components(p)
    else:
        script, div = "", ""
    
    result = {"script": script, "div": div}
    if len(error_list) > 0:
        result["notFound"] = error_list
    
    return jsonify(result)  

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    


