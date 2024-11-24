import pandas as pd

#Dataset - order_payments_dataset
data1 = pd.read_csv("olist_order_payments_dataset.csv")
df1 = pd.DataFrame(data1)

#check null values
df1.isnull().sum()

#check datatypes
df1.dtypes

df1.info()

df1.describe()

#Dataset - order_reviews_dataset
data2 = pd.read_csv("olist_order_reviews_dataset.csv")
df2 = pd.DataFrame(data2)

#check null values
print(df2.isnull().sum())

#check datatypes
df2.dtypes

df2.info()

df2.describe()