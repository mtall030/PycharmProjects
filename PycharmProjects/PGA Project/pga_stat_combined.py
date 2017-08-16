import requests
from bs4 import BeautifulSoup
import re
import csv
import time


def start_program():
    run = input("Run Progam? (y/n)")

    while run == "y":

        pages = stat_page()

        program = int(input("1: Lookup Player or 2: Print CSV: "))

        if program == 1:
            player_name = input("Input Player Name: ")

            count = 1
            for item in pages[0]:
                print(str(count) + ": " + item)
                count = count + 1

            selection = input("Please select one of the above: ")
            selection = int(selection) - 1

            single_player_stats(pages[1][selection], pages[0][selection], player_name)

        if program == 2:
            count = 1
            for item in pages[0]:
                print (str(count)+ ": " + item)
                count = count + 1

            selection = input("Please select one of the above: ")
            selection = int(selection) - 1

            csv_stats(pages[1][selection], pages[0][selection])
            print (pages[0][selection] + " CSV created!")

        run = input("Run again? (y/n)")


def stat_page():
    # retreiving HTML from webpage
    url = "http://www.pgatour.com/stats.html"
    r = requests.get(url)

    # takes HTML content in and converts to something to usable
    soup = BeautifulSoup(r.content, 'html.parser')

    # finding all "a" tags with class "see-all" - links to all the stat tables
    links = soup.find_all("a", {"class": "see-all"})
    link_list = []
    for item in links:
        link_list.append((item.get("href")))

    # finding the table names
    table_names = soup.find_all("div", {"class": "table-header"})
    table_list = []
    for item in table_names:
        item = item.text.replace("\n", "")
        table_list.append(item)

    return [table_list, link_list]


def csv_stats(stat, stat_name):
    #retreiving HTML from webpage
    #url = "http://www.pgatour.com/stats/stat.138.html"
    url = "http://www.pgatour.com" + stat
    r = requests.get(url)

    #takes HTML content in and converts to something to usable
    soup = BeautifulSoup(r.content, 'html.parser')

    #finding all td tags with class "player-name"
    player = soup.find_all("td", {"class": "player-name"})

    #finding all td tags with class "hidden-small...."
    data = soup.find_all("td", {"class": "hidden-small hidden-medium"})

    #finding all th tags, column labels
    col_headers = soup.find_all("th")

    #getting a list of rankings
    rankings = soup.find_all("td", {"class": ""})

    #lists of data
    player_names = []
    headers = []
    rank = []
    last_week_rank = []
    current_week_rank = []
    stats = []
    stat_lists = [current_week_rank, last_week_rank, player_names]

    #get a list of player names
    for item in player:
        player = item.text.replace("\n", "")
        player = player.replace("\xa0", " ")
        player_names.append(player)

    #setting up dictionary of col headers
    for item in col_headers:
        headers.append(item.text)

    #getting a list of rankings
    for item in rankings:
        myRegex = re.compile("\d+")
        mo = myRegex.findall(item.text)
        if len(mo) > 0:
           rank.append(mo[0])

    count = 1
    for item in rank:
        if count % 2 == 0:
            last_week_rank.append(item)
        else:
            current_week_rank.append(item)
        count = count + 1

    #getting a list of stats
    for item in data:
        stats.append(item.text)

    #creating new stat list for each stat
    count = 0
    for i in range(len(headers)-3):
        new_stat = stats[count::len(headers)-3]
        stat_lists.append(new_stat)
        count = count + 1

    #writing data to CSV file
    with open(stat_name + " " + time.strftime("%m-%d-%y") + ".csv", 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')

        data = [headers]
        a.writerows(data)

        data = stat_lists
        data = zip(*data)
        a.writerows(data)


def single_player_stats(stat, stat_name, player_name):
    #retreiving HTML from webpage
    #url = "http://www.pgatour.com/stats/stat.138.html"
    url = "http://www.pgatour.com" + stat
    r = requests.get(url)

    #takes HTML content in and converts something to usable
    soup = BeautifulSoup(r.content, 'html.parser')

    #finding all td tags with class "player-name"
    player = soup.find_all("td", {"class": "player-name"})

    #finding all td tags with class "hidden-small...."
    data = soup.find_all("td", {"class": "hidden-small hidden-medium"})

    #finding all th tags, column labels
    col_headers = soup.find_all("th")

    #getting a list of rankings
    rankings = soup.find_all("td", {"class": ""})

    #lists/dictionaries to draw from
    player_names = []
    headers = []
    rank = []
    last_week_rank = []
    current_week_rank = []
    stats = []

    #get a list of player names
    for item in player:
        player = item.text.replace("\n", "")
        player = player.replace("\xa0", " ")
        player_names.append(player)

    #setting up dictionary of col headers
    for item in col_headers:
        headers.append(item.text)

    #getting a list of rankings
    for item in rankings:
        myRegex = re.compile("\d+")
        mo = myRegex.findall(item.text)
        if len(mo) > 0:
           rank.append(mo[0])

    count = 1
    for item in rank:
        if count % 2 == 0:
            last_week_rank.append(item)
        else:
            current_week_rank.append(item)
        count = count + 1

    #getting a list of stats
    for item in data:
        stats.append(item.text)

    #player to search for
    player_index =  (player_names.index(player_name))

    #finding and printing stats
    print (stat_name)
    print (headers[2] + ": " + player_name)
    print (headers[0] + ": " + current_week_rank[player_index])
    print (headers[1] + ": " + last_week_rank[player_index])

    count = 0
    for i in range(len(headers)-3):
        print (headers[3 + count] + ": " + stats[player_index * (len(headers) - 3) + count])
        count = count + 1


start_program()