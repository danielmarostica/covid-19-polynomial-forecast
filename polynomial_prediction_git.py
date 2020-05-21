# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from matplotlib import rc

#TeX fonts
# rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

#COVID-19 BRAZIL
#by Daniel Marostica
#github danielmarostica

dias = 85
to_predict = 10
casos = ['10','casos']
mortes = ['11','mortes']
coluna = int(mortes[0])
print('Este código faz previsão para mortes nos próximos 10 dias, usando dados de 85 dias.')
configurar = raw_input('Gostaria de configurar os números? (s/n) ')
if configurar == 's':
    coluna = raw_input('Casos ou mortes? ')
    dias = int(input('Quantos dias disponíveis no arquivo (padrão = 85)? '))
    to_predict = int(input('Realizar projeção para quantos dias (padrão = 10)? '))
else:
    pass

if coluna == 'casos':
    coluna = int(casos[0])
    coluna_str = casos[1]
else:
    coluna = int(mortes[0])
    coluna_str = mortes[1]
print('Lendo arquivo...')

coluna = [coluna]
#----------------

#altere o nome do arquivo baixado do site do ministério
dataset = pd.read_excel('HIST_PAINEL_COVIDBR_20mai2020.xlsx', nrows=dias, usecols=coluna)
#extracts 2D array
y = dataset.iloc[:, [0]].values

X = np.arange(0,dias)
#converts to 2D array because fit_transform() requires it
X = np.reshape(X,(len(X),1))


#transforms
poly_reg  = PolynomialFeatures(degree = 5)

#transforms array values into matrix with 0, 1 and 2 degrees of the values
X_poly = poly_reg.fit_transform(X)

#creates linear regression with the multiple powers matrix (mocking a multiple-variable regression)
lin_reg = LinearRegression()
lin_reg.fit(X_poly,y)

#adds days to prevision
X_topredict = X
for i in range(0,to_predict):
    X_topredict = np.append(X_topredict, len(X_topredict))
X_topredict = np.reshape(X_topredict,(len(X_topredict),1))

#creates matrix with multiple powers of X_topredict
X_topredict_poly = poly_reg.fit_transform(X_topredict)
# applies trained lin_reg to predict X_topredict_poly
predicted = lin_reg.predict(X_topredict_poly)

print('Coeficientes do polinômio:')
print lin_reg.coef_

#plot
plt.figure(figsize=(8,5))
plt.plot(X_topredict,predicted, color='red',zorder=5,label='Proje\c{c}\~{a}o')
plt.scatter(X,y,zorder=5,label='Dados oficiais')
plt.title('Proje\c{c}\~{a}o: %s a partir do dia %i (13/05/2020)'%(coluna_str, dias-1), fontsize=16)
plt.xlim((0,dias+to_predict+5))
plt.ylim(bottom=0)
plt.grid(zorder=10, alpha=0.2)
plt.xlabel('Dias desde o primeiro caso', size=16)
plt.ylabel('Mortes confirmadas', size=16)
plt.tick_params(which='minor', axis='both', direction='in')
plt.legend(loc='upper left', shadow=False, fontsize=12)
plt.savefig('predict.jpg', dpi=400, bbox_inches='tight')
