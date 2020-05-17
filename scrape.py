import selenium.webdriver as wd
import uuid
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from bs4.element import Tag
import pandas as pd
import numpy as np


def get_results(search_engine,search_term,top_n):
    f=None
    yahoo_df=pd.DataFrame(columns=['rank','unique_DocID','url','title_snippet'])
    if(search_engine=="google"):
        print("By Google")
        file_name=search_term+"_Google.txt"
        f = open(file_name, "w")
        google_df = get_google_results(f,search_engine,search_term,top_n)
        f.close()
        return google_df
    elif search_engine=="yahoo":
        print("By Yahoo")
        url="https://in.search.yahoo.com/search?p="+search_term+"&n="+str(top_n)
        file_name=search_term+"_Yahoo.txt"
        f = open(file_name, "w")
        browser=wd.Chrome()
        browser.implicitly_wait(20)
        browser.get(url)
        web_div=browser.find_element_by_id("results")
        links=web_div.find_elements_by_xpath("//h3//a")
        snippets=web_div.find_elements_by_xpath("//div[@class='compText aAbs']//p")
        results=[]
        index=0
        unique_DocID=uuid.uuid1()
        for link in links:
            #print("Index --> ",index)
            if index>29:
                break
            href=link.get_attribute("href")
            print("link",href)
            title=link.get_attribute("innerText")
            #print("title",title)
            snippet=""
            if search_engine=="yahoo":
                snippet=snippets[index].get_attribute("innerText")
            #print("snippet",snippet)
            
            #unique_DocID=uuid.uuid1()
            unique_DocID=uuid.uuid5(uuid.NAMESPACE_DNS, href)
            #print(unique_DocID)
            document=str(unique_DocID)+"\t"+title+' '+snippet+"\n"
            f.write(document)
            yahoo_df.loc[index]=[index,str(unique_DocID),href,(title+snippet)]
            index=index+1
        browser.close()
        f.close()
    return yahoo_df


def get_google_results(f,search_engine,search_term,top_n):
    df=pd.DataFrame(columns=['rank','unique_DocID','url','title_snippet'])
    browser = wd.Chrome()
    google_url = "https://www.google.com/search?q="+search_term+"&num="+str(top_n+2)
    browser.get(google_url)
    browser.implicitly_wait(20)

    soup = BeautifulSoup(browser.page_source,'lxml')
    result_div = soup.find_all('div', attrs={'class': 'g'})
    unique_DocID=uuid.uuid1()
    index=0
    for r in result_div:
        # Checks if each element is present, else, raise exception
        try:
            
            
            link = r.find('a', href=True)
            title = None
            title = r.find('h3')
            if isinstance(title,Tag):
                title = title.get_text()
            snippet = None
            snippet = r.find('span', attrs={'class': 'st'})
            if isinstance(snippet, Tag):
                snippet = snippet.get_text()
            # Check to make sure everything is present before appending
            #is_not_bia_link = not link.startswith('/search?')
            if link != ''  and title != '' and snippet != '':
                print("link",link['href'])
                #print("title",title)
                #print("snippet",snippet)
                #unique_DocID=uuid.uuid1()
                unique_DocID=uuid.uuid5(uuid.NAMESPACE_DNS, link['href'])
                #print(unique_DocID)
                related_search = link['href'].startswith('/search?') 
                #if title != None and snippet != None and not related_search:
                if not related_search:
                    document=str(unique_DocID)+"\t"+title+' '+snippet+"\n"
                    f.write(document)
                    df.loc[index]=[index,str(unique_DocID),link['href'],(title+snippet)]
                    index=index+1
        # Next loop if one element is not present
        except Exception as e:
            print(e)
            continue
    browser.close()
    return df

              