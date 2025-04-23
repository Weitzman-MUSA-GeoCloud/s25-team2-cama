# Import packages
import numpy as np
import pandas as pd
import pandas_gbq
import datetime

from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV

from scipy.stats import loguniform

# Load BigQuery training data table
project_id = "musa5090s25-team2"

sql = """
SELECT *
FROM `musa5090s25-team2.derived.current_assessments_model_training_data`
"""
data_raw = pandas_gbq.read_gbq(sql, project_id=project_id)

# Shape data for modeling
data_modeling = data_raw.query('can_train == True')

categorical_columns_subset = [
    'category_code_description', 
    'building_code_description_new', 
    'exterior_condition', 
    'interior_condition', 
    'number_of_bathrooms', 
    'number_of_bedrooms', 
    'number_stories',
    'neighborhood', 
    'school',
    'zoning'
]

numerical_columns_subset = [
    'year_built', 
    'total_area',     
    'distance_to_nearest_septa'
]

pd.options.mode.copy_on_write = True
train_predictors = data_modeling[categorical_columns_subset + numerical_columns_subset]
train_predictors[categorical_columns_subset] = X[categorical_columns_subset].astype("category")
train_target = data_modeling['sale_price']

production_predictors = data_raw[categorical_columns_subset + numerical_columns_subset]
production_predictors[categorical_columns_subset] = X[categorical_columns_subset].astype("category")

# Specify model with optimized hyperparameters
model_production = ensemble.HistGradientBoostingRegressor(loss='gamma', max_iter=1000, early_stopping=True, random_state=0,
                                                          max_depth=6, learning_rate=0.069)

# Model fit
model_production.fit(train_predictors, train_target)

# Model prediction
prediction = model_production.predict(production_predictors)

# Prepare output
datetime = datetime.now()

ready = data_raw
ready['predicted_value'] = prediction
ready['predicted_at'] = datetime

# Create or replace output table on BigQuery
pandas_gbq.to_gbq(
    ready, 'derived.current_assessments', project_id=project_id, if_exists='replace',
)
