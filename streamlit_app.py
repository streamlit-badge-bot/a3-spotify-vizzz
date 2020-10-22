import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from altair import datum
from collections import Counter

st.title("What is the relationship between time and the music that I listen to?")
st.subheader("In this application, we will explore how time affects our " \
		+ "music listening habits by visualizing an export of personal Spotify data.");

# Loading the Data Tables and Merging Tables
data_source = 'public'

streaming_history_url = "streaming_history_{}.csv".format(data_source)
track_features_url = "track_features_{}.csv".format(data_source)
artists_url = "artists_{}.csv".format(data_source)
genres_url = "genres_{}.csv".format(data_source)

@st.cache  # add caching so we load the data only once
def load_data(url):
    return pd.read_csv(url)

@st.cache(allow_output_mutation=True)
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

broad_genres = ["Other", "Hip Hop", "Pop",  "Rap",  "R&B", "Electronica", "Rock", "Jazz", "Classical", "Indie", "Folk/Country", "No Genre", "Tie Genre"]
hip_hop_genres = ["hop", "boom bap", "funk", "urban contemporary", "lo-fi"]
pop_genres = ["pop", "shibuya-kei", "new jack swing", "motown"]
rap_genres = ["rap", "trap"]
r_b_genres = ["r&b", "soul", "blues"]
electronica_genres = ["electronica", "electro", "tronica", "techno", "electronic", "electric", "house", "step", "electra", "glitch", "vapor twitch", "chillwave", "edm"]
rock_genres = ["rock", "metal", "grindcore"]
jazz_genres = ["jazz", "bossa nova", "mpb"]
classical_genres = ["classical", "baroque", "piano cover", "impressionism", "early music"]
folk_country_genres = ["country", "folk"]
indie_genres = ["indie"]

# India motion picture industry: filmi, 

# categorizing the genres table
# genres_extra_df = genres_df.copy()
# broad_genres = []
# for index, row in genres_extra_df.iterrows():
# 	specific_genre = row['genre']
# 	if any(substring in specific_genre for substring in hip_hop_genres):
# 		broad_genres.append("Hip Hop")
# 	elif any(substring in specific_genre for substring in pop_genres):
# 		broad_genres.append("Pop")
# 	elif any(substring in specific_genre for substring in rap_genres):
# 		broad_genres.append("Rap")
# 	elif any(substring in specific_genre for substring in r_b_genres):
# 		broad_genres.append("R&B")
# 	elif any(substring in specific_genre for substring in electronica_genres):
# 		broad_genres.append("Electronica")
# 	elif any(substring in specific_genre for substring in rock_genres):
# 		broad_genres.append("Rock")
# 	elif any(substring in specific_genre for substring in jazz_genres):
# 		broad_genres.append("Jazz")
# 	elif any(substring in specific_genre for substring in classical_genres):
# 		broad_genres.append("Classical")
# 	else:
# 		broad_genres.append("Other")

# genres_extra_df['broad_genre'] = broad_genres
# st.write(genres_extra_df)

# categorizing the artists table
artists_extra_df = artists_df.copy()
artists_broad_genres = []
other_array = []
# tie_count = 0
for index, row in artists_extra_df.iterrows():
	genre_array = row['genres']
	if (str(genre_array) == "nan"):
		artists_broad_genres.append("No Genre")
	else:
		trimmed_genre_array = genre_array[1:-1].replace("'", "").replace(", ", ",")
		specific_genre_array = trimmed_genre_array.split(",")
		# st.write(index, specific_genre_array, len(specific_genre_array))
		if len(specific_genre_array) == int(1) and specific_genre_array[0] == "":
			artists_broad_genres.append("No Genre")
		else:
			count_array = [0] * len(broad_genres)
			for specific_genre in specific_genre_array:
				if any(substring in specific_genre for substring in hip_hop_genres):
					count_array[broad_genres.index("Hip Hop")] += 1
				elif any(substring in specific_genre for substring in pop_genres):
					count_array[broad_genres.index("Pop")] += 1
				elif any(substring in specific_genre for substring in rap_genres):
					count_array[broad_genres.index("Rap")] += 1
				elif any(substring in specific_genre for substring in r_b_genres):
					count_array[broad_genres.index("R&B")] += 1
				elif any(substring in specific_genre for substring in electronica_genres):
					count_array[broad_genres.index("Electronica")] += 1
				elif any(substring in specific_genre for substring in rock_genres):
					count_array[broad_genres.index("Rock")] += 1
				elif any(substring in specific_genre for substring in jazz_genres):
					count_array[broad_genres.index("Jazz")] += 1
				elif any(substring in specific_genre for substring in classical_genres):
					count_array[broad_genres.index("Classical")] += 1
				elif any(substring in specific_genre for substring in indie_genres):
					count_array[broad_genres.index("Indie")] += 1
				elif any(substring in specific_genre for substring in folk_country_genres):
					count_array[broad_genres.index("Folk/Country")] += 1
				else:
					count_array[broad_genres.index("Other")] += 1
					other_array.append(specific_genre)
			# artists_broad_genres
			max_num = np.array(count_array).max()
			if (count_array.count(max_num) > 1):
				# st.write(index, specific_genre_array, count_array)
				# st.write("======================================")
				# tie_count += 1
				artists_broad_genres.append("Tie Genre")
			else:
				artists_broad_genres.append(broad_genres[np.array(count_array).argmax()])

