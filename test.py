import pandas as pd

#pip install openpyxl
'''excel_file = pd.ExcelFile('static/dataset.xlsx')

print(excel_file)

dat=excel_file.values

for ss in dat:
    print(ss)'''

dat=pd.read_excel('static/dataset.xlsx')  
print(dat.values)
