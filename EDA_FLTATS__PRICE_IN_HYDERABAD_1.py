#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import requests
from bs4 import BeautifulSoup

import re
import time


# In[2]:


get_ipython().system('pip install bs4 requests')


# In[3]:


URL='https://www.makaan.com/hyderabad-residential-property/buy-property-in-hyderabad-city'


# In[4]:


page = requests.get(URL)


# In[5]:


page.status_code


# In[6]:


page.headers


# In[7]:


page.text


# In[8]:


soup = BeautifulSoup(page.text)
soup


# In[9]:


print(soup.prettify())


# In[10]:


loc=soup.find_all('span',attrs={'itemprop':'addressLocality'})


# In[11]:


location=[]
for i in loc:
    location.append((i).text)
location


# In[12]:


p=soup.find_all('span',attrs={'class':'val','itemprop':'offers'})


# In[13]:


price=[]
for i in p:
    price.append(i.text)
price


# In[14]:


per_sqft=soup.find_all('td',attrs={'class':'lbl rate'})


# In[15]:


price_sqft=[]
for i in per_sqft:
    price_sqft.append(i.text)
price_sqft


# In[16]:


a=soup.find_all('td',attrs={'class':'size'})


# In[17]:


area=[]
for i in a:
    area.append(i.text)
area


# In[18]:


b=soup.find_all('a',attrs={'class':'seller-name'})


# In[19]:


builder=[]
for i in b:
     builder.append(i.text)
builder        


# In[20]:


con_status=soup.find_all('td',attrs={'class':'val'})


# In[21]:


building_status=[]
for i in con_status:
    building_status.append(i.text)
building_status


# In[22]:


flat=[]
h=[]
flat1=soup.find_all('div',class_="title-line")
for i in flat1:
    h.append(i.find("span",class_="val"))
for i in h:
        if i is None:
            flat.append(np.NaN)
        else:
            flat.append(i.text)


# In[23]:


flat


# In[24]:


rera_approved = []
for x in soup.find_all('div', attrs={'class':'infoWrap','itemprop':'event'}):
    rera = x.find('div', attrs={'class': 'rera-tag-new'})
    if rera is None:
        rera_approved.append(False)
    else:
        rera_approved.append(True)
        


# In[25]:


rera_approved


# In[26]:


location=[]
price=[]
price_sqft=[]
area=[]
builder=[]
building_status=[]
flat=[]
rera_approved=[]
unit=[]
for i in range(1,110):
    a='https://www.makaan.com/hyderabad-residential-property/buy-property-in-hyderabad-city?page="+str(i)+"&_=1699869484722S'
    page=requests.get(a)
    soup=BeautifulSoup(page.text)
    for x in soup.findAll('div',attrs={'class':'infoWrap','itemprop':'event'}):
        loc=x.find('span',attrs={'itemprop':'addressLocality'})
        p=x.find('span',attrs={'class':'val','itemprop':'offers'})
        per_sqft=x.find('td',attrs={'class':'lbl rate'})
        a=x.find('td',attrs={'class':'size'})
        b=x.find('a',attrs={'class':'projName'})
        con_status=x.find('td',attrs={'class':'val'})
        flat1=x.find('div',class_="title-line")
        rera = x.find('div', attrs={'class': 'rera-tag-new'})
        un=x.find('span',attrs={'class':'unit'})
        if loc==None:
            location.append(np.NaN)
        else:
            location.append(loc.text)
        if p ==None:
            price.append(np.NaN)
        else:
            price.append(p.text)
        if per_sqft==None:
            price_sqft.append(np.NaN)
        else:
            price_sqft.append(per_sqft.text)
        if a==None:
            area.append(np.NaN)
        else:
            area.append(a.text)
        if b==None:
            builder.append(np.NaN)
        else:
            builder.append(b.text)
        if con_status==None:
            building_status.append(np.NaN)
        else:
            building_status.append(con_status.text)
        if flat1==None:
            flat.append(np.NaN)
        else:
            flat.append(flat1.text)
        if rera==None:
            rera_approved.append(False)
        else:
            rera_approved.append(True)
        if un==None:
            unit.append(np.NaN)
        else:
            unit.append(un.text)
            


