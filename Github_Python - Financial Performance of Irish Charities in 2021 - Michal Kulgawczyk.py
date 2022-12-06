#!/usr/bin/env python
# coding: utf-8

# # Financial Performance of Irish Charities in 2021 
# 
# Data has been sourced from DATA.GOV.IE
# 
# Direct link to the data source: [Register of Charities in Ireland](https://data.gov.ie/dataset/register-of-charities-in-ireland?package_type=dataset)
# 
# Number of files: 2;   Format: CSV
# 
# File 1: "Register of Charities in Ireland"
# 
# File 2: "Annual Reports filed with the Charities Regulator"
# 
# Description: This data set is listing details of registered and de-registered charities in Ireland. Information is also provided on all annual reports submitted to the Charities Regulator. 
# 
# <img src=https://data.gov.ie/img/dgi-logo-new.png width = 200> 
# 

# ## Table of Content
# 
# 1. [Part 1](#Part_1)
#     2. [Importing File 1 - "Register of Charities in Ireland"](#Importing_File_1)
#     3. [Initial cleaning of File 1](#clean_file1)
#     4. [Importing File 2 - "Annual Reports filed with the Charities Regulator"](#import_file2)
#     5. [Initial cleaning of File 2](#clean_file2)
#     6. [Merging two datasets: File_1 & File_2](#merge)
# 2. [Part 2](#Part_2)
#     1. [Data Exploration](#explore)
#     
# 3. [Part 3](#Part_3)
#     1. [Data Analysis - Top Questions:](#analysis)
#         1. [What is Total Gross Income for all charities in 2021?](#q1)
#         2. [Top 5 charities with the highest Total Gross Income in 2021?](#q2)
#         3. [Top 5 charities with the highest Total Gross Expenditure in 2021?](#q3)
#         4. [Top 5 charities with the highest Total Net Income in 2021?](#q4)
#         5. [Top 5 charities with the lowest Total Net Income in 2021?](#q5)
#         6. [How many charities did not have any gross income in 2021?](#q6)
#         7. [Top 5 charities with the highest donations in 2021?](#q7)
#         8. [Top 5 Beneficiars and the amount of funds dedicted to support them in 2021?](#q8)
#         9. [Top 5 charities based on their main purpose in 2021?](#q9)
#         10. [Top 5 charities based on their governing form in 2021?](#q10)
#         11. [Total Gross Income - identifying outliers based on IQR (Interquartile Range)](#q11)
#         12. [What are the incomes and spendings based on the country where the charity was established?](#q12)
# 
#     

# <a id ='Part_1'></a>
# ## Part 1 
# 
# Let's start from installing and importing the necessary Python modules for this exercise.
# 
# `pip install pandas
#  pip install matplotlib
#  pip install numpy
#  pip install seaborn
# `

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# <a id ='Importing_File_1'></a>
# ### Importing File 1 - "Register of Charities in Ireland"

# In case of the following error:"urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed", please try the following option: 
# 
# - Create unverified https context in SSL:
# 
#     `import ssl`
# 
#     `ssl._create_default_https_context = ssl._create_unverified_context` This tip was sourced from: <a href="https://www.howtouselinux.com/post/ssl-certificate_verify_failed-in-python">Howtouselinux.com</a>
# 
# Please note:
# 
# - read_csv command takes an encoding option to deal with files in different formats. 
# Due to an initial error during loading the file: "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3496: invalid continuation byte", I decided to add: encoding = "ISO-8859-1". 
# This tip was sourced from: <a href="https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python">Stackoverflow.com</a>
# 

# In[2]:


import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# In[3]:


url="https://www.charitiesregulator.ie/media/1663/register-of-charities.csv"
file_1 = pd.read_csv(url, 
                 encoding = "ISO-8859-1")
file_1.head()


