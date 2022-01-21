import pandas as pd
import pickle
from os import listdir
from os.path import isfile, join
file_path='C:/Users/Ryan/PycharmProjects/NySearch\Phase_2'
onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]
data_out=pd.DataFrame()
for file in onlyfiles:
    data=pd.read_csv(file_path+'/'+file, skiprows=4)
    data=data.drop(columns='TIME')
    data_out=pd.concat([data_out,data],axis=1)

phase_1_data=pd.read_pickle('Full_Dataset.pkl')

Final_Data=pd.concat([data_out,phase_1_data],axis=1)

Final_Data.to_pickle('1_2_Full_Dataset.plk')