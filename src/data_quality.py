import pandas as pd
import numpy as np
import os

# Improvement ideas
# Follow directory structure, input and outputs using directory strucure (os.path + join)

# Setting the appropriate directory
print(os.getcwd())
os.chdir("F:/Deep Learning/Ayundante/src")

# Loading the input dataset for data quality report generation
input_data = pd.read_csv("../data/application_train.csv")

# Storing the output storage path
output_path = "F:/Deep Learning/Ayundante/outputs/"

def data_type_info(data):
    """
    This function will calculate the datatype of each of the columns in input data
    and output the results in csv format
    :param data:
    :return csv file containing datatypes of each column for further exploration:
    """

    data_types = pd.DataFrame(data.dtypes)
    data_types.rename({0: "column_type"}, axis=1, inplace=True)
    data_types.sort_values(by=['column_type'], inplace=True)
    data_types.to_csv(output_path + "data_type_info.csv")

# Testing the function with sample data
data_type_info(input_data)




input_data.dtypes
# data_types = pd.DataFrame(input_data.dtypes)
# data_types.rename({0: "column_type"}, axis=1, inplace=True)
# data_types.sort_values(by=['column_type'], inplace=True)
# data_types.to_csv("../outputs/data_types.csv")

len(input_data.columns)
len(input_data.select_dtypes(include=[np.number]).columns.tolist())
len(input_data.select_dtypes(exclude=[np.number]).columns.tolist())

# for col in input_data.select_dtypes(include=[np.number]).columns.tolist():
#     input_data[col]

x = input_data.describe(percentiles=[0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99], include=[np.number])
xt = x.T
xt['missing'] = input_data.shape[0] - xt['count']
xt['missing %'] = (input_data.shape[0] - xt['count']) / input_data.shape[0] * 100
xt['#unique'] = input_data.select_dtypes(include=[np.number]).nunique()
xt['is_possible_id'] = np.where(xt['count'] == xt['#unique'], 1, 0)
xt.to_csv("../outputs/x.csv")

y = pd.DataFrame(input_data['NAME_CONTRACT_TYPE'].value_counts(normalize=True).reset_index().head(10))
z = pd.DataFrame(input_data['CODE_GENDER'].value_counts(normalize=True).reset_index().head(10))

value = pd.DataFrame()
value = pd.concat([value, z], axis=1)
value = pd.concat([value, y], axis=1)


r = pd.concat([y, z],  axis=1, ignore_index=True)

a = input_data.select_dtypes(exclude=[np.number]).apply(lambda e: e.value_counts()).T.stack()

a = input_data[['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'NAME_TYPE_SUITE']]\
    .apply(lambda e: e.value_counts()).T.stack()

# data = input_data[['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'NAME_TYPE_SUITE']]


dic = {}
for col in data.columns:
   dic[col] = pd.DataFrame(data[col].value_counts(normalize=True).reset_index().head(10))


from pandas import ExcelWriter

def save_xls(dict_df, path):
"""
Save a dictionary of dataframes to an excel file, with each dataframe as a seperate page
"""
    writer = ExcelWriter('F:/Deep Learning/Ayundante/outputs/my_path.xls')
    for key in dict_df:
        dict_df[key].to_excel(writer, '%s' % key)
    writer.save()

save_xls(dict_df = dic, path = 'F:/Deep Learning/Ayundante/outputs/my_path.xls')


writer = pd.ExcelWriter('F:/Deep Learning/Ayundante/outputs/value_counts.xls')
for c in data.columns:
    a = data[c].value_counts(dropna=False).fillna(0).head(10).reset_index()
    a['%'] = a[c] / sum(a[c]) * 100
    a.to_excel(writer, sheet_name=c[:30])
writer.save()
