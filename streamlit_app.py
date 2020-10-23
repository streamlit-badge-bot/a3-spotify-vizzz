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

# add caching so we load the data only once
@st.cache
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

st.write("To see the raw data we gathered from the provided streaming history file and the Spotify API or" +
    " the merged data, which is the join of the separate raw data tables, click these check boxes.")

if st.checkbox("Show Raw Data", value=False):
    st.write("Streaming History.")
    st.write(streaming_history_df.head(40))
    st.write("Track Features.")
    st.write(track_features_df.head(40))
    st.write("Artists.")
    st.write(artists_df.head(40))
    st.write("Genres.")
    st.write(genres_df.head(40))

# The broad genres are what will be used
broad_genres = ["Classical", "Electronica", "Folk/Country", "Hip Hop", "Indie", "Jazz", "No Genre", "Other", "Pop",  "R&B", "Rap", "Rock", "Tie Genre"]
# These are specific key words that differentiate the specific genres and allow us to categorizez them
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

# categorizing the artists table into broad genres
artists_extra_df = artists_df.copy()
artists_broad_genres = []
other_array = []
for index, row in artists_extra_df.iterrows():
    genre_array = row['genres']
    # check that the array is not 'nan', which means that there is no data for the artist
    if (str(genre_array) == "nan"):
        artists_broad_genres.append("No Genre")
    else:
        trimmed_genre_array = genre_array[1:-1].replace("'", "").replace(", ", ",")
        specific_genre_array = trimmed_genre_array.split(",")
        # Check that the array is non-empty, meaning that it has specified genres
        if len(specific_genre_array) == int(1) and specific_genre_array[0] == "":
            artists_broad_genres.append("No Genre")
        else:
        	# Go through each of the specific genres that have been provided, and
            # increase the count of the broad genre that they are associated with
            # The 'other' genre is a catch-all for not-one-of-the-others
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
            
            # Get the broad genre that has the max count
            max_num = np.array(count_array).max()
            # If there is a tie, the genre is categorized as 'tie genre'
            if (count_array.count(max_num) > 1):
            	# If we wanted to try to reduce the number of genres where
            	# there is a tie between two or more genres, we would use
            	# this print statement
                # st.write(index, specific_genre_array, count_array)
                # st.write("======================================")
                artists_broad_genres.append("Tie Genre")
            else:
            	# Otherwise, the genre is categorized as the genre that its max value
            	# is associated with
                artists_broad_genres.append(broad_genres[np.array(count_array).argmax()])

# This print statement shows the genres that are being classified as 'other' in decreasing
# order of the number of times that they appear. We used this to add keywords to the 'genres'
# arrays above in order to categorize the specific genres that have unique names
# st.write(sorted(Counter(other_array).items(), key=lambda pair: pair[1], reverse=True))
artists_extra_df['broad_genres'] = artists_broad_genres

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

st.write("In our exploratory analysis, we discovered that there are many songs that are not listened all the way through."
    + " These are most likely songs that were unintentionaly listened to: skipped over in a playlist or clicked by mistake."
    + " There are also some songs that have been played for more than their duration, likely because the user rewound the song."
    + " You can use the slider to explore the relationship between the number of seconds, the proportion of the song that was"
    + " listened to, and the distribution of the proportions in the data. The tooltip provides the exact count of songs in the"
    + " bar being hovered over. To improve the quality of the data analyzed, in allowing following charts we filter out songs"
    + " that were listened to for less than 20 seconds.")

df = df.copy()
df['percent_listened'] = df['msPlayed'] / df['duration_ms']
df['percent_listened'] = df['percent_listened'].clip(0, 1.1) * 100.

# unit conversions
ms_per_second = 1000
seconds_per_minute = 60
minutes_per_hour = 60
# make a slider that goes from 0 to 6 minutes played with a step size of 0.5 seconds
seconds_slider = alt.binding_range(min=0, max=8*seconds_per_minute, step = 0.5, name="Cutoff (seconds):")
# make the selection that is based off of the slider and can be used by the chart, initialized to 20 seconds
seconds_selector = alt.selection_single(name="SelectorName", fields=["cutoff"],
        bind=seconds_slider, init={"cutoff": 20})
