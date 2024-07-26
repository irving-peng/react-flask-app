from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import io
from flask import (Flask, send_file,  redirect, render_template, request,
                   send_from_directory, url_for)
from flask import jsonify
import pandas as pd
import numpy as np
import math
import statistics

app = Flask(__name__, static_folder='my-app/build', static_url_path='')
CORS(app)

# Global variable to store item
stored_item = None
sale_table = None
market_table = None 
price_table = None
rate_table = None
# used to check if data is avaliable for market
have_mdata = True
have_pdata = True
@app.route('/api', methods=['GET'])
@cross_origin()
def index():
    return {
        "tutorial" : "Sales Trend Visualization"
    }

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')
    #return "hello world"

@app.route('/submit-item', methods=['POST'])
def submit_item():
    global stored_item
    global sale_table
    global market_table
    global price_table
    global rate_table
    global have_mdata
    global have_pdata
    data = request.get_json()
    item = data.get('item')
    # Process the item as needed
    stored_item = item
    print(f"Received item: {item}")
    
    # stored sale_table, market_table
    df = pd.read_csv("./my-app/public/sell_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    input_id = [stored_item]  ## change to check for different hu
    itemID = input_id #input the item id you want to search
    mask = df['ItemID'].isin(itemID)
    filtered_item = df[mask]
    sale_table = filtered_item.groupby(filtered_item.Date.dt.year)['Quantity'].sum()
    sale_table = pd.DataFrame({'Year':sale_table.index, 'Qty':sale_table.values})
    sale_table = sale_table.reset_index()  # make sure indexes pair with number of rows

    # market-table not stored in this function yet
    input_id = [stored_item]
    if stored_item == None:
        return None
    df = pd.read_csv("./my-app/public/data.csv")
    itemID = input_id #input the item id you want to search
    mask = df['ItemID'].isin(itemID)
    filtered_item = df[mask]
    # check if data is avaliable for this item
    if not filtered_item.empty:
        have_mdata = True # set this to True
        yearly_total = {}
        for index, row in filtered_item.iterrows(): # nice method to use
            year = row['Year']
            quantity = row['Quantity']
            if year not in yearly_total:
                yearly_total[year] = quantity
            else:
                yearly_total[year] += quantity 
        years = list(yearly_total.keys())
        # creating the prediction of all total demand in the after-market (2010 -> 2027)
        scrappage_rate = 0.05
        after_market = {}
        for current_year in range(years[0]+3,years[len(years)-1]+14,1):
            # check year that are in the after-market
            start_year = current_year -13
            end_year = current_year -3
            if(start_year < years[0]):
                start_year = years[0]
            year_included = years[start_year -years[0]:end_year-years[0]+1]
            #### calculate total up to current year###
            total = 0
            for year in year_included:
                total += yearly_total[year] *0.95**(current_year-(year+3)+1) ## 0.95 should be multiply extra n times for extra n years after 2010, 2010 is 1 time
            after_market[current_year] = int(total)
        # turn the dictionary into a df
        market_table = pd.DataFrame(after_market.items(), columns=['Year', 'Qty'])
    else:
        #generate a dictionary with 0s from start year of sales table to 2024
        have_mdata = False # set this to false
        start_year = sale_table.iloc[0]['Year']
        years =  range(start_year, 2024)# should be creating a df of the same length as sales_table
        d = {'Year':years, 'Qty': np.ones(len(years))}
        market_table = pd.DataFrame(data=d)
    # remove the row prior to the start year of sale_table
    start_year = sale_table.iloc[0]['Year']
    remove_year = []
    for i, row in market_table.iterrows():
        if (market_table.iloc[i]['Year'] < start_year):
            print(market_table.iloc[i]['Year'], "is out! ")
            remove_year.append(i)
    market_table = market_table.drop(labels=remove_year, axis=0)
    market_table = market_table.reset_index()
    market_table = market_table.drop(labels="index", axis=1)

    # calculate the price table
    #also remove the year prior to the starting year of sale table
    df = pd.read_csv("./my-app/public/sale_price.csv")
                    # index_col = 'Year',
                    # parse_dates=False)
    df['Date'] = pd.to_datetime(df['Date'])
    itemID = [stored_item] #input the item id you want to search
    mask = df['ItemID'].isin(itemID)
    filtered_item = df[mask]
    if not filtered_item.empty:
        have_pdata = True # set this to True
        price_table = filtered_item.groupby(filtered_item.Date.dt.year)['Price'].mean().round(0)
        price_table = pd.DataFrame({'Year':price_table.index.astype(int), 'Price': price_table.values.astype(int)})
    else:
        have_pdata = False
        years =  range(start_year, 2024)# should be creating a df of the same length as sales_table
        d = {'Year':years, 'Price': np.ones(len(years))}
        price_table = pd.DataFrame(data=d)
    # remove the row prior to the start year of sale_table
    start_year = sale_table.iloc[0]['Year']
    remove_year = []
    for i, row in price_table.iterrows():
        if (price_table.iloc[i]['Year'] < start_year):
            print(price_table.iloc[i]['Year'], "is out! ")
            remove_year.append(i)
    price_table = price_table.drop(labels=remove_year, axis=0)
    price_table = price_table.reset_index()
    price_table = price_table.drop(labels="index", axis=1)

    # calculate the sales-market ratio
    if have_mdata:
        end_year = 0
        if market_table.iloc[len(market_table)-1]['Year'] > sale_table.iloc[len(sale_table)-1]['Year']:
            end_year = sale_table.iloc[len(sale_table)-1]['Year']
        else:
            end_year = sale_table.iloc[len(market_table)-1]['Year']

        valid_year_index = sale_table.index[sale_table['Year'] <= end_year].tolist()
        valid_years = sale_table.iloc[:len(valid_year_index)]['Year']

        rates = []
        for i in (valid_year_index):
            sale = sale_table.iloc[i]['Qty']
            market = market_table.iloc[i]['Qty']
            rates.append(sale/market)

        d = {'Year':valid_years, 'Qty':rates}
        rate_table = pd.DataFrame(data=d)
    else:
        start_year = sale_table.iloc[0]['Year']
        years = range(start_year, 2024)
        d = {'Year':years, 'Qty': np.ones(len(years))}
        rate_table = pd.DataFrame(data=d)
    # Send a response back to the client
    return jsonify({'status': 'success', 'item': item})

@app.route('/get-item', methods=['GET'])
def get_item():
    global stored_item
    if stored_item is None:
        return jsonify({'status': 'error', 'message': 'No item found'}), 404
    return jsonify({'status': 'success', 'item': stored_item})


# example plotting method
@app.route('/plot')
def plot():
    # Generate a simple plot
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3], marker='o')
    plt.title('Sample Plot')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Return the image file
    return send_file(img, mimetype='image/png')