# st.write(tie_count)

# st.write(sorted(Counter(other_array).items(), key=lambda pair: pair[1], reverse=True))
artists_extra_df['broad_genres'] = artists_broad_genres
st.write(artists_extra_df.head(40))

if st.checkbox("Show Univariate Summaries", value=False):
	# genres_univariate = alt.Chart(genres_extra_df).mark_bar().encode(
	# 	x = "count():Q",
	# 	y = alt.Y("genre:N", sort='-x'),
	# 	tooltip = ["count():Q", "broad_genre:N"],
	# 	color = alt.Color("broad_genre:N",  sort='-x')
	# )
	# # st.write(genres_univariate)

	broad_genres_univariate = alt.Chart(artists_extra_df).mark_bar().encode(
		x = "count():Q",
		y = alt.Y("broad_genre:N", sort='-x'),
		color = alt.Y("broad_genre:N", sort='-x'),
		tooltip = ["count():Q"]
	)
	st.write(broad_genres_univariate)


df = merge_data(streaming_history_df, track_features_df, artists_extra_df)
if st.checkbox("Show Merged Data", value=False):
	st.write(df)
	
# Filter out the rows where the song is not listened all the way through (assume that this indicates switching between songs)

st.header('When I listen to music, do I listen to the whole song?')

# Visualizations
# Trying to answer the question, are all the songs fully played and also
# if a person played a song multiple times, would msPlayed have the aggregate total or would there be multiple records for the same song?
# For the public dataset, the chart shows that the majority of the songs are not listened to all the way through (msPlayed < 0.10 * duration_ms)
# It also shows that there are some songs that are listened to for more than the duration, a few almost double the duration, meaning that the aggregate
# total is reported.
# Not shown in this chart, but discovered in the process of developing it, is that there are very few songs whose msPlayed exactly equals the duration
# Some are 1 - 100 ms difference. Ideas: filter out songs that were listened to for less than 'z' ms; filter out songs that were listened to less than 'w'%
# of their duration; re-calculate the num_listens? (round up/down to the nearest integer so that those songs that were listened to close to 2 times would
# be counted as such)

df = df.copy()
df['percent_listened'] = df['msPlayed'] / df['duration_ms']
df['percent_listened'] = df['percent_listened'].clip(0, 1.1) * 100.

# want the slider to be in seconds not milliseconds
ms_per_second = 1000
# calculate the max of seconds played
max_seconds_played = max(df["msPlayed"]) / ms_per_second
# make a slider that goes from 0 to max seconds played with a step size of 0.5 seconds
seconds_slider = alt.binding_range(min=0, max=60*6, step = 0.5, name="Cutoff (seconds):")
# make the selection that is based off of the slider and can be used by the chart
seconds_selector = alt.selection_single(name="SelectorName", fields=["cutoff"], 
		bind=seconds_slider, init={"cutoff": 20})
# make the chart whose x-axis in the ratio of milliseconds played to duration of the song (binned over steps of 0.1, meaning 10%)
# and whose y-axis is the count of the number of rows that fall into the ratio bin
# the selector (above) is used to color in the records whose milliseconds played are less than the specified selection
# the width and height of the chart are specified to try to provide better visibility
played_vs_duration = alt.Chart(df).mark_bar().encode(
	alt.X("percent_listened:Q", bin=alt.Bin(step=10), title="Percent of Song"),
	alt.Y("count():Q", title="Count of Streams"),
	alt.Color("played_less_than_cutoff_seconds:N", title="Stream Played Shorter than Cutoff", 
			scale=alt.Scale(domain=['true', 'false'], range=['#d8b365', '#5ab4ac'])),
	tooltip = [alt.Tooltip("count():Q", title="Count of Streams")]
).transform_calculate(
	played_less_than_cutoff_seconds = datum.msPlayed < (seconds_selector.cutoff * ms_per_second)
).add_selection(
	seconds_selector
).properties(
	title = "Percent of Songs Listened to per Stream",
	width = 1000,
	height = 400
)
st.write(played_vs_duration)

