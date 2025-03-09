from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import qrcode, cv2, numpy, threading, smtplib, json, re, datetime, os
from .models import Student, Present
from django.conf import settings
from email.message import EmailMessage
from django.utils.timezone import now
from googleapiclient.discovery import build
import google.auth
from google.oauth2 import service_account
import google.oauth2.credentials
from django.shortcuts import redirect, render
import google_auth_oauthlib.flow

@csrf_exempt  # Disable CSRF for testing/development; remove this in production if not necessary
def otp(request):
    if request.method == 'POST':
        try:
            # Parse JSON from the POST request body
            data = json.loads(request.body)
            email = data.get('email')
            qr_url = data.get('qr_url')

            # Debug: Print email and QR URL
            # print(f"Email: {email}, QR URL: {qr_url}")

            if not email or not qr_url:
                return JsonResponse({"error": "Missing email or QR code URL"}, status=400)

            # Full path to the QR code
            qr_full_path = os.path.join(settings.MEDIA_ROOT, qr_url.lstrip('/media/'))
            # print(f"Full QR path: {qr_full_path}")

            if not os.path.exists(qr_full_path):
                # print(f"File not found at path: {qr_full_path}")
                return JsonResponse({"error": "QR code file not found"}, status=404)

            def send_email():
                from_mail = 'chak7755@gmail.com'
                to_mail = email
                msg = EmailMessage()
                msg['subject'] = 'QR Code Created Successfully'
                msg['from'] = from_mail
                msg['to'] = to_mail
                msg.set_content(f"Hello,\n\nYour Student Unique QR Code has been generated successfully.")
                try:
                    with open(qr_full_path, 'rb') as qr_file:
                        msg.add_attachment(
                            qr_file.read(),
                            maintype='image',
                            subtype='png',
                            filename=os.path.basename(qr_full_path)  # Attach the file with the original name
                        )

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(from_mail, 'hdyy zqsp bmha cyrn')  # Note: Keep credentials secure
                    server.send_message(msg)
                    server.quit()
                    print("Email sent successfully!")
                except FileNotFoundError:
                    print("QR code file not found.")
                except smtplib.SMTPException as e:
                    print(f"Failed to send email: {e}")

            # Start a new thread for sending the email to avoid blocking
            threading.Thread(target=send_email).start()

            return JsonResponse({"message": "OTP email sent successfully."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
def index(request):
    return render(request,'index.html')
def exit(request):
    return render(request, 'exit.html')
def idcard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Unauthorized access. Please log in.")
        return redirect('userlogin')
    # Fetch student details based on ID
    student = Student.objects.filter(id=user_id).first()
    return render(request, 'idcard.html', {'studentdetails': student})

def userRegister(request):
    context = {
        'classes': range(1, 11)
    }
    if request.method == 'POST':
        studentname = request.POST.get('studentname', '').strip()
        roll = request.POST.get('roll', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        dob = request.POST.get('dob', '').strip()
        address = request.POST.get('address', '').strip()
        classes = request.POST.get('classes', '').strip()
        blood = request.POST.get('blood', '').strip()
        college = request.POST.get('college', '').strip()
        password = request.POST.get('password', '').strip()
        status = request.POST.get('status', '').strip()

        if Student.objects.filter(roll=roll).exists():
            messages.error(request, "Roll Number already taken!")
            return render(request, 'userRegister.html')

        if Student.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile Number already registered!")
            return render(request, 'userRegister.html')

        user = Student(studentname=studentname, roll=roll, email=email, mobile=mobile, dob=dob, address=address, classes=classes, blood=blood, college=college, password=password, status=status)
        user.save()

        # Store the user's ID in the session
        request.session['student_id'] = user.id
        request.session['send_email'] = True

        return redirect('/userlogin')
    return render(request, 'userRegister.html', context)
def userlogin(request):
    if request.method == 'POST':
        studentname = request.POST.get('studentname')
        password = request.POST.get('password')
        try:
            user = Student.objects.get(studentname=studentname)
            if user.password == password:
                if user.status == "Waiting":
                    messages.info(request,"Your account status is currently Waiting. Please wait until it is activated.")
                    return render(request, 'userlogin.html')

                # Store user ID in session to persist across views
                request.session['user_id'] = user.id

                if request.session.get('send_email'):
                    del request.session['send_email']

                # Redirect to userhome without using GET parameters
                return redirect('/userhome')

            else:
                messages.error(request, "Invalid studentname or password!")
                return render(request, 'userlogin.html')

        except Student.DoesNotExist:
            messages.error(request, "Studentname or password is incorrect")
            return render(request, 'userlogin.html')

    return render(request, 'userlogin.html')
def userhome(request):
    # Retrieve user ID from session
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Unauthorized access. Please log in.")
        return redirect('userlogin')
    # Fetch student details based on ID
    student = Student.objects.filter(id=user_id).first()
    return render(request, 'userhome.html', {'studentdetails': student})

def adminlogin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            if name == 'admin' and password == 'admin':
                return redirect('/adminhome')
            else:
                messages.error(request, "Invalid username or password!")
                return render(request, 'adminlogin.html')
        except Student.DoesNotExist:
            messages.error(request, "Username or password is incorrect")
            return render(request, 'adminlogin.html')
    return render(request, 'adminlogin.html')

def adminhome(request):
    selected_date = now().date()  # Default to today if invalid format
    #Fetch all classes
    total_classes = Student.objects.values_list('classes', flat=True).distinct().count()
    # Fetch all students
    total_students = Student.objects.count()
    # Get present students for selected date
    present_students = Present.objects.filter(date=selected_date).count()
    present = Present.objects.filter(date=selected_date)
    # Absent students = Total students - Present students
    absent_students = total_students - present_students
    # Fetch distinct classes from the Student table
    classes_with_students = Student.objects.values_list('classes', flat=True).distinct()
    return render(request, 'adminhome.html', {
        "total_classes": total_classes,
        'total_students': total_students,
        'present_students': present_students,
        'present': present,
        'absent_students': absent_students,
        'selected_date': selected_date
    })
def students(request):
    user = Student.objects.all()
    # Get filter values from request
    student_id = request.GET.get('id', '').strip()
    roll_number = request.GET.get('roll', '').strip()
    blood_group = request.GET.get('blood_group', '').strip()
    mobile_number = request.GET.get('mobile', '').strip()
    student_class = request.GET.get('class', '').strip()
    status = request.GET.get('status', '').strip()  # Active or Waiting
    # Apply filters dynamically
    if student_id:
        user = user.filter(id=student_id)
    if roll_number:
        user = user.filter(roll=roll_number)
    if blood_group:
        user = user.filter(blood__iexact=blood_group)
    if mobile_number:
        user = user.filter(mobile__icontains=mobile_number)
    if student_class:
        user = user.filter(classes__iexact=student_class)
    if status:
        user = user.filter(status__iexact=status)  # Assuming status is stored as a string (Active/Waiting)
    return render(request, 'students.html', {'userdetails': user})

def presents(request):
    selected_date = request.GET.get('date', now().date())  # Get date from request or default to today

    try:
        selected_date = now().strptime(str(selected_date), "%Y-%m-%d").date()  # Convert string to date
    except ValueError:
        selected_date = now().date()  # Default to today if invalid date format

    if selected_date > now().date():  # Prevent future date selection
        return render(request, 'presents.html',
                      {'error': "You cannot select a future date!", 'selected_date': now().date()})

    present_students = Present.objects.filter(date=selected_date)  # Fetch present students for the selected date

    return render(request, 'presents.html', {'userdetails': present_students, 'selected_date': selected_date})
def absents(request):
    selected_date = request.GET.get('date', now().date())  # Get date from request or default to today
    try:
        selected_date = now().strptime(str(selected_date), "%Y-%m-%d").date()  # Convert string to date
    except ValueError:
        selected_date = now().date()  # Default to today if invalid date format
    if selected_date > now().date():  # Future date validation
        return render(request, 'absents.html', {'error': "You cannot select a future date!", 'selected_date': now().date()})
    st = Student.objects.all()  # Fetch all students
    pr = Present.objects.filter(date=selected_date).values_list('roll', flat=True)  # Get present roll numbers for the date
    absent_students = [student for student in st if student.roll not in pr]  # Filter absentees
    return render(request, 'absents.html', {'absent_students': absent_students, 'selected_date': selected_date})

def classes(request):
    user = Student.objects.all()
    return render(request, 'classes.html',{'userdetails': user})

def activateuser(request):
    print(request.GET)
    id = request.GET.get('id')  # Fetch id from query parameters
    ur = Student.objects.get(id=id)
    ur.status = 'Active'
    ur.save()
    return redirect('/students')
def deactivateuser(request):
    print(request.GET)
    id = request.GET.get('id')  # Fetch id from query parameters
    ur = Student.objects.get(id=id)
    ur.status = 'Waiting'
    ur.save()
    return redirect('/students')
def deleteuser(request):
    print(request.GET)
    id = request.GET.get('id')
    ur = Student.objects.get(id=id)
    ur.delete()
    return redirect('/students')

def qrcodeimg(request):
    # Fetch student from the database
    id = request.GET.get('id')

    if not id:
        return HttpResponse("Invalid request. Missing student ID.", status=400)

    student = Student.objects.filter(id=id).first()  # Get one specific student

    if not student:
        return HttpResponse("Student not found", status=404)

    # Prepare QR code data
    # studentname,mobile,roll,classes,blood,college
    qr_data = f"{student.studentname},{student.mobile},{student.roll},{student.classes},{student.blood},{student.college}"
    # print(f"QR Data: {qr_data}")

    # Define the path to save the QR code
    qr_directory = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    os.makedirs(qr_directory, exist_ok=True)  # Ensure directory exists

    qr_filename = re.sub(r'[^\w\-_. ]', '_', f"{student.studentname}_{student.roll}.png")

    qr_path = os.path.join(qr_directory, qr_filename)

    # Check if QR code already exists
    if not os.path.exists(qr_path):
        # Generate and save QR code only if it doesn't exist
        qr = qrcode.make(qr_data)
        qr.save(qr_path)

        # Save the path to the student model (if needed)
        student.qr = f"qrcodes/{qr_filename}"  # Save relative path
        student.save(update_fields=['qr'])  # Update only the 'qr' field

    # Return QR URL and email in a JSON response
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            "qr_url": f"{settings.MEDIA_URL}qrcodes/{qr_filename}",
            "email": student.email
        })

    return redirect('/idcard')  # Redirect to the ID card page

@csrf_exempt
def QRattendance(request):
    if 'processed_qr_codes' not in request.session:
        request.session['processed_qr_codes'] = []

    processed_qr_codes = set(request.session['processed_qr_codes'])

    if request.method == 'POST':
        # Get the image from the POST request
        image_file = request.FILES.get('frame')

        if image_file:
            # Convert image file to numpy array
            nparr = numpy.frombuffer(image_file.read(), numpy.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Use OpenCV to detect QR codes
            qr_detector = cv2.QRCodeDetector()
            data, bbox, _ = qr_detector.detectAndDecode(frame)

            if data:
                data = data.strip()

                # Parse the data
                try:
                    studentname, mobile, roll, classes, blood, college = data.split(',')

                    # Get the current date in 'YYYY-MM-DD' format
                    date = datetime.datetime.now().strftime('%Y-%m-%d')

                    # Update Google Sheet with the new data
                    update_google_sheet(request, studentname, mobile, roll, classes, blood, college, date)

                    # Check if an entry already exists in the database for the same student and date
                    if not Present.objects.filter(roll=roll, date=date).exists():
                        user = Present(studentname=studentname, roll=roll, mobile=mobile, classes=classes, college=college, date=date)
                        user.save()

                    # Add this QR code data to the set of processed codes
                    processed_qr_codes.add(data)

                    # Save the updated set to the session
                    request.session['processed_qr_codes'] = list(processed_qr_codes)
                    request.session.modified = True  # Ensure the session is saved

                    return JsonResponse({'qr_code': data})
                except ValueError:
                    return JsonResponse({'error': 'Invalid QR code format'}, status=400)
    return render(request, 'QRattendance.html')

# # Path to your credentials.json
# CREDENTIALS_PATH = os.path.join("credentials", "credentials.json")
# SCOPES = ['https://www.googleapis.com/auth/drive',
#           'https://www.googleapis.com/auth/documents',
#           'https://www.googleapis.com/auth/spreadsheets'
#          ]

# # Specify the sheet to update
# SPREADSHEET_ID = '1OECWblIzGxduK6Kjo8j5TtC55Fs89at-J5ui1UPq_mU'  # Replace with your Google Doc ID

# # OAuth redirect URI
# REDIRECT_URI = "http://localhost:8000/oauth2callback"  # Ensure this is the same URI you configured in Google Cloud Console

# def google_auth(request):
#     # Initialize the OAuth flow
#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         CREDENTIALS_PATH, scopes=SCOPES
#     )
#     flow.redirect_uri = REDIRECT_URI

#     # Generate the authorization URL
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true'
#     )

#     # Save the state in the session for validation after the callback
#     request.session['state'] = state

#     # Redirect to the Google OAuth consent page
#     return redirect(authorization_url)

# def oauth2callback(request):
#     # Retrieve the state saved in the session
#     state = request.session.get('state')

#     # Recreate the OAuth flow to exchange the authorization code
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         CREDENTIALS_PATH, scopes=SCOPES, state=state
#     )
#     flow.redirect_uri = REDIRECT_URI

#     # Exchange the authorization code for credentials
#     authorization_response = request.build_absolute_uri()
#     flow.fetch_token(authorization_response=authorization_response)

#     # Save credentials in the session
#     credentials = flow.credentials
#     request.session['credentials'] = {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes
#     }

#     return redirect('QRattendance')  # Redirect to the update form after authentication

# # Function to update a Google Sheets with user input (Main Changes)
# def update_google_sheet(request, studentname, mobile, roll, classes, blood, college, date):
#     if 'credentials' not in request.session:
#         return redirect('google_auth')

#     credentials = google.oauth2.credentials.Credentials(
#         **request.session['credentials']
#     )

#     # Connect to Google Sheets API
#     service = build('sheets', 'v4', credentials=credentials)

#     # Specify the spreadsheet to update
#     SPREADSHEET_ID = '1OECWblIzGxduK6Kjo8j5TtC55Fs89at-J5ui1UPq_mU'
#     # Specify the range to append the data to
#     RANGE = 'Sheet1!A:G'  # Ensure enough columns are specified for the data

#     result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
#     existing_values = result.get('values', [])

#     # Normalize new row
#     new_row = [studentname.strip(), mobile.strip(), roll.strip(), classes.strip(), blood.strip(), college.strip(), date.strip()]

#     # Check for duplicates in existing values
#     if new_row in existing_values:
#         return  # Exit without updating if the row is already present

#     # Body of the request
#     body = {
#         'values': [new_row]
#     }

#     # Append the data to the sheet
#     service.spreadsheets().values().append(
#         spreadsheetId=SPREADSHEET_ID,
#         range=RANGE,
#         valueInputOption='RAW',
#         insertDataOption='INSERT_ROWS',
#         body=body
#     ).execute()

# SERVICE_PATH = os.path.join("credentials", "service-account.json")
# def download_sheet(request):
#     # Load credentials manually
#     creds = service_account.Credentials.from_service_account_file(
#         SERVICE_PATH, scopes=SCOPES
#     )
#     # Initialize Google Drive API service
#     drive_service = build("drive", "v3", credentials=creds)

#     # File ID (same as Spreadsheet ID)
#     FILE_ID = "1OECWblIzGxduK6Kjo8j5TtC55Fs89at-J5ui1UPq_mU"

#     try:
#         # Export file as Excel (.xlsx)
#         request = drive_service.files().export(
#             fileId=FILE_ID,
#             mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )

#         # Get file content
#         file_content = request.execute()

#         # Create HTTP response for file download
#         response = HttpResponse(file_content,
#                                 content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#         response["Content-Disposition"] = 'attachment; filename="google_sheet.xlsx"'

#         return response  # ✅ Now returning an HTTP Response!

#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}", status=500)



# Path to your credentials.json
# CREDENTIALS_PATH = os.path.join("credentials", "credentials.json")
credentials_json = os.getenv('GOOGLE_CREDENTIALS')

if not credentials_json:
    raise ValueError("Google OAuth credentials not found in environment variables")

    # Decode the base64 credentials
credentials_data = json.loads(base64.b64decode(credentials_json).decode('utf-8'))

SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/spreadsheets'
         ]

# Specify the sheet to update
SPREADSHEET_ID = '1OECWblIzGxduK6Kjo8j5TtC55Fs89at-J5ui1UPq_mU'  # Replace with your Google Doc ID

# OAuth redirect URI
REDIRECT_URI = "http://localhost:8000/oauth2callback"  # Ensure this is the same URI you configured in Google Cloud Console

def google_auth(request):
    # Initialize OAuth flow
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        credentials_data, scopes=SCOPES
    )

    # # Initialize the OAuth flow
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     CREDENTIALS_PATH, scopes=SCOPES
    # )
    flow.redirect_uri = REDIRECT_URI

    # Generate the authorization URL
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    # Save the state in the session for validation after the callback
    request.session['state'] = state

    # Redirect to the Google OAuth consent page
    return redirect(authorization_url)

