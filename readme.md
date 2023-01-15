# FHNW DAS Data Science - Software Engineering Project

House-Price-Predictor-App
Check-out: https://fhnw-ds-hs-2022-software-engineering-group-prod-ao7fiu5bra-oa.a.run.app/

## Project team
- Roman Sonder
- Adrian Hausmann
- Stefan Caminada

## About the Project
### Schedule
> **26.11.2022**: Start<br>
> **17.12.2022**: Interim Presentation<br>
> **18.01.2023**: Deadline<br>

### Goals
The main task is to implement a small machinelearning model and get it to production. Important/assessed parts are: 
- A program which predicts something (this is not really important it just has to work)
- Clean and readable python Code
- Working in a team
- GIT Releasemanagement
- Automated CI/CD pipeline
- Cloud deployment (e.g. Goodle Cloud)

### Software Architecture 
This is the chosen architecture for our "House-Price-Predictor-App":
![Architecture House-Price-Predictor-App](https://github.com/caminada87/FHNW_DS_HS-2022_Software_Engineering_Group2/blob/dev/images/SW-Eng_Gruppe-2_Architektur_House-Price-Predictor_v1.png)

## Project Log:

> **15.01.2023**
- Format code with black "black --line-length 79"
- Check code with flask8
- Insert docstrings

> **14.01.2023**
- Running some pytests
- Code cleaning
- documenation 

> **13.01.2023**
- Finally getting predictions running on GCR - the issue was that 2 requests had to run parallel and the gunicorn webserver was running with just 1 worker. It took some days to fix that.

> **12.01.2023**
- Team Meeting
- Created Prod-Service on GCP: fhnw-ds-hs-2022-software-engineering-group-prod
- Merging to Main-Branch

> **09.01.2023**
- Team Meeting

> **02.01.2023**
- CI/CD-Pipeline with GitHub Actions

> **30.12.2022**
- generated private keys on GCP
- Secrets on GitHub

> **24.12.2022 - 03.01.2023**
- Get CI/CD Pipeline running
- Thinned out the application as 2 containers using docker-compose was quite a hard entry to get into this topic. Everything is now a single app.
- Get Homepage and API's running on GCR

> **-24.12.2022**
- Finalize first version of the frontend and api

> **17.12.2022**
- Presentation Software-Architectur @ FHNW

> **16.12.2022**
- Integrated Software-Architectur  

> **30.11.2022**
- Created Dev-Service on GCP: fhnw-ds-hs-2022-software-engineering-group2
- Created FHNW-Software-Eng-Group2 on Google Cloud Plattform  

> **29.11.2022**
- Flask frontend using REST API for a fake prediction. 
- Frontend saves that data into the DB and is able to show recent predictions.
- ToDo: API: Access the actual model!

> **28.11.2022**
- Created Webapp (Flask, Sqlite, pytailwindcss)
- Still ToDo: API for predictions

> **27.11.2022**
- Created project structure
- Created readme.md
- Created .gitignore file
- Created repository FHNW_DS_HS-2022_Software_Engineering_Group2 on GitHub
- First Commit/Push

> **26.11.2022:** 
- Teams formed
- Defined the first task for our Members:
    - Stefan Caminada
        Initiate GIT Repo on GITHub
        Frontend --> Backend Interface (REST) with FLASK
    - Roman Sonder
        Find a Dataset 
        Build a model (write a prediction Method for unseen data)
    - Adrian Hausmann
        Start Teams Group for Communication
        Draft for presentation
        Check how to use CI/CD (Google Cloud)
- Scheduled next teammeeting for 2022.11.27 13:30-14:30 with the following agenda:
    - UI definition
    - Discuss the whole Flow CI/CD
    - Every members IDE is properly running (Virtual Environment is created for the project)
    - GIT is running for everyone
    - Next steps...
