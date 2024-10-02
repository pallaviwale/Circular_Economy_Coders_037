import pandas as pd
import numpy as np
import streamlit as st
import Preprocessor

order_data = pd.read_csv("olist_orders_dataset.csv")
df = pd.DataFrame(order_data)

df = Preprocessor.fetch_time_features(df)






