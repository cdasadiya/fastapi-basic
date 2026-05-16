from fastapi import FastAPI,Path, HTTPException,Query
import json

app = FastAPI()

def load_data():
    return json.load(open("patients.json"))

@app.get("/")
def read_root():
    return {"message": "Patient management API "}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/about")
def read_about():
    return {"message": "Fully Functional API  to manage the patient records"}


@app.get("/view")
def view_patients():
    return load_data()

@app.get("/view/patient/{patient_id}")
def view_patiend_record(patient_id: str = Path(...,title="Patient ID",description="Patient ID for the patients to be viewed:",examples=["P001","P002","P003"])  ):
    data = load_data()
    if patient_id in data:
        return data.get(patient_id)
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort/patient")
def sort_patients(sort_by : str = Query(...,description="Sort Key for the patients to be sorted:height,weight,bmi"),
        order: str = Query("asc", description="Order of the patients to be sorted:asc,desc")):
    
    valid_fields = ["height","weight","bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail="Invalid order select between asc and desc")
    
    data = load_data()
    sort_order=True if order =='desc' else False
    return sorted(data.values(),key=lambda x: x.get(sort_by),reverse=sort_order)



