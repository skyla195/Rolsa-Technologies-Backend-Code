from fastapi import HTTPException, APIRouter, Header, Body
import json
from models.models import RegisterMethod, LoginMethod, BookingConsultationMethod, BookingInstallationMethod, EnergyUsageMethod, ViewUserDetails

App = APIRouter() 

# using def to get users and save new users to the database. using with open with the url path to the database.json file, and reading and saving data to the file.
def get_users():
    with open ("./database/database.json", "r") as file:
        return json.load(file)
    
def save_new_users(all_users):
    with open ("./database/database.json", "w") as file:
        file.write(json.dumps(all_users, indent=4))

# authenticating sign-up, to see if user can create an account, without exisiting emails and password. 




@App.post("/Sign-up")
def sign_up(register_data:RegisterMethod):
# we are getting all the users from the database
    all_users = get_users()  
    # creating email and password, which will be used to check if email and password already exists or not. 
    email = register_data.email
    password = register_data.password

# checking if email exists in the database
    if email in all_users:
        raise HTTPException(409, "user already exists")
    
# checking if password exists in the database, for any user details

    for user_details in all_users.values():
        if user_details["password"] == password:
            raise HTTPException(409, "Password already used. Use another one.")
    
# if email and password are not used then the new user is created and stores to the database and a message is given back to the user

    new_user = {
        "email": register_data.email,
        "name": register_data.name,
        "password": register_data.password,
    }

    all_users[email] = new_user
    save_new_users(all_users)
    return {"message": "Account created successfully"}



  

#  post method to see if users can log back into their account.  
@App.post("/Login")
def login(login_data: LoginMethod):
    # we are getting all the users from the database
    all_users = get_users()
 # creating name and password, which will be used to check if name and password already exists or not. 
    name = login_data.name
    password = login_data.password

 # iterating over all users in the database, to check if the entered name exists and if the password for that name matches
    for user_emails, user_details in all_users.items():
        if user_details["name"] == name:
            if user_details["password"] == password:
                return_data = {
                    "email" :user_emails,
                    "name" : user_details["name"]
                }
                return {
                    "message": "Login successful",
                    "data":return_data
                }
            else:
                raise HTTPException(401, "incorrect password")
        
    raise HTTPException(404, "User does exists. Try again")





#  post method to see if users can book consultation 
@App.post("/Booking-Consultation")
# the def funciton here, is used to get the attributes  from the booking consultaiton method class
def book_consultation(booking_consultation_data:BookingConsultationMethod):
    # we are getting all the users from the database
    all_users = get_users()

    # creating email, which will be used to check if email already exists or not
    email = booking_consultation_data.email

# if statement is used here, to check if the email entered exists in the database.
# if it does then all the booking information, will be stored inside the entered email
    if email not in all_users:
        raise HTTPException(409, "Email doesn't exists. Use the same email when registered.")

# getting the email key from the database using the get_user() function
    user_details = all_users[email]

# checking to see if the consultationbooking exists or not, if it doesn't than the booking is going to be stored and saved
    if "consultationBookings" not in user_details:
        user_details["consultationBookings"] = []

# here we are checking to see if the same booking is not entered. 
# checking if the same consultation, date and time is not entered in a new booking,
# otherwise, message will be shown
    for checkbookings in user_details["consultationBookings"]:
        if (checkbookings["consultationFor"] == booking_consultation_data.consultationFor
            and checkbookings["date"] == booking_consultation_data.date
            and checkbookings["time"] == booking_consultation_data.time):
            raise HTTPException(409, "Booking already exists.")
        

# if the booking does not exists under the email, then the new booking is created

    new_booking = {
        "scheduleFor": "Consultation",
        "email":booking_consultation_data.email,
        "name":booking_consultation_data.name,
        "phoneNumber":booking_consultation_data.phoneNumber,
        "consultationFor":booking_consultation_data.consultationFor,
        "date":booking_consultation_data.date,
        "time":booking_consultation_data.time,
    }

# the new booking created is added to the consultationBookings in the database 
    user_details["consultationBookings"].append(new_booking)

# and then the the database is updated and a message is given 
    save_new_users(all_users)

    return{"message":"Booking confirmed"}

