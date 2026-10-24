# school-assistant

## What is it?
a python based asynchronous Telegram bot academic assistant that synchonized courwork from Google classroom into a local SQLite cache database. 

## Why did I build it?
I built this project to make keeping track of school work easier while also giving myself experience with database and API's

## Features
- Google Classroom sync
- SQLite local caching
- Telegram bot commands
- Scheduled assignment reminders


## How it works
Google Classroom data is fetched and cached into a local database through the Google Classroom API. That database holds the information on courses and coursework that the Telegram bot will access. Then, the Telegram bot sends the data when commanded to by the user or when its scheduled to do so


## Stack

- Python
- Google Classroom API 
- aiosqlite
- asyncio
- Telegram bot API 


## Database
* Courses 
    - course_id
    - course_name

* CourseWork
    - work_id
    - course_id
    - title
    - due_date
    - status


each course has its own unique id that google classroom created for it and each coursework is tied to one of those ids


## REQUIREMENTS
- Google Cloud with Google Classroom API
- Telegram bot token
