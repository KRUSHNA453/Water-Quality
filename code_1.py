# -*- coding: utf-8 -*-
"""CODE-1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bMOe84j3GpZFJJLoB-DtM6EmH21qh6WH
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Load the dataset
csv_file_path = "/content/water_dataX.csv"
data = pd.read_csv(csv_file_path, encoding="ISO-8859-1")
data.fillna(0, inplace=True)
print(data.head())

# Data preprocessing and feature engineering
# Conversions
data['Temp'] = pd.to_numeric(data['Temp'], errors='coerce')
data['D.O. (mg/l)'] = pd.to_numeric(data['D.O. (mg/l)'], errors='coerce')
data['PH'] = pd.to_numeric(data['PH'], errors='coerce')
data['B.O.D. (mg/l)'] = pd.to_numeric(data['B.O.D. (mg/l)'], errors='coerce')
data['CONDUCTIVITY (µmhos/cm)'] = pd.to_numeric(data['CONDUCTIVITY (µmhos/cm)'], errors='coerce')
data['NITRATENAN N+ NITRITENANN (mg/l)'] = pd.to_numeric(data['NITRATENAN N+ NITRITENANN (mg/l)'], errors='coerce')
data['TOTAL COLIFORM (MPN/100ml)Mean'] = pd.to_numeric(data['TOTAL COLIFORM (MPN/100ml)Mean'], errors='coerce')

#initialization
start=2
end=1779
station=data.iloc [start:end ,0]
location=data.iloc [start:end ,1]
state=data.iloc [start:end ,2]
do= data.iloc [start:end ,4].astype(np.float64)
value=0
ph = data.iloc[ start:end,5]
co = data.iloc [start:end ,6].astype(np.float64)

year=data.iloc[start:end,11]
tc=data.iloc [2:end ,10].astype(np.float64)


bod = data.iloc [start:end ,7].astype(np.float64)
na= data.iloc [start:end ,8].astype(np.float64)
na.dtype

data.head()

data = pd.concat([station, location, state, do, ph, co, bod, na, tc, year], axis=1)
data.columns = ['station', 'location', 'state', 'do', 'ph', 'co', 'bod', 'na', 'tc', 'year']

# Calculation of Ph
data['npH'] = data.ph.apply(lambda x: (100 if (8.5 >= x >= 7)
                                       else (80 if (8.6 >= x >= 8.5) or (6.9 >= x >= 6.8)
                                             else (60 if (8.8 >= x >= 8.6) or (6.8 >= x >= 6.7)
                                                   else (40 if (9 >= x >= 8.8) or (6.7 >= x >= 6.5)
                                                         else 0)))))

# Calculation of dissolved oxygen
data['ndo'] = data.do.apply(lambda x: (100 if (x >= 6)
                                       else (80 if (6 >= x >= 5.1)
                                             else (60 if (5 >= x >= 4.1)
                                                   else (40 if (4 >= x >= 3)
                                                         else 0)))))

# Calculation of total coliform
data['nco'] = data.tc.apply(lambda x: (100 if (5 >= x >= 0)
                                       else (80 if (50 >= x >= 5)
                                             else (60 if (500 >= x >= 50)
                                                   else (40 if (10000 >= x >= 500)
                                                         else 0)))))

# Calc of B.D.O
data['nbdo'] = data.bod.apply(lambda x: (100 if (3 >= x >= 0)
                                         else (80 if (6 >= x >= 3)
                                               else (60 if (80 >= x >= 6)
                                                     else (40 if (125 >= x >= 80)
                                                           else 0)))))

# Calculation of electrical conductivity
data['nec'] = data.co.apply(lambda x: (100 if (75 >= x >= 0)
                                       else (80 if (150 >= x >= 75)
                                             else (60 if (225 >= x >= 150)
                                                   else (40 if (300 >= x >= 225)
                                                         else 0)))))

# Calulation of nitrate
data['nna'] = data.na.apply(lambda x: (100 if (20 >= x >= 0)
                                       else (80 if (50 >= x >= 20)
                                             else (60 if (100 >= x >= 50)
                                                   else (40 if (200 >= x >= 100)
                                                         else 0)))))

data.head()
data.dtypes

data['wph']=data.npH * 0.165
data['wdo']=data.ndo * 0.281
data['wbdo']=data.nbdo * 0.234
data['wec']=data.nec* 0.009
data['wna']=data.nna * 0.028
data['wco']=data.nco * 0.281
data['wqi']=data.wph+data.wdo+data.wbdo+data.wec+data.wna+data.wco
data

#calculation overall wqi for each year
ag=data.groupby('year')['wqi'].mean()
data = ag.reset_index(level=0, inplace=False)
ag
data

# Visualizing the filtered data
year = data['year'].values
AQI = data['wqi'].values
data['wqi'] = pd.to_numeric(data['wqi'], errors='coerce')
data['year'] = pd.to_numeric(data['year'], errors='coerce')

plt.rcParams['figure.figsize'] = (20.0, 10.0)
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(year,AQI, color='red')
plt.show()
data

# Scatter plot of data points
cols = ['year']

y = data['wqi']
x = data[cols]

plt.scatter(x, y)
plt.show()

data = data.set_index('year')
data.plot(figsize=(15, 6))
plt.show()

data = data.reset_index(level=0, inplace=False)
data

# Using linear regression to predict
cols = ['year']
y = data['wqi']
x = data[cols]

reg = LinearRegression()
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=4)

# Linear Regression
reg_linear = LinearRegression()
reg_linear.fit(x_train, y_train)
y_pred_linear = reg_linear.predict(x_test)
mse_linear = mean_squared_error(y_test, y_pred_linear)
rmse_linear = np.sqrt(mse_linear)
mae_linear = mean_absolute_error(y_test, y_pred_linear)

print('Linear Regression Metrics:')
print('MSE:', mse_linear)
print('RMSE:', rmse_linear)
print('MAE:', mae_linear)

# Decision Tree
reg_tree = DecisionTreeRegressor()
reg_tree.fit(x_train, y_train)
y_pred_tree = reg_tree.predict(x_test)
mse_tree = mean_squared_error(y_test, y_pred_tree)
rmse_tree = np.sqrt(mse_tree)
mae_tree = mean_absolute_error(y_test, y_pred_tree)

print('\nDecision Tree Metrics:')
print('MSE:', mse_tree)
print('RMSE:', rmse_tree)
print('MAE:', mae_tree)

# Random Forest
reg_rf = RandomForestRegressor()
reg_rf.fit(x_train, y_train)
y_pred_rf = reg_rf.predict(x_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
rmse_rf = np.sqrt(mse_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)

print('\nRandom Forest Metrics:')
print('MSE:', mse_rf)
print('RMSE:', rmse_rf)
print('MAE:', mae_rf)

# Support Vector Machine (SVM)
reg_svm = SVR()
reg_svm.fit(x_train, y_train)
y_pred_svm = reg_svm.predict(x_test)
mse_svm = mean_squared_error(y_test, y_pred_svm)
rmse_svm = np.sqrt(mse_svm)
mae_svm = mean_absolute_error(y_test, y_pred_svm)

print('\nSVM Metrics:')
print('MSE:', mse_svm)
print('RMSE:', rmse_svm)
print('MAE:', mae_svm)

#using gradient descent to optimize it further
x = (x - x.mean()) / x.std()
x = np.c_[np.ones(x.shape[0]), x]
x

alpha = 0.1 #Step size
iterations = 3000 #No. of iterations
m = y.size #No. of data points
np.random.seed(4) #Setting the seed
theta = np.random.rand(2) #Picking some random values to start with

def gradient_descent(x, y, theta, iterations, alpha):
    past_costs = []
    past_thetas = [theta]
    for i in range(iterations):
        prediction = np.dot(x, theta)
        error = prediction - y
        cost = 1/(2*m) * np.dot(error.T, error)
        past_costs.append(cost)
        theta = theta - (alpha * (1/m) * np.dot(x.T, error))
        past_thetas.append(theta)

    return past_thetas, past_costs

past_thetas, past_costs = gradient_descent(x, y, theta, iterations, alpha)
theta = past_thetas[-1]

# Print the results...
print("Gradient Descent: {:.2f}, {:.2f}".format(theta[0], theta[1]))

# Plotting the cost function
plt.title('Cost Function J')
plt.xlabel('No. of iterations')
plt.ylabel('Cost')
plt.plot(past_costs)
plt.show()

#prediction of january(2013-2015) across india
import numpy as np
newB=[74.76, 2.13]

def rmse(y,y_pred):
    rmse= np.sqrt(sum(y-y_pred))
    return rmse


y_pred=x.dot(newB)

dt = pd.DataFrame({'Actual': y, 'Predicted': y_pred})
dt=pd.concat([data, dt], axis=1)
dt

plt.figure(figsize=(10, 6))
plt.scatter(dt['year'], dt['Actual'], label='Actual', color='blue')
plt.scatter(dt['year'], dt['Predicted'], label='Predicted', color='red')
plt.title('Actual vs Predicted Water Quality Index (WQI)')
plt.xlabel('Year')
plt.ylabel('WQI')
plt.legend()
plt.grid(True)
plt.show()

# Visualization
plt.scatter(x_test.index, y_test, label='Actual')
plt.plot(x_test.index, y_pred_linear, label='Linear Regression', color='r')
plt.plot(x_test.index, y_pred_tree, label='Decision Tree', color='g')
plt.plot(x_test.index, y_pred_rf, label='Random Forest', color='b')
plt.plot(x_test.index, y_pred_svm, label='SVM', color='purple')
plt.legend()
plt.title('Model Predictions vs Actual WQI Values')
plt.show()