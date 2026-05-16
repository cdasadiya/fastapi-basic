from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

class Patient(BaseModel):
    id: str
    #name: str = Field(max_length=50, min_length=2, description="Name of the patient")
    name: str = Field(max_length=50, min_length=2, description="Name of the patient")
    
    email : EmailStr
    linkedin_url : AnyUrl
    age: int
    gender: str
    height: float
    weight: float = Field(gt=0,lt=500,description="Weight of the patient")
    married : bool
    allergies : Optional[List[str]]=None 
    contact_info : Dict[str,str]

    # by default all fiels are required if not provide default value then it will throw error
    # Optional for used the optional value into the class
    # EmailStr for used the email validation
    # AnyUrl for used the url validation

def display_patient(patient: Patient):
    print("Patient ID: ",patient.id)
    print("Patient Name: ",patient.name)
    print("Patient Email: ",patient.email)
    print("Patient LinkedIn URL: ",patient.linkedin_url)
    print("Patient Age: ",patient.age)
    print("Patient Gender: ",patient.gender)
    print("Patient Height: ",patient.height)
    print("Patient Weight: ",patient.weight)
    print("Patient Married: ",patient.married)
    print("Patient Allergies: ",patient.allergies)
    print("Patient Contact Info: ",patient.contact_info)

patient_info = {
 'id':"1001",
 'name':"Chaitanya Dasadiya",
 'email':"cdasadiya@gmail.com",
 'linkedin_url':"https://www.linkedin.com/in/johndoe/",
 'age':30,
 'gender':"Male",
 'height':5.9,
 'weight':120,
 'married':True,
 'allergies':["Peanut Allergy"],
 'contact_info':{
    "phone":"123-456-7890",
    "email":"abc@gmail.com",
    "address":"123 Main St"
 }

}

patient_info = Patient(**patient_info)
display_patient(patient_info)
