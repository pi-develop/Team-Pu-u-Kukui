# Team-Pu-u-Kukui

<img align="left" width="250" src="https://raw.githubusercontent.com/datjandra/Team-Pu-u-Kukui/refs/heads/main/logo.png">
Hawaii Digital Equity Dashboard

<div id="toc">
  <ul align="left" style="list-style: none">
    <summary>
      <h2>Inspiration</h2>
    </summary>
  </ul>
</div>

We set out to create a digital dashboard that helps bridge Hawaii's digital equity gap. Our vision was to build an intuitive platform that presents key data visually, allowing users to understand Hawaii's digital equity landscape at a glance. To accomplish our vision, we want to make an open source, simple yet effective tool to view the state of digital equity in Hawaii, for policy decision makers and the general public.

<br/>

## Solution

An accessible, user-friendly dashboard that clearly visualizes digital equity metrics across Hawaii. It integrates data from multiple sources including digital literacy, device access and broadband access.

## Design and Technology

Using Figma, we crafted a clean, aesthetic interface with an emphasis on clarity and ease of use. Our color palette draws from Hawaii's natural beauty - ocean blues and hibiscus pinks - creating a distinctly local feel while maintaining professional readability. The technology stack is Python and Streamlit on the front-end, and MySQL database as the back-end.

## Challenges

Our main challenge was data curation. With extensive information available, we needed to carefully select the most relevant metrics that would effectively show the digital equity program's implementation and impact. We also had difficulties finding data to measure objectives such as impact of digital equity initiatives.

## Lessons

This project revealed the complexity and potential of visualizing digital equity data. We learned the importance of thoughtful data selection and clear visual presentation in helping users understand Hawaii's digital equity landscape.

## Cloud Deployment
1. Create a MySQL database.
2. Execute **data/Create_Insert_Tables.sql** script in this repo to create tables with data.
3. Fork this GitHub repo.
4. Sign up for Streamlit account at https://streamlit.io/ using GitHub account.
5. Create an app and select the option to deploy a public app from GitHub.
6. Select the repo and enter **app.py** as the main file path.
7. Click advanced settings and enter the MySQL configuration.
```
[connections.mysql]
dialect = "mysql"
host = "database host"
database = "database name"
username = "username"
password = "password"
```
