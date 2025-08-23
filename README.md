# ***Appointment booking system*** 🚀
## ***I used Blueprint routing and not app level routing👌✍️***

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

### ***E. Personnel CRUD operations like:***
- *Uploading list of personnel for all the different kinds of appointments(POST)*
- *Retrieving personnel details from database(GET)*
- *Retrieving all the personnel and their details from database(GET)*
- *Updating personnel information in database(PUT)*
- *Deleting of personnel that is no longer available(DELETE)

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
##### ***Endpoint:*** "/api/user-bp/user"
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
##### ***Endpoint:*** "/api/user-bp/promote"
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
##### ***Endpoint:*** "/api/user-bp/users"
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
##### ***Endpoint:*** "/api/user-bp/update"
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
##### ***Endpoint:*** "/api/user-bp/delete"
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
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
"Status":201
{
    "financial_advisory": "Financial advisory appointment was booked successfully!",
    "googleCalendarLink": ""
}
```
##### ***III. Real Estate Agent Appointment:***
##### ***Endpoint:*** /api/professional/real-estate
##### ***Method:*** POST
##### ***Payload:***
```json
{
    "gender":"",
    "name":"",
    "address":"",
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
"Status":201
{
    "googleCalenderEvent": "",
    "real_estate_agent": "Real estate agent appointment was booked successfully!"
}
```
#### ***c. Education And Tutoring🧑‍🏫:***
##### ***I. Academic Advising:***
##### ***Endpoint:*** /api/education-bp/academic
##### ***Method:*** POST
##### ***Payload:***
```json
{
    "gender":"",
    "name":"",
    "address":"",
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
"Status":201
{
    "Academic_advising": "Academic advising appointment was booked successfully!",
    "googleCalenderEvent": ""
}
```
##### ***II. Career Counseling:***
##### ***Endpoint:*** /api/education-bp/career
##### ***Method:*** POST
##### ***Payload:***
```json
{
    "gender":"",
    "name":"",
    "address":"",
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
"Status":201
{
    "Career_counseling": "Career counseling appointment was booked successfully!",
    "googleCalenderEvent": ""
}
```
##### ***III. One-On-One-Tutoring-Session:***
##### ***Endpoint:*** /api/education-bp/tutoring
##### ***Method:*** POST
##### ***Payload:***
```json
{
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
    "gender":"",
    "name":"",
    "address":"",
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
"Status":201
{
    "googleCalenderEvent": "",
    "home_service": "Home service appointment was booked successfully!"
}
```
### ***D. Appointment-Operations:***
#### ***I. Retrieving a user appointment details(GET)***
##### ***Endpoint:*** /api/appointment-act/user-appointment
##### ***Method:*** GET
##### ***Response:***
```json
"Status":200
{
    "user_appointments": [
        {
            "address": "55c community road, obadore",
            "appointment_date": "Tue, 09 Sep 2025 00:00:00 GMT",
            "appointment_description": "dental appointment",
            "appointment_endTime": "10:30:00",
            "appointment_time": "3:00:00",
            "appointment_types": "AcademicAdvising(EducationAndTutoring)",
            "created_at": "2025-08-16T22:43:06",
            "duration": 90,
            "gender": "male",
            "id": 1,
            "next_of_kin": "ekene",
            "next_of_kin_address": "30c community road, obadore",
            "next_of_kin_phone_number": "07045637823",
            "organization_address": "55c, community road, off lasu-ishere road, lagos state",
            "organization_name": "Healthdpro",
            "personnel_id": 2,
            "personnel_role": "Dentist",
            "personnel_tel": "07034969842",
            "price": 40000.0,
            "update_at": "2025-08-16T22:43:06",
            "user_id": 1,
            "user_phone_number": "07025347099",
            "username": "CHUKWUTEM EMI"
        },
        
    ]
}
```
#### ***III. Updating a user appointment details(PUT)***
##### ***Endpoint:*** /api/appointment-act/update-user-appointment
##### ***Method:*** PUT
##### ***Payload:***
```json
{
    "gender":"",
    "address":"",
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
##### ***Endpoint:*** /api/appointment-act/delete-appointment
##### ***Method:*** DELETE
##### ***Response:***
```json
"Status":200
{
    "user_appointment_details": "User appointment details was deleted successfully!"
}
```
#### ***E. Personnel CRUD operations***:
- *Uploading of personnel into the database*:
##### ***Endpoint:*** /api/personnel-bp/personnel
##### ***Methods:*** POST
##### ***Payloads:***
```json
{
    "name":"",
    "role":"",
    "specialization":"",
    "organization":"",
    "organization_address":"",
    "email": "",
    "phone_number":""
}
```
##### ***Response:***
```json
"Status":201,
{
    "success": "Personnel created and uploaded successfully"
}
```
- *Get a personnel from database*:
##### ***Endpoint:*** /api/personnel-bp/one-personnel
##### ***Methods:*** GET
##### ***Payload:***
```json
{
    "email":""
}
```
##### ***Response:***
```json
"Status":200,
{
    "one-personnel": {
        "email": "",
        "name": "",
        "organization": "",
        "organization_address": "",
        "phone_number": "",
        "role": "",
        "specialization": ""
    }
}
```
- *Get all personnel from database*
##### ***Endpoint:*** /api/personnel-bp/all-personnel
##### ***Methods:*** GET
##### ***Response:***
```json
"Status":200
{
    "all-personnel": [
        {
            "email": "",
            "id": ,
            "name": "",
            "organization": "",
            "organization_address": "",
            "phone_number": "",
            "role": "",
            "specialization": ""
        }
    ]
}
```
- *Updated personnel information*:
##### ***Endpoint:*** /api/personnel-bp/update-personnel
##### ***Methods:*** PUT
##### ***Payload:***
```json
{
    "name":"",
    "role":"",
    "specialization":"",
    "organization":"",
    "organization_address":"",
    "email": "",
    "phone_number":""
}
```
##### ***Response:***
```json
"Status":200
{
    "updated": "Personnel information was updated successfully!."
}
```
- *Delete personnel from database*:
##### ***Endpoint:***/api/personnel-bp/delete-personnel
##### ***Methods:*** DELETE
##### ***Response:***
```json
"status":200
{
    "deleted": "The deletion of personnel was successful"
}
```
## ***I also created some features that i will use to lock the APP in situations when the APP is undergoing maintenance or if the APP is under cyber attack. These features are found in App.py file***


### ***Base url:***
https://appointment-booking-system-dgpm.onrender.com

### ***Endpoint to get all the routes:***
https://appointment-booking-system-dgpm.onrender.com/debug/routes