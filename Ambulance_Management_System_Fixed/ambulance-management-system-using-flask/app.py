from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "ambulance-demo-secret-key"

# --- MOCK DATABASE (Easy for beginners to read and modify) ---
ambulances = [
    {"id": 1, "plate": "AMB-911", "driver": "Al-Amin", "phone": "01816844840", "status": "Available", "type": "Advanced Life Support", "zone": "Uttara"},
    {"id": 2, "plate": "AMB-102", "driver": "Rahman", "phone": "01816844841", "status": "Available", "type": "Basic Life Support", "zone": "Banani"},
    {"id": 3, "plate": "AMB-777", "driver": "Poran", "phone": "01816844842", "status": "Busy", "type": "ICU Ambulance", "zone": "East Zone"},
    {"id": 4, "plate": "AMB-505", "driver": "Samin Khan", "phone": "01816844843", "status": "Available", "type": "Cardiac Ambulance", "zone": "Badda"}
]

emergency_requests = [
    {
        "id": 1,
        "patient": "Rafiqul Islam",
        "phone": "01816844840",
        "location": "Basundhara Residential Area",
        "condition": "Severe Chest Pain",
        "priority": "Critical",
        "status": "Pending",
        "assigned_ambulance": "None"
    }
]


def get_next_request_id():
    """Return a safe new request ID even if records are edited later."""
    if not emergency_requests:
        return 1
    return max(req["id"] for req in emergency_requests) + 1


def find_request(req_id):
    return next((req for req in emergency_requests if req["id"] == req_id), None)


def find_ambulance(ambulance_id):
    return next((amb for amb in ambulances if amb["id"] == ambulance_id), None)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name', '').strip()
        phone = request.form.get('phone', '').strip()
        location = request.form.get('location', '').strip()
        condition = request.form.get('condition', '').strip()
        priority = request.form.get('priority', 'Medium').strip()

        if not patient_name or not phone or not location or not condition:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))

        new_request = {
            "id": get_next_request_id(),
            "patient": patient_name,
            "phone": phone,
            "location": location,
            "condition": condition,
            "priority": priority,
            "status": "Pending",
            "assigned_ambulance": "None"
        }

        emergency_requests.append(new_request)
        flash('Emergency request submitted successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', requests=emergency_requests)


@app.route('/dashboard')
def dashboard():
    total_requests = len(emergency_requests)
    pending_requests = len([req for req in emergency_requests if req['status'] == 'Pending'])
    dispatched_requests = len([req for req in emergency_requests if req['status'] == 'Dispatched'])
    completed_requests = len([req for req in emergency_requests if req['status'] == 'Completed'])
    available_ambulances_count = len([amb for amb in ambulances if amb['status'] == 'Available'])

    stats = {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "dispatched_requests": dispatched_requests,
        "completed_requests": completed_requests,
        "available_ambulances": available_ambulances_count
    }

    return render_template(
        'dashboard.html',
        ambulances=ambulances,
        requests=emergency_requests,
        stats=stats
    )


@app.route('/assign/<int:req_id>', methods=['POST'])
def assign_ambulance(req_id):
    """Assign an available ambulance to a pending emergency request."""
    req = find_request(req_id)

    try:
        ambulance_id = int(request.form.get('ambulance_id', 0))
    except ValueError:
        ambulance_id = 0

    amb = find_ambulance(ambulance_id)

    if req is None:
        flash('Emergency request not found.', 'error')
        return redirect(url_for('dashboard'))

    if req['status'] != 'Pending':
        flash('Only pending requests can be dispatched.', 'error')
        return redirect(url_for('dashboard'))

    if amb is None:
        flash('Please select a valid ambulance.', 'error')
        return redirect(url_for('dashboard'))

    if amb['status'] != 'Available':
        flash('This ambulance is already busy. Please select another one.', 'error')
        return redirect(url_for('dashboard'))

    req['status'] = 'Dispatched'
    req['assigned_ambulance'] = amb['plate']
    amb['status'] = 'Busy'

    flash(f"{amb['plate']} has been dispatched to {req['patient']}.", 'success')
    return redirect(url_for('dashboard'))


@app.route('/complete/<int:req_id>')
def complete_request(req_id):
    req = find_request(req_id)

    if req is not None:
        req['status'] = 'Completed'

        for amb in ambulances:
            if amb['plate'] == req['assigned_ambulance']:
                amb['status'] = 'Available'
                break

    return redirect(url_for('dashboard'))


@app.route('/reset')
def reset_demo():
    for amb in ambulances:
        if amb['plate'] != 'AMB-777':
            amb['status'] = 'Available'
        else:
            amb['status'] = 'Busy'

    for req in emergency_requests:
        if req['status'] != 'Completed':
            req['status'] = 'Pending'
            req['assigned_ambulance'] = 'None'

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
