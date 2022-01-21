import pandas as pd
import pickle

csv_location = 'Full_Dataset.csv'
Data = pd.read_csv(csv_location)
Data.to_pickle('Full_Dataset.plk')