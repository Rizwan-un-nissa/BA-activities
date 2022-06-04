import streamlit as st
import pickle 
import numpy as np
from recommend import show_recommend_page
from feedback import show_feedback_page

page = st.sidebar.selectbox("Recommend or Feedback", ("Recommend" , "Feedback"))

if page == "Recommend":
	show_recommend_page()
else:
	show_feedback_page()