# make the chart whose x-axis in the ratio of milliseconds played to duration of the song (binned over steps of 0.1, meaning 10%)
# and whose y-axis is the count of the number of rows that fall into the ratio bin
# the selector (above) is used to color in the records whose milliseconds played are less than the specified selection
# the width and height of the chart are specified to try to provide better visibility
played_vs_duration = alt.Chart(df).mark_bar().encode(
    alt.X("percent_listened:Q", bin=alt.Bin(step=10), title="Percent of Song"),
    alt.Y("count():Q", title="Count of Songs"),
    alt.Color("played_less_than_cutoff_seconds:N", title="Songs Played for Less than Cutoff",
            scale=alt.Scale(domain=['true', 'false'], range=['#d8b365', '#5ab4ac']), 
            legend=alt.Legend(orient="bottom")),
    tooltip = [alt.Tooltip("count():Q", title="Count of Songs")]
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

# For now, chose a max value of 20s from the played vs duration chart
# This means that there can be 0 - 3 records in the filtered table
# that have the same end time
seconds_cutoff = 20
ms_cutoff = seconds_cutoff * ms_per_second

st.header('What are my weekly and daily listening patterns?')

st.write("To explore how consistently Spotify is being used to listen to music, and if there are clear seasonal, weekly, and daily patterns"
    + " we designed a heat map whose x-axis represents the hour in the day and whose y-axis represents the day of the week, which is augmented"
    + " by a histogram with dates on the x-axis and count of songs listened on the y-axis."
    + " Selecting an interval of time in the bottom chart filters the data being displayed in the top chart. Both charts are color-coded"
    + " with the count of songs listened to and the tooltip also specifies the count of songs listened to, which is useful when"
    + " the difference between two colors is difficult to quantify. We observed that the data is somewhat sparse, and there are some listening "
    + " sessions that are much greater than others. We also observed that when looking at all the data, songs were primarily listened to  during"
    + " the 20:00 to 22:00 hour segments on the weekdays, but when looking at specific time periods, listening occurs at many different hour segments."
)

st.subheader('Use the bottom chart to narrow down a region of time to investigate on the top chart.')

date_range_selection = alt.selection_interval()

heat_map = alt.Chart(df).mark_rect().encode(
    alt.X('yearmonthdate(endTime_loc):T', title='Date'),
    alt.Y('count()', title='Count of Songs Listened')
).transform_filter(
    datum.msPlayed > ms_cutoff
).properties(
    width = 1000,
    height = 400
)

daysOrdered = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
hoursOrdered = [alt.DateTime(hours = 0), alt.DateTime(hours = 1), alt.DateTime(hours = 2), alt.DateTime(hours = 3), alt.DateTime(hours = 4),
    alt.DateTime(hours = 5), alt.DateTime(hours = 6), alt.DateTime(hours = 7), alt.DateTime(hours = 8), alt.DateTime(hours = 9), 
    alt.DateTime(hours = 10), alt.DateTime(hours = 11), alt.DateTime(hours = 12), alt.DateTime(hours = 13), alt.DateTime(hours = 14),
    alt.DateTime(hours = 15), alt.DateTime(hours = 16), alt.DateTime(hours = 17), alt.DateTime(hours = 18), alt.DateTime(hours = 19),
    alt.DateTime(hours = 20), alt.DateTime(hours = 21), alt.DateTime(hours = 22), alt.DateTime(hours = 23)]

st.write(
    heat_map.encode(
        alt.X('hours(endTime_loc):O', title="Hour of Day", scale=alt.Scale(domain = hoursOrdered)),
        alt.Y('day_of_week:O', title='Day of Week', sort=daysOrdered, scale = alt.Scale(domain=daysOrdered)),
        alt.Color('count():Q', title='Count of Songs Listened'),
        tooltip = 'count():Q'
    ).transform_filter(date_range_selection)
    & heat_map.encode(alt.Color('count():Q', title='Count of Songs Listened'), tooltip = 'count():Q').properties(height=250).add_selection(
        date_range_selection).transform_filter(datum.msPlayed > ms_cutoff).transform_calculate(
        minutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute))
)

