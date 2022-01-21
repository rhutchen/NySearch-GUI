import pandas as pd


test_matrix_1=pd.read_excel('Test_Matrix.xlsx')
test_matrix_1['HVAC'] = 'None'
test_matrix_2=pd.read_excel('Test_Matrix_081820.xlsx')
test_matrix=pd.concat([test_matrix_1,test_matrix_2])
test_matrix['Name'] = test_matrix['Name'].str.replace('Test_', '')

print(test_matrix)

test_matrix.to_pickle('Test_Matrix.plk')

