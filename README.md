# QR Code Attendance System for Schools

<img src="https://github.com/user-attachments/assets/0179431f-4e54-4b3a-ae12-81a7adb04126" alt="Image." width="1000">

Say goodbye to manual roll calls! Our advanced QR code-based system lets students scan their unique codes upon entry, ensuring real-time, accurate, and hassle-free attendance tracking while enhancing security and reducing paperwork. 🚀

## 📌 Note
Before running the project, create credentials and service accounts by logging into Google Console and download `credentials.json` and `service.json` files. Create a new folder named `credentials` and place these files in it. This enables access to Google Sheets API and Google Drive API.

---

## ✨ Key Features
✅ Automated Attendance Marking – Students scan their QR codes to register attendance instantly.

✅ Secure and Unique Identification – Each student receives a unique QR code, preventing proxy attendance.

✅ Real-Time Tracking & Reporting – Administrators and teachers can monitor attendance records in real time.

✅ Integration with School Management System – Easily integrates with existing student databases for seamless operation.

✅ Cloud-Based Storage – Attendance data is securely stored in the cloud, ensuring reliability, backup, and easy access from any device.

✅ User-Friendly Interface – The system offers a simple and intuitive UI, making it easy for students and administrators to manage attendance records.

✅ Secure Logins – Management and student accounts are secured with authentication.

---

## 🏛 Modules
### 🔹 Management
- Management dashboard to view school attendance statistics and activities.
- Login using predefined credentials.
- Activate, deactivate, or delete users or students.
- View students of all classes.
- View present and absent students.
- Download an Excel sheet of present students.

### 🔹 Student Registration
- Students can securely register to a school account.
- Cannot login until the management activates the student account.

### 🔹 Student Login
- Secure student login to access the dashboard.
- View profile information.
- Download school ID card.

### 🔹 QR Attendance Scanner
- Scans students' QR codes for attendance.
- Updates the present list.
- Posts attendance to Google Sheets through OAuth-verified Google Account.

---

## 📷 Some Screenshots

<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/6bf2ed8f-56a4-4352-9858-031621c7251a" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/774afd71-42d8-429c-908b-b468fb20d847" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/43d1bcba-1d81-4d70-b12a-d93d4c90876e" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/0156efe0-64ff-4566-8504-2ec4b39aea16" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/9bd45419-abc6-414e-8ebd-cd49a3430b9c" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/59014f42-abd1-492f-b954-143818c5b742" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/86487bc1-2572-4260-a0fc-a8cebf134fd2" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/3ed56bc6-2c35-4b0f-8ff3-aa4d8c8c2dbe" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/0afdc150-ba53-4d8f-81c8-51b9b2f1ff16" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/984526dc-9083-4a7f-9ede-bd3c850efa5e" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/9bfd2a0a-8606-48d9-b82c-99932a46088e" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/b8602289-f64c-40c2-a3c7-b3dee08eca16" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/e3dd1b35-2e14-440d-8e22-ef0dee1b76f3" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/cf15a12e-5a37-45e1-a575-c78d84e9c821" />
<img width="500px" alt="Image" src="https://github.com/user-attachments/assets/10e7a2f3-d010-4297-8aef-9d291caaa8a0" />

---

## 🔧 Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/chiruchaitanya77/QR_Attendance_System.git
   ```
2. Navigate to the project directory:
   ```sh
   cd QR_Attendance_System
   ```
3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the development server:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
5. Open your browser and visit: [http://localhost:8000](http://localhost:8000)

---

## 🤝 Contributing
Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```sh
   git checkout -b my-feature
   ```
3. Commit your changes:
   ```sh
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```sh
   git push origin my-feature
   ```
5. Open a pull request.

---

## 🚀 Usage

### Management
- Log in to the management dashboard.
- View attendance statistics.
- Activate/deactivate/delete student accounts.
- View Classes
- Export attendance records.

### Student
- Register and wait for activation.
- Receives a mail of Generated QR Code
- Log in to access the dashboard.
- Download student ID card.

### QR Attendance Scanner
- Scan QR codes.
- Update attendance records.
- Sync data with Google Sheets.

---

Made with ✨ by Chiru Chaitanya

