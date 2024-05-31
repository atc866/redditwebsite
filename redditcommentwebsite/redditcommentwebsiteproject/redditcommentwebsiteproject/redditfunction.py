import praw
import collections
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import text2emotion as te
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import seaborn as sns
import nltk
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.corpus import stopwords
import gensim
import numpy as np
import math
import base64
from io import BytesIO
reddit = praw.Reddit(
    client_id="HWLAINfomkxC4xx8vDjM-A",
    client_secret="k_DGIYSoFi2SGqxwTWAh-fFJV-WlbA",
    password="chuli189003",
    user_agent="scrapecomments",
    username="epiclol866",
)
def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph 
def getcomments(url):
    rv=[]
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments.list()[1:100]:
        print(top_level_comment.body)
        rv.append(top_level_comment.body)
    return rv

def sentiment_scores(comment):
    
    sia = SentimentIntensityAnalyzer()

    sentiment_dict = sia.polarity_scores(comment)
     
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    print("Sentence Overall Rated As", end = " ")
 
    if sentiment_dict['compound'] >= 0.05 :
        return("positive")
 
    elif sentiment_dict['compound'] <= - 0.05 :
        return("negative")
 
    else :
        return ('neutral')
def getemotion(comment):
    emotions=te.get_emotion(comment)
    print(emotions)
def createwordcloud(commentlist):
    joined=" ".join(commentlist)
    seperator = ", "
    joined=seperator.join(commentlist)
    joined=joined.lower()
    text = joined
    stop_list = nltk.corpus.stopwords.words("English")
    gensim_stopwords = gensim.parsing.preprocessing.STOPWORDS
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        STOPWORDS.add(letter)
    for word in stop_list:
        STOPWORDS.add(word)
    stopwords = set(STOPWORDS)
    print(stopwords)
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,5))
    wordcloud = WordCloud(width = 500,height = 500,max_words=100,stopwords=stopwords,max_font_size = 450,colormap='Blues', background_color="gray",normalize_plurals=True,collocations =True,include_numbers=True).generate(text)
    buffer=BytesIO()
    wordcloud.to_image().save(buffer,format='png')
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph 
def emotiongraph(commentlist):
    emotionlist=[]
    for comment in commentlist:
        emotionlist.append(te.get_emotion(comment))
    counter = collections.Counter()
    for d in emotionlist:
        counter.update(d)

    result = dict(counter)
    factor=1.0/np.sum(math.fsum(list(result.values())))
    for k in result:
      result[k] = result[k]*factor
    labels = ['Happy', 'Angry', 'Surprise', 'Sad','Fear']
    colors=["#f8d664","#ff0000","#e11584","#0000ff","#000000"]
    explode=(0.05,0.05,0.05,0.05,0.05)
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,5))
    plt.pie(result.values(),colors=colors,  labels=labels, autopct='%1.1f%%', startangle=90)
    centre_circle = plt.Circle((0,0),0.75,fc='white')
    plt.gcf()
    plt.gca().add_artist(centre_circle)
    plt.tight_layout()
    plt.title("percentage of feelings among 100 comments")
    graph=get_graph()
    return graph

def createbargraph(commentlist):
    mydic={"positive":0,"negative":0,"neutral":0}
    for comment in commentlist:
        print(sentiment_scores(comment))
        mydic[sentiment_scores(comment)]+=1
    #fig,ax=plt.subplot()
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,5))
    sns.barplot(x=list(mydic.keys()),y=list(mydic.values()))
    plt.title("frequency of top 100 comment sentiment")
    plt.xlabel("sentiment")
    plt.ylabel("comment count")
    plt.tight_layout()
    graph=get_graph()
    return graph

def checkurl(url):
    try:
        submission = reddit.submission(url=url)
        submission.comments
    except praw.exceptions.InvalidURL as error:
        return ("invalid url, please enter a valid url")
    except:
        return("there was a error please re-enter a valid link")
    try:
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=0)
        if(len(submission.comments.list())<100):
            raise ValueError("the reddit post you linked doesn't have enough comments")
    except ValueError as exp:
        return ("please enter a reddit post with atleast 100 comments")
    return True
    