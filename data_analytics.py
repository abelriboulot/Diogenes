import pandas as pd 
from pykrige.rk import RegressionKriging
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder, LabelBinarizer
import numpy as np
from itertools import product
from itertools import product

gridx = np.arange(34.97, 37.02, 0.0005)
gridy = np.arange(138.83, 140.87, 0.0005)
xy = list(product(gridx,gridy))
svr_model = SVR(C=0.1)
rf_model = RandomForestRegressor(n_estimators=1000)
lr_model = LinearRegression(normalize=True, copy_X=True, fit_intercept=True)
mlp_model = MLPRegressor(
    hidden_layer_sizes=(100,3),  activation='relu', solver='adam', alpha=0.001, batch_size='auto',
    learning_rate='constant', learning_rate_init=0.01, power_t=0.5, max_iter=100000, shuffle=True,
    random_state=9, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True,
    early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
xgb_model = xgb.XGBRegressor()

#models = [xgb_model, rf_model, mlp_model, lr_model, svr_model]
models = [xgb_model]

data = pd.read_csv("data/entire_apartments_tokyo.csv")
data = data[(data.lng > 0) & (data.Shiki < 10000) & (data.Rei <10000) & (data.rent < 10000)]
encoder = LabelBinarizer()
types_room = encoder.fit_transform(data['Typoroom'])

temp_df = pd.get_dummies(data[['m2','age','floor_detail','floors','units_number','Typoroom','material','unknown3','manshionka']], columns=['Typoroom','material','unknown3','manshionka'])
p = np.asarray(temp_df)
x = np.asarray([list(a) for a in zip(data['lng'],data['lat'])])
target = data["rent"] + data["Shiki"]/24 + data["Rei"]/24
target = target.as_matrix()

p_train, p_test, x_train, x_test, target_train, target_test \
    = train_test_split(p, x, target, test_size=0.3, random_state=42)

for m in models:
	print('=' * 40)
	print('regression model:', m.__class__.__name__)
	m_rk = RegressionKriging(regression_model=m)
	m_rk.fit(p_train, x_train, target_train)
	print('Regression Score: ', m_rk.regression_model.score(p_test, target_test))
	print('RK score: ', m_rk.score(p_test, x_test, target_test))
	price_map = m_rk.krige_residual(xy)
	price_map_out = pd.DataFrame(zip(xy[:,0],xy[:,1],price_map))
	pd.write_csv(m.__class__.__name__+'_price_map.csv')