st.header("How much time do I spend listening to each genre? How do my listening habits compare across genres?")

st.write('Spotify provides a list of genres for most artists.  These genres are very specific '
    + 'such as "norwegian pop" or "thai indie rock".  There were 501 unique genre names in our dataset. '
    + 'In order to perform analyisis we clustered these specific genres into broad genres such as '
    + '"Pop", "Rock", or "Classical".  We used keywords to match each specific genre to broad genre. '
    + 'In the charts below you can see each genre and how they were listened to throughout the day.  '
    + 'Some artists did not have genre information from '
    + 'Spotify leading to a "No Genre" categorization.  If two or more broad genres seemed equally apt'
    + ', we categorized the artist as "Tie Genre".  "Other" was used when no keywords matched the specific genre '
    + 'to broad genre.')

st.write('Use the plots below to understand how much music is listened to during the average day. '
    + 'Then investigate how each genre is listened to throughout the day.  Notice that some genres '
    + 'are evenly distributed while most are concentrated in the morning and evening.'
    + ' Please note that each genre in the violin plot has equal total density despite some '
    + 'being listened to more frequently.  This violin plot if for comparing the listening habits for each genre.'
    + ' Tooltip over both plots to see the average number of minutes played for a particular genre in that hour (streamgraph) or '
    + 'the density measurement of minutes played for a particular genre in that hour (violin plot)')

n_weeks_in_dataset = (pd.to_datetime(df['endTime_loc'], utc=True).dt.week.astype(str)
    + pd.to_datetime(df['endTime_loc'], utc=True).dt.year.astype(str)).nunique()

df['minutesPlayed'] = df['msPlayed'] / ms_per_second / 60

weird = alt.Chart(df).mark_area().encode(
    alt.X('hours(endTime_loc):T', title="Hour of Day",
        axis=alt.Axis(format='%H', domain=False, tickSize=0)
    ),
    alt.Y('sum(averageMinutesPlayed):Q', stack='center', title="Avg. Minutes Played in Hour Span"),
    alt.Color('broad_genres:N',
        scale=alt.Scale(scheme='tableau10'), title="Genre"
    ),
    tooltip=[alt.Tooltip('hours(endTime_loc)', title="Hour of the day"),
            alt.Tooltip('sum(averageMinutesPlayed):Q', title="Avg. Minutes Played"),
            alt.Tooltip('broad_genres', title="Genre")]
).transform_calculate(
    averageMinutesPlayed = datum.msPlayed / (ms_per_second * seconds_per_minute) / n_weeks_in_dataset
).properties(
    width=1300,
    height=500,
    title="Average Time Music was Played Throughout the Day by Genre"
)

df['minute_of_day'] = pd.to_datetime(df['endTime_loc'], utc=True).dt.hour * 60 + pd.to_datetime(df['endTime_loc'], utc=True).dt.minute
df['hour_of_day'] = 24 - (df['minute_of_day'] / 60.)
violin = alt.Chart(df).transform_density(
    'hour_of_day',
    as_=['hour_of_day', 'density'],
    extent=[0, 24],
    groupby=['broad_genres']
).mark_area(orient='horizontal').encode(
    y=alt.Y('hour_of_day:Q', title="Hour of Day"),
    color=alt.Color('broad_genres:N', title="Genre", scale=alt.Scale(scheme='tableau10')),
    x=alt.X(
        'density:Q',
        stack='center',
        impute=None,
        title=None,
        axis=alt.Axis(labels=False, values=[0],grid=False, ticks=True),
    ),
    column=alt.Column(
        'broad_genres:N',
        title="Genre",
        header=alt.Header(
            titleOrient='bottom',
            labelOrient='bottom',
            labelPadding=0,
        ),
    ),
    tooltip=[alt.Tooltip('hour_of_day', title="Hour of the day"),
            alt.Tooltip('density:Q', title="Density Minutes Played"),
            alt.Tooltip('broad_genres', title="Genre")]
).properties(
    width=90,
    title="How each genre is listened to throughout the day"
)
# .configure_facet(
#     spacing=0
# ).configure_view(
#     stroke=None
# )

