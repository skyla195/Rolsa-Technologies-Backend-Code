from pydantic import BaseModel

class RegisterMethod(BaseModel):
    email: str
    name: str
    password: str

class LoginMethod(BaseModel):
    name: str
    password: str

class BookingConsultationMethod(BaseModel):  
    email: str
    name: str
    phoneNumber: str
    consultationFor: str
    date: str
    time: str

class BookingInstallationMethod(BaseModel):  
    email: str
    name: str
    phoneNumber: str
    homeAddress: str
    city: str
    postCode: str
    bookingDate: str
    installationFor: str
    quantity: str
    cardholderName: str
    cardNumber: str
    expiryDate: str
    cvv: str
    costforInstallation: float

class EnergyUsageMethod(BaseModel):
    email: str
    month: str
    power: float
    time: float
    totalenergyUsage: float


class ViewUserDetails(BaseModel):
    email: str