# the same steps are used for booking installation.
#  post method to see if users can book installation 






@App.post("/Booking-Installation")
def book_installation(booking_installation_data:BookingInstallationMethod):
    # we are getting all the users from the database
    all_users = get_users()
    email = booking_installation_data.email

    if email not in all_users:
        raise HTTPException(409, "Email doesn't exists. Use the same email when registered.")

    user_details = all_users[email]

    if "installationBookings" not in user_details:
        user_details["installationBookings"] = []

    for checkbookings in user_details["installationBookings"]:
        if (checkbookings["installationFor"] == booking_installation_data.installationFor
            and checkbookings["bookingDate"] == booking_installation_data.bookingDate
            and checkbookings["quantity"] == booking_installation_data.quantity
            and checkbookings["cardNumber"] == booking_installation_data.cardNumber):
            raise HTTPException(409, "Booking already exists.")
        

    new_booking = {
        "scheduleFor": "Installation",
        "email":booking_installation_data.email,
        "name":booking_installation_data.name,
        "phoneNumber":booking_installation_data.phoneNumber,
        "homeAddress":booking_installation_data.homeAddress,
        "city":booking_installation_data.city,
        "postCode":booking_installation_data.postCode,
        "bookingDate":booking_installation_data.bookingDate,
        "installationFor":booking_installation_data.installationFor,
        "quantity":booking_installation_data.quantity,
        "cardholderName":booking_installation_data.cardholderName,
        "cardNumber":booking_installation_data.cardNumber,
        "expiryDate":booking_installation_data.expiryDate,
        "cvv":booking_installation_data.cvv,
        "costforInstallation":booking_installation_data.costforInstallation

    }

    user_details["installationBookings"].append(new_booking)

    save_new_users(all_users)

    return{"message":"Booking confirmed"}





@App.post("/Calculate-Energy-Usage")
def energy_usage(energy_usage_data: EnergyUsageMethod):
    print(f"Received data: {energy_usage_data}")  # Log the received data

    all_users = get_users()
    email = energy_usage_data.email

    if email not in all_users:
        raise HTTPException(409, "User not found.")

    user_details = all_users[email]

    if "energyUsages" not in user_details:
        user_details["energyUsages"] = []

    new_energy_record = {
        "month": energy_usage_data.month,
        "power": energy_usage_data.power,
        "time": energy_usage_data.time,
        "totalenergyUsage": energy_usage_data.totalenergyUsage
    }

    user_details["energyUsages"].append(new_energy_record)

    save_new_users(all_users)

    return {
        "message": "Energy usage saved successfully",
        "month": energy_usage_data.month,
        "totalenergyUsage": energy_usage_data.totalenergyUsage
    }


@App.post("/View-Energy-Usage")
def view_energy_usage(user_details: ViewUserDetails):
    all_users = get_users()
    email = user_details.email

    if email not in all_users:
        raise HTTPException(404, "User not found.")

    user_details = all_users[email]

    user_energy_usages = user_details.get("energyUsages", [])

    if not user_energy_usages:
        raise HTTPException(404, "No energy usage records found.")


    return{
        "message": "Your energy usages record",
        "energyUsages": user_energy_usages
        
    }




@App.post("/View-Booking-Details")
def view_booking_details(user_details: ViewUserDetails):
    user_email = user_details.email  # Extract the email from the model
    all_users = get_users()

    if user_email not in all_users:
        raise HTTPException(404, "User  not found.")

    user_details = all_users[user_email]

    user_con_booking_details = user_details.get("consultationBookings", [])
    user_insta_raw_booking_details = user_details.get("installationBookings", [])

    user_insta_booking_details = []
    for bookings in user_insta_raw_booking_details:
        filtered_bookings = {key: value for key, value in bookings.items() if key not in ["cvv", "expiryDate"]}
        user_insta_booking_details.append(filtered_bookings)

    if not user_con_booking_details and not user_insta_booking_details:
        raise HTTPException(404, "No booking records found.")

    return {
        "message": "Your booking details",
        "consultationBookings": user_con_booking_details,
        "installationBookings": user_insta_booking_details        
    }