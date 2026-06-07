from fastapi import FastAPI,HTTPException,Header,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
import mysql.connector
import bcrypt

app = FastAPI()

security = HTTPBearer()
SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: str
   

class patients(BaseModel):
    patient_id:str
    name:str
    age : int 
    gender : str 
    city : str
    phone:str 
    height:float
    weight:float
    bmi:float
    verdict:str
    created_at:datetime
    updated_at:datetime
    
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="clinic_user",
        password="1234",
        database="smart_clinic"
    )
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
@app.get("/")
def home():
    return {"message": "Smart Clinic API Running"}
@app.post("/register")
def register_user(user: UserRegister):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (user.email,)
    )
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")
    cursor.execute(
        """
        INSERT INTO users
        (username,email,password,role)
        VALUES (%s,%s,%s,%s)
        """,
        (user.username, user.email, hashed_password, user.role)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User Registered Successfully"}




@app.post("/login")
def login_user(email:str,password:str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )
    
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    stored_password = user[3]
    if not bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = create_access_token(
    {
        "id": user[0],
        "email": user[2],
        "role": user[4]
    })   
    return {
    "message": "Login Successful",
    "access_token": token,
    "token_type": "bearer"
}
    
@app.post("/patients")
def create_patient(
    patient: patients,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Token verify karo
    token = credentials.credentials
    user = verify_token(token)
    doctor_email = user["email"]
    if not doctor_email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # DB mein save karo
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO patients 
            (patient_id, name, age, gender, city, phone, height, weight, bmi, verdict, created_at, updated_at,created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
            """,
            (
                patient.patient_id,
                patient.name,
                patient.age,
                patient.gender,
                patient.city,
                patient.phone,
                patient.height,
                patient.weight,
                patient.bmi,
                patient.verdict,
                patient.created_at,
                patient.updated_at,
                doctor_email
            )
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")

    finally:
        cursor.close()
        conn.close()

    return {
        "message": "Patient Created Successfully",
        "patient_id": patient.patient_id,
        "created_by": user["email"]
    }
@app.get("/patients")
def get_my_patients(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    user = verify_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    doctor_email = user["email"]

    conn = get_db()
    cursor = conn.cursor(dictionary=True)   # ⭐ IMPORTANT FIX

    try:
        cursor.execute(
            "SELECT * FROM patients WHERE created_by=%s",
            (doctor_email,)
        )

        rows = cursor.fetchall()

        return {
            "doctor": doctor_email,
            "total_patients": len(rows),
            "patients": rows
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()
@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = verify_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    conn.close()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient
@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = verify_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE patient_id=%s",
        (patient_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Patient deleted successfully"
    }
@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: str,
    patient: patients
    ,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = verify_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """ Update patients
         SET
            name=%s,
            age=%s,
            city=%s,
            phone=%s,
            height=%s,
            weight=%s,
            bmi=%s,
            verdict=%s
        WHERE patient_id=%s
        """,
        (
            patient.name,
            patient.age,
            patient.city,
            patient.phone,
            patient.height,
            patient.weight,
            patient.bmi,
            patient.verdict,
            patient_id
        )
        
      
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "message": "Patient Updated Successfully"

    }
@app.get("/patients/search/{name}")
def search_patient(
    name: str,
    
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user = verify_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM patients WHERE name=%s",
        (name,)
    )

    patients = cursor.fetchall()

    cursor.close()
    conn.close()

    if not patients:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patients