# <a id ='clean_file1'></a>
# ### Initial cleaning of the File 1
# 
# As we can see, there is a blank row on the top of the file. There is also an empty column called "Unnamed 10" which is not a part of original dataset. 
# 
# 
# 
# - To skip the first empty row in the file, we will use index position: **skiprows=[0]**. This tip was sourced from:
# <a href="https://linuxhint.com/skip-header-row-csv-python/#:~:text=Line%201%3A%20We%20import%20the%20Pandas%20library%20as%20a%20pd,output%20without%20the%20header%20row">Linuxhint.com</a>
# 
# 
# - To skip the last empty column, we will use: **usecols=range(0,10)** and say to Python that we are only intersted in the first 10 columns. 
# 
# 
# Ok, let's import the file 1 once again and check what it contains.
# 

# In[4]:


url="https://www.charitiesregulator.ie/media/1663/register-of-charities.csv"
file_1 = pd.read_csv(url, 
                 encoding = "ISO-8859-1", 
                 skiprows=[0], 
                 usecols=range(0,10))
file_1.head()


# The file 1 has been uploaded. We have also received an info regarding mixed types of the columns and recommendation that the dtype option should specified. 
# 
# Let's review all variables and their types:

# In[5]:


file_1.dtypes


# In[6]:


file_1.info()


# In[7]:


file_1['Registered Charity Number'].dtype


# The first column is shown as type float64 and remaining 9 columns as type object. By reviewing the columns and their content, we can notice that they are all type "string" .
# 
# Let's convert all the columns in the File 1 to type "string".

# In[8]:


file_1 = file_1.astype({'Registered Charity Number':'string','Registered Charity Name':'string',
                'Status':'string','Also Known As':'string',
                'Primary Address':'string','Governing Form':'string',
                'CRO Number':'string','Country Established':'string',
                'Charitable Purpose':'string','Charitable Objects':'string'})
file_1.dtypes


# Let's check the first value from the column 1 and confirm if that is trully type "string".

# In[9]:


file_1['Registered Charity Number'].dtype


# In[10]:


(file_1['Registered Charity Number'].eq('20136598.0')).any()


# In[11]:


file_1.info()


# In[12]:


file_1.head()


# The first column "Registered Charity Number" contains ".0" at the of each value. 
# 
# Let's remove that part by using "replace" method:

# In[13]:


file_1['Registered Charity Number'] = file_1['Registered Charity Number'].astype('string').replace('\.0', '', regex=True)


# In[14]:


file_1.head()


# In[15]:


file_1['Registered Charity Number']


# Let's look at the statistics on the file 1:

# In[16]:


file_1.describe(include="all")


# File 1 has 13877 rows, however when we checked, individual column ```file_1['Registered Charity Number']```, we were informed that the lenght of the column was "1048574. It looks like we have many rows with NA values. 
# 
# Let's confirmed that by checking the second column:

# In[17]:


file_1[['Registered Charity Number','Registered Charity Name']]


# OK, it is time to remove all those empty rows to ensure that we only deal with our original 13887 rows. 
# 
#  ```drop_duplicates()```method, helps remove all rows where all data across columns is exactly the same.

# In[18]:


file_1 = file_1.drop_duplicates()
file_1[['Registered Charity Number','Registered Charity Name']]


# Let's check the number of missing values for each column:

# In[19]:


file_1.isna().sum()


# Every single column has a missing value. Let's check those columns individually and remove missing values.

# In[20]:


missing_value = pd.isnull(file_1['Registered Charity Number'])
file_1[missing_value]


# It looks like that the entire row in the first column ```Registered Charity Number``` has NA values.
# 
# Let's remove rows in file_1 which contains all NA values.

# In[21]:


file_1.dropna(axis = 0, how = 'all', inplace = True)


# Results after dropping all rows filled with NA values only:

# In[22]:


file_1.isna().sum()


# We still have 4 columns contaning missing values. Let's check them and remove those values.

# In[23]:


missing_value = pd.isnull(file_1['Primary Address'])
file_1[missing_value]


# In[24]:


file_1["Primary Address"].fillna("", inplace = True)


# In[25]:


missing_value = pd.isnull(file_1['CRO Number'])
file_1[missing_value]


# In[26]:


file_1["CRO Number"].fillna("", inplace = True)


