import streamlit as st
import pandas as pd
import altair as alt
from altair import datum

st.title("Let's analyze some Spotify Data :)")

# Loading the Data Tables and Merging Tables
data_source = 'public'
# data_source = 'peter'

streaming_history_url = "streaming_history_{}.csv".format(data_source)
track_features_url = "track_features_{}.csv".format(data_source)
artists_url = "artists_{}.csv".format(data_source)
genres_url = "genres_{}.csv".format(data_source)

#@st.cache  # add caching so we load the data only once
def load_data(url):
    return pd.read_csv(url)

#@st.cache(allow_output_mutation=True)
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

# Filter out the rows where the song is not listened all the way through (assume that this indicates switching between songs)

st.title('When I listen to music, do I listen to the whole song?')

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
df['prop_listened'] = df['msPlayed'] / df['duration_ms']
df['prop_listened'] = df['prop_listened'].clip(0, 1.1)

# want the slider to be in seconds not milliseconds
ms_per_second = 1000
# calculate the max of seconds played
max_seconds_played = max(df["msPlayed"]) / ms_per_second
# make a slider that goes from 0 to max seconds played with a step size of 0.5 seconds
seconds_slider = alt.binding_range(min=0, max=60*5, step = 0.5, name="Cutoff (seconds):")
# make the selection that is based off of the slider and can be used by the chart
seconds_selector = alt.selection_single(name="SelectorName", fields=["cutoff"], bind=seconds_slider, init={"cutoff": 5})
# make the chart whose x-axis in the ratio of milliseconds played to duration of the song (binned over steps of 0.1, meaning 10%)
# and whose y-axis is the count of the number of rows that fall into the ratio bin
# the selector (above) is used to color in the records whose milliseconds played are less than the specified selection
# the width and height of the chart are specified to try to provide better visibility
played_vs_duration = alt.Chart(df).mark_bar().encode(
	alt.X("prop_listened:Q", bin=alt.Bin(step=0.1)),
	y = "count():Q",
	color = "played_less_than_cutoff_seconds:N",
	tooltip = ["count():Q"]
).transform_calculate(
	#played_div_duration = min(datum.msPlayed/datum.duration_ms, '1.1:Q'),
	played_less_than_cutoff_seconds = datum.msPlayed < (seconds_selector.cutoff * ms_per_second)
).add_selection(
	seconds_selector
).properties(
	width = 1000,
	height = 400
)
st.write(played_vs_duration)


# For now, chose a max value of 20s from the played vs duration chart
# This means that there can be 0 - 3 records in the filtered table
# that have the same end time
seconds_cutoff = 20
ms_cutoff = seconds_cutoff * ms_per_second

# calculating the total hours played to see how much sparcity we might expect
seconds_per_minute = 60
minutes_per_hour = 60
sum_hours_played = sum(df["msPlayed"]) / (ms_per_second * seconds_per_minute * minutes_per_hour)
st.write("Total hours played = ", sum_hours_played)


st.title('When do I listen to music?')

st.write('How many songs have I listened to each day?')

# On x-axis: time, on y-axis: sum song count listened per x-axis day
num_songs_chart = alt.Chart(streaming_history_df).mark_bar().encode(
	alt.X("yearmonthdate(endTime_loc):T"),
	y="count():Q",
	tooltip = ["count():Q", "sum(minutesPlayed):Q"]
).transform_calculate(
	minutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute)
).transform_filter(
	datum.msPlayed > ms_cutoff
).properties(
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
#
# st.write(num_songs_chart2)

# On x-axis: time, on y-axis sum time listened to music per x-axis day
num_time_chart = alt.Chart(streaming_history_df).mark_bar().encode(
	alt.X("yearmonthdate(endTime_loc):T"),
	y="sum(minutesPlayed):Q",
	tooltip = ["count():Q", "sum(minutesPlayed):Q"]
).transform_calculate(
	minutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute)
).transform_filter(
	datum.msPlayed > ms_cutoff
).properties(
	width = 1000
)
st.write(num_time_chart)



st.title("What types of music do I listen to?")


music_metrics = ["danceability", "energy", "valence", "instrumentalness", "speechiness", "acousticness"]

correlation_chart = alt.Chart(df).mark_circle().encode(
    alt.X(alt.repeat("column"), scale = alt.Scale(zero=False), type = "quantitative"),
    alt.Y(alt.repeat("row"), scale=alt.Scale(zero=False), type="quantitative")
).transform_filter(
    datum.msPlayed > ms_cutoff
).repeat(
    row = music_metrics,
    column = music_metrics
)
st.write(correlation_chart)


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

st.write("There are serveral music metrics for each song I listened to:")
metric_histograms = []
for music_metric in music_metrics:
    if st.checkbox("Show " + music_metric, value=False):
        metric_histogram = alt.Chart(df).mark_bar().encode(
            alt.X(music_metric + ":Q", bin=alt.Bin(step=0.1)),
            y = "count():Q",
            tooltip = ["count():Q"]
        ).properties(
            width = 600,
            height = 200
        )
        st.write(metric_histogram)


date_range_selection = alt.selection_interval()

heat_map = alt.Chart(df).mark_rect().encode(
    alt.X('yearmonthdate(endTime_loc):T', title='hour of day'),
    alt.Y('count()', title='day of week'),
    alt.Color('count():Q', title='Count Songs Listened')
).transform_filter(
    datum.msPlayed > ms_cutoff
).properties(
    width = 1000,
    height = 400
)
#st.write(heat_map)
st.write(heat_map.encode(
    alt.X('hours(endTime_loc):O'), alt.Y('day_of_week:O', title='day of week'), #, scale=alt.Scale(domain=date_range_selection))
).transform_filter( date_range_selection) & heat_map.properties(height=50).add_selection(date_range_selection).transform_filter( datum.msPlayed > ms_cutoff)
)
# st.write(heat_map.add_selection(date_range_selection).transform_filter(date_range_selection))
# For when selection interaction is used!
#.add_selection(
#	alt.selection_single(fields=["msPlayed"])
#

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