@app.route('/sales-plot')
def sales_plot():
    global stored_item
    global sale_table
    if stored_item == None:
        return None
    plt.figure(figsize=(20, 10))  # Set figure size
    sale_table['Qty'].plot(legend = True, label = 'Qty', title = \
        "Sales By Year", style = '-', linewidth = 2.5, fontsize=15,figsize=(20, 10))
    # naming the x and y axis
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Qty', fontsize=15)
    plt.xticks(sale_table.index,sale_table["Year"].values)
    
    # Adjust layout
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    # Return the image file
    return send_file(img, mimetype='image/png')

@app.route('/market-plot')
def market_plot():
    global stored_item
    global sale_table
    global market_table
    global have_mdata
    if stored_item == None:
        return jsonify({'status': 'error', 'message': 'No item found'}), 404
    if not have_mdata:
        return jsonify({'status': 'error', 'message': 'No Data Found'}), 404
    plt.figure(figsize=(20, 10))  # Set figure size
    market_table['Qty'].plot(legend = True, label = 'Qty', title = \
        "Market Demand by year", style = '-', linewidth = 2.5, fontsize=15,figsize=(20, 10))
    # naming the x and y axis
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Qty', fontsize=15)
    plt.xticks(market_table.index,market_table["Year"].values)
    # Adjust layout
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    # Return the image file
    return send_file(img, mimetype='image/png')
    
@app.route('/price-plot')
def price_plot():   
    global price_table
    global stored_item
    print("price table", price_table)
    if stored_item == None:
        return None
    if not have_pdata:
        return jsonify({'status': 'error', 'message': 'No Data Found'}), 404
     # plotting
    plt.figure(figsize=(20, 10))  # Set figure size
    price_table['Price'].plot(legend = True, label = 'Price', title = \
      "Sale price by year", style = '-', linewidth = 2.5, fontsize=15,figsize=(20, 10))
    # naming the x and y axis
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Price', fontsize=15)
    plt.xticks(price_table.index,price_table["Year"].values)
    # Adjust layout
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    # Return the image file
    return send_file(img, mimetype='image/png')

@app.route('/rate-plot')
def rate_plot():
    global rate_table
    global have_mdata
    if stored_item == None:
        return jsonify({'status': 'error', 'message': 'No Item Found'}), 404
    if not have_mdata:
        return jsonify({'status': 'error', 'message': 'No Data Found'}), 404
    plt.figure(figsize=(20, 10))  # Set figure size
    rate_table['Qty'].plot(legend = True, label = 'Market-Share-Rate', title = \
        "sales: market share rate", style = '-', linewidth = 2.5, fontsize=15,figsize=(20, 10))
    # naming the x and y axis
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Rate', fontsize=15)
    plt.xticks(rate_table.index,rate_table["Year"].values)
    # Adjust layout
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    # Return the image file
    return send_file(img, mimetype='image/png')

