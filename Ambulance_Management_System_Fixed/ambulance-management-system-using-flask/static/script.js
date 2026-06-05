function validateForm() {
    let patientName = document.getElementById("patient_name").value.trim();
    let phone = document.getElementById("phone").value.trim();
    let location = document.getElementById("location").value.trim();
    let condition = document.getElementById("condition").value.trim();

    if (patientName === "" || phone === "" || location === "" || condition === "") {
        alert("Please fill in all emergency request fields before submitting.");
        return false;
    }

    if (phone.length < 6) {
        alert("Please enter a valid contact number.");
        return false;
    }

    alert("Emergency request submitted successfully!");
    return true;
}
