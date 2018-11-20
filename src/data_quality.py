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

input_data.dtypes
data_types = pd.DataFrame(input_data.dtypes)
data_types.rename({0: "column_type"}, axis=1, inplace=True)
data_types.sort_values(by=['column_type'], inplace=True)
data_types.to_csv("../outputs/data_types.csv")

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
