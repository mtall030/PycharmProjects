import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import style
import re

style.use("dark_background")
path = "C:/Users/IBM_ADMIN/PycharmProjects/examples/intraQuarter/intraQuarter"

def Key_Stats(gather=None):

    if gather is None:
        gather = ["Total Debt/Equity",
                  'Trailing P/E',
                  'Price/Sales',
                  'Price/Book',
                  'Profit Margin',
                  'Operating Margin',
                  'Return on Assets',
                  'Return on Equity',
                  'Revenue Per Share',
                  'Market Cap',
                  'Enterprise Value',
                  'Forward P/E',
                  'PEG Ratio',
                  'Enterprise Value/Revenue',
                  'Enterprise Value/EBITDA',
                  'Revenue',
                  'Gross Profit',
                  'EBITDA',
                  'Net Income Avl to Common ',
                  'Diluted EPS',
                  'Earnings Growth',
                  'Revenue Growth',
                  'Total Cash',
                  'Total Cash Per Share',
                  'Total Debt',
                  'Current Ratio',
                  'Book Value Per Share',
                  'Cash Flow',
                  'Beta',
                  'Held by Insiders',
                  'Held by Institutions',
                  'Shares Short (as of',
                  'Short Ratio',
                  'Short % of Float',
                  'Shares Short (prior month) ']

    statspath = path + "/_KeyStats" #setting path name to folder containing all the stock folders
    stock_list = [x[0] for x in os.walk(statspath)] #going to gather all the folder names in statspath direc
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 ##############
                                 'DE Ratio',
                                 'Trailing P/E',
                                 'Price/Sales',
                                 'Price/Book',
                                 'Profit Margin',
                                 'Operating Margin',
                                 'Return on Assets',
                                 'Return on Equity',
                                 'Revenue Per Share',
                                 'Market Cap',
                                 'Enterprise Value',
                                 'Forward P/E',
                                 'PEG Ratio',
                                 'Enterprise Value/Revenue',
                                 'Enterprise Value/EBITDA',
                                 'Revenue',
                                 'Gross Profit',
                                 'EBITDA',
                                 'Net Income Avl to Common ',
                                 'Diluted EPS',
                                 'Earnings Growth',
                                 'Revenue Growth',
                                 'Total Cash',
                                 'Total Cash Per Share',
                                 'Total Debt',
                                 'Current Ratio',
                                 'Book Value Per Share',
                                 'Cash Flow',
                                 'Beta',
                                 'Held by Insiders',
                                 'Held by Institutions',
                                 'Shares Short (as of',
                                 'Short Ratio',
                                 'Short % of Float',
                                 'Shares Short (prior month)',
                                 ##############
                                 'Status']) #creating a panda data frame with list of column names

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv") #creates a panda dataframe using the SP500 data

    ticker_list = [] # blank ticker list to be appended later when going through the folders


    for each_dir in stock_list[1:]: #for each folder (stock) in stock_list (all folders)
        each_file = os.listdir(each_dir) #sets each_file = to the path to each individual stokc folder
        ticker = each_dir.split("\\")[1] #sets the ticker to the name of the folder (which the name of the folder is the ticker)
        ticker_list.append(ticker) #appends the ticker list for each ticker name

        starting_stock_value = False #sets values to false to be used later in logic to ensure first data point calculated properly
        starting_sp500_value = False #sets values to false to be used later in logic to ensure first data point calculated properly

        if len(each_file) > 0: #as long as the file has a value at all
            for file in each_file: #each stock folder (each_file) has 1 file for the last ten years
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html') #setting the date stamp to the name to each file in each folder, which are named for the date
                unix_time = time.mktime(date_stamp.timetuple()) #setting a unix time based on the regular date

                full_file_path = each_dir + '/' + file #the file path all the way to each specific date file
                source = open(full_file_path, 'r').read() #opens up each individual file

                try:
                    value_list = []

                    for each_data in gather:
                        try:
                           regex = re.escape(each_data) + r'.*?(\-?\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                           value = re.search(regex, source)
                           value = (value.group(1))

                           if "B" in value:
                               value = float(value.replace("B", ''))*1000000000

                           elif "M" in value:
                               value = float(value.replace("M", '')) * 1000000

                        except Exception as e:
                            value = "N/A"
                            value_list.append(value)

                        value_list.append(value)


                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d') #sets the sp500 date using the unix time for particular folder
                        row = sp500_df[(sp500_df.index == sp500_date)] #grabs the row of data in the sp500 dataframe with the same unix time (like a vlookup)
                        sp500_value = float(row["Adj Close"]) #sets the sp500_value to the data in the Adj Close row if there was a match on unix time
                    except: #goes through same try process, but in case there was not a unix time match, jumps back 3 days
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d') #259200 = 3 days, subtracting 3 days to get out of the weekend
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])

                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0]) #grabs the stock price from the source file of each stock
                    except Exception as e:
                        try:
                            stock_price = source.split('</small><big><b>')[1].split('</b></big>')[0]
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            #print (stock_price)

                        except Exception as e:
                            try:
                                stock_price = source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0]
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                                stock_price = float(stock_price.group(1))
                                #print (stock_price)
                            except Exception as e:
                                #print ('Stock Price Exception', str(e))
                                pass




                    if not starting_stock_value: #logic to setup equation for getting percentage change for the first data point
                        starting_stock_value = stock_price

                    if not starting_sp500_value: #logic to setup equation for getting percentage change for the first data point
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100 #calculating the stock percentage change year to year
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100 #calculating the sp500 stock percentage change year to year

                    difference = stock_p_change - sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

                    # if value_list.count("N/A") > 0:
                    #     pass
                    # else:



                        df = df.append({'Date':date_stamp,
                                                'Unix':unix_time,
                                                'Ticker':ticker,

                                                'Price':stock_price,
                                                'stock_p_change':stock_p_change,
                                                'SP500':sp500_value,
                                                'sp500_p_change':sp500_p_change,
                                                'Difference':difference,
                                                'DE Ratio':value_list[0],
                                                #'Market Cap':value_list[1],
                                                'Trailing P/E':value_list[1],
                                                'Price/Sales':value_list[2],
                                                'Price/Book':value_list[3],
                                                'Profit Margin':value_list[4],
                                                'Operating Margin':value_list[5],
                                                'Return on Assets':value_list[6],
                                                'Return on Equity':value_list[7],
                                                'Revenue Per Share':value_list[8],
                                                'Market Cap':value_list[9],
                                                'Enterprise Value':value_list[10],
                                                 'Forward P/E':value_list[11],
                                                 'PEG Ratio':value_list[12],
                                                 'Enterprise Value/Revenue':value_list[13],
                                                 'Enterprise Value/EBITDA':value_list[14],
                                                 'Revenue':value_list[15],
                                                 'Gross Profit':value_list[16],
                                                 'EBITDA':value_list[17],
                                                 'Net Income Avl to Common ':value_list[18],
                                                 'Diluted EPS':value_list[19],
                                                 'Earnings Growth':value_list[20],
                                                 'Revenue Growth':value_list[21],
                                                 'Total Cash':value_list[22],
                                                 'Total Cash Per Share':value_list[23],
                                                 'Total Debt':value_list[24],
                                                 'Current Ratio':value_list[25],
                                                 'Book Value Per Share':value_list[26],
                                                 'Cash Flow':value_list[27],
                                                 'Beta':value_list[28],
                                                 'Held by Insiders':value_list[29],
                                                 'Held by Institutions':value_list[30],
                                                 'Shares Short (as of':value_list[31],
                                                 'Short Ratio':value_list[32],
                                                 'Short % of Float':value_list[33],
                                                 'Shares Short (prior month)':value_list[34],
                                                'Status':status}, ignore_index = True) #appending the dataframe with the data gathered in each loop

                except Exception as e:
                    pass


    # for each_ticker in ticker_list: #plotting each ticker in the ticker list
    #     try:
    #         plot_df = df[(df['Ticker'] == each_ticker)] #the plotting dataframe = our dataframe at index ticker == each_ticker in ticker_list
    #         plot_df = plot_df.set_index(['Date']) #setting the index to plot against as the Date field
    #
    #         if plot_df['Status'][-1] == "underperform":
    #             color = 'r'
    #         else:
    #             color = 'g'
    #
    #
    #         plot_df['Difference'].plot(label=each_ticker, color = color) #plotting the difference data
    #
    #         #plt.legend()
    #
    #     except:
    #         pass
    #
    # plt.show()

    df.to_csv('key_stats.csv') #saving a csv
    print ("CSV Created")


Key_Stats()