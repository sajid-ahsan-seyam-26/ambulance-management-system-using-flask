from flask import Flask , render_template , request , redirect , url_for
app=Flask(__name__)
ambulances = [
    {"id": 1, "plate": "AMB-911", "driver": "Al -Amin", "phone": "+1 555-0191", "status": "Available", "type": "Advanced Life Support", "zone": "Central City"},
    {"id": 2, "plate": "AMB-102", "driver": "Rahman", "phone": "+1 555-0102", "status": "Available", "type": "Basic Life Support", "zone": "North Zone"},
    {"id": 3, "plate": "AMB-777", "driver": "Poran", "phone": "+1 555-0777", "status": "Busy", "type": "ICU Ambulance", "zone": "East Zone"},
    {"id": 4, "plate": "AMB-505", "driver": "Samin Khan", "phone": "+1 555-0505", "status": "Available", "type": "Cardiac Ambulance", "zone": "West Zone"}
]
emergency_requests=[
        {
        "id": 1,
        "patient": "Rafiqul islam",
        "phone": "01816844840",
        "location": "Basundhara Residential Area",
        "condition": "Severe Chest Pain",
        "priority": "Critical",
        "status": "Pending",
        "assigned_ambulance": "None"
    }

]
@app.route('/',method=['GET','POST'])
def index():
    if request=='POST':
        patient_name=request.form['patient_name']
        phone=request.form['phone']
        location=request.form['location']
        condition=request.form['condition']
        priority=request.form['priority']
        new_id=len(emergency_requests)+1
        new_request={
            "id":new_id,
            "patient":patient_name,
            "phone":phone,
            "condition":condition,
            "priority":priority,
            "status":"pending",
            "assigned_ambulance":"None"
        }
        emergency_requests.append((new_request))
        return redirect(url_for('index'))
    return render_template('index.html',request=emergency_requests)
@app.route('/dashboard')
def dashboard():
    total_request=len(emergency_requests)
    pending_requests = len([req for req in emergency_requests if req['status'] == 'Pending'])
    dispatched_requests = len([req for req in emergency_requests if req['status'] == 'Dispatched'])
    completed_requests = len([req for req in emergency_requests if req['status'] == 'Completed'])
    available_ambulances = len([amb for amb in ambulances if amb['status'] == 'Available'])
    stats={
        "total_request":total_request,
        "pending_request":pending_requests,
        "dispatched_request":dispatched_requests,
        "complete_request":completed_requests,
        "available_ambulance":available_ambulances

    }
    return render_template('dashboard.html',ambulances=ambulances,request=emergency_requests,stats=stats)
