# Introduction

The SuperHeroes application allows users to browse a list of superheroes,
view detailed information about each superhero, and get recommendations for team formations based on criteria
for team selection - random or balanced in terms of powers.
Users should be able to save their favourite superheroes and provide functionality to update superhero information. \
It uses the Superhero API (https://www.superheroapi.com/) to get information about the superheroes to seed the database.


# Assumptions and Limitations

* Superhero creation or update doesn't support attaching image.
* We are only interested in strength, speed, power and intelligence power stats of a superhero.
* No support of deleting a superhero.
* Team size is fixed to 3.
* Non-responsive UI.
* No protection against SQL injection.


# Design

* The app uses a FastAPI backend hosted on port 8000 and react frontend on port 3000. 
* The communication happens using REST APIs.
* The backend used Sqlite as the database file to store the superheroes in a table with ID as primary.


# How to Start

1. Install docker compose on the system.
2. cd into the project directory and run the following commands
    ##
   <tab><tab> docker-compose build --no-cache <br/> docker-compose up


3. The web application UI should be accessible on address localhost:3000/superheroes which is accessible in a web browser.


# List of Features

1. Get list of all superheroes \
Get list of all superheroes based on search query.
The search parameter should be a substring of the superhero name.
If no search value is specified then we fetch list of all users.
The information is represented in a table where for each superhero, the list contains their ID and name.

2. Cache and database \
The list of all superheroes is stored in an in-memory cache.
The superheroes are fetched from the Superhero web API when the application starts and loaded into the cache
and the Sqlite database file.
For subsequent API calls to get list of all superheroes, result from the cache are returned.
The size of the cache increases with every superhero insertion.

3. View detailed information about each superhero \
When the user clicks on a superhero from the superheroes table. 
The superhero details appear the top of the screen with superhero's ID, name, powerstats and image.

4. Add new superhero \
If we want to add a new superhero, we can click on the '+' icon on the left side of the search bar.
It will open a form to create a superhero.
ID must be greater than zero and not present in current list of superheroes.
Upon clicking 'Create' button, the form is submitted and the new hero is added to the table.

5. Update superhero \
To update a superhero, first we need to open the superhero details.
Then we can update everything except the ID and image.
Clicking 'Update' button will update the superhero in the database and the cache.

6. Generate team suggestion \
In the teams tab, we can choose a team formation criteria which is set to random by default.
Clicking on 'Fetch Teams' will fetch a list of superheroes.
The other criteria named balanced will choose the first superhero randomly
and then select other superheroes iteratively to maximize the powerstat that the team is weakest in.
The team is shown in a table with ID, name, powerstats and image.
At the table footer, the combined powerstats of the team are shown.

7. API documentation \
The API docs are available at /docs path of the backend server.
