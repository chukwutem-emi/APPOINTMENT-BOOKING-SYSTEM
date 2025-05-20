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

### ***D. Appointment-Operations Like:***
- *Retrieving a user appointment details(GET)*
- *Retrieving all users appointment details(GET)*
- *Updating a user appointment details(PUT)*
- *Deleting user appointment details(DELETE)*

### ***A. Authentication page:***
#### ***1. Register(signUp):***
##### ***Endpoint:*** "/api/auth/register"
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
##### ***Endpoint:*** "/api/auth/login"
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
##### ***Endpoint:*** "/api/user_bp/user"
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
##### ***Endpoint:*** "/api/user_bp/promote"
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
##### ***Endpoint:*** "/api/user_bp/users"
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
##### ***Endpoint:*** "/api/user_bp/update"
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
##### ***Endpoint:*** "/api/user_bp/delete"
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
##### ***Endpoint:*** /api/healthcare/consult
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
"Status": 201
{
    "Consultation": "Consultation appointment was booked successfully!"
}
```
##### ***II. counseling Sessions:***
##### ***Endpoint:*** /api/healthcare/counseling
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
"Status":201
{
    "Counseling": "Counseling appointment was booked successfully!",
    "googleCalendarLink": ""
}
```
##### ***III. Dental Appointment:***
##### ***Endpoint:*** /api/healthcare/dental
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
"Status":201
{
    "Dental": "Dental appointment was booked successfully!",
    "googleCalendarLink": ""
}
```
##### ***IV. Physiotherapy Session:***
##### ***Endpoint:*** /api/healthcare/physiotherapy
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
"Status":201
{
    "Physiotherapy": "Physiotherapy appointment was booked successfully!",
    "googleCalendarLink": ""
}
```
##### ***V. Vaccination Appointment:***
##### ***Endpoint:*** /api/healthcare/vaccination
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
"Status":201
{
    "googleCalendarLink": "",
    "vaccination": "Vaccination appointment was booked successfully!"
}
```
#### ***b. Professional Services🧑‍🏫:***
##### ***I. Business Consultations:***
##### ***Endpoint:*** /api/professional/business
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
"Status":201
{
    "business_consultation": "Business consultation appointment was booked successfully!",
    "googleCalendarLink": ""
}
```
##### ***II. Financial Advisory:***
##### ***Endpoint:*** /api/professional/financial
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
"Status":201
{
    "financial_advisory": "Financial advisory appointment was booked successfully!",
    "googleCalendarLink": ""
}
```
##### ***III. Real Estate Agent Appointment:***
##### ***Endpoint:*** /api/professional/real_estate
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
"Status":201
{
    "googleCalenderEvent": "",
    "real_estate_agent": "Real estate agent appointment was booked successfully!"
}
```
#### ***c. Education And Tutoring🧑‍🏫:***
##### ***I. Academic Advising:***
##### ***Endpoint:*** /api/education_bp/academic
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
"Status":201
{
    "Academic_advising": "Academic advising appointment was booked successfully!",
    "googleCalenderEvent": ""
}
```
##### ***II. Career Counseling:***
##### ***Endpoint:*** /api/education_bp/career
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
"Status":201
{
    "Career_counseling": "Career counseling appointment was booked successfully!",
    "googleCalenderEvent": ""
}
```
##### ***III. One-On-One-Tutoring-Session:***
##### ***Endpoint:*** /api/education_bp/tutoring
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
"Status":201
{
    "googleCalenderEvent": "",
    "one_one_tutoring": "One_on_one tutoring appointment was booked successfully!"
}
```
#### ***d. Technical And Repair Service🛠️🪛:***
##### ***I. Electronics Repair:***
##### ***Endpoint:*** /api/technical/electrical
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
"Status":201
{
    "electronics_repair": "Electrical repair appointment was booked successfully!",
    "googleCalenderEvent": ""
}
```
##### ***II. Home Service:***
##### ***Endpoint:*** /api/technical/home
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
"Status":201
{
    "googleCalenderEvent": "",
    "home_service": "Home service appointment was booked successfully!"
}
```
### ***D. Appointment-Operations:***
#### ***I. Retrieving a user appointment details(GET)***
##### ***Endpoint:*** /api/appointment_act/user_appointment
##### ***Method:*** GET
##### ***Response:***
```json
"Status":200
{
    "user_appointments": [
        {
            "address": "",
            "appointment_date": "",
            "appointment_description": "",
            "appointment_endTime": "",
            "appointment_time": "",
            "appointment_types": "",
            "created_at": "",
            "doctor": "",
            "duration": ,
            "email_address": "",
            "first_name": "",
            "gender": "",
            "hospital": "",
            "id": 27,
            "last_name": "",
            "location": "",
            "next_of_kin": "",
            "next_of_kin_address": "",
            "next_of_kin_phone_number": "",
            "price": ,
            "tel": "",
            "update_at": "",
            "user_id": 4,
            "user_phone_number": ""
        },
        {
            "address": "",
            "appointment_date": "",
            "appointment_description": "",
            "appointment_endTime": "",
            "appointment_time": "",
            "appointment_types": "",
            "created_at": "",
            "doctor": "",
            "duration": ,
            "email_address": "",
            "first_name": "",
            "gender": "",
            "hospital": "",
            "id": 28,
            "last_name": "",
            "location": "",
            "next_of_kin": "",
            "next_of_kin_address": "",
            "next_of_kin_phone_number": "",
            "price": ,
            "tel": "",
            "update_at": "",
            "user_id": 4,
            "user_phone_number": ""
        }
    ]
}
```
#### ***II. Retrieving all users appointment details(GET)***
##### ***Endpoint:*** /api/appointment_act/users_appointment
##### ***Method:*** GET
##### ***Response:***
```json
"Status":200
{
    "All_appointments": [
        {
            "address": "",
            "appointment_date": "",
            "appointment_description": "",
            "appointment_time": "",
            "appointment_types": "",
            "doctor": "",
            "duration": ,
            "email_address": "",
            "first_name": "",
            "gender": "",
            "hospital": "",
            "id":,
            "last_name": "",
            "location": "",
            "next_of_kin": "",
            "next_of_kin_address": "",
            "next_of_kin_phone_number": "",
            "price": ,
            "tel": "",
            "user_id": 2,
            "user_phone_number": ""
        },
        {
            "address": "",
            "appointment_date": "",
            "appointment_description": "",
            "appointment_time": "",
            "appointment_types": "",
            "doctor": "",
            "duration": ,
            "email_address": "",
            "first_name": "",
            "gender": "",
            "hospital": "",
            "id": 26,
            "last_name": "",
            "location": "",
            "next_of_kin_address": "",
            "next_of_kin_phone_number": "",
            "price": ,
            "tel": "",
            "user_id": 2,
            "user_phone_number": ""
        },
        {
            "address": "",
            "appointment_date": "",
            "appointment_description": "",
            "appointment_types": "",
            "doctor": "",
            "duration": ,
            "email_address": "",
            "first_name": "",
            "gender": "",
            "hospital": "",
            "id": 27,
            "last_name": "",
            "location": "",
            "next_of_kin": "",
            "next_of_kin_address": "",
            "next_of_kin_phone_number": "",
            "price":,
            "tel": "",
            "user_id": 4,
            "user_phone_number": ""
        },
        {
            "address": "",
            "appointment_date": "",
            "appointment_description": "",
            "appointment_time": "",
            "appointment_types": "",
            "doctor": "",
            "duration": ,
            "email_address": "",
            "first_name": "",
            "gender": "",
            "hospital": "",
            "id": 28,
            "last_name": "",
            "location": "",
            "next_of_kin": "",
            "next_of_kin_address": "",
            "next_of_kin_phone_number": "",
            "price": ,
            "tel": "",
            "user_id": 4,
            "user_phone_number": ""
        }
    ]
}
```
#### ***III. Updating a user appointment details(PUT)***
##### ***Endpoint:*** /api/appointment_act/update_user_appointment
##### ***Method:*** PUT
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
    "appointment_description":"",
    "appointment_time":"",
    "appointment_date":""
}
```
##### ***Response:***
```json
"Status":200
{
    "user_appointment_info": "☑️ User appointment details updated successfully!"
}
```
#### ***IV. Deleting user appointment details(DELETE)***
##### ***Endpoint:*** /api/appointment_act/delete_appointment
##### ***Method:*** DELETE
##### ***Response:***
```json
"Status":200
{
    "user_appointment_details": "User appointment details was deleted successfully!"
}
```
### ***Base url:***
https://appointment-booking-system-dgpm.onrender.com

### ***Endpoint to get all the routes:***
https://appointment-booking-system-dgpm.onrender.com/debug/routes