import streamlit as st
import pandas as pd
import numpy as np
import os.path
import pickle 

if os.path.exists("df_feedback.csv"):
	df_feedback = pd.read_csv("df_feedback.csv")
else:
	df_feedback = pd.DataFrame(columns=["values",  'category', 'level_of_difficulty','related_mood', 'activities'])

def load_model():
	with open('saved_steps.pkl', 'rb') as file:
		KM = pickle.load(file)
	return KM

KM = load_model()

KM_reloaded = KM["recommender"]
le_values = KM["le_values"]
le_cat = KM["le_cat"]
le_lod = KM["le_lod"]
le_rm = KM["le_rm"]

def show_feedback_page():

	st.title("User Feedback")
	st.text("")
	st.markdown("<div style='text-align: justify;'> Please provide your feedback for the selected actviity suggested to you. This will allow us to personalize activities for you in future. </div>", unsafe_allow_html=True)
	st.text("")
	st.text("")
	if os.path.exists("df_feedback.csv"):
		df_feedback = pd.read_csv("df_feedback.csv")
	else:
		df_feedback = pd.DataFrame(columns=["values",  'category', 'level_of_difficulty','related_mood', 'activities'])


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

	activity = st.text_input("Enter your chosen activity")
	value = st.selectbox("Value", values)
	category = st.selectbox("Category", category)
	lod = st.selectbox("Level of difficulty", level_of_difficult)
	rm = st.selectbox("Mood", related_mood)

	feedback = st.button("Feedback")
	if feedback:
		Inp = np.array([[value, category, lod, rm]])
		Inp[:,0] = le_values.transform(Inp[:,0])
		Inp[:,1] = le_cat.transform(Inp[:,1])
		Inp[:,2] = le_lod.transform(Inp[:,2])
		Inp[:,3] = le_rm.transform(Inp[:,3])
		Inp = Inp.astype(int)
		Inp = list(*Inp)
		Inp.append(activity)

		if len(df_feedback.loc[df_feedback['activities'] == Inp[4] ] ) == 0:
			df_feedback = df_feedback.append(pd.Series(Inp, index = df_feedback.columns), ignore_index=True)
		else:
			df_feedback.replace(df_feedback.loc[df_feedback["activities" ]==Inp[4]].iloc[0][0], Inp[0], inplace=True)
			df_feedback.replace(df_feedback.loc[df_feedback["activities" ]==Inp[4]].iloc[0][1], Inp[1], inplace=True)
			df_feedback.replace(df_feedback.loc[df_feedback["activities" ]==Inp[4]].iloc[0][2], Inp[2], inplace=True)
			df_feedback.replace(df_feedback.loc[df_feedback["activities" ]==Inp[4]].iloc[0][3], Inp[3], inplace=True)
			

		df_feedback.to_csv("df_feedback.csv", index = False)

		st.write(" Thank you for your feedback.")

		


