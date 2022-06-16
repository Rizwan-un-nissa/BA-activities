import streamlit as st
import pickle 
import numpy as np
import pandas as pd 

data = pd.read_csv("BA_dataset.csv")


def load_model():
	with open('saved_steps_new.pkl', 'rb') as file:
		KM = pickle.load(file)
	return KM

KM = load_model()

KM_reloaded_4 = KM["recommender_4"]
KM_reloaded_8 = KM["recommender_8"]
le_values = KM["le_values"]
le_cat = KM["le_cat"]
le_lod = KM["le_lod"]
le_rm = KM["le_rm"]

def show_recommend_page():
	st.title("Behavioural Activation Activities")
	
	st.markdown('<div style="text-align: justify;"> BA is a structured behaviour therapy that focuses on decreasing negative reinforcements and increasing positive reinforcements. It will take some effort to start an activity but it holds a strong potential to improve your mental health. </div>',unsafe_allow_html=True)
	st.text("")
	st.markdown("**Please select your inputs to get recommended activities**.")
	st.text("")
	values = (
		'Citizenship/Community', 'Employment', 'Family Relations',
       'Friendship/Social Relations', 'Hobbies',
       'Mental/Emotional Health', 'Personal Growth/Education',
       'Physical wellbeing', 'Spirituality', 'Self-care'
		)

	category = (
		'Valued activity', 'Pleasure', 'Mastery'
		)

	level_of_difficult = (
		'Easy', 'Medium', 'Hard', 'Very hard'
		)

	related_mood = (
		'Lonely', 'Disconnected', 'Stressed', 'Depressed', 'Sluggish',
       'Uncreative', 'Feeling stuck', 'Anxious', 'Isolated', 'Burned-out',
       'Exhausted', 'Bored', 'Unproductive', 'Uncreative ', 'Self-doubt',
       'feeling stuck', 'Tired', 'Over-worked', 'Self-neglect',
       'Out-of-control', 'Drained', 'Unhealthy', 'Procrastination',
       'Hopeless'
       )

	value = st.selectbox("Value", values)
	category = st.selectbox("Category", category)
	lod = st.selectbox("Level of difficulty", level_of_difficult)
	rm = st.selectbox("Mood", related_mood)

	
	recommend = st.button("Recommend activities")
	if recommend:
		# Encoding inputs
		Inp = np.array([[value, category, lod, rm]])
		Inp[:,0] = le_values.transform(Inp[:,0])
		Inp[:,1] = le_cat.transform(Inp[:,1])
		Inp[:,2] = le_lod.transform(Inp[:,2])
		Inp[:,3] = le_rm.transform(Inp[:,3])
		Inp = Inp.astype(int)

		# Predicting clusters according to KM4
		cluster_4 = KM_reloaded_4.predict(Inp)
		p_4 = cluster_4[0]

		# Predicting clusters according to KM8
		cluster_8 = KM_reloaded_8.predict(Inp)
		p_8 = cluster_8[0]

		# Recommendations
		if len( data[(data["km4"]==p_4) & (data["values"] == Inp[:,0][0])]['activities']) == 0: 
			activities = data[(data["km4"]==p)]['activities'].sample(3)

		elif len( data[(data["km8"]==p_8) & (data["values"] == Inp[:,0][0])]['activities']) == 0:
			activities = data[(data["km8"]==p)]['activities'].sample(3)
		else:
			activities = data[(data["km4"]==p_4) & (data["values"] == Inp[:,0][0])]['activities']
		st.subheader("Recommended activities are:")
		st.write(activities)
		
	

	










