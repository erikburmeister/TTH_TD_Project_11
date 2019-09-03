# TTH_TD_Project_11
 Pug or Ugh API

In project #10 we are tasked with developing an API using Django REST Framework.
The API built for this project allows a user to look through a variety of dogs 
available for adoption. The user can sort by their preferences and then move 
dogs to 3 different categories. "Undecided" which means the user has not made up
their mind about that dog. "Liked" which means the user is interested in those
dogs. Finally, "Disliked" which means the user is not interested in that dog. 

We need make the following:

* Create Models
* Build the URLs the front end is expecting
* Make tests to cover a total of at least 50% of the code.

-----------------------------------------

User login info

User: test_user
password: password

Feel free to create new users in the `admin/` page. 
Under `AUTHENTICATION AND AUTHORIZATION`
Users > ADD USER+ (on the upper-right side of the screen)

-----------------------------------------

Check test coverage

* coverage run --source='.' manage.py test pugorugh
* coverage report

TOTAL = 68%

-----------------------------------------

Check requirements.txt Info on package versions on it.

* coverage==4.5.4
* Django==2.2.4
* djangorestframework==3.10.2
* pytz==2019.2
* sqlparse==0.3.0