# In[27]:


print(len(location))
print(len(price))
print(len(price_sqft))
print(len(area))
print(len(builder))
print(len(building_status))
print(len(flat))
print(len(rera_approved))


# In[28]:


data=pd.DataFrame({'Location':location,'Total_Price':price,'Price_Per_sqft':price_sqft,'Area_sqft':area,'Builder':builder,'Construction_Status':building_status,'BHK':flat,'Rera':rera_approved,'Unit':unit})


# In[29]:


col_order=['Location','Total_Price','Unit','BHK','Price_Per_sqft','Area_sqft','Builder','Construction_Status','Rera']


# In[30]:


data=data[col_order]


# In[31]:


data


# In[32]:


re.findall(r'[0-9] BHK',data['BHK'][0])


# In[33]:


data.rename(columns={'BHK':'Features'},inplace=True)


# In[34]:


data.head()


# In[35]:


data['BHK']=data['Features'].apply(lambda x:"".join(re.findall(r'[0-9]',x)))


# In[36]:


data['BHK']=pd.to_numeric(data['BHK'])


# In[37]:


re.findall(r'(?:Apartment|Villa|Independent House)',data['Features'][19])


# In[38]:


data['PropertyType']=data['Features'].apply(lambda x:"".join(re.findall(r'(?:Apartment|Villa|Independent House|Plot) in',x)))


# In[39]:


data['PropertyType']=data['PropertyType'].apply(lambda x:x[:-3])


# In[40]:


data['Price']=data['Total_Price']+data['Unit']


# In[41]:


data.drop(["Total_Price","Unit","Features"],axis=1,inplace=True)


# In[42]:


data.head()


# # DATA CLEANING

# In[43]:


import pickle
with open('makaan.pkl','wb') as f:
        pickle.dump(data,f)


# In[44]:


with open('makaan.pkl','rb') as f:
    data1=pickle.load(f)


# In[45]:


def extract_price(x):
    if 'Cr' in x:
        return float((re.findall(r'[0-9]{1,2}\.?[0-9]{1,2}',x)[0]))*100
    else:
        return float(re.findall(r'[0-9]{1,2}\.?[0-9]{1,2}',x)[0])


# In[46]:


data['PriceX']=data['Price'].apply(extract_price)


# In[47]:


data.head()


# In[48]:


data["Price_Per_sqft"]=data["Price_Per_sqft"].apply(lambda x: x.split()[0]).str.replace(",","")


# In[49]:


data.head()


# In[50]:


data.drop("Price",axis=1,inplace=True)


# In[51]:


data.head(2)


# In[52]:


data.rename(columns={'PriceX':'Price_in_lakhs'},inplace=True)


# In[53]:


data.head()


# In[54]:


data.isnull().sum()


# In[55]:


data.info()


# In[56]:


data["Price_Per_sqft"]=data["Price_Per_sqft"].apply(lambda x:int(x))


# In[57]:


data["Area_sqft"]=data["Area_sqft"].apply(lambda x:int(x))


# In[58]:


data['BHK']


# In[59]:


data['BHK'].value_counts(dropna=False)


# In[60]:


data['BHK']=data['BHK'].fillna(3)


# In[61]:


data['BHK']=data['BHK'].apply(lambda x:int(x))


# In[62]:


data.info()


# In[63]:


data.describe().T


# # Finding Outliers

# In[64]:


df=data.copy()


# In[65]:


df.describe()


# In[66]:


sns.boxplot(df['BHK'])


# In[67]:


q1=df['BHK'].quantile(0.25)
q3=df['BHK'].quantile(0.75)
iqr=q3-q1


# In[68]:


q1,q3,iqr


# In[69]:


upper_limit=q3+(1.5*iqr)
lower_limit=q1-(1.5*iqr)
lower_limit,upper_limit


