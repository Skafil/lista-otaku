const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid-feedback');
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea")
const passwordField = document.querySelector("#passwordField")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".input-submit")

const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent === "Pokaż") {
        showPasswordToggle.textContent = "Ukryj";
        passwordField.setAttribute("type", "text");
    } 
    else {
        showPasswordToggle.textContent = "Pokaż";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener('click', handleToggleInput);

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;

    emailFeedBackArea.style.display = "none";

    if(emailVal.length >= 0) {
        fetch('/validate-email', {
            body: JSON.stringify({ email: emailVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then(data=>{
                console.log('data', data);
                if(data.email_error){
                    submitBtn.disabled = true;
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`;
                }
                else{
                    submitBtn.removeAttribute("disabled");
                }
        });
    }
});

usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;


    feedBackArea.style.display = "none";

    if(usernameVal.length > 0) {
        fetch('/validate-username', {
            body: JSON.stringify({ username: usernameVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then(data=>{
                usernameSuccessOutput.style.display = "none";
                if(data.username_error){
                    feedBackArea.style.display = "block";
                    feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
                    submitBtn.disabled = true;
                }
                else {
                     submitBtn.removeAttribute("disabled");
                }
        });
    }
});