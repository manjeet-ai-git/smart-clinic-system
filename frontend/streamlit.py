import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Smart Clinic",
    page_icon="🏥",
    layout="wide"
)

# ================= SESSION =================
if "token" not in st.session_state:
    st.session_state.token = None

# ================= CSS =================
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #1f3c88;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ================= HOME (LOGIN / REGISTER) =================
if not st.session_state.token:

    st.markdown("<div class='title'>🏥 Smart Clinic System</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    # -------- LOGIN --------
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", key="login_password")


        if st.button("Login"):
            res = requests.post(
                f"{API}/login",
                params={"email": email, "password": password}
            )

            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    # -------- REGISTER --------
    with tab2:
        username = st.text_input("Username")
        email_r = st.text_input("Email (Register)")
        password_r = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["doctor", "patient"])

        if st.button("Register"):
            payload = {
                "username": username,
                "email": email_r,
                "password": password_r,
                "role": role
            }

            res = requests.post(f"{API}/register", json=payload)

            st.write(res.json())

# ================= DASHBOARD =================
else:

    st.markdown("<div class='title'>🏥 Dashboard</div>", unsafe_allow_html=True)

    st.sidebar.success("Logged in ✔")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Add Patient",
            "View Patients",
            "Search by ID",
            "Search by Name",
            "Logout"
        ]
    )

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # -------- DASHBOARD --------
    if menu == "Dashboard":

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Patients", "120")

        with col2:
            st.metric("Doctors", "12")

        with col3:
            st.metric("Appointments", "35")

    # -------- ADD PATIENT --------
    elif menu == "Add Patient":

        st.subheader("➕ Add Patient")

        pid = st.text_input("Patient ID")
        name = st.text_input("Name")
        age = st.number_input("Age", 1, 120)

        gender = st.selectbox("Gender", ["Male", "Female"])
        city = st.text_input("City")
        phone = st.text_input("Phone")

        height = st.number_input("Height")
        weight = st.number_input("Weight")

        bmi = round(weight / ((height/100)**2), 2) if height > 0 else 0

        verdict = st.selectbox("Verdict", ["Normal", "Overweight", "Underweight"])

        if st.button("Save Patient"):

            payload = {
                "patient_id": pid,
                "name": name,
                "age": age,
                "gender": gender,
                "city": city,
                "phone": phone,
                "height": height,
                "weight": weight,
                "bmi": bmi,
                "verdict": verdict,
                "created_at": "2026-01-01T00:00:00",
                "updated_at": "2026-01-01T00:00:00"
            }

            res = requests.post(f"{API}/patients", json=payload, headers=headers)

            st.success(res.json())

    # -------- VIEW PATIENTS --------
    elif menu == "View Patients":

        res = requests.get(f"{API}/patients", headers=headers)

        if res.status_code == 200:
            st.dataframe(res.json()["patients"], use_container_width=True)

    # -------- SEARCH BY ID --------
    elif menu == "Search by ID":

        pid = st.text_input("Enter Patient ID")

        if st.button("Search"):

            res = requests.get(f"{API}/patients/{pid}", headers=headers)

            if res.status_code == 200:
                st.json(res.json())
            else:
                st.error("Patient not found")

    # -------- SEARCH BY NAME --------
    elif menu == "Search by Name":

        name = st.text_input("Enter Name")

        if st.button("Search"):

            res = requests.get(f"{API}/patients/search/{name}", headers=headers)

            if res.status_code == 200:
                st.dataframe(res.json())
            else:
                st.error("No result found")

    # -------- LOGOUT --------
    elif menu == "Logout":

        st.session_state.token = None
        st.success("Logged out successfully")
        st.rerun()