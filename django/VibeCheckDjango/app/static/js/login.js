window.onload = function () { 
    const remembered = localStorage.getItem("remember-me")==="true";
    if(remembered) {
        document.getElementById("username").value = localStorage.getItem("username") || "";
        document.getElementById("password").value = localStorage.getItem("password") || "";
        document.getElementById("remember-me").checked = true;
    }            
};

function saveCredentials() {
    const remember = document.getElementById("remember-me").checked;
    localStorage.setItem("remember-me", remember);

    if (remember) {
        localStorage.setItem("username", document.getElementById("username").value);
        localStorage.setItem("password", document.getElementById("password").value);
    } else {
        localStorage.removeItem("username");
        localStorage.removeItem("password");
    }
}

function saveUsername() {
const username = document.getElementById("username").value;
localStorage.setItem("username", username);
}

// hardcoded admin login
const loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;

    if (username && password && username === "admin" && password === "123") {
        navigateToPage("../templates/admin.html");
    } else if (username && password && username === "moderator" && password === "123"){
        navigateToPage("../templates/moderator.html");
    } else {
        navigateToPage("../templates/user.html");
    }
});

function navigateToPage(page) {
    window.location.href = page;
}