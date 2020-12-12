# About this Project
## Overview:
### Register:
- Standard log in and sign up procedure
### Home page/ browsing products:
- Each products are listed according to their category.
- Once in category, products can be filtered by their sub-category.
  **Popular section:** Contains products with rating > 2
  **Flash Sale section:** Contains products that has an ongoing sale on them
  **Covid 19 protection:** An extra section made in consideration for covid
### Cart:
- Customer can add products to the cart. 
- Once in cart, customer can change the amount of products and then proceed to checkout from here
### Checkout:
- Billing informations are pre-loaded from customer's profile. 
- He/she can change the billing address for this particular checkout as his/her choice.
- Email and phone no are uneditable as they are user specific data
- Customer can redeem points in checkout
### Rating:
- Customer can rate(from 0 to 5) the products he/she bought after last checkout
### Profile:
- Customer can edit their details in profile
- Email and phone no has to be unique
- Credit points are added to their account automatically, depending on how much they spent

## Framework:
- Django

## Languages:
- Python
- css
- javascript

## Database:
- Oracle, cx-oracle
- pl/sql

## Installation and setups required:
- [cx oracle installation](https://github.com/Srj/Demo_Django)
- oracle installation

## Creating a user and granting privileges to work with in oracle:
![image](https://user-images.githubusercontent.com/57999057/101983155-3a470200-3ca3-11eb-9845-143772d92739.png)
- Run the command `GRANT ALL PRIVILEGES TO KUMPIR`


## The journey:
The beginning felt like a maze, with me not knowing how to start, where to go, what to do. I started looking around youtube tutorials trying to 
get the grasp of how to use django. And even before that, creating a user in oracle was a huge hassle overcoming which took me days, only due to the
fact that I was too lazy to work around something new.

After creating schema, installing django, setting up database, I finally decided to open an experimental project following [this](https://www.youtube.com/watch?v=xv_bwpA_aEA&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO&ab_channel=DennisIvy) to get myself familiar
with what I will be working with. This experimental project turned out to be the main project later on, which caused me some pain later on.

## Things I could've done better:
##### Starting things early (Duh)
##### Organizing project directory
- The templates and static directories are not in sync with how django works
- Using same code in more than one html in <script> tag. **Should've used seperate js and css files** for each django app and made life easier
##### **NOT** mixing different stylesheets taken from different templates and messing things up