# In[27]:


missing_value = pd.isnull(file_1['Charitable Purpose'])
file_1[missing_value]


# In[28]:


file_1["Charitable Purpose"].fillna("", inplace = True)


# In[29]:


missing_value = pd.isnull(file_1['Charitable Objects'])
file_1[missing_value]


# In[30]:


file_1["Charitable Objects"].fillna("", inplace = True)


# In[31]:


file_1.isna().sum()


# All the missing values in the file_1 has been removed or replaced by blank space.

# Let's see the data:

# In[32]:


file_1.head()


# In[33]:


file_1.info()


# In[34]:


file_1.describe()


# We will clean column ```Country Established``` and rename all columns containing data for Ireland but using other names than "Ireland", for example: 'Republic of Ireland'.
# 
# Let's find unique values in ```Country Established```

# In[35]:


file_1['Country Established'].unique()


# Let's rename all values standing for 'Ireland': ```'Republic of Ireland', 'Republic Of Ireland', 'Poblacht na hÉireann'``` and change their names to ```Ireland```

# In[36]:


file_1['Country Established'] = file_1['Country Established'].replace(['Republic of Ireland', 'Republic Of Ireland', 'Poblacht na hÉireann'], 'Ireland')


# In[37]:


file_1['Country Established'].unique()


# Done: file_1 looks good.
# 
# It is time to import file_2.

# <a id ='import_file2'></a>
# 
# ### Importing File 2 - "Annual Reports filed with the Charities Regulator"

# In[38]:


url="https://www.charitiesregulator.ie/media/1664/charity-annual-reports.csv"
file_2 = pd.read_csv(url, 
                 encoding = "ISO-8859-1")
file_2.head()


# In[39]:


file_2.info()


# <a id ='clean_file2'></a>
# ### Initial cleaning of the File 2
# 
# Similarly to the File 1, there is also a blank row on the top of the File 2. There are also two empty columns at the end of the data set: "Unnamed 19" and "Unnamed 20" which are not the part of original dataset. In addition the last 3 columns will not be needed for our financial analysis, therefore they will also be removed from the File_2 dataset. 
# 
# 
# 
# - To skip the first empty row in the file, we will use index position: **skiprows=[0]**. This tip was sourced from:
# <a href="https://linuxhint.com/skip-header-row-csv-python/#:~:text=Line%201%3A%20We%20import%20the%20Pandas%20library%20as%20a%20pd,output%20without%20the%20header%20row">Linuxhint.com</a>
# 
# 
# - To remove five last columns(including 2 empty columns), we will use: **usecols=range(0,16)** and say to Python that we are only intersted in the first 16 columns. 
# 
# 
# Ok, let's import the File 2 once again and check what it contains.

# In[40]:


url="https://www.charitiesregulator.ie/media/1664/charity-annual-reports.csv"
file_2 = pd.read_csv(url, 
                 encoding = "ISO-8859-1", 
                 skiprows=[0], 
                 usecols=range(0,16))
file_2.head()


# The 1st column named "Registered\nCharity\nNumber" in the File2 will be use as a "merge column" to join the File 1.
# 
# Unfortunately the name of the column does not match its coresponding column in the File 1 and need to be changed.
# 
# We will also rename columns containing the new line character "\n"

# In[41]:


file_2.rename(columns={'Registered\nCharity\nNumber': 'Registered Charity Number',
                      'Period\nStart Date': 'Period Start Date',
                      'Period\nEnd Date': 'Period End Date'}, inplace = True)


# Let's review all variables and their types:

# In[42]:


file_2.info()


# The first column is shown as type int64  and the remaining 9 columns as type object. 
# 
# Let's convert all the columns in File 2 to their appropriate type.

# In[43]:


file_2 = file_2.astype({'Registered Charity Number':'string','Registered Charity Name':'string',
                        'Report Activity':'string',
                        'Activity Description':'string','Beneficiaries':'string'})


# In[44]:


file_2["Period Start Date"] =  pd.to_datetime(file_2["Period Start Date"], format="%d/%m/%Y")


