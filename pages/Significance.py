import streamlit as st
import pandas as pd
import numpy as np
import math
from scipy import stats
from datetime import datetime
from pytz import timezone
import pymc3 as pm
import arviz as az

az.style.use("arviz-darkgrid")

st.header("Significance Calculator")

col1, col2 = st.columns(2)

with col1:
    number_groups = int(st.selectbox(
        "Select number of groups.",
        ("2", "3", "4", "5", "6"),
    )
)


st.write("Put the results into the table below.")

df = pd.DataFrame(
    [
       {"groups": "control", "number of samples": 4, "conversions": 1} if i == 0
        else {"groups": f"variant_{i}", "number of samples": 4, "conversions": 1}
        for i in range(number_groups)
   ]
)

edited_df = st.experimental_data_editor(df)
st.write(f"Table status updated ! {datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M:%S')}")


length_groups = len(edited_df)
total_sample_size = edited_df['number of samples'].sum()
conversion_rate = edited_df['conversions'] / edited_df['number of samples']


p_values = []
powers = []
group_combination = []
significance = []
z_scores = []
for i in range(length_groups):
    for j in range(length_groups):
        if i >= j :
            pass
        else :
            pooled_conversion_rate = (edited_df['conversions'][i] + edited_df['conversions'][j]) / (edited_df['number of samples'][i] + edited_df['number of samples'][j])
            pooled_std_err = np.sqrt(pooled_conversion_rate * (1-pooled_conversion_rate) * (1/edited_df['number of samples'][i] + 1/edited_df['number of samples'][j]))
            z_score = (conversion_rate[j] - conversion_rate[i]) / pooled_std_err
            p_value = 2 * (1 - stats.norm.cdf(np.abs(z_score), 0, 1))

            pooled_variance = pooled_conversion_rate * (1- pooled_conversion_rate)
            effect_size = np.abs(edited_df['conversions'][i] - edited_df['conversions'][j]) / np.sqrt(pooled_variance)
            power = 1 - stats.norm.cdf(z_score - effect_size*np.sqrt(edited_df['number of samples'][i]) , 0 , 1)

            p_values.append(p_value)
            powers.append(power)
            group_combination.append(f"{edited_df['groups'][i]} vs {edited_df['groups'][j]}")
            z_scores.append(z_score)
            if (p_value<=0.05) & (power>=0.8) :
                significance.append('**')
            else :
                significance.append(' ')

if st.button("Calculate"):
    dff =  st.experimental_data_editor(pd.DataFrame({'between group': group_combination, 'p_value' : p_values, 'power' : powers, 'z_score' : z_scores,'significance' : significance}))

