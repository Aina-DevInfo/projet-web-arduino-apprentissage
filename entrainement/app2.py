import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

nosDonneDHT = pd.read_csv("dht22_final.csv", sep=';', encoding='latin1')

target = nosDonneDHT['Humidite']

# Convertir les heures en secondes pour une meilleure manipulation
nosDonneDHT['Heure'] = pd.to_timedelta(nosDonneDHT['Heure']).dt.total_seconds()

# Re-diviser les caractéristiques et la cible après conversion
features = nosDonneDHT[['Heure']]
#print(features)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
# Construire et entraîner le modèle de régression linéaire
algorithmeMRL = LinearRegression()
algorithmeMRL.fit(X_train, y_train)
# Prédire les valeurs sur l'ensemble de test
y_pred = algorithmeMRL.predict(X_test)
# Évaluer le modèle
score = r2_score(y_test, y_pred)
print("LinearRegression")
print(f"R2 Score: {score:.2f}")
# Afficher les coefficients du modèle
print("Coefficients du modèle :", algorithmeMRL.coef_)
print("Intercept du modèle :", algorithmeMRL.intercept_)

# ********** algorithme Decision Tree Regressor ************
algorithmeDTR = DecisionTreeRegressor()

algorithmeDTR.fit(X_train, y_train)

predictions = algorithmeDTR.predict(X_test)

precisions = r2_score(y_test, predictions)
print("DecisionTreeRegressor")
print(predictions)
print(precisions)    

# ********** algorithme Random Forest Regressor ************
print("RandomForestRegressor")
algorithmeRFR = RandomForestRegressor()

algorithmeRFR.fit(X_train, y_train)

predictions = algorithmeRFR.predict(X_test)
precisions_apprentissage = algorithmeRFR.score(X_train, y_train)
precisions = r2_score(y_test, predictions)
print(predictions)
print(precisions) 

import joblib
fichier = 'modele_DHT_Hum.mod'
joblib.dump(algorithmeRFR, fichier)
joblib.dump(algorithmeRFR, 'modele_Humidite.pkl')