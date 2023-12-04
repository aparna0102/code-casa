#!/usr/bin/env python
# coding: utf-8

# In[4]:


import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font
import pandas as pd
import numpy as np
import ast
credits_df = pd.read_csv("C:\\Users\\Admin\\OneDrive\\Desktop\\credits.csv")
movies_df = pd.read_csv("C:\\Users\\Admin\\OneDrive\\Desktop\\movies.csv")

pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)

movies_df= movies_df.merge(credits_df, on='title')
movies_df = movies_df[['movie_id','title','overview','genres','keywords','cast','crew']]
movies_df.dropna(inplace=True)
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

movies_df['genres']=movies_df['genres'].apply(convert)
movies_df['keywords']=movies_df['keywords'].apply(convert)

def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

movies_df['cast']=movies_df['cast'].apply(convert3)

def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
    return L

movies_df['crew']=movies_df['crew'].apply(fetch_director)
movies_df['overview']=movies_df['overview'].apply(lambda x:x.split())

movies_df['genres']=movies_df['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['keywords']=movies_df['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['cast']=movies_df['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['crew']=movies_df['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['tags']=movies_df['overview']+movies_df['genres']+movies_df['keywords']+movies_df['cast']+movies_df['crew']

new_df=movies_df[['movie_id','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:' '.join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

from sklearn.feature_extraction.text import CountVectorizer as ctv
cv= ctv(max_features=5000, stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()

#import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)
from sklearn.metrics.pairwise import cosine_similarity as cs
similarity = cs(vectors)

def recommend():
    movie=entry.get()
    movie_index=new_df[new_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    for i in movies_list:
        recommendation=Label(text=new_df.iloc[i[0]].title)
        recommendation.pack()
        
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

def display_name():
    name = entry.get()
    display_label.config(text=f"{name}")

#creating tk object
root = tk.Tk()
root.title("WatchNext")
root.geometry("400x400")
#entry_message=Label(text="Today's picks:")
entry_message=Label(text="Enter name of the movie you watched:",bg="black",fg="white",padx=40,font=("Cambria",16,"bold"))
entry_message.pack(pady=12)
csv_file_path = "C:\\Users\\Admin\\OneDrive\\Desktop\\movies.csv"
df=pd.read_csv(csv_file_path)
excel="C:\\Users\\Admin\\OneDrive\\Desktop\\movieout.xlsx"
with pd.ExcelWriter('C:\\Users\\Admin\\OneDrive\\Desktop\\movieout.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
wb=openpyxl.load_workbook(excel)
sheet=wb['Sheet1']


entry = tk.Entry(root)
entry.pack(pady=20)

display_button = tk.Button(root, text="Watch Next", command=recommend)
display_button.pack(pady=20)  

display_label = tk.Label(root, text="")
display_label.pack(pady=20)  
    
root.mainloop()


# In[ ]:




