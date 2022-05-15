import requests
import json
import time
from pymongo import MongoClient
import pandas as pd
import datetime
from flask import Flask, jsonify, request, render_template

app= Flask(__name__)
app.jinja_env.filters['zip'] = zip

client = MongoClient("mongodb+srv://BDAT_dmistry@cluster0.a2ygj.mongodb.net/WeatherData?retryWrites=true&w=majority")
db =client.get_database('Project1')
records = db.WeatherData


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/googlecharts/pie-chart')
def googel_pie_chart():
	return render_template('piechart.html')

@app.route('/googlecharts/bar-chart')
def googel_bar_chart():
  formated_date_list = []
  query = { "city.name": {"$eq" : "Toronto"} }
  
  #data = {'dt': 1649808000, 'temp': {'average_max': 284.95, 'average_min': 274.05}}
  #data ={'list': [{'temp': {'average_max': 285.24}}, {'temp': {'average_max': 285.27}}, {'temp': {'average_max': 283.83}}   ]}
  
  m_data = records.find_one(query, {'_id':0,'list':{'dt':1, 'temp':{'average_max':1,'average_min':1} } })
  m_data_list = records.find_one(query, {'_id':0,'list':{'dt':1 } })
  list_data = m_data['list']
  
  for i in m_data_list['list']:
    your_timestamp = i['dt']
    date1= datetime.datetime.utcfromtimestamp(your_timestamp).strftime('%Y-%m-%d')
    formated_date_list.append(date1)
  #print(formated_date_list)
  
  return render_template('barchart.html',data=list_data , date_list =formated_date_list)


if __name__=="__main__":
	app.run()