@app.route('/combined-plot')
def combined_plot():
    global sale_table
    global market_table
    global price_table
    global rate_table
    global have_mdata
    # adjust all four of the table to make them appear on a scale 1-10
    m_t = 0
    s_t = 0
    r_t = 0
    p_t = 0

    #calculating total
    for i in range(len(market_table)):
        m_t += (market_table.iloc[i]['Qty'])
    for i in range(len(sale_table)):
        s_t += (sale_table.iloc[i]['Qty'])
    for i in range(len(rate_table)):
        r_t += (rate_table.iloc[i]['Qty'])
    for i in range(len(price_table)):
        p_t += (price_table.iloc[i]['Price'])

    #calculating average
    market_avg = m_t / len(market_table)
    sale_avg = s_t / len(sale_table)
    rate_avg = r_t / len(rate_table)
    price_avg = p_t / len(price_table)

    # Calculate number of digits after first digit
    if have_mdata:
        market_d = math.floor(math.log10(market_avg)) 
    else:
        market_d = 1
    sale_d = math.floor(math.log10(sale_avg))
    if have_mdata: 
        rate_d = math.floor(math.log10(rate_avg))
    else:
        rate_d = 1
    price_d = math.floor(math.log10(price_avg))

    digit_list = [market_d, sale_d, rate_d,price_d]
    max_digit = max(market_d, sale_d, rate_d,price_d)

    # iterrate through digit_list to see which table need adjustment
    adjustment_list =[]
    for i in range(len(digit_list)):
        digit = digit_list[i]
        if i==0:
            if digit < max_digit:
                adjustment_list.append("market")             
        if i==1:
            if digit < max_digit:
                adjustment_list.append("sale")
        if i==2:
            if digit < max_digit:
                adjustment_list.append("rate")
        if i==3:
            if digit < max_digit:
                adjustment_list.append("price")
    if "market" in adjustment_list:
        for i in range(len(market_table)):
            market_table.loc[i, 'Qty'] = market_table.loc[i, 'Qty'] * 10**(max_digit - market_d)
    if "sale" in adjustment_list:
        for i in range(len(sale_table)):
            sale_table.loc[i, 'Qty'] = sale_table.loc[i, 'Qty'] * 10**(max_digit - sale_d)
    if "rate" in adjustment_list:
        for i in range(len(rate_table)):
            rate_table.loc[i, 'Qty'] = rate_table.loc[i, 'Qty'] * 10**(max_digit - rate_d)   
    if "price" in adjustment_list:
        for i in range(len(price_table)):
            price_table.loc[i, 'Price'] = price_table.loc[i, 'Price'] * 10**(max_digit - price_d)

    # plotting sale table
    plt.figure(figsize=(20, 10))  # Set figure size

    my_title = str(stored_item) +" Sales graph"
    sale_table['Qty'].plot(legend = True, label = 'Sales-Qty', title = \
        my_title, style = '-', linewidth = 2.5, fontsize=15,figsize=(20, 10))
    # naming the x and y axis
    plt.xlabel('Year', fontsize=15)
    plt.ylabel('Qty', fontsize=15)
    plt.xticks(sale_table.index,sale_table["Year"].values)

    # plotting market table
    if have_mdata:
        market_table['Qty'].plot(legend = True, label = 'Market-Qty', title = \
            my_title, style = '-', linewidth = 2.5, fontsize=15,figsize=(20, 10))
        # naming the x and y axis
        plt.xlabel('Year', fontsize=15)
        plt.ylabel('Qty', fontsize=15)

    # plotting rate table 
    if have_mdata:
        rate_table['Qty'].plot(legend = True, label = 'Market-Share-Rate', title = \
            my_title, style = '-', linewidth = 2.5, fontsize=15,figsize=(20, 10))
        # naming the x and y axis
        plt.xlabel('Year', fontsize=15)
        plt.ylabel('Qty', fontsize=15)

    # plotting price table
    if have_pdata:
        price_table['Price'].plot(legend = True, label = 'Price(Inverse)', title = \
            my_title, style = '--', linewidth = 2.5, fontsize=15,figsize=(20, 10), color='red')
        # naming the x and y axis
        plt.xlabel('Year', fontsize=15)
        plt.ylabel('Qty', fontsize=15)

    if market_table.iloc[len(market_table)-1]['Year'] > sale_table.iloc[len(sale_table)-1]['Year']:
        plt.xticks(market_table.index,market_table["Year"].values)
    else:
        plt.xticks(sale_table.index,sale_table["Year"].values)
    # Adjust layout
    plt.tight_layout()

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()
    # Return the image file
    return send_file(img, mimetype='image/png')

    

if __name__ == '__main__':
    app.run()