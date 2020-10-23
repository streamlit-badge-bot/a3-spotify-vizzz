# CMU Interactive Data Science Assigment 3

* **Team members**: pldaviso@andrew.cmu.edu and pschalde@andrew.cmu.edu
* **Online URL**: https://share.streamlit.io/cmu-ids-2020/a3-spotify-vizzz

# What can I learn about my music listening habits?
In this application, we explore the relationship between time, genre, and song characteristics for the music that a user of Spotify listens to.  The data presented in this application is provided by [saraclay on Kaggle](https://www.kaggle.com/saraclay/my-spotify-streaming-history). If you are a spotify user, you can export your data and use it with this application too using [these instructions for exporting](https://www.spotify.com/ca-en/account/privacy/).  You can then use our notebook `Transform Streaming History.ipynb` to get your data ready for the streamlit application, clone this repository, add your files to the repository, replace the run the 'data_source' with the suffix of your file names, and run the application with your data from the command line using the command `streamlit run streamlit_app.py`

## Goal
The primary question that we are exploring in this application is "what can we learn about the user’s listening habits through three aspects of their Spotify data: time when songs were listened to, music genre associated with the song's artist, and characteristics of individual songs?" This question was interesting to us because of the idea that such habits often go unrecognized and can be difficult to discover using only the Spotify application. The nearest feedback is from the 'rewind' playlists that Spotify produces, which use their own algorithms to select the user's favorite songs during a time period. The dimensions and measures that we examine are not readily available through the Spotify application - we collected the spotify genres and track features using tools presented through Spotify for Developers (https://developer.spotify.com/) and categorized the provided specific genres into broader genre groups for our analysis.

Some of the specific questions that we hope this application enables the user to explore are:
* How consistently does the user listen through spotify? Are there weekly, monthly, yearly patterns? When do they most often listen?
* What are the user's preferences as far as music genre? How much variety in genre does the data display? Do they like listening to certain genres at certain times of the day?
* What do the danceability, energy, etc. of songs show about the user's preferences? Are those characteristics associated with the genre being listened to or the time of day that listening occurs?

We provide the tools to explore our primary questions and these specific questions in our application by building up the dimensions being included. We start with an aspect of data quality that was unexpected and interesting: "When I listen to music, do I listen to the whole song?" We then present plots that analyze the time that listening occurs: "What are my weekly and daily listening patterns?" We enable the user to explore the relationship between time and genre through a streamgraph and violin plot: "How much time do I spend listening to each genre? How do my listening habits compare across genres?" And then we add in the music characteristics (called track features by Spotify) to allow exploration of the three aspects of time, genre, and music characteristic together: "What are the characteristics of the music that I listen to? Are there any patterns across genre and time of day?"

## Rationale

We chose simple uni-variate visualizations to introduce the data and see its distributions. For example, we displayed barcharts showing how many minutes and how many songs had been listened to each day.  This is just to get an idea of the density of the streaming dataset: Does the user listen to music everyday? What date range does this dataset cover? Does it have pre-pandemic and pandemic data?  Similary, we show histograms of each music metric so that users can get a sense of how the metric is measures: Does this person listen to very danceable music? Are most of the songs lyrical or instrumental?

To achieve our goal, we used more complex plots with interactions to allow users to seek answers themselves.  To answer the question "When do I listen to music?", we used a heat map that showed density of listening with axes for time of day versus day of the week.  With this plot the user can make out trends across days of the week and time of day.  Additionally, there is a filter below where the user can select time of year data.  Now the user can explore if their listening habits change across the seasons of the year.


## Development Process

Equal time was spent between Paulina and Peter.  Initially working separately, Peter and Paulina had two long zoom meetings to discuss the topic and the dataset.  Then working separately, Peter had time to work on converting the raw data into clean csv files.  It took about a half hour to get all the data from the Spotify API for each track and artist.  Paulina then worked on some initial visualizations of the data.  Then, through a series of zoom calls with peer programming, they completed the assignment together.

Cleaning the dataset at first took about 4 hours then doing some song genre imputation took about 4 hours.  The genres that were linked from the Spotify API were too specific ("norwegian indie rock", "post-teen pop") so we needed to create an algorithm to map these specific genres to broad genres.  We used keywords and voting to match each artist with a broad genre.  See `streamlit_app.py` for details.  The most difficult and time consuming process of the project was making specific plots in altair.  It was very easy to do certain things with altair, but trying to get something very specific to work could take almost hours.  The 6 zoom meetings were each about 3 hours long.  All in all, each partner spent about 25 hours on the project for a total of 50 people-hours.

## Instructions

### Run Locally

Check out the Streamlit [getting started](https://docs.streamlit.io/en/stable/getting_started.html) guide and setup your Python environment.

To run the application locally, install the dependencies with `pip install -r requirements.txt` (or another preferred method to install the dependencies listed in `requirements.txt`). Then run `streamlit run streamlit_app.py`.

### View Online

Before you can view your application online, you need to have it set up with Streamlit Sharing. To do this, create an issue that asks the TAs to deploy your repo. To create the issue, you can follow [this link](../../issues/new?body=Dear+TAs%2C+please+add+our+repo+to+Streamlit+sharing+and+then+respond+to+this+issue+with+the+URL+to+the+deployed+application.&title=Setup+Streamlit+sharing&assignees=aditya5558,kunalkhadilkar,erbmoth) They will respond with a URL for your application. Once the repo is set up, please update the URL as the top of this readme and add the URL as the website for this GitHub repository.

### Deliverables

- [ ] An interactive data science or machine learning application using Streamlit.
- [ ] The URL at the top of this readme needs to point to your application online. It should also list the names of the team members. 
- [ ] A write-up that describes the goals of your application, justifies design decisions, and gives an overview of your development process. Use the `writeup.md` file in this repository. You may add more sections to the document than the template has right now.
