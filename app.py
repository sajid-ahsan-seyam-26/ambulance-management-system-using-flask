from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ambulances = [
    {"id": 1, "plate": "AMB-911", "driver": "Al-Amin", "phone": "+1 555-0191", "status": "Available", "type": "Advanced Life Support", "zone": "Uttara"},
    {"id": 2, "plate": "AMB-102", "driver": "Rahman", "phone": "+1 555-0102", "status": "Available", "type": "Basic Life Support", "zone": "Banani"},
    {"id": 3, "plate": "AMB-777", "driver": "Poran", "phone": "+1 555-0777", "status": "Busy", "type": "ICU Ambulance", "zone": "East Zone"},
    {"id": 4, "plate": "AMB-505", "driver": "Samin Khan", "phone": "+1 555-0505", "status": "Available", "type": "Cardiac Ambulance", "zone": "Badda"}
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        phone = request.form['phone']
        location = request.form['location']
        condition = request.form['condition']
        priority = request.form['priority']

        new_id = len(emergency_requests) + 1

        new_request = {
            "id": new_id,
            "patient": patient_name,
            "phone": phone,
            "location": location,
            "condition": condition,
            "priority": priority,
            "status": "Pending",
            "assigned_ambulance": "None"
        }

        emergency_requests.append(new_request)

        return redirect(url_for('index'))

    return render_template('index.html', requests=emergency_requests)


@app.route('/dashboard')
def dashboard():
    total_requests = len(emergency_requests)

    pending_requests = len(
        [req for req in emergency_requests if req['status'] == 'Pending']
    )

    dispatched_requests = len(
        [req for req in emergency_requests if req['status'] == 'Dispatched']
    )

    completed_requests = len(
        [req for req in emergency_requests if req['status'] == 'Completed']
    )

    available_ambulances = len(
        [amb for amb in ambulances if amb['status'] == 'Available']
    )

    stats = {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "dispatched_requests": dispatched_requests,
        "completed_requests": completed_requests,
        "available_ambulances": available_ambulances
    }

    return render_template(
        'dashboard.html',
        ambulances=ambulances,
        requests=emergency_requests,
        stats=stats
    )


@app.route('/complete/<int:req_id>')
def complete_request(req_id):
    for req in emergency_requests:
        if req['id'] == req_id:
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

    for req in emergency_requests:
        if req['status'] != 'Completed':
            req['status'] = 'Pending'
            req['assigned_ambulance'] = 'None'

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)