st.write(weird & violin)


st.header("What are the characteristics of the genres of music that I listen to?")

st.write("The Spotify API provides music metrics about each track, which quantify different characteristics of the track, and are used internally by Spotify."
    + " We chose a subset of these metrics to compare across genres and across the time in a day: danceability, energy, valence, instrumentalness, speechiness, "
    + " and acousticness. The danceability, energy and valence (positivity) metrics have somewhat similar distributions and the instrumentalness, speechiness, and"
    + " acousticness (non-electric) metrics have somewhat similar distributions. All the metrics that we chose have domains from 0.0 to 1.0."
    + " Descriptions of the music metrics are provided courtesy of Spotify API Reference: https://developer.spotify.com/documentation/web-api/reference/")

music_metrics = ["danceability", "energy", "valence", "instrumentalness", "speechiness", "acousticness"]

spotify_features_explanations = {
        'key':'The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.',
        'danceability':'Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.',
        'energy':'Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.',
        'valence':'A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry). ',
        'instrumentalness':'Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.',
        'speechiness':'Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks. ',
        'acousticness':'A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.',
        }

st.subheader("Use the music metric dropdown (above the charts) to select the metric that will be presented in the charts."
    + " Use the broad genre dropdown (below the charts) to view only the data of that genre."
    + " Click and drag to select a subset of points in the scatter plot and view their music metric distribution in the histogram."
    + " Use tooltip to see the artist name and track (song) name for a particular data point.")

hoursMinutesOrdered = []
for hour in range(0, 24):
    for minute in range(0, 60):
        hoursMinutesOrdered.append(alt.DateTime(hours = hour, minutes = minute))

input_dropdown = alt.binding_select(options=broad_genres, name = "Broad Genre: ")
selection = alt.selection_single(fields=['broad_genres'], bind=input_dropdown)
color = alt.condition(selection, alt.Color('broad_genres:N'), alt.value('#00000000'))

scatter_brush = alt.selection(type='interval')

metric_dropdown = st.selectbox('Music Metric:', music_metrics)
st.write(spotify_features_explanations[metric_dropdown])

base_danceability_vs_hour = alt.Chart(df).mark_point().encode(
    x=alt.X('hoursminutes(endTime_loc):O', title="Hour of the Day", scale = alt.Scale(domain=hoursMinutesOrdered)),
    y=alt.Y(metric_dropdown, type="quantitative", scale=alt.Scale(zero=False, domain=[0.0, 1.0]))
).properties(
    width=700, height=500
)

metric_danceability_vs_hour = base_danceability_vs_hour.mark_bar().encode(
    alt.X(metric_dropdown + ":Q", bin=alt.Bin(step=0.05), title=metric_dropdown, scale = alt.Scale(domain=[0.0, 1.0])),
    alt.Y("count():Q", title="Number of Songs"),
    tooltip = ["count():Q"],
    color = alt.Color("broad_genres:N", scale=alt.Scale(scheme='tableau10'))
).properties(
    width = 600,
    height = 150
).transform_filter(
    selection
).add_selection(
    selection
).transform_filter(
    scatter_brush
)

danceability_vs_hour = base_danceability_vs_hour.encode(
  color=alt.condition(selection, alt.Color('broad_genres:N', scale=alt.Scale(scheme='tableau10')), alt.value('#00000000'))
).add_selection(
  selection,
  scatter_brush
)

overlay_danceability_vs_hour = base_danceability_vs_hour.encode(
  opacity=alt.value(0),
  tooltip=['artistName:N', 'trackName:N']
).transform_filter(
  selection
)

st.write(metric_danceability_vs_hour & (danceability_vs_hour + overlay_danceability_vs_hour))