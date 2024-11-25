# ***Appointment booking system*** 🚀


## ***Features***:

### ***A. Authentication page🔐***:
- *Register(signUp)*
- *Login(signIn)*
- *AccessToken(wrapper function to protect all the routes, prompting the user to provide an accessToken)*

### ***B. User page👥***:
*This is the page where users can make a request to fetch, delete, update and promote other users to an admin-user.*
- *GetUser*
- *GetAllUsers(only for admin-users)*
- *UpdateUser*
- *PromoteUser(the user have to provide email_address of the user for promotion and a code to be able to access the the page)*
- *DeleteUser*

### ***C. Landing page(It includes the various types appointment and their categories)*** 🛬:
#### ***HealthCare Appointments*** 🧑‍⚕️:
- *Doctor consultations(general checking, specialist)*
- *Dental appointments*
- *Counseling sessions*
- *Physiotherapy sessions*
- *Vaccination appointments*
#### ***Professional Services*** 🧑‍🏫:
- *Financial advisory*
- *Real estate agent appointment(property viewing)*
- *Business consultation or mentoring*
#### ***Education And Tutoring*** 🧑‍🏫:
- *One-on-one tutoring sessions*
- *Academic advisory*
- *Career counseling*
#### ***Technical And Repair Services*** 🛠️🪛:
- *Electronics repair(phone, laptops)*
- *Home service(plumbing, electrical)*



### ***A. Authentication page:***
#### ***1. Register(signUp):***
##### ***Endpoint:*** "/register"
##### ***Method:*** POST
##### ***Payload:***
```json
{
    "username":"",
    "password":"",
    "email_address":"",
    "phone_number": ""
}
```
##### ***Response:***
```json
"Status": 201
{
    "success": "User created and uploaded successfully!"
}
```
#### ***2. Login(signIn):***
##### ***Endpoint:*** "/login"
##### ***Method:*** POST
##### ***Payload:***
```json
{
    "email_address":"",
    "password": ""
}
```
##### ***Response:***
```json
"Status": 200
{
    "Token": ""
}
```
### ***B. User page👥***:
#### ***I. GetUser***
##### ***Endpoint:*** "/user"
##### ***Method:*** GET
##### ***Response:***
```json
"Status": 200
{
    "user": {
        " public_id": "",
        "admin": ,
        "email_address": "",
        "phone_number": "",
        "username": ""
    }
}
```
#### ***II. PromoteUser:***
##### ***Endpoint:*** "/promote"
##### ***Method:*** PUT
##### ***Payload:***
```json
{
    "email_address":"",
    "code": ""
}
```
##### ***Response:***
```json
"Status": 200
{
    "Promoted": "User has been Promoted to an Admin-user"
}
```
#### ***III. GetAllUsers:***
##### ***Endpoint:*** "/users"
##### ***Method:*** GET
##### ***Response:***
```json
"Status": 200
{
    "Users": [
        {
            "admin": ,
            "created_at": "",
            "email_address": "",
            "phone_number": "",
            "public_id": "",
            "updated_at": "",
            "username": ""
        },
        {
            "admin": ,
            "created_at": "",
            "email_address": "",
            "phone_number": "",
            "public_id": "",
            "updated_at": "",
            "username": ""
        }
    ]
}
```
#### ***IV. UpdateUser:***
##### ***Endpoint:*** "/update"
##### ***Method:*** PUT
##### ***Payload:***
```json
{
    "username":"",
    "password":"",
    "email_address":"",
    "phone_number":""
}
```
##### ***Response:***
```json
"Status": 200
{
    "Updated": "Your details has been uploaded and updated successfully!"
}
```
#### ***V. DeleteUser:***
##### ***Endpoint:*** "/delete"
##### ***Method:*** DELETE
##### ***Response:***
```json
"Status": 200
{
    "Deleted": "User information has been deleted from the database successfully!"
}
```
### ***C. Landing page(It includes the various types appointment and their categories)*** 🛬:
#### ***a. HealthCare Appointments*** 🧑‍⚕️:
##### ***I. Doctor consultations(general checking, specialist):***
##### ***Endpoint:*** /consult
##### ***Method:*** POST
##### ***Payload:***
```json
{
    "first_name":"",
    "last_name":"",
    "gender":"",
    "user_phone_number":"",
    "address":"",
    "email_address":"",
    "next_of_kin":"",
    "next_of_kin_phone_number":"",
    "next_of_kin_address":"",
    "amount":,
    "appointment_description":"",
    "appointment_time":"",
    "appointment_date":""
}
```
##### ***Response:***
```json
"Status": 200
{
    "Consultation": "Consultation appointment was booked successfully!"
}
```
##### ***II. Dental appointments:***
##### ***Endpoint:*** /dental
##### ***Method:*** POST
##### ***Payload:***
```json

```