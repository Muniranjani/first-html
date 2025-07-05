function validateForm() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    let valid = true;
document.getElementById("emailError").style.display = 'none';
    document.getElementById("passwordError").style.display = 'none';
 if (email === "" || !email.includes("@") || !email.includes(".")) {
        document.getElementById("emailError").style.display = 'block';
        valid = false;
    }

if (password.length < 4 || password.length > 60) {
        document.getElementById("passwordError").style.display = 'block';
        valid = false;
    }
if (valid) {
        alert("Form submitted successfully!");
        return true;
    }
  return false;
}