import streamlit as st
import pandas as pd
import altair as alt

st.title("Let's analyze some Spotify Data :)")

'''
Loading the Data Tables and Merging Tables
'''
data_source = 'public'

streaming_history_url = "streaming_history_{}.csv".format(data_source)
track_features_url = "track_features_{}.csv".format(data_source)
artists_url = "artists_{}.csv".format(data_source)
genres_url = "genres_{}.csv".format(data_source)

@st.cache  # add caching so we load the data only once
def load_data(url):
    return pd.read_csv(url)

@st.cache
def merge_data(sh, tracks, artists):
    df = sh.merge(tracks, on=['trackName', 'artistName'], suffixes=['_strm_hist', '_track'])
    df = df.merge(artists, on=['artistName'], suffixes=['_track', '_artist'])
    return df

streaming_history_df = load_data(streaming_history_url)
track_features_df = load_data(track_features_url)
artists_df = load_data(artists_url)
genres_df = load_data(genres_url)

if st.checkbox("Show Raw Data", value=False):
	st.write("Streaming History.")
	st.write(streaming_history_df)
	st.write("Track Features.")
	st.write(track_features_df)
	st.write("Artists.")
	st.write(artists_df)
	st.write("Genres.")
	st.write(genres_df)

df = merge_data(streaming_history_df, track_features_df, artists_df)

if st.checkbox("Show Merged Data", value=False):
	st.write(df)

'''
Visualizations
'''

chart = alt.Chart(track_features_df).mark_point().encode(
    x=alt.X("energy", scale=alt.Scale(zero=False)),
    y=alt.Y("danceability", scale=alt.Scale(zero=False)),
    color=alt.Y("n_listens")
).properties(
    width=600, height=400
).interactive()

st.write(chart)

pop_df = track_features_df.merge(artists_df, on=['artistName'], suffixes=['_track', '_artist'])
st.write(pop_df)
popularity_chart = alt.Chart(pop_df).mark_point().encode(
    x=alt.X("popularity_track:Q", scale=alt.Scale(zero=False)),
    y=alt.Y("popularity_artist:Q", scale=alt.Scale(zero=False)),
    color=alt.Y("n_listens_track:Q", scale=alt.Scale(type='log')),
    tooltip=['artistName', 'trackName']
).properties(
    width=600, height=400
).interactive()

st.write(popularity_chart)

histogram = alt.Chart(streaming_history_df).mark_bar().encode(
    alt.X("day_of_week", bin=False),
    y='sum(msPlayed)',
).properties(
    width=600, height=400
).interactive()

st.write(histogram)
