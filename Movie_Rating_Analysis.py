#!/usr/bin/env python
# coding: utf-8

# In[12]:


#Exploring on Movie Rating Analysis using Kaggle's dataset of 5000 movies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Loading dataset
movies = pd.read_csv("C:/Users/shema/OneDrive/Desktop/Final_Projects/Movie Analysis/archive/tmdb_5000_movies.csv")
#Viewing first few rows of the movies dataset
movies.head()


# In[4]:


pip install openpyxl


# In[9]:


#All columns, their count,and data types - Column information
movies.info()


# In[10]:


#Statistical Summary of dataset
movies.describe()


# In[27]:


#Columns 
movies.columns


# In[44]:


#Data Cleaning 
#Step-1: Any Missing Data?
falsy_values = (0, False, None, '', [], {})
any(falsy_values)
#No missing data.


# In[37]:


print(movies.info())
print()
#Checking for missing data
print(movies.isnull().sum())
#No missing data


# In[42]:


#Step-2: Cleaning Not Null Values
#for release_date
movies=movies.loc[movies['release_date'].notnull()] 
print(movies.info())
#Checking for any null values in release_date
print()
print(movies.isnull().sum())


# In[45]:


#for tagline
#filling the tagline null values with movies' titles
movies['tagline'] = movies['tagline'].fillna(movies['title'])
print(movies.info())
print()
print(movies.isnull().sum())


# In[46]:


#for overview 
movies=movies.loc[movies['overview'].notnull()] 
print(movies.info())
print()
print(movies.isnull().sum())


# In[6]:


#for homepage
#dropping down this column as not all movies can have a homepage, and it is not significantly important
movies.drop('homepage', axis=1, inplace=True)
print(movies.info())
print()
print(movies.isnull().sum())


# In[7]:


#loading another dataset, Credits
#credits = pd.read_csv("C:/Users/shema/OneDrive/Desktop/Final_Projects/Movie Analysis/archive/tmdb_5000_credits.csv")
#credits.info()


# In[9]:


movies['release_date']


# In[11]:


#changing the dtype of release_date from object to date format
movies['release_date']=pd.to_datetime(movies['release_date'])
movies['release_date']


# In[12]:


print(f"Movies dataset shape: {movies.shape}")
print(f"Credits dataset shape: {credits.shape}")


# In[14]:


#Understanding Rating Distribution
plt.figure(figsize=(8, 5))
sns.histplot(movies['vote_average'], bins=20, kde=True)
plt.title("Distribution of Movie Ratings")
plt.xlabel("Vote Average")
plt.ylabel("Number of Movies")
plt.show()


# In[15]:


#from the distribution, are there any outliers? 
#Yes
#most ratings are in between the 6-7 range
#understanding the vote count
movies['vote_count']


# In[18]:


#To avoid "fake high scores" from movies with very few votes, filter the data
#popular movies has a vote_count above 500
popular_movies = movies[movies['vote_count'] > 500]  
#finding the rating of popular movies
top_rated = popular_movies.sort_values('vote_average', ascending=False)
#display first 100 rows of the popular movies along with their titles, vote_average and vote_count
top_rated[['title', 'vote_average', 'vote_count']].head(100)


# In[21]:


#understanding the genre column
#movies['genres'].head(10)


# In[22]:


#there are multiple genres for each movie
#so, it can be split for better analyis of data
#splitting the genres
#movies['genres_split'] = movies['genres'].str.split()


# In[28]:


#explode the data, i.e, make sure that each row has one genre only
#explodedMovieData = movies.explode('genres_split')
#explodedMovieData['genres_split'].head(10)


# In[26]:


#now group by genres
#and find the average rating by genre
#avg_rating_by_genre = explodedMovieData.groupby('genres_split')['vote_average'].mean().sort_values(ascending=False)
#avg_rating_by_genre.plot(kind='bar', figsize=(10, 5), title='Average Rating by Genre',color='orange')
#plt.ylabel('Average Vote')
#plt.xlabel('Genre')
#plt.xticks(rotation=80)
#plt.show()


# In[ ]:


#just realised - the genre values are in JSON string format 


# In[8]:


#Check for missing data
#credits.isnull().sum()


# In[35]:


#converting release year to year
movies['release_year'] = pd.DatetimeIndex(movies['release_date']).year
#groupby release year and vote_average and find their mean
avg_rating_by_year = movies.groupby('release_year')['vote_average'].mean()
#plot the average rating over the years with the help of avg_rating_by_year's index and values
plt.figure(figsize=(10, 5))
sns.lineplot(x=avg_rating_by_year.index, y=avg_rating_by_year.values)
plt.title("Average Rating Over the Years")
plt.xlabel("Year")
plt.ylabel("Average Rating")
plt.show()


# In[39]:


#from the plot, the ratings have been decreasing over a long period of time (from 1970s to 2018)
#and then it spikes up towards 2020


# In[8]:


#Analysing budget and rating relation
moviesClean = movies.dropna(subset=['budget', 'vote_average'])

plt.figure(figsize=(10, 6))
plt.scatter(moviesClean['budget'], moviesClean['vote_average'], alpha=0.5, color='teal')

plt.title('Budget vs Movie Rating', fontsize=16)
plt.xlabel('Budget (in USD)', fontsize=12)
plt.ylabel('Vote Average (Rating)', fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()


# In[22]:


#Analysing movie runtime 
movies.plot.scatter(x='runtime',y='vote_average', color='yellow')
plt.title('Vote Average vs Movie Runtime')


# In[ ]:


#from the above scatter plot, we can conclude the following - 
#1. average movie length = 80-100 minutes
#2. As the runtime increases the average vote also increases


# In[30]:


plt.scatter(movies['vote_count'], movies['vote_average'], alpha=0.4, color='green')
# Helpful due to wide range
plt.xscale('log')  
plt.xlabel('vote count')
plt.ylabel('vote average')
plt.title('Vote Count vs Vote Average')


# In[ ]:


#from scatter plot, we can conclude that 
#The vote count and vote average are strongly related to each other.


# In[40]:


#to understand revenue trends
movies['release_year'] = pd.to_datetime(movies['release_date'], errors='coerce').dt.year
movies.groupby('release_year')['revenue'].mean().plot()


# In[50]:


#understanding language distribution
langDistributionCount = movies['original_language'].value_counts()
#print(langDistributionCount)

#to have a readable chart, show only top few languages, and rest as "others"
topLanguages = langDistributionCount.head(6)
otherLanguages = langDistributionCount[6:].sum()
#combine into a single Series
langDistribution = topLanguages.append(pd.Series({'Others': otherLanguages}))

plt.figure(figsize=(8,8))
plt.pie(langDistribution.values, labels=langDistribution.index, autopct='%1.1f%%')
#autopct shows percentages inside pie portions

plt.axis('equal')  
#keeps the pie chart circular


# In[36]:


movies[['budget', 'revenue', 'vote_average', 'vote_count', 'runtime']].corr()

plt.figure(figsize=(8,6))
sns.heatmap(movies.corr(), annot=True, cmap='coolwarm')