# In[45]:


file_2["Period End Date"] =  pd.to_datetime(file_2["Period End Date"], format="%d/%m/%Y")


# In[46]:


file_2.info()


# We still have 8 columns which correspond to financial data that should be converted to type float. All those columns had in their orignal CSV file, a symbol standing for Euro currency "€". That symbol was imported to our file_2 as unknown character and it needs to be removed.
# 
# Let's remove all unknown characters, printed instead "€" symbol. This tip was sourced from: [https://www.statology.org/](https://www.statology.org/pandas-remove-special-characters/)

# In[47]:


file_2['Financial: Income from Central Government or Local Authorities'] = file_2['Financial: Income from Central Government or Local Authorities'].str.replace('\W', '', regex=True)
file_2['Financial: Income from other public bodies'] = file_2['Financial: Income from other public bodies'].str.replace('\W', '', regex=True)
file_2['Financial: Income from philantrophic organisations'] = file_2['Financial: Income from philantrophic organisations'].str.replace('\W', '', regex=True)
file_2['Financial: Income from donations'] = file_2['Financial: Income from donations'].str.replace('\W', '', regex=True)
file_2['Financial: Income from trading and commercial activities'] = file_2['Financial: Income from trading and commercial activities'].str.replace('\W', '', regex=True)
file_2['Financial: Income from other sources'] = file_2['Financial: Income from other sources'].str.replace('\W', '', regex=True)
file_2['Financial: Gross Income'] = file_2['Financial: Gross Income'].str.replace('\W', '', regex=True)
file_2['Financial: Gross Expenditure'] = file_2['Financial: Gross Expenditure'].str.replace('\W', '', regex=True)


# In[48]:


file_2.head()


# Last 8 columns related to financials are currently shown as objects and they need to be converted to floats. 

# In[49]:


file_2 = file_2.astype({'Financial: Income from Central Government or Local Authorities':float,
                        'Financial: Income from other public bodies':float,
                        'Financial: Income from philantrophic organisations':float,
                        'Financial: Income from donations':float,
                        'Financial: Income from trading and commercial activities':float,
                        'Financial: Income from other sources':float,
                        'Financial: Gross Income':float,
                        'Financial: Gross Expenditure':float})


# In[50]:


file_2.info()


# Let's check the number of missing values for each column:

# In[51]:


file_2.isna().sum()


# In[52]:


file_2.isna().sum().reset_index(name="n").plot.bar(x='index', y='n', rot=90)


# Missing values - proportion per column:

# In[53]:


plt.figure(figsize=(10,6))
sns.displot(
    data=file_2.isna().melt(value_name="missing values"),
    y="variable",
    hue="missing values",
    multiple="fill",
    aspect=1.50
)
plt.savefig("visualizing_missing_data_with_barplot_Seaborn_distplot.png", dpi=100)


# Let's also look at NaN missing values populated in one of the financial columns and confirm if they are really missing values by using ```isnull()``` method. 

# In[54]:


file_2['Financial: Gross Income']


# In[55]:


file_2['Financial: Gross Income'].isnull()


# Yes, one 'NaN' value is the missing values - the 3rd value boolean response is ```True``` corresponding to NaN value, while the first 2 responses are ```False``` which correspond to numerical values.
# 
# NaN values will be replaced with 0.

# In[56]:


file_2[['Financial: Income from Central Government or Local Authorities',
                        'Financial: Income from other public bodies',
                        'Financial: Income from philantrophic organisations',
                        'Financial: Income from donations',
                        'Financial: Income from trading and commercial activities',
                        'Financial: Income from other sources',
                        'Financial: Gross Income',
                        'Financial: Gross Expenditure']] = file_2[['Financial: Income from Central Government or Local Authorities',
                        'Financial: Income from other public bodies',
                        'Financial: Income from philantrophic organisations',
                        'Financial: Income from donations',
                        'Financial: Income from trading and commercial activities',
                        'Financial: Income from other sources',
                        'Financial: Gross Income',
                        'Financial: Gross Expenditure']].fillna(0)


