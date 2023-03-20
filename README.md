
# ZeroOnes

a blogging website for programmers and software engineers, in which they can share their experciences and see others's.

in python with flask.

#### Video Demo: https://youtu.be/KfVengIMnXI
## Description and features
- #### register (Join Us)
    - Require that the user input a username,email,password.
    - Render an apology if the any of user inputs is blank or the email already exists.
    - paswords are hashed before being stored in the database.

- #### Log In
    -  require the email and the password.
    - An apology appears if the any of user inputs is blank or wrong.

- #### Home Page
    - Display all posts with descending order of date in which they posted.
    - Display "profile", "add post", and "Logout" links (only if the user is logged in).
    - Display Log In and Join Us links (if the user is not logged in).
- #### Add Post
    - User can add posts through a form with three required inputs: title, tag, and the content.
    - The post is associated with the user by author_id since author_id = user_id.
- #### Edit post and Delete Post
    - User has the ability to edit any of the blog posts that he has posted or delete it at all.
    - If any user trys out to edit or delete a post that he didn't posted through the url, a flash message that say: "You Aren't Authorized To Edit This Post..." will be displayed.
- #### profile
    - Display User's info. and his posts.
- #### search
    - Filter posts by the search word.
    - If the user searched with a term that does not have any matches with all of posts a message thats say: "
        Sorry, No results found for 'that term' ..."   will be displayed.
- #### Logout
    - Clear the user session.

## MVC Paradigm
Our ZeroOnes website implements the MVC (Model–view–controller) Paradigm.
- The controller contains our “business logic”, code that manages our application overall, given user input. In our website, this will be our Python code in app.py.
- The view includes templates and visuals for the user interface, like the HTML and CSS that the user will see and interact with. (files in 'templates" and "static" folders).

- The model is our application’s data which is stored in a sqlite3 database (ourdb.db file).

## Files Discription
- templates folder: This folder contains all templates and HTML files of the user interface.
    - layout.html: This file contains the general structure of all Html pages of our website.
    - index.html: has the user interface of the home page which contains almost all links to other pages of the website, all posts of all users are displayed in descending order of date of posting, and a search bar to search for specific posts.
    - register.html: has the user interface for the user registration.
    - login.html: has the user interface of a user to login.
    - user.html: The UI of user profile page which has his personal info.(name, email, etc.) and posts that he has posted.
    - addpost.html: has a form to add a new post with a title, tag and content.
    - editpost.html: has a form to edit an existing post.
    - post.html: display UI of an individual post, and options to edit it or remove which are authorized only to the post owner.
    - apology.html: has the general UI of pages that will be displayed if there are any errors or any notes which we want the user to know.
    - search.html: has the UI that will be displayed if the user searches for anything.
- static folder: contains images, style sheets, and icons of the website.
    - favicon2.ico: the brand icon of our website.
    - default_profile.png: the default profile picture of all users that appears in their profile pages.
    - style.css: the CSS style that will be applied to the HTML pages.
- app.py: has all the code that manages our website overall, manages which pages appear as a response to which URLs, handles user inputs, receives/listens to requests, and generates suitable responses.
## Database
- ourdb.db file hold the website database.
- SQL module of cs50 is used.
- Two tables are used one for users and the other for posts.
- Users and Posts are associated together as author_id = user.id.