st.write("You can use the slider above to determine that a large portion of the songs "
	+ "listened to in this data have been listened to for less than 20 seconds. "
	+ "These are most likely songs that were unintentionly listened to: skipped over in "
	+ "a playlist or clicked by mistake.  We will filter these streams "
	+ "that were listened to for less than 20 seconds out from subsequent visualizations.")

st.write("Some songs have been listened to for >100%.  This is because the user would rewind songs.")


# For now, chose a max value of 20s from the played vs duration chart
# This means that there can be 0 - 3 records in the filtered table
# that have the same end time
seconds_cutoff = 20
ms_cutoff = seconds_cutoff * ms_per_second

# calculating the total hours played to see how much sparcity we might expect
seconds_per_minute = 60
minutes_per_hour = 60
sum_hours_played = sum(df["msPlayed"]) / (ms_per_second * seconds_per_minute * minutes_per_hour)
st.write("Total hours of music played = ", sum_hours_played)


st.header('When do I listen to music?')

st.write('How many songs have I listened to each day?')

# On x-axis: time, on y-axis: sum song count listened per x-axis day
num_songs_chart = alt.Chart(streaming_history_df).mark_bar().encode(
	alt.X("yearmonthdate(endTime_loc):T", title="Date"),
	alt.Y("count():Q", title="Number of Streams"),
	tooltip = ["count():Q", "sum(minutesPlayed):Q"]
).transform_calculate(
	minutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute)
).transform_filter(
	datum.msPlayed > ms_cutoff
).properties(
	title="Streams per Day",
	width = 1000
)

st.write(num_songs_chart)

# df['week'] = pd.to_datetime(pd.to_datetime(df['endTime_loc'], utc=True).dt.strftime('%Y %U'), format="%Y %U")#pd.to_datetime(df['endTime_loc']) / 7
# st.write(df['week'])
# # On x-axis: time, on y-axis: sum song count listened per x-axis day
# num_songs_chart2 = alt.Chart(streaming_history_df).mark_bar().encode(
#     alt.X("week:T"),
#     y="count():Q",
#     tooltip = ["count():Q", "sum(minutesPlayed):Q"]
# ).transform_calculate(
#     #num_week = ,
#     minutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute)
# ).transform_filter(
#     datum.msPlayed > ms_cutoff
# ).properties(
#     width = 1000
# )

# st.write(num_songs_chart2)

st.write('How many minutes of music do I listen to each day?')

# On x-axis: time, on y-axis sum time listened to music per x-axis day
num_time_chart = alt.Chart(streaming_history_df).mark_bar().encode(
	alt.X("yearmonthdate(endTime_loc):T", title="Date"),
	alt.Y("sum(minutesPlayed):Q", title="Minutes Streamed"),
	tooltip = ["count():Q", "sum(minutesPlayed):Q"]
).transform_calculate(
	minutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute)
).transform_filter(
	datum.msPlayed > ms_cutoff
).properties(
	title="Minutes Played per Day",
	width = 1000
)
st.write(num_time_chart)

st.header('What are my weekly and daily listening patterns?')
st.subheader('Use the chart below to narrow down a region of time to investigate.')

date_range_selection = alt.selection_interval()

heat_map = alt.Chart(df).mark_rect().encode(
    alt.X('yearmonthdate(endTime_loc):T', title='Date'),
    alt.Y('count()', title='Count Songs')
).transform_calculate(
	averageMinutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute)
).transform_filter(
    datum.msPlayed > ms_cutoff
).properties(
    width = 1000,
    height = 400
)

daysOrdered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

st.write(
	heat_map.encode(
	    	alt.X('hours(endTime_loc):O', title="Hour of the Day"),
	    	alt.Y('day_of_week:O', title='Day of Week', sort=daysOrdered),
	    	alt.Color('count():Q', title='Count Songs Listened') #, scale=alt.Scale(domain=date_range_selection))
	).transform_filter( date_range_selection) & heat_map.properties(height=50).add_selection(date_range_selection).transform_filter( datum.msPlayed > ms_cutoff)
)

st.header("What types of music do I listen to?")


music_metrics = ["danceability", "energy", "valence", "instrumentalness", "speechiness", "acousticness"]

