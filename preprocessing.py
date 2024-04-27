#!/usr/bin/env python
# coding: utf-8

# In[92]:


import json
import pandas as pd
import re  # for cleaning text
import nltk
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# In[207]:


df = pd.read_json(r'C:\Users\Thinpad\Desktop\products_data1.json')
df


# In[156]:


df.isnull().sum()


# In[ ]:





# In[12]:


## description , reviews  --> clean 
## nan remove 

## fill nan with knn  -> rating


# In[ ]:





# In[208]:


df['gender'] = df['gender'].replace({'male': 'M', 'Men': 'M', 'female': 'F', 'women': 'F'})
#df


# In[209]:


df['price'] = df['price'].str.replace('$', '').str.replace(',', '.')
df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

# Round to the nearest whole number
df['price'] = df['price'].round().astype(int)

#df


# In[210]:


df['asin'] = df['asin'].apply(lambda x: 0 if x == 'China' else x)
df['asin'] = df['asin'].fillna(0)


# In[211]:


df['brand_name'] = df['brand_name'].str.lower()
df['color_links'] = df['color_links'].str.lower()
df['category'] = df['category'].str.lower()
df['sub_category'] = df['sub_category'].str.lower()


# In[212]:


#df


# In[213]:


mean_rating = df['ratings'].mean()
df['ratings'].fillna(mean_rating, inplace=True)


# In[214]:


#df


# In[215]:


df['color_links'].fillna('nan', inplace=True)
df['sub_category'].fillna('nan', inplace=True)
df['description'].fillna('nan', inplace=True)
df['brand_name'].fillna('nan', inplace=True)


# In[184]:


df


# In[191]:


#df["description"]


# In[134]:


pattern = r'[^a-zA-Z0-9\s]'  # Matches any character that is not a letter or whitespace
# Apply the sub() function to clean the 'text' column
df['description'] = df['description'].apply(lambda x: re.sub(pattern, '', x))
df['reviews'] = df['reviews'].astype(str)
df['reviews'] = df['reviews'].apply(lambda x: re.sub(pattern, '', x))


# In[151]:


nltk.download('stopwords')


# In[146]:


pattern = r'[^a-zA-Z\s]'  # Matches any character that is not a letter or whitespace

# Apply the sub() function to clean the 'text' column
df['description'] = df['description'].apply(lambda x: re.sub(pattern, '', x.lower()))


# In[217]:


lemmatizer = WordNetLemmatizer()

# Define regular expression pattern to match non-alphabetic characters and numbers
pattern = r'[^a-zA-Z\s]'  # Matches any character that is not a letter or whitespace

# Define stop words
stop_words = set(stopwords.words('english'))


# Function to clean and lemmatize text
def clean_text(text):
    if isinstance(text, list):  # Check if text is a list
        cleaned_text = []
        for item in text:
            item = re.sub(pattern, ' ', str(item).lower())  # Remove non-alphabetic characters and convert to lowercase
            item = ' '.join([lemmatizer.lemmatize(word) for word in item.split() if word not in stop_words])  # Lemmatize and remove stop words
            cleaned_text.append(item.strip())  # Strip leading and trailing whitespaces
        return cleaned_text
    else:
        text = re.sub(pattern, ' ', str(text).lower())  # Remove non-alphabetic characters and convert to lowercase
        text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])  # Lemmatize and remove stop words
        return text.strip()  # Strip leading and trailing whitespaces

# Apply the clean_text function to the 'description' and 'reviews' columns
df['description'] = df['description'].apply(clean_text)
df['reviews'] = df['reviews'].apply(clean_text)

# Function to lemmatize text
def lemmatize_text(text):
    if isinstance(text, list):  # Check if text is a list
        lemmatized_texts = []
        for sentence in text:
            lemmatized_tokens = [lemmatizer.lemmatize(token) for token in word_tokenize(sentence)]
            lemmatized_texts.append(' '.join(lemmatized_tokens))
        return lemmatized_texts
    else:
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in word_tokenize(text)]
        return ' '.join(lemmatized_tokens)
    
    

