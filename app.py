#    __.-._
#    '-._"7'
#     /'.-c
#     |  /T
#    _)_/LI

from flask import Flask, flash, request, redirect, url_for, render_template, session
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import requests
import os

app = Flask(__name__)
app.secret_key = 'hui'

link = requests.get("https://en.wikipedia.org/wiki/List_of_wars_by_death_toll").text
soup = BeautifulSoup(link, 'lxml')

table = soup.find_all('table', class_ = "wikitable")


df = None
for i in table:
    if df == None:
        df = pd.read_html(str(i))
    else:
        df = df + pd.read_html(str(i))    

df = pd.concat([df[0],df[1],df[2]], axis=0)
df["Deathrange"] = df["Deathrange"].str.replace("[citation needed]", "")
df["Deathrange"] = df["Deathrange"].str.replace("[", "")
df["Deathrange"] = df["Deathrange"].str.replace("]", "")

df.reset_index(inplace=True, drop=True)
#login
@app.route('/', methods=['post', 'get'])
def search():
    pogdanov = []
    if request.method == 'POST':
        searchResult = request.form.get('fname')
        tempDf = df[df['War'].str.contains(searchResult, case = False)]
        pogdanov = tempDf["War"].to_list()
    return render_template('warSearch.html', daList = pogdanov)

@app.route('/wars/<war>')
def result(war):
    for i in df["War"].to_list():
        if i == war:
            #return redirect("https://wikipedia.com/wiki/"+war)
            deaths = df.loc[df["War"] == war, "Deathrange"].to_list()[0]
            daDate = df.loc[df["War"] == war, "Date"].to_list()[0]
            ppl = df.loc[df["War"] == war, "Combatants"].to_list()[0]
            loc = df.loc[df["War"] == war, "Location"].to_list()[0]
            nts = df.loc[df["War"] == war, "Notes"].to_list()[0]
            
                        
            return render_template("war.html", message = war, deaths = deaths, ppl = ppl, loc = loc, nts = nts, daDate = daDate)
    return redirect("/404")

@app.route('/404')
def func404():
    return render_template("404.html")


if __name__ =='__main__':
    app.run(debug=True)




