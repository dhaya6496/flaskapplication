from flask import Flask
import pandas as pd
import os
import requests
from flask import make_response

app = Flask(__name__)

@app.route("/")
def hello():
    #getting the request from the url
    data= requests.get('https://api.covid19india.org/data.json')
    #checking the status_code
    print(data.status_code)

    recovered_list=[]
    confiremd_list =[]
    date_list=[]
    #getting the data as json
    if data.status_code == 200:
        covid_json = data.json()
        for d in covid_json['cases_time_series']:
            rec =  d['totalrecovered']
            conf = d['totalconfirmed']
            date = d['date']
            recovered_list.append(rec)
            confiremd_list.append(conf)
            date_list.append(date)

    #creation of output file
    df = pd.DataFrame({'date':date_list,'confirmed':confiremd_list,'recovered':recovered_list})
    resp = make_response(df.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename=api.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
    
    

if __name__ == "__main__":
    app.run()
