# Job Rotation
A Slack application using Flask and Slack API to create tasks and participants and manage job rotation using simple slash commands. The application is used by IT team at Great Lakes Fund Solutions to manage code peer reviews and other mundane tasks, as well as by Earlham College Residence’s Life office to manage Resident Assistant shifts.

Tech Stack: Python, Flask, PostgreSQL, Docker, Slack API

Author: Ali Shahram Musavi
Email: amusavi15@earlham.edu

CoAuthor: Sirajus Salikin
Email: ssalek14@earlham.edu



## Installation

 - Clone the application to your local machine and make sure you have docker installed

 - Edit Dockerfile, and make WORKDIR point to correct directory on your local machine

 - Build docker image
  ```
    docker build . -t rotation-bot
  ```

  - Run the application
  ```
    docker run -p 5000:5000 rotation_bot
  ```

  A few helpful links:
  
    Slack app development: https://api.slack.com/start/overview

    Ngrok for local slack development: https://api.slack.com/tutorials/tunneling-with-ngrok



## Endpoints

The application provides four endpoints/slash commands that can be used from inside the slack app to manage tasks and participants

1.
```
  /newQ task_name [task_participants]

  Create a new queue or update an existing one

  Example:
    command: /newQ food-delivery [John, Mike, Lisa, Tom]
    result: New task created  [John, Mike, Lisa, Tom]
```


2.
```
  /nextNQ task_name

  Returns the next participant inline

  Example:
    Command: /nextNQ food-delivery
    Result:  John
```


3.
```
  /showQ task_name

  Returns the list of participants for the given task

  Example:
    Command; /showQ food-delivery
    Result:  [John, Mike, Lisa, Tom]
```


4.
```
  /deleteQ task_name

  Returns the list of participants for the given task

  Example:
    Command; /deleteQ food-delivery
    Result:  Successfuly deleted task
```
