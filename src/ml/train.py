import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

#1. Generate fake data (Pattern: 3 mins per km)
#We add some randomness (noise) to make it more realistic
n_samples = 100
distances = np.random.uniform(1, 20, n_samples) # 1-20 km
battery_levels = np.random.uniform(10, 100, n_samples) # 10-100%

#Formula: Minutes = 3 * distance + (small battery penalty)
minutes = (3 * distances) + (100 - battery_levels) * 0.05 + np.random.normal(0, 2, n_samples) # Adding some noise with mean=0 and std=2
X = pd.DataFrame({'distance_km': distances, 'battery_level': battery_levels}) 
y = minutes

#2. Train a linear regression model
model = LinearRegression()
model.fit(X, y) #Train the model using the generated data

#3.Save the model using joblib
print('Training completed.Saving model...')
joblib.dump(model, 'src/ml/trip_predictor.joblib')
print('Model saved as src/ml/trip_predictor.joblib')