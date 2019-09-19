import pandas as pd
import numpy as np
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row, gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import file_html
from bokeh.resources import CDN
import quandl
import os
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
Quandl_Token = os.environ['Quandl_Token']
@app.route('/')
def index():

  return render_template('12Day.html')

@app.route('/search', methods=['GET','POST'])
def about():
  ticker_input = request.form['Ticker']
  #print(ticker)

  #Getting the ticker prices
  quandl.ApiConfig.api_key = Quandl_Token
  df = quandl.get_table('WIKI/PRICES', ticker=ticker_input,
                        qopts={'columns': ['ticker', 'date', 'adj_close']},
                        date={'gte': '2015-12-31', 'lte': '2016-12-31'},
                        paginate=True)
  print(df.head())


  df = df[['ticker', 'date', 'adj_close']]
  df['date'] = pd.DatetimeIndex(df['date'])

  def datetime(x):
    return np.array(x, dtype=np.datetime64)

  output_notebook()
  p1 = figure(x_axis_type="datetime", title="Data from Quandle WIKI set")
  p1.grid.grid_line_alpha = 0.3
  p1.xaxis.axis_label = 'Date'
  p1.yaxis.axis_label = 'Price'

  p1.line(datetime(df['date']), df['adj_close'], legend='Adj. Close')
  p1.legend.location = "top_left"

  output_file("stocks.html", title="Stock_Info_Output", mode='relative', \
              root_dir='/templates')

  output_plot = gridplot([[p1]], plot_width=400, plot_height=400)
  html = file_html(output_plot,CDN, "Quandl prices")




  return html

if __name__ == '__main__':
  app.run(port=33507)
