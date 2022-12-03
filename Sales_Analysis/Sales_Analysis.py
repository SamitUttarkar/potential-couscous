#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns


# #### Merging 12 months of sales data into single CSV file

# In[2]:


df = pd.read_csv('Sales_data/Sales_April_2019.csv')
files = [file for file in os.listdir('Sales_Data')]
all_months_data = pd.DataFrame()
for file in files:
    #print(file)
    df = pd.read_csv('Sales_Data/'+file)
    
    all_months_data = pd.concat([all_months_data,df])
all_months_data.to_csv('all_data.csv',index = False)


# In[3]:


df.head()


# In[4]:


all_data = pd.read_csv('all_data.csv')
all_data.head()


# ## Cleaning Data

# In[5]:


nan_df = all_data[all_data.isna().any(axis = 1)]
nan_df.head()


# In[6]:


all_data = all_data.dropna(how = 'all')


# In[7]:


all_data.isnull().values.any()


# In[8]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']


# In[9]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()
# we use inplace = true becase we don't need to assing it to a new variable again 


# ### Converting str to int

# In[10]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])


# In[11]:


all_data['Sales'] = all_data['Quantity Ordered']* all_data['Price Each']


# In[12]:


all_data.head()


# #### What was the best month for sales? How much was earned thatt month?

# In[13]:


new_sales = all_data.groupby('Month').sum()
new_sales = new_sales.reset_index() # imoprtant to plot 


# In[14]:


new_sales


# In[15]:


months = range(1,13)
plt.bar(months, new_sales['Sales'])
plt


# In[16]:


all_data.groupby('Month')['Sales'].sum().plot(kind = 'bar')


# In[17]:


sns.barplot(x="Month",
           y="Sales",
           data=new_sales)


# ### What US City has to higest sales 

# In[18]:


# let's use the .apply() method 
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]
all_data['City'] = all_data['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})") #lambda x:x.split(',')[1
all_data.head()


# In[19]:


city_sales = all_data.groupby('City')['Sales'].sum()
city_sales = city_sales.reset_index()


# In[20]:


g = sns.barplot(x = city_sales['City'], y = city_sales['Sales'] ,data = city_sales)
g.set_xticklabels(g.get_xticklabels(), rotation=30)


# In[21]:


all_data.groupby('City')['Sales'].sum().plot(kind = 'bar')


# In[22]:


plt.bar(city_sales['City'],city_sales['Sales'])
plt.xticks(rotation = 80)
plt.show()


# ### What time should we display advertisements to maximize likelihood of customer's buying product ?

# In[23]:


#using date_time library cause it will help us get differnt types of date and times 
all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[24]:


#all_data.drop(columns = 'Column', inplace = True)
all_data.head()


# In[25]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data.head()


# In[26]:


by_hour = all_data.groupby('Hour')['Sales'].sum()
by_hour = by_hour.reset_index()


# In[27]:


sns.lineplot(x = by_hour['Hour'], y = by_hour['Sales'])


# In[28]:


plt.plot(by_hour['Hour'], by_hour['Sales'],linewidth=3.0)
plt.xticks(by_hour['Hour'])
plt.grid()
plt.show()


# In[29]:


s = 0
for i in all_data.duplicated():
    if i == True:
       s += 1
print(s)

        


# ### Which products are sold the most ?

# In[48]:


df = all_data[all_data['Order ID'].duplicated(keep = False)]


# In[49]:


df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x:',' .join(x))
df.head()


# In[50]:


df = df[['Order ID','Grouped']].drop_duplicates()


# In[51]:


df.head()


# In[56]:


prod_data = all_data.groupby('Product')['Quantity Ordered'].sum()
prod_data = prod_data.reset_index()


# In[60]:


prices = all_data.groupby('Product').mean()['Price Each']
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(prod_data['Product'],prod_data['Quantity Ordered'], color = 'g')
ax2.plot(prod_data['Product'],prices,'b-')
ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color = 'g')
ax2.set_ylabel('Price',color = 'b')
ax1.set_xticklabels(prod_data['Product'],rotation = 90,size = 8)
plt.show()


# In[ ]:




