# 3DSubjectChatbot

## Overview
The Subject Chatbot helps the student to ask some basic questions about the given subject(I have considered AI and ML books for traning it).

## How to run it
Project consists of both frontend react and backend flask components. Below, you'll find explanations of the working of each folder, along with the commands to run the Python (backend) and React (frontend) applications.

- run frontend react app
``` 
npm install
npm run build
npm start 
```

- run backend flask
```
pip install -r requirements.txt
python app.py
```
Note: before executing the above commands, be sure you are in the respective folder.

### Frontend
The `frontend` folder contains the user interface components of the chatbot which is created using react and react-three/fiber

#### Features
- It contains an input field where user can enter the question and the chatbot returns the answer.
- it also contains 4 buttons as conversation starters

### Backend
#### Features
- Backend is designed using flask.
- We take the input from the user and using langchain we get the answer from the pretrained openAI network and then send back the answer to the user.


![image](ui.JPG)



### Deployed working prototype
- The working prototype can be checked in the following url
``` 
https://3-d-subject-chatbot.vercel.app/
```