import streamlit as st
import pandas as pd
import numpy as np
import math
from scipy import stats
from PIL import Image



# comparing to means
def sample_size_calculator(alpha, power, baseline, minimum_effect):
    z_alpha = stats.norm.ppf(1-alpha/2)
    z_beta = stats.norm.ppf(power)
    pooled_sd = math.sqrt((baseline*(1-baseline)) + ((baseline + baseline*minimum_effect)*(1-(baseline + baseline*minimum_effect))))
    effect_size = (baseline + baseline*minimum_effect) - baseline
    n = ((z_alpha + z_beta)**2 * 2 * pooled_sd**2) / effect_size**2
    return math.ceil(n/2)

# st.set_page_config(page_title="Minimum Sample Size Calculator for A/B Test", page_icon=":pencil:", layout="wide", page_header=f"assets/alarmy_logo")
st.set_page_config(page_title=" Minimum Sample Size Calculator for A/B Test",
                   # page_icon="::",
                   layout="wide")

image = Image.open('assets/alarmy_logo.png')
st.image(image)

st.title("Minimum Sample Size Calculator for A/B Test")
# st.write("")

alpha = st.slider("Significance level (alpha)", 0.01, 0.2, 0.05, 0.01)
power = st.slider("Power (1 - beta)", 0.5, 0.99, 0.8, 0.01)
# baseline = st.slider("Baseline conversion rate", 0.01, 0.5, 0.1, 0.01)
# minimum_effect = st.slider("Minimum detectable effect", 0.01, 0.5, 0.1, 0.01)

baseline = st.number_input('baseline Conversion Rate (%)')/100 # baseline
minimum_effect = st.number_input('Minimum effect (%)')/100 # MDE percentage



if st.button("Calculate"):
    sample_size = sample_size_calculator(alpha, power, baseline, minimum_effect)
    st.write(f"Minimum sample size per each variant: {sample_size}")


