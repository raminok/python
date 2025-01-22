import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures 
%matplotlib inline

file_name='https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DA0101EN/coursera/project/kc_house_data_NaN.csv'
df=pd.read_csv(file_name)
df.head()
df.dtypes
df.describe()
df.drop(["id","Unnamed: 0"],inplace=True,axis=1)
df.describe()
print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())
mean=df['bedrooms'].mean()
df['bedrooms'].replace(np.nan,mean, inplace=True)
mean=df['bathrooms'].mean()
df['bathrooms'].replace(np.nan,mean, inplace=True)
print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())
u_count=df['floors'].value_counts()
u_count.to_frame()
sns.boxplot(x="waterfront", y="price", data=df)

sns.regplot(x="sqft_above", y="price", data=df)
df.corr()['price'].sort_values()
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
X = df[['long']]
Y = df['price']
lm = LinearRegression()
lm
lm.fit(X,Y)
lm.score(X, Y)
X=df[['sqft_living']]
Y=df['price']
lm = LinearRegression()
lm
lm.fit(X,Y)
lm.score(X, Y)
features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]     
X = df[features]
Y=df['price']
lm = LinearRegression()
lm
lm.fit(X,Y)
lm.score(X, Y)
Input=[('scale',StandardScaler()),('polynomial', PolynomialFeatures(include_bias=False)),('model',LinearRegression())]
pipe=Pipeline(Input)
pipe
pipe.fit(X,Y)
pipe.score(X,Y)

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
print("done")

features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]    
X = df[features ]
Y = df['price']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=1)


print("number of test samples :", x_test.shape[0])
print("number of training samples:",x_train.shape[0])

from sklearn.linear_model import Ridge

ridgeReg = Ridge(alpha=0.1)

ridgeReg.fit(x_train,y_train)

pred = ridgeReg.predict(x_test)
ridgeReg.score(x_test, y_test)

from sklearn.preprocessing import PolynomialFeatures
pr = PolynomialFeatures(degree = 2)
x_test_trans = pr.fit_transform(x_test)
x_train_trans = pr.fit_transform(x_train)
ridgeReg = Ridge(alpha = 0.1)
ridgeReg.fit(x_train_trans,y_train)
ridgeReg.score(x_test_trans,y_test)