def oauth2callback(request):
    # Retrieve the state saved in the session
    state = request.session.get('state')

    # # Recreate the OAuth flow to exchange the authorization code
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    #     CREDENTIALS_PATH, scopes=SCOPES, state=state
    # )
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        credentials_data, scopes=SCOPES, state=state
    )
    flow.redirect_uri = REDIRECT_URI

    # Exchange the authorization code for credentials
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Save credentials in the session
    credentials = flow.credentials
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect('QRattendance')  # Redirect to the update form after authentication

# Function to update a Google Sheets with user input (Main Changes)
def update_google_sheet(request, studentname, mobile, roll, classes, blood, college, date):
    if 'credentials' not in request.session:
        return redirect('google_auth')

    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials']
    )

    # Connect to Google Sheets API
    service = build('sheets', 'v4', credentials=credentials)

    # Specify the spreadsheet to update
    SPREADSHEET_ID = '1OECWblIzGxduK6Kjo8j5TtC55Fs89at-J5ui1UPq_mU'
    # Specify the range to append the data to
    RANGE = 'Sheet1!A:G'  # Ensure enough columns are specified for the data

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    existing_values = result.get('values', [])

    # Normalize new row
    new_row = [studentname.strip(), mobile.strip(), roll.strip(), classes.strip(), blood.strip(), college.strip(), date.strip()]

    # Check for duplicates in existing values
    if new_row in existing_values:
        return  # Exit without updating if the row is already present

    # Body of the request
    body = {
        'values': [new_row]
    }

    # Append the data to the sheet
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()

SERVICE_PATH = os.path.join("credentials", "service-account.json")
def download_sheet(request):
    # Load credentials manually
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_PATH, scopes=SCOPES
    )
    # Initialize Google Drive API service
    drive_service = build("drive", "v3", credentials=creds)

    # File ID (same as Spreadsheet ID)
    FILE_ID = "1OECWblIzGxduK6Kjo8j5TtC55Fs89at-J5ui1UPq_mU"

    try:
        # Export file as Excel (.xlsx)
        request = drive_service.files().export(
            fileId=FILE_ID,
            mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Get file content
        file_content = request.execute()

        # Create HTTP response for file download
        response = HttpResponse(file_content,
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="google_sheet.xlsx"'

        return response  # ✅ Now returning an HTTP Response!

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)