# correlation_chart = alt.Chart(df).mark_circle().encode(
#     alt.X(alt.repeat("column"), scale = alt.Scale(zero=False), type = "quantitative"),
#     alt.Y(alt.repeat("row"), scale=alt.Scale(zero=False), type="quantitative")
# ).transform_filter(
#     datum.msPlayed > ms_cutoff
# ).repeat(
#     row = music_metrics,
#     column = music_metrics
# ).properties(
# 	width=1500
# )
# st.write(correlation_chart)


# metric_dropdown = alt.binding_select(options=music_metrics)
# metric_select = alt.selection_single(fields=["Metric"], bind=metric_dropdown, name="Music Metrics")

# metric_histograms = alt.Chart(df).mark_bar().encode(
#     alt.X("metric:Q", bin=alt.Bin(step=0.1)),
#     y = "count():Q",
#     #color = "played_less_than_cutoff_seconds:N",
#     tooltip = ["count():Q"]
# ).transform_calculate(
#     metric = alt.Column(field = metric_select.Metric)
# ).transform_filter(
#     datum.msPlayed > ms_cutoff
# ).add_selection(
#     metric_select
# ).properties(
#     width = 1000,
#     height = 400
# )
# st.write(metric_histograms)

st.subheader("With Spotify's API we have the following music metrics for the songs listened to: ")

metric_histograms = []
for music_metric in music_metrics:
    if st.checkbox("Show " + music_metric, value=True):
        metric_histogram = alt.Chart(track_features_df).mark_bar().encode(
            alt.X(music_metric + ":Q", bin=alt.Bin(step=0.1), title=music_metric),
            alt.Y("count():Q", title="Number of Songs"),
            tooltip = ["count():Q"]
        ).properties(
            width = 600,
            height = 200
        )
        st.write(metric_histogram)

input_dropdown = alt.binding_select(options=broad_genres)
selection = alt.selection_single(fields=['broad_genres:N'], bind=input_dropdown, name='Country of ')
color = alt.condition(selection,
                    alt.Color('broad_genres:N'),
                    alt.value('#00000000'))

danceability_vs_hour = alt.Chart(df).mark_point().encode(
    x=alt.X('hoursminutes(endTime_loc):O', title="Hour of the Day"),
    y=alt.Y("valence:Q", scale=alt.Scale(zero=False), title="Danceability"),
    color=color,
).add_selection(
    selection
).properties(
	width=2000, height=600
)

# genre_dropdown = alt.binding_select(options=broad_genres)
# genre_selection = alt.selection_single(fields=['broad_genre'], bind=genre_dropdown, name='Genre is ')
# genre_color = alt.condition(genre_selection,
#                     alt.Color('broad_genre:N', legend=None),
#                     alt.value('lightgray'))

# danceability_vs_hour = alt.Chart(df).mark_point().encode(
#    x=alt.X('hoursminutes(endTime_loc):O', title="Hour of the Day"),
#    y=alt.Y("danceability", scale=alt.Scale(zero=False), title="Danceability"),
#    color= genre_color, # alt.Color("broad_genre:N", title="Genre"),
#    tooltip=[alt.Tooltip("trackName", title="Track Name"), alt.Tooltip("n_listens_track", title="Number of Listens")]
# ).transform_filter(
#     datum.msPlayed > ms_cutoff
# ).properties(
#    width=1000, height=400
# ).add_selection(
#     genre_selection
# ).transform_filter(
#     genre_selection
# )

st.write(danceability_vs_hour)

# VISUALIZATIONS FROM SATURDAY
#chart = alt.Chart(track_features_df).mark_point().encode(
#    x=alt.X("energy", scale=alt.Scale(zero=False)),
#    y=alt.Y("danceability", scale=alt.Scale(zero=False)),
#    color=alt.Y("n_listens")
#).properties(
#    width=600, height=400
#).interactive()

#st.write(chart)

#pop_df = track_features_df.merge(artists_df, on=['artistName'], suffixes=['_track', '_artist'])
#st.write(pop_df)
#popularity_chart = alt.Chart(pop_df).mark_point().encode(
#    x=alt.X("popularity_track:Q", scale=alt.Scale(zero=False)),
#    y=alt.Y("popularity_artist:Q", scale=alt.Scale(zero=False)),
#    color=alt.Y("n_listens_track:Q", scale=alt.Scale(type='log')),
#    tooltip=['artistName', 'trackName']
#).properties(
#    width=600, height=400
#).interactive()

#st.write(popularity_chart)

#histogram = alt.Chart(streaming_history_df).mark_bar().encode(
#    alt.X("day_of_week", bin=False),
#    y='sum(msPlayed)',
#).properties(
#    width=600, height=400
#).interactive()

#st.write(histogram)

