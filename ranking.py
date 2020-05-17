
import pandas as pd
import string

def rank_by_approach1(google_df,yahoo_df,unique_df):
    app1_df=pd.DataFrame(columns=['unique_DocID','score','rank','title_snippet'])
    total=len(unique_df['unique_DocID'])
    for docID in unique_df['unique_DocID']:
        google_rank=75
        yahoo_rank=75
        rank=unique_df[unique_df['unique_DocID'] == docID].index[0]
        if docID in google_df.unique_DocID.values:
            google_rank=google_df[google_df['unique_DocID'] == docID].index[0]+(1/total)
            print('google: '+str(google_rank)+'-'+docID)
        if docID in yahoo_df.unique_DocID.values:
            yahoo_rank=yahoo_df[yahoo_df['unique_DocID'] == docID].index[0]+(2/total)
            print('yahoo: '+str(yahoo_rank)+'-'+docID)
        
        
        print('unique: '+str(rank)+'-'+docID)
       
        meta_rank=min(google_rank,yahoo_rank)
        print('meta_rank: '+str(meta_rank))
        print('\n')
        app1_df.loc[len(app1_df)] = [ docID,meta_rank,0, unique_df['title_snippet'][len(app1_df)]]
        
    app1_df.sort_values(by=['score'], inplace=True)
    app1_df['rank']=app1_df['score'].rank(method='first')
    app1_df['rank']=app1_df['rank'].astype(int)
    print(app1_df)
    return app1_df

def rank_by_approach2(search_terms,unique_df):
    app2_df=pd.DataFrame(columns=['unique_DocID','score','rank','title_snippet'])
    for document in unique_df['title_snippet']:
        score = measure_relevance(search_terms,document)
        app2_df.loc[len(app2_df)] = [unique_df['unique_DocID'][len(app2_df)], score,0,unique_df['title_snippet'][len(app2_df)]]
    
    app2_df.sort_values(by=['score'], inplace=True)
    print(app2_df)
    app2_df['rank']=app2_df['score'].rank(method='first')
    app2_df['rank']=app2_df['rank'].astype(int)
    #for i in range(0,len(app2_df)):
        #app2_df.loc[i].rank=i
    print(app2_df)
    return app2_df

def measure_relevance(search_terms,document):
    rel=1
    punct=str.maketrans('', '', string.punctuation)
    all_terms=document.lower().split()
    all_terms = [w.translate(punct) for w in all_terms]
    terms=search_terms.split()
    for term in terms:
        print(term,all_terms.count(term.lower()))
        tf=all_terms.count(term)
        rel = rel * 0.5 * ((tf/len(all_terms))+2)
    return rel