# Let's format float values and add comma separators by default. 
# 
# In addition, to make all large values nice and easy to read, we will remove decimal points. 
# 
# Finally, we will add '€' symbol to all float values.
# 
# This tip was sourced from: [https://stackoverflow.com/](https://stackoverflow.com/questions/43102734/format-a-number-with-commas-to-separate-thousands)

# In[57]:


pd.options.display.float_format = '€{:,.0f}'.format


# In[58]:


file_2.head()


# One of our goals is to review charities financials only for year 2021.
# 
# File_2 currently contains financial data since 2014. That is recorderd on 50793 rows. 
# 
# Before we merge our tables, let's filter file_2 and only retrieve data for the year 2021.

# In[59]:


file_2 = file_2.loc[(file_2['Period Start Date'] == '2021-01-01')
                     & (file_2['Period End Date'] == '2021-12-31')]
file_2


# We have retrieved 3340 rows. That is significant difference in comparison to 50593 rows previously received and it will definitly improve performance of further queries.  
# 

# In[60]:


file_2.info()


# <a id ='merge'></a>
# ### Merging two datasets: File_1 & File_2
# 
# Please note, file_1 will be merged with the filtered ```file_2_2021```.
# 
# We will use ```Registered Charity Number``` column to merge two datasets. 
# We will also merge the datasets using right join, to ensure that we do not miss any financials from 2021. 
# 
# 

# In[61]:


file_3 = pd.merge(file_1, file_2, on='Registered Charity Number', how='right')
file_3.head()


# In[62]:


file_3.info()


# ```Registered Charity Name``` (x & y) columns were located in both datasets (file_1 and file_2), therefore they have been populated in file_3 twice. Let's delete ```Registered Charity Name_y``` from file_3 and change ```Registered Charity Name_x``` column's name to ```Registered Charity Name```.
# 
# Finally, we will shorten the name of columns containing financial data.

# In[63]:


file_3.rename(columns={'Registered Charity Name_x':'Registered Charity Name',
                       'Financial: Income from Central Government or Local Authorities':'Income: Central_Gov Local_Auth',
                        'Financial: Income from other public bodies':'Income: Other Public Bodies',
                        'Financial: Income from philantrophic organisations':'Income: Philantrophic Orgs',
                        'Financial: Income from donations':'Income: Donations',
                        'Financial: Income from trading and commercial activities':'Income: Trading & Commercial',
                        'Financial: Income from other sources':'Income: Other Sources',
                        'Financial: Gross Income':'Total Gross Income',
                        'Financial: Gross Expenditure':'Total Gross Expenditure'}, inplace = True)


# In[64]:


del file_3['Registered Charity Name_y']


# In[65]:


#file_3 = file_3.rename(columns={'Registered Charity Name_x':'Registered Charity Name'})


# In[66]:


file_3.info()


# <a id ='Part_2'></a>
# ## Part 2
# <a id ='explore'></a>
# ### Data Exploration
# 

# Check a type of the file that will be explored:

# In[67]:


type(file_3)


# In[68]:


type(file_3['Registered Charity Name'])


# Let's look at the top and the bottom of data:

# In[69]:


file_3.head()


# In[70]:


file_3.tail()


# Let's check the size of the file_3:

# In[71]:


file_3.shape


# In[72]:


file_3.count()


# There are 24 columns and 3340rows.
# 

# Let's see how the data is displayed for all the columns presenting the financial results only:

# In[73]:


file_3.iloc[0:10, 16:24]


# Let's check the totals for each financial data: 

# In[74]:


total = file_3.iloc[:,16:24].sum()
total


# Description of the data in file_3:

# In[75]:


file_3.describe()


# Let's visualise all financial data using boxplot. 
# 
# To make it easier to review, 8 columns coresponding to financial information will be stored in a new dataframe: ```financials```

# In[76]:


