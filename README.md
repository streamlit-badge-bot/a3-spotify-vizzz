# CMU Interactive Data Science Assigment 3

* **Team members**: pldaviso@andrew.cmu.edu and pschalde@andrew.cmu.edu
* **Online URL**: https://share.streamlit.io/cmu-ids-2020/a3-spotify-vizzz

# How does time affect my music listening habits?
In this application, we explore the relationship between time and the types of music that a user of Spotify listens to.  We have music streaming data provided by [saraclay on Kaggle](https://www.kaggle.com/saraclay/my-spotify-streaming-history).  If you are a spotify user, you can export your data and use it with this application too using [these instructions for exporting](https://www.spotify.com/ca-en/account/privacy/).  You can then use our notebook `Transform Streaming History.ipynb` get your data ready for the streamlit application run using `streamlit run streamlit_app.py`

## Goal
Our goal in this application was to explore the types of music listened to, when the music was listened to, and how the types and time of music listened relate (or don't).


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
