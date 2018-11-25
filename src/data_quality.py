import pandas as pd
import numpy as np
import os

# Improvement ideas
# Follow directory structure, input and outputs using directory structure (os.path + join)

# Setting the appropriate directory
print(os.getcwd())
os.chdir("F:/Deep Learning/Ayundante/src")

# Loading the input data set for data quality report generation
input_data = pd.read_csv("../data/application_train.csv")

# Storing the output storage path
output_path = "F:/Deep Learning/Ayundante/outputs/"

def data_type_info(data):
    """
    This function will calculate the data type of each of the columns in input data
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

def numeric_type_info(data):
    """
    This function will calculate all the major information related to numeric variables like mean, median
    standard deviation, minimum, maximum, missing values etc.
    :param numeric_col_data:
    :return csv file containing information about numeric columns:
    """
    numeric_data = data.select_dtypes(include=[np.number])
    numeric_info = numeric_data.describe(percentiles=[0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    numeric_info = numeric_info.T
    numeric_info['#missing'] = numeric_data.shape[0] - numeric_info['count']
    numeric_info['missing %'] = (input_data.shape[0] - numeric_info['count']) / input_data.shape[0] * 100
    numeric_info['#unique'] = numeric_data.nunique()
    numeric_info['is_possible_id'] = np.where(numeric_info['count'] == numeric_info['#unique'], 1, 0)
    numeric_info.to_csv(output_path + "numeric_type_info.csv")

# Testing the function with sample data
numeric_type_info(input_data)


def categorical_type_info(data, max_categories=10):
    """
    This function will return the frequency of top n categories of all the categorical column in the data set
    The function will work best in case its already filtered for categorical columns as there can be many
    columns in data set which can be categorical but are not useful top n category analysis (for.e.g ID variables)
    :param
    categorical_data: Data set containing possible categorical columns
    max_categories: Number of maximum categories per column to be expected in the outputs
    :return csv files containing top n categories for each column in different sheets:
    """
    writer = pd.ExcelWriter(output_path + "categorical_value_counts.xls")
    categorical_data = data.select_dtypes(exclude=[np.number])
    for col in categorical_data.columns:
        val_count = categorical_data[col].value_counts(dropna=False).fillna(0).head(max_categories).reset_index()
        val_count['%'] = val_count[col] / sum(val_count[col]) * 100
        val_count.to_excel(writer, sheet_name=col[:30])
    writer.save()

categorical_type_info(input_data)
