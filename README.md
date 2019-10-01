<p align="center">
  <a href="https://www.gatsbyjs.org">
    <img alt="Gatsby" src="static/logo.png" width="50" />
  </a>
</p>
<h1 align="center">
  Digital Fortress API
</h1>

This is the backend repository built on Django framework, hosted in AWS EC2 server with load balancing optimised.

**How to run:**

1. First, install the requiremnents by running the command **pip install -r requirements.txt**
2. Then, apply the migrations using **python manange.py migrate**
3. Run the server using **python manage.py runserver**

The API links:

quiz/auth/register - For registering a user
quiz/auth/login - For logging in a user
quiz/getRound - To get the round for a user
quiz/checkRound - To check the answer submitted by a user for a given round
quiz/getClue - To get the clues for a particular round
quiz/checkClue - To check the answer submitted for a given clue question
quiz/leaderboard - To get the current leaderboard
quiz/saveLeaderBoard - To save the leaderboard in a CSV file format
