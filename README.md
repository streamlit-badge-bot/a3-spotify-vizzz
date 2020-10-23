# CMU Interactive Data Science Assigment 3

* **Team members**: pldaviso@andrew.cmu.edu and pschalde@andrew.cmu.edu
* **Online URL**: https://share.streamlit.io/cmu-ids-2020/a3-spotify-vizzz

# What can I learn about my music listening habits?
In this application, we explore the relationship between time, genre, and song characteristics for the music that a user of Spotify listens to.  The data presented in this application is provided by [saraclay on Kaggle](https://www.kaggle.com/saraclay/my-spotify-streaming-history). If you are a spotify user, you can export your data and use it with this application too using [these instructions for exporting](https://www.spotify.com/ca-en/account/privacy/).  You can then use our notebook `Transform Streaming History.ipynb` to get your data ready for the streamlit application, clone this repository, add your files to the repository, replace the run the 'data_source' with the suffix of your file names, and run the application with your data in Streamlit.

See the writeup.md for information about the goals of the project, rationale, and development process.

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
