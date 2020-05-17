from flask import Flask, render_template,request, redirect
import selenium.webdriver as wd
import uuid
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from bs4.element import Tag
import pandas as pd
from scrape import get_results
from ranking import rank_by_approach1,rank_by_approach2

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home() :
    if request.method == 'POST':
        return 'POST'
    return render_template("index.html")
	#return "<h1>Hello! Welcome to IR Assignment-1 Demo</h1>"


yahoo_df=None
google_df=None
search_term=None
rank1_df=None
rank2_df=None


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search_term = request.form['query']
        top_n = request.form['topn']
        yahoo_df=get_results("yahoo",search_term,int(top_n))
        print(yahoo_df)
        google_df=get_results("google",search_term,int(top_n))
        print(google_df)
        f=open("search_term.txt","w")
        f.write(search_term)
        f.close()
        return render_template("index.html", search_response="Results Saved in "
                               +search_term+"_Yahoo.txt & "+search_term+"_Google.txt files")
#get_google_results()

@app.route('/merge', methods=['GET', 'POST'])
def merge_results():
    if request.method == 'POST':
        try:
            search_term
        except NameError:
            f=open("search_term.txt","r")
            search_term=f.read()
            f.close()
        yahoo_df = pd.read_csv(search_term+'_Yahoo.txt', sep="\t", header=None)
        yahoo_df.columns = ["unique_DocID", "title_snippet"]

        google_df = pd.read_csv(search_term+'_Google.txt', sep="\t", header=None)
        google_df.columns = ["unique_DocID", "title_snippet"]

        print(yahoo_df.shape)

        print(google_df.shape)

        merge = pd.concat([google_df,yahoo_df])
        print(merge.shape)
        print(merge[merge.duplicated(['unique_DocID'])])

        merge = pd.concat([google_df,yahoo_df]).drop_duplicates(subset=['unique_DocID'])
        #.reset_index(drop=True)
        print(merge.shape)
    
        file_name="UniqueDocuments.txt"
        merge.to_csv(file_name, sep="\t", header=None, index=False)
    
    return render_template("index.html", search_response="Done",merge_response="Merged Results saved in UniqueDocuments.txt")


@app.route('/rank', methods=['GET', 'POST'])
def rank_results():
    if request.method == 'POST':
        unique_df = pd.read_csv('UniqueDocuments.txt', sep="\t", names=(['unique_DocID','title_snippet']))
        try:
            search_term
        except NameError:
            f=open("search_term.txt","r")
            
            search_term=f.read()
            print(search_term)
            f.close()
        try:
            yahoo_df
        except NameError:
            yahoo_df = pd.read_csv(search_term+'_Yahoo.txt', sep="\t", header=None)
            yahoo_df.columns = ["unique_DocID", "title_snippet"]
        try:
            google_df
        except NameError:
            google_df = pd.read_csv(search_term+'_Google.txt', sep="\t", header=None)
            google_df.columns = ["unique_DocID", "title_snippet"]
        print(unique_df.head)
        print(google_df.head)
        print(yahoo_df.head)
        rank1_df=rank_by_approach1(google_df,yahoo_df,unique_df)
        #file_name="UniqueDocuments.txt"
        rank_app1_file_name="ResultantRanks_A1.txt"
        #f = open(file_name, "w")
        #cols = ["unique_DocID", "title_snippet"]
        rank1_df.to_csv(rank_app1_file_name, sep="\t", header=None, index=False)
        
        rank_app2_file_name="ResultantRanks_A2.txt"
        rank2_df=rank_by_approach2(search_term,unique_df)
        #f = open(file_name, "w")
        rank2_df.to_csv(rank_app2_file_name, sep="\t", header=None, index=False)
    
    return render_template("index.html", search_response="Done",merge_response="Done",
                           rank_response="Ranked Results saved in ResultantRanks_A1.txt "+
                           "and ResultantRanks_A2.txt files")

@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate_results():
    if request.method == 'POST':
        print("yes")
    
    return render_template("index.html", search_response="Done",merge_response="Done",
                           rank_response="Done",evaluate_response="Evaluation in progress")

if __name__ == "__main__":
	app.run()
              