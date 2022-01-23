# Power By People Challenge
Create a web client form and an API endpoint for travel permit inquiries using Django.


### Input data
API must take the following fields as input:

* Date of travel 
* Date of return (optional)
* Country of origin 
* Country of destination 
* Age of traveller

### Criteria Check:
* Date of travel is between the next 2 and 5 following working days from the date of request. Otherwise, the travel permit must be denied. 
* If Date of return is present, and date of return is within 2 months of the Date of travel, then the travel can be approved. In any other case the travel permit must be denied. 
* Country of origin and Country of destination must be valid country names. 
* Travel is only allowed from countries where the number of Covid cases in the Country of origin is lower than in the Country of destination. 
* Travel is only allowed for travellers older than 21 and younger than 65. However, if a traveler is older than 15 years old, he/she can travel with the supervision of an adult. (You must show this prompt in your output when appropriate)
* Tests for the above scenarios

### Requirements
To run the solution ensure to meet the following:
* Ubuntu 18+
* Python3
* Postgres10+

### Setup
To run solution follow the steps below
```shell
# install required libraries
pip install -r requirements.txt
# Configure database
1. Access postgres service
2. Create database
3. Assignment priviledges to user
# Create .env
1. cp .env.example .env
2. Change variables according to your prefence

```

### Run
Run develop server
```shell
# Migrate migrations
./manage.py migrate
# Run server
./manage.py runserver
```
### Create Superuser
```shell
# Create Super User
./manage.py createsuperuser
```
### Run Server
```shell
# Run Development Server
./manage.py runserver
```
### Test
```shell
./manage.py test travel
```
### Access Project
To access solution, open your preferred browser ensure the development server is running.
```shell
http://localhost:8000
```
### To Access Travel Permit form page
```shell
http://localhost:8000/travel/permit/
```
### API Documentation

[Postman Collection](https://www.getpostman.com/collections/c557372d10e61f080bf7)