import numpy as np,pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
financials = pd.DataFrame(file_3, columns=['Income: Central_Gov Local_Auth',
                                           'Income: Other Public Bodies',
                                           'Income: Philantrophic Orgs',
                                           'Income: Donations',
                                           'Income: Trading & Commercial',
                                           'Income: Other Sources',
                                           'Total Gross Income',
                                           'Total Gross Expenditure'])


# In[77]:


financials.info()


# In[78]:


plt.boxplot(financials)
plt.show()


# We can see that 3 variables have highly visible outliers:
# 
# - Income: Central_Gov Local_Auth
# - Total Gross Income
# - Total Gross Expenditure

# Let's look at all financial variables and check their distributions:

# In[79]:


plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.boxplot(file_3['Income: Central_Gov Local_Auth'])
plt.subplot(2,2,2)
sns.boxplot(file_3['Income: Other Public Bodies'])
plt.subplot(2,2,3)
sns.boxplot(file_3['Income: Philantrophic Orgs'])
plt.subplot(2,2,4)
sns.boxplot(file_3['Income: Donations'])
plt.show()


# In[ ]:





# In[80]:


plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.boxplot(file_3['Income: Trading & Commercial'])
plt.subplot(2,2,2)
sns.boxplot(file_3['Income: Other Sources'])
plt.subplot(2,2,3)
sns.boxplot(file_3['Total Gross Income'])
plt.subplot(2,2,4)
sns.boxplot(file_3['Total Gross Expenditure'])
plt.show()


# In[81]:


file_3.describe(include=[np.number]).T


# We can see that every single financial variable has values outside the whiskers of the plot, significantly distant from the rest of the data. 
# 
# Those values represent outliers.

# <a id ='Part_3'></a>
# <a id ='analysis'></a>
# ## Part 3
# 
# ### Data Analysis

# #### Top Questions:
# 1. [What is Total Gross Income for all charities in 2021?](#q1)
# 2. [Top 5 charities with the highest Total Gross Income in 2021?](#q2)
# 3. [Top 5 charities with the highest Total Gross Expenditure in 2021?](#q3)
# 4. [Top 5 charities with the highest Total Net Income in 2021?](#q4)
# 5. [Top 5 charities with the lowest Total Net Income in 2021?](#q5)
# 6. [How many charities did not have any gross income in 2021?](#q6)
# 7. [Top 5 charities with the highest donations in 2021?](#q7)
# 8. [Top 5 Beneficiars and the amount of funds dedicted to support them in 2021?](#q8)
# 9. [Top 5 charities based on their main purpose in 2021?](#q9)
# 10. [Top 5 charities based on their governing form in 2021?](#q10)
# 11. [Total Gross Income - identifying outliers based on IQR (Interquartile Range)](#q11)
# 12. [What are the incomes and spendings based on the country where charity was established?](#q12)

# <a id ='q1'></a>
# #### 1. What is Total Gross Income for all charities in 2021?

# In[82]:


Total_Gross_Income = total = file_3['Total Gross Income'].sum()
Total_Gross_Income


# <a id ='q2'></a>
# #### 2. Top 5 charities with the highest Total Gross Income in 2021?

# In[83]:


file_3.nlargest(n=5, columns=['Total Gross Income'])


# Top 5 charities with the highest ```Total Gross Income``` earned more than half a billion euros.
# 
# Let's query if there are any more charities with ```Total Gross Income``` over half a billion euros.

# In[84]:


half_billion = file_3.query("`Total Gross Income` >= 500000000")
half_billion.head()


# Top 5 charities in Ireland are aslo only charities with ```Total Gross Income``` above half a billion Euros in 2021.
# 
# HSE(Health Service Executive) is on the top of the list with over €22 billions of the ```Total Gross Income```and it is followed by HEA(Higher Education Authority) with over €20 billions less in the ```Total Gross Income``` - €1,880,530,000, that is very significant difference.
# 
# HSE clearly looks like an outlier among other charities based on ```Total Gross Income```

# <a id ='q3'></a>
# #### 3. Top 5 charities with the highest Total Gross Expenditure in 2021?

# In[85]:


file_3.nlargest(n=5, columns=['Total Gross Expenditure'])