# In[70]:


df.loc[(df['BHK']>upper_limit)|(df['BHK']<lower_limit)]


# In[71]:


df_out=df.loc[(df['BHK']<upper_limit)&(df['BHK']>lower_limit)]
print('before removing outliers :',len(df))
print('after removing outliers :',len(df_out))
print('outliers :',len(df)-len(df_out))


# In[72]:


df_out.describe()


# In[73]:


df=df_out.copy()


# In[74]:


df.describe()


# In[75]:


sns.boxplot(df['Price_in_lakhs'])


# In[76]:


q1=df['Price_in_lakhs'].quantile(0.25)
q3=df['Price_in_lakhs'].quantile(0.75)
iqr=q3-q1


# In[77]:


q1,q3,iqr


# In[78]:


upper_limit=q3+(1.5*iqr)
lower_limit=q1-(1.5*iqr)
lower_limit,upper_limit


# In[79]:


df.loc[(df['Price_in_lakhs']>upper_limit)|(df['Price_in_lakhs']<lower_limit)]


# In[80]:


new_df=df.loc[(df['Price_in_lakhs']<upper_limit)&(df['Price_in_lakhs']>lower_limit)]
print('before removing outliers :',len(df))
print('after removing outliers :',len(new_df))
print('outliers :',len(df)-len(new_df))


# In[81]:


df=new_df.copy()


# In[82]:


df.describe()


# In[83]:


df.head()


# # Data visualization and Data Analysis
# # Univariate

# In[84]:


plt.figure(figsize=(3,3))
sns.countplot(x='Construction_Status',data=data)
plt.title("Construction_Status")
plt.xticks(rotation=90)
plt.show()


# In[85]:


plt.figure(figsize=(4,4))
sns.countplot(x='Rera', data=data)
plt.title("RERA approved Builders")
plt.show()


# In[99]:


plt.xlabel('location') 
data['Location'].value_counts()[:5].plot(kind='bar')
plt.title('Top 5 Location')
plt.show()


# In[87]:


fig,axs=plt.subplots(figsize=(16,6),ncols=3)
sns.histplot(x='Area_sqft',data=df,kde=True,ax=axs[0])
sns.histplot(x='Price_in_lakhs',data=df,kde=True,ax=axs[1])
sns.histplot(x='Price_Per_sqft',data=df,kde=True,ax=axs[2])
plt.show()


# # Bivariate

# In[89]:


pd.crosstab(df['Construction_Status'],df['BHK']).plot(kind='bar')
plt.title('Construction Status')
plt.ylabel('Count')
plt.show()


# In[88]:


plt.ylabel('Area_sqft')
df.groupby(by='BHK')['Area_sqft'].mean().plot(kind='bar')
plt.title('Area sqft & BHK')
plt.show()


# In[90]:


df.describe()


# In[100]:


sns.barplot(x='Location', y='Price_in_lakhs', data=df)
plt.title("Location & Price in lakhs")
plt.xticks(rotation = 90)
plt.show()


# In[101]:


df.describe().T


# In[102]:


df.isnull().sum()


# In[95]:


plt.figure(figsize=(4,4))
sns.scatterplot(x = "Area_sqft", y = "Price_in_lakhs", data=df)
plt.title('scatter plot')
plt.show()


# # Multivariate

# In[96]:


#heatmap
data[['Price_in_lakhs','Price_Per_sqft','Area_sqft','BHK']].corr()


# In[97]:


plt.figure(figsize=(5,4)) #need to update title
sns.heatmap(data[['Price_in_lakhs','Price_Per_sqft','Area_sqft','BHK']].corr(), cmap='Reds', annot=True)
plt.title('heatmap plot')
plt.show()


# In[98]:


#plt.figure(figsize=(0,0))
sns.pairplot(data = df, vars=["Price_Per_sqft","Area_sqft","Price_in_lakhs"])
plt.show()


# In[ ]:





# In[ ]:




