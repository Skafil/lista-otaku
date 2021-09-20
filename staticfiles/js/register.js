// 'const <wartość>' - stałe nawiązanie do wartości, czyli że mają być pobierane
// cały czas z tego samego źródła i nie wolno niczego zmieniać w tym źródle!

// "document.querySelector('')" - zwraca pierwszą wartość, która pasuje do
// podanej klasy lub podanego id.

// "addEventListener('event", funkcja) - gdy nastąpi podane wydarzenie,
// program ma uruchomić określoną funkcję.

// Strona przechwytuje wszystko, co użytkownik pisze w polu nazwy użytkownika
// (dosłownie kiedy użytkownik wciśnie jakiś klawisz) i zwraca jakiś event (e).

// "e.target.value" - e oznacza jakiś event, target to element, który powoduje 
// rozpoczęcie eventu (w tym przypadku 'input'), a value to wartość
//  przechowywana przez target (czyli wartość 'inputa')

// "fetch('url', {options})" - wysyłanie zapytanie(request) do strony o podanym
// adresie url. 'options' określa co i w jaki sposób wysyłamy. 

const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid-feedback');
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea")
const passwordField = document.querySelector("#passwordField")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".input-submit")

// Jeżeli przełącznik wyświetla nazwę 'Pokaż', to po kliknięciu na niego nazwa
// zmienia się na 'Ukryj', a pole hasła zmienia typ z hasła na tekst.
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

// Działanie takie same, jak w polu użytkownika (kod poniżej).
emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;
    emailSuccessOutput.style.display = "block";
    emailFeedBackArea.style.display = "none";
    emailField.style.boxShadow = "-1px 0px 24px -2px rgba(180, 180, 180, 0.71)"

    if(emailVal.length > 0) {
        fetch('/validate-email', {
            body: JSON.stringify({ email: emailVal}),
            method: "POST",
        })
            .then(res=>res.json())
            .then(data=>{
                emailSuccessOutput.style.display = "none";
                if(data.email_error){
                    submitBtn.disabled = true;
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`;
                    emailField.style.boxShadow = "-1px 0px 24px -2px red";
                }
                else{
                    submitBtn.removeAttribute("disabled");
                }
        });
    }
});


// Jeśli użytkownik zacznie wypełniać pole nazwy użytkownika (eventem jest
// wciskanie klawiszy) poprawnie, to ustaw domyślny styl z pliku style.css oraz
// wyświetl informację, że sprawdzana jest poprawność wprowadzonej nazwy użytkownika
// (widać przy wolniejszym połączeniu internetowym).
usernameField.addEventListener('keyup', (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Sprawdzam ${usernameVal}`;
    feedBackArea.style.display = "none";
    usernameField.style.boxShadow = "-1px 0px 24px -2px rgba(180, 180, 180, 0.71)"

    // Jeżeli pole nazwy użytkownika nie jest puste, to wyślij zapytanie
    // na podany adres url o zwężoną (stringify) wartość tego pola metodą POST.
    // (wartość body i data była używana w pliku users/views.py w validation view)
    if(usernameVal.length > 0) {
        fetch('/validate-username', {
            body: JSON.stringify({ username: usernameVal}),
            method: "POST",
        })
            // Zwróconą odpowiedź analizuj w formie pliku JSON...
            .then(res=>res.json())
            // i zwróć ją.
            .then(data=>{
                // Ukryj informację o sprawdzaniu, jesli wszystko jest w porządku.
                usernameSuccessOutput.style.display = "none";
                // Jeżeli nazwa użytkownika zawiera błąd, to pobierz treść tego
                // błędu i wyświetl go w formie bloku (style.display="block"),
                // wyświetl czerwoną obramówkę i wyłącz przycisk zatwierdzenia.
                if(data.username_error){
                    feedBackArea.style.display = "block";
                    feedBackArea.innerHTML=`<p>${data.username_error}</p>`;
                    usernameField.style.boxShadow = "-1px 0px 24px -2px red";
                    submitBtn.disabled = true;
                }
                // Jezeli błąd zniknął to włącz przycisk z powrotem.
                else {
                     submitBtn.removeAttribute("disabled");
                }
        });
    }
});