# Apply lemmatization to the 'reviews' column while maintaining its form
df['reviews'] = df['reviews'].apply(lemmatize_text)
df['description'] = df['description'].apply(lemmatize_text)



# In[ ]:





# In[218]:


df


# In[219]:


df.to_csv(r'C:\Users\Thinpad\Desktop\cleaned_data.csv')


# In[192]:


nltk.download('wordnet')


# In[ ]:





# In[220]:


pip install mysqlclient


# In[221]:


pip install pymysql


# In[222]:


pip install mysql-connector-python


# In[233]:


from sqlalchemy import create_engine, Table, Column, Integer, String, Float, ForeignKey, MetaData


# In[248]:


import mysql.connector
from sqlalchemy import create_engine


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="syeda_sql4",
    database="amazon_data"
)

# Create SQLAlchemy engine
engine = create_engine('mysql://root:syeda_sql4@localhost/amazon_data')


# In[239]:


metadata = MetaData()

subcategories_table = Table(
    'subcategories',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True)  # Ensure name is unique
)

# Define products table
products_table = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('subcategory_id', Integer, ForeignKey('subcategories.id')),
    Column('title', String(255)),
    Column('ratings', Float),
    Column('price', Float),
    Column('brand_name', String(255)),
    Column('color_links', String(255)),
    Column('description', String(1000))
)

# Define reviews table
reviews_table = Table(
    'reviews',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('review_text', String(1000))
)

# Create tables
metadata.create_all(engine)

# Insert unique subcategories data into the subcategories table
subcategories_data = df['sub_category'].drop_duplicates().reset_index(drop=True)
subcategories_data.name = 'name'
subcategories_data.to_sql('subcategories', engine, if_exists='append', index=False)

# Insert data into products table
products_data = df[['asin', 'sub_category', 'title', 'ratings', 'price', 'brand_name', 'color_links', 'description']].copy()
products_data.columns = ['id', 'sub_category', 'title', 'ratings', 'price', 'brand_name', 'color_links', 'description']
products_data['subcategory_id'] = products_data['sub_category'].map(subcategories_data.reset_index().set_index('name')['id'])
products_data.drop(columns=['sub_category'], inplace=True)  # Drop the sub_category column as it's now redundant
products_data.to_sql('products', engine, if_exists='append', index=False)

# Insert data into reviews table
reviews_data = df[['asin', 'reviews']].copy()
reviews_data.columns = ['product_id', 'review_text']
reviews_data['product_id'] = reviews_data['product_id'].map(products_data.set_index('id')['id'])
reviews_data.to_sql('reviews', engine, if_exists='append', index=False)


# In[ ]:


import mysql.connector

# Establish connection to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="syeda_sql4",
    database="amazon_data"
)

# Create cursor
cursor = mydb.cursor()

# Iterate over DataFrame rows and insert data into MySQL
for index, row in df.iterrows():
    try:
        # Check if category exists in the database
        cursor.execute("SELECT category_id FROM categories WHERE category = %s", (row['category'],))
        category_result = cursor.fetchone()

        if category_result:
            category_id = category_result[0]
        else:
            # Insert category if not exists
            cursor.execute("INSERT INTO categories (category) VALUES (%s)", (row['category'],))
            category_id = cursor.lastrowid

        # Insert product data into products table
        insert_product_query = """
            INSERT INTO products (URL, title, asin, ratings, price, gender, category_id, sub_category, brand_name, color_links, description, reviews)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        product_values = (
            row['URL'], row['title'], row['asin'], row['ratings'], row['price'],
            row['gender'], category_id, row['sub_category'], row['brand_name'],
            row['color_links'], row['description'], row['reviews']
        )
        cursor.execute(insert_product_query, product_values)
        
        print(f"Inserted data for product with asin: {row['asin']}")
        
    except mysql.connector.Error as err:
        print(f"Error inserting data for product with asin {row['asin']}: {err}")

# Commit changes
mydb.commit()

# Close cursor and database connection
cursor.close()
mydb.close()


# In[ ]:




