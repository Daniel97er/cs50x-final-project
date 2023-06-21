# E-Shop-simulator program

## Description:

My CS50x project is to simulate a floor and door online shop. I
worked with Python, Flask Framework, SQL, Jinja Template language, HTML
and CSS. Thanks to pixabay.com for the nice pictures.


## How to use?
1. Open the Code with Github Codespace or other development environment
2. Install Python if not already installed
3. Install Python Flask Framework with the command: pip3 install flask
4. Install flask_session with the command: pip3 install flask_session 

### app.py

This is the main program where flask starts and runs.
First I include some libaries. Flask for the web application and
Session for current user. SQL to work with database. Werkzeug to
handle with passwords, make passwords hash values and decode them.
Datetime to get the current date.

First start Flask and set app.config to render automate the
templates. Then set a secret key and start the database.

#### Function index

This is the function who leads to the homepage of the web
application. The homepage is also a purchase documentation.
First the function check if user is logged in. If user is not logged
in, the page will be render for non-logged in users.
If the user is logged in, the id of the current user is
determined first. Then get name and cash value from the current
user with a database table user query. After this get data from
transactions table from database. All thetime when something goes
wrong throw a exception and redirect to homepage for not logged in
users. Create a total price list and fill with all user transactions
from database with amount times price of the purchased item. Finally
render index homepage with infos for navbar and the purchase
documentation for logged in users.

#### Function registration

Registration is a function where user is signed up to database.
Render registration page with registration formular from template.
First get data from registration page with post method and then
check the data. If some data was not correct like password
confirmation wrong or username or email is always in database
redirect to registration and throw a flash message with the reason.
If passed data is allowed create a database entry in table user and
throw a flash that registration is successful. Render the login page.

#### Function login

Login is a funtion where user go through the log in process.
Render the login page with login formular from template.
If post method then clear a possible logged in user. Then get
entered data from login page and check if username and password is
correct when not render login page again and throw a flash message.
If username and password is correct do the login process with user
id. Finally redirect to homepage with logged in user.

#### Function logout

Logout is a function which logged out the user and lead him to
homepage without user data. First the function make a session clear
to log out the user and then redirect to homepage.

#### Function emarket

Function emarket render the emarket page for logged in and not logged
in users. First create a dictionary with all the items from database
table items. Then check with try and except if user is logged in.
When user is logged in get user name and user cash for navbar and
render emarket page with items from items dictionary. When user is
not logged in render emarket page with items from items dictionary
but without data for the navbar.

#### Function bought

The bought function first checks whether the purchase can be
executed and then executes it.
First get all data from database items table. Then check is user
is logged in and get data from emarket page. Afterward get data
from database users and items to check if the purchased is correct.
Check if entered amount is greater then zero and if user has enough
cash to buy price of item times amount. Then calculate the current
cash value and update in database users the cash value of the
current user. Next get the transactions date with datetime function
and formatted in the right format. Insert into the database table
transactions the purchased. Finally count the new transactions of the
current user and update the value in database table transactions.
Return to the purchasing documentation with updated values. If
something goes wrong render the emarket page with items but without
user data.

#### Error_404 and Error_500

This functions come when error 404 or error 500 is occured. Render
own designed error page.


### Databse

The database consist of three tables where are user information,
transaction information and items information.


### Styles

The file styles is a css stylesheet. The design of my page is dark
because it is better for the eyes and battery. I tried to make it an
evenly pleasant shade but also incorporated some creativity. Some
things are from bootstrap.


### Templates

Here I give an overview describe of the templates

#### layouts

The two layout templates are for the error handling pages and for
the other all pages. In layout2 are the meta information. Bootstrap
include is also there. The navbar and some jinja syntax for the
function of the navbar when user is logged in or not is also there.
Finally I have the background color define with css.

#### error 404 and 500 templates

First the pages extends by layout1.html template.
Then print the individual created error messages.

#### Login and registration templates

First the pages extend by layout2.html template.
The login and registration templates are with a form for data input.
The design is with gold color and there is flash message for alerts.

#### Index template

Ffirst the page extends by the layout2.html template.
If user is not logged in add a please login message to the purchase
documentation title. Then create a table with six columns and a head
row. Every second row is in a other color for the bette readability.
The items and information for the table get from transactions table
database with jinja syntax. Finally I have design the page with some
CSS.

#### Emarket template

First the page extends the layout2.html template.
Then maybe throw flash message if user do something wrong.
After that print the whole e-market page with all pictures
and information of the items table database. I left commented
space in the html code to easily add more items. 
