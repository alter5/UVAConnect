# UVAConnect

This repository contains code for the UVAConnect project created by a team of UVA students.

Tech Stack:
- The frontend and backend uses Django with Bootstrap
- The spaCy AI library is used to compare student profiles and generate a match score
- WebSocket is used for the website's chat feature
- This project is deployed onto Heroku using Travis CI for continuous integration

## Directions 
Below is a step-by-step guide for a first time user to navigate through our site to try and test all our functionalities:

- [First-Time-User](#First-Time-User)
    - [SignUp](#SignUp)
    - [ProfileCreation](#ProfileCreation)
    - [SignOut](#SignOut)
- [Returning-User](#Returning-User)
    - [LogIn](#LogIn)
    - [FriendRequests](#FriendRequests)
    - [Chat](#Chat)
    - [ProfileModification](#ProfileModification)

## Website Address

Access our website by clicking at the link below:
<a href="https://uva-connect.herokuapp.com/"> https://uva-connect.herokuapp.com/ </a>

## First-Time-User

### SignUp

You will be using your google account to sign up for our app. You can use your UVA or non-uva email address.

- Locate the <b>Log-in</b> button located at the top right side of the navigation bar
- Click on the Log-in Button and you will be redirected to your list of google accounts
- Select the google account that you want to use for signing up with our app
- Congrats! You are signed up. Proceed to the next step: 


### ProfileCreation

In this step you will be completing your user profile for our website

- After signing up, you were redirected to the page where you can complete your user profile
- Enter your major, favorite food, movie and hobbies. Fill out your bio. 
- This information would be available to other users on the website.
- Upload a user profile picture. 
- Alternatively we will use your current profile picture from the google account that you used to sign up
- Click on Submit. Your profile is now complete and you will be redirected to the home page of our website

### SignOut

- After completing your user-profile, you can signout from our app
- Locate the <b>Log-OUT</b> button located at the top right side of the navigation bar
- Click on the Log-out Button and you will be logged-out, you can log back in at any time using these [log in](#LogIn) instructions
- If you would like to continue navgating without signing out, use these [friend request](#FriendRequests) instructions


## Returning-User

### LogIn

- Locate the <b>Log-in</b> button located at the top right side of the navigation bar
- Click on the Log-in Button and you will be redirected to your list of google accounts
- Select the google account that you previously used to sign up for our app

### FriendRequests

In this step you will be navigating through other user profiles on our website to find your matches

- After completing your user profile or loggin in, you should have been redirected to the home page of our website
- If you are not at the home page already, Locate and click the <b>Home</b> button located at the top left side of the navigation bar
- The profiles are listed in descending order of similiarity with your interests
- You can see your top 3 friend recommendations. These are three users whose interests and major match yours more than others
- Each User Profile contains a similiarity bar which shows the percentage of similiarity between your profiles

- <b> Sending Requests: </b>Click on a User's Profile to access their complete profile and send them a friend request
- <b> Accepting Requests: </b>If another user sends you a friend request, it will appear at the top of the homepage
- Click on the friend request. This will redirect you to the user's profile
- Accept or Reject the friend request by clicking on the "Accept Friend Request" or "Reject Friend Request" button next to the user's name

### Chat

In this step you will be be able to chat with the users who are your friends

- Locate the <b>Chat</b> button located at the top left side of the navigation bar
- Click on the Chat Button and you will be redirected to your chat room
- The left side displays the profile pictures and names of users who are your friends
- <b>CLICK</b> on the user profile that you would like to converse with
- Enter a message in the chat box and hit send

### ProfileModification

- Locate the <b>Profile</b> button located at the top right side of the navigation bar
- Click on the Profile Button and you will be redirected to your Profile Page
- Modify any information you would like to change
- Click on the Update Button to apply the changes
