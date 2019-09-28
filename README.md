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

1. First, install the requirements with **pip install -r requirements.txt**.
2. Then, run the backend using **python manage.py runserver**.

## Response Status Code

**400** - User not registered
**401** - Question not found
**402** - Email Already registred  
**404** - Authentication Failed  
**600** - Level Ended
