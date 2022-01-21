import pandas as pd

full_data=pd.DataFrame()
multi_sheet_file = pd.ExcelFile('Sensor_Coordinates_All_SJJ_081820.xlsx')
excel_sheet_names = multi_sheet_file.sheet_names

for sheet in excel_sheet_names:
    location_data=pd.read_excel(multi_sheet_file,sheet_name=sheet,header=None)
    full_data=full_data.append(location_data,ignore_index=True)


full_data=full_data.iloc[:,0:5]
sensor_data=full_data.iloc[:,0].str.split("-", n = 4, expand = True)
full_data=pd.concat([sensor_data,full_data],axis=1)
print(full_data)
#full_data.to_pickle('Location_Data_2.plk')