# <a id ='q4'></a>
# #### 4. Top 5 charities with the highest Total Net Income in 2021?

# As we do not have a column ```Total Net Income```, we will need to create it by subtracting ```Total Gross Expenditure``` from ```Total Gross Income```

# In[86]:


file_3['Total Net Income']= file_3['Total Gross Income'] - file_3['Total Gross Expenditure']


# In[87]:


file_3.nlargest(n=5, columns=['Total Net Income'])


# <a id ='q5'></a>
# #### 5. Top 5 charities with the lowest Total Net Income in 2021?

# In[88]:


file_3.nsmallest(n=5, columns=['Total Net Income'])


# HSE had over €240 milsions of net loss in 2021.

# <a id ='q6'></a>
# #### 6. How many charities did not have any gross income in 2021?

# In[89]:


count = (file_3['Total Gross Income'] == 0).sum()
count


# <a id ='q7'></a>
# #### 7. Top 5 charities with the highest donations in 2021?

# In[90]:


file_3.nlargest(n=5, columns=['Income: Donations'])


# Concern Worldwide is the most popular in terms of donations in Ireland.

# <a id ='q8'></a>
# #### 8. Top 5 Beneficiars and the funds dedicted to support them (Total Gross Expenditure)

# Column ```Beneficiaries```contains several values(responses) in one field seperated by ';'.
# 
# The first value (response) in the filed will be retrieved and used as a main value for that field. We will call it ```Lead Beneficiary```. That will help us further analyse top beneficiaries. 

# In[91]:


file_3['Lead Beneficiary'] = file_3['Beneficiaries'].str.split(';').str[0]


# In[92]:


file_3


# Let's count top 10 beneficiaries:

# In[93]:


top_beneficiaries_count = file_3.groupby(['Lead Beneficiary']).agg({'Total Gross Expenditure': 'count'}).nlargest(n=5, columns=['Total Gross Expenditure'])


# In[94]:


top_beneficiaries_count


# In[95]:


file_3['Lead Beneficiary'].value_counts()


# Let's check top 10 beneficiaries and the funds dedicted to support them in 2021

# In[96]:


top_beneficiaries_amount = file_3.groupby(['Lead Beneficiary']).agg({'Total Gross Expenditure': 'sum'}).nlargest(n=5, columns=['Total Gross Expenditure'])


# In[97]:


top_beneficiaries_amount


# <a id ='q9'></a>
# #### 9. Top 5 charities based on their main purpose in 2021

# Similarly to column ```Beneficiaries```, column ```Charitable Purpose```contains several values(responses) in one field seperated by ';'.
# 
# The first value (response) in the filed will be retrieved and used as a main value for that field. We will call it ```Charity Purpose```. That will help us further analyse that field. 

# In[98]:


file_3['Charity Purpose'] = file_3['Charitable Purpose'].str.split(';').str[0]


# In[99]:


file_3


# Let's count top 5 charity purposes:

# In[100]:


top_purpose_count = file_3.groupby(['Charity Purpose']).agg({'Total Gross Expenditure': 'count'}).nlargest(n=5, columns=['Total Gross Expenditure'])


# In[101]:


top_purpose_count


# In[102]:


file_3['Charity Purpose'].value_counts()


# Let's check top 5 charitiy purposes and the funds dedicted to support them in 2021

# In[103]:


top_purpose_amount = file_3.groupby(['Charity Purpose']).agg({'Total Gross Expenditure': 'sum'}).nlargest(n=5, columns=['Total Gross Expenditure'])


# In[104]:


top_purpose_amount


# <a id ='q10'></a>
# #### 10. Top 5 charities based on their governing form in 2021

# Let's count top 5 governing forms:

# In[105]:


top_governing_form_count = file_3.groupby(['Governing Form']).agg({'Total Gross Expenditure': 'count'}).nlargest(n=5, columns=['Total Gross Expenditure'])


# In[106]:


top_governing_form_count


# In[107]:


file_3['Governing Form'].value_counts()


# Let's check top 5 governing forms and their spendings in 2021:

# In[108]:


top_governing_form_amount = file_3.groupby(['Governing Form']).agg({'Total Gross Expenditure': 'sum'}).nlargest(n=5, columns=['Total Gross Expenditure'])


# In[109]:


top_governing_form_amount


# <a id ='q11'></a>
# #### 11. Total Gross Income - identifying outliers based on IQR (Interquartile Range)

# Firstly, let's check descriptive statistics for```Total Gross Income```and look at top 5 highest values.

# In[110]:


file_3[['Total Gross Income']].describe()


# In[111]:


file_3['Total Gross Income'].nlargest(n=5)


# There are 2 charities which achieved ```Total Gross Income``` over €1 billion and the mean for ```Total Gross Income``` variable is only €10,590,663.
# 
# Let's look closer on ```Total Gross Income``` column and check how the data is distributed.

# In[112]:


plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.distplot(file_3['Total Gross Income'])
plt.subplot(2,2,2)
sns.boxplot(file_3['Total Gross Income'])
plt.show()


# To detect outliers we will use IQR rule. 
# 
# This technique was sourced from: [youtube.com](https://www.youtube.com/watch?v=Cw2IvmWRcXs)

# In[113]:


Q1 = file_3['Total Gross Income'].quantile(0.25)
Q1


# In[114]:


Q3 = file_3['Total Gross Income'].quantile(0.75)
Q3


# In[115]:


IQR = Q3 - Q1
IQR


# In[116]:


lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR


# In[117]:


lower_limit


# In[118]:


upper_limit


# Let's see the ouliers:

# In[119]:


file_3.loc[(file_3['Total Gross Income'] > upper_limit) | (file_3['Total Gross Income'] < lower_limit)]


# There have been found 468 outliers.
# 
# Let's remove the outliers and save trimmed data in a new dataframe```file_3_no_outliers```. We will then visualise that dataframe using boxplot.

# In[120]:


file_3_no_outliers = file_3.loc[(file_3['Total Gross Income'] <= upper_limit) & (file_3['Total Gross Income'] >= lower_limit)]
print('number of values before removing outliers:', len(file_3))
print('number of values after removing outliers:',len(file_3_no_outliers))
print('outliers:', len(file_3)-len(file_3_no_outliers))


# In[121]:


sns.boxplot(x=file_3_no_outliers['Total Gross Income'])


# We will use capping method to set all outliers values to upper and lower limit. This technique will also 
# help us save all original data without deleting any values.

# In[122]:


file_3_no_outliers = file_3.copy()
file_3_no_outliers.loc[(file_3_no_outliers['Total Gross Income']>=upper_limit), 'Total Gross Income'] = upper_limit
file_3_no_outliers.loc[(file_3_no_outliers['Total Gross Income']<=lower_limit), 'Total Gross Income'] = lower_limit


# Let's see the distribution of ```Total Gross Income``` after removing the outliers.

# In[123]:


sns.boxplot(x=file_3_no_outliers['Total Gross Income'])


# In[124]:


plt.figure(figsize=(16,8))
plt.subplot(2,2,1)
sns.distplot(file_3_no_outliers['Total Gross Income'])
plt.subplot(2,2,2)
sns.boxplot(file_3_no_outliers['Total Gross Income'])
plt.show()


# In[125]:


len(file_3_no_outliers)


# Thanks to the capping method, we can see that no raws in ```Total Gross Income``` have been deleted.

# In[126]:


file_3.head()


# <a id ='q12'></a>
# #### 12. What are the incomes and spendings based on the country where charity was established?

# In[127]:


file_3.groupby("Country Established").agg({
    'Income: Central_Gov Local_Auth':'sum',
    'Income: Other Public Bodies':'sum',
    'Income: Philantrophic Orgs':'sum',
    'Income: Donations':'sum',
    'Income: Trading & Commercial':'sum',
    'Income: Other Sources':'sum',
    'Total Gross Income':'sum',
    'Total Gross Expenditure': 'sum',
    'Total Net Income':'sum'})


# #### The End
# 
# ### Thank You
