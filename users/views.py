from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

class EmailThread(threading.Thread):
    """Przyśpiesz wysyłanie wiadomości e-mail."""
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

class UsernameValidationView(View):
    """ Widok sprawdzania poprawności nazwy użytkownika."""
    def post(self, request):
        # Pobierz dane z formularza i umieść je w zmiennych.
        data = json.loads(request.body)
        username = data['username']

        # Sprawdź, czy nazwa użytkownika zawiera tylko litery oraz cyfry.
        # Jeśli nie - wyświetl błąd.
        if not str(username).isalnum():
            return JsonResponse({
                'username_error': 'Nazwa użytkownika może zawierac tylko litery i cyfry!'},
                status=400)

        # Sprawdź, czy nazwa użytkownika jest zajęta.
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'username_error': 'Ta nazwa użytkownika jest już zajęta.'},
                status=409)

        # Jeżeli nazwa użytkownika jest poprawnie zapisana i nie jest zajęta,
        # zwróć True.
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    """ Widok sprawdzania poprawności adresu e-mail."""
    def post(self, request):
        # Pobierz dane z formularza i umieść je w zmiennych.
        data = json.loads(request.body)
        email = data['email']

        # Wyświetl komunikat błędu, jeśli adres e-mail jest zapisany nieprawidłowo.
        if not validate_email(email):
            return JsonResponse({
                'email_error': 'Podany adres e-mail jest nieprawdidłowy!'},
                status=400)

        # Sprawdź, czy nazwa użytkownika jest zajęta.
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'email_error': 'Ten adres e-mail jest już zajęty.'},
                status=409)

        if not email:
            return JsonResponse({
                'email_error': "Wpisz adres e-mail."},
                status=400)

        # Jeżeli nazwa użytkownika jest poprawnie zapisana i nie jest zajęta,
        # zwróć True.
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    """ Widok rejestracji. """
    def get(self, request):
        context = {}
        return render(request, 'register.html', context)

    def post(self, request):
        # Wyświetla komunikaty w zależności od wprowadzonych danych po 
        # zatwierdzeniu.

        #messages.success(request, "Success whatsapp success")
        #messages.warning(request, "Success whatsapp warning")
        #messages.info(request, "Success whatsapp info")
        #messages.error(request, "Success whatsapp error")
        
        # Pobierz dane użytkownika.
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            'fieldValues': request.POST,
        }
        # Sprawdź, czy nazwa użytkownika i adres e-mail nie są zajęte oraz czy
        # hasło zawiera conajmniej 8 znaków.
        try:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if len(password) <= 7:
                        messages.error(request, "Hasło musi się składać z conajmniej 8 znaków.")
                        return render(request, 'register.html', context)

                    # Stworz nieaktywowane konto użytkownika i wyślij wiadomość e-mail
                    # z linkiem do aktywacji konta.
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    email_body = {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    }

                    link = reverse('activate', kwargs={
                        'uidb64': email_body['uid'], 'token': email_body['token']})

                    email_subject = 'Aktywuj swoje konto'

                    activate_url = 'http://'+current_site.domain+link

                    email = EmailMessage(
                        email_subject,
                        'Witaj '+user.username + ',wejdź na poniższy link, by aktywować swoje konto \n'+activate_url,
                        'listajam2021@gmail.com',
                        [email],
                    )
                    EmailThread(email).start()
                    messages.success(request, 'Konto zostało stworzone. Na podany adres e-mail została wysłana wiadomość z linkiem aktywującym konto. Bez aktywacji konta nie będziesz mógł się zalogować.')
                    return render(request, 'register.html', context)
        except ValueError:
            messages.error(request, "Nie wszystkie pola zostały wypełnione")
            return render(request, 'register.html', context)

        return render(request, 'register.html', context)

class VerificationView(View):
    """Widok z linku wysłaneog na e-mail. Aktywuje konto i przekierowuje na 
    stronę logowania."""
    def get(self, request, uidb64, token):
        try:
            # Pozyskaj id i powiąż je z konkretnym użytkownikiem.
            id=force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # Sprawdź czy użytkownik jest już aktywny.
            if not account_activation_token.check_token(user, token):
                return redirect('login')

            if user.is_active:
                return redirect('login')

            # Aktywacja konta użytkownika.
            user.is_active = True
            user.save()

            messages.success(request, "Konto zostało aktywowane.")
            return redirect('login')

        except Exception as ex:
            raise

        return redirect('login')

class LoginView(View):
    """Widok logowania użytkownika."""
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        """Logowanie użytkownika."""
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('table_titles')

                messages.error(request, "Konto nie jest aktywne. Sprawdź, czy"
                    " otrzymałeś wiadomość e-mail z linkiem aktywacyjnym.")
                return render(request, 'login.html')

            messages.error(request, "Nieprawidłowe dane. Spróbuj ponownie.")    
            return render(request, 'login.html')

        messages.error(request, "Wypełnij wszystkie pola.")    
        return render(request, 'login.html')

def logout_view(request):
    auth.logout(request)
    return redirect('index')

class RequestPasswordResetEmail(View):
    """ Prośba o zmianę hasła poprzez e-mail. """
    def get(self, request):
        return render(request, 'reset-password.html')

    def post(self, request):
        email = request.POST.get('email')
        context = {
            'values': request.POST,
        }

        if not validate_email(email):
            messages.error(request, "Podany e-mail jest zapisany nieprawidłowo.")
            return render(request, 'reset-password.html', context)

        current_site = get_current_site(request)

        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Reset hasła'

            reset_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Witaj, wejdź na podany poniżej link, by zresetować swoje hasło \n'+reset_url,
                'listajam2021@gmail.com',
                [email],
            )
            EmailThread(email).start()

        messages.success(request, "Wysłaliśmy na podany e-mail wiadomość z dalszymi instrukcjami.")

        return render(request, 'reset-password.html')        

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Link do zmiany hasła jest nieaktualny, poproś o nowy.")
                return render(request, 'reset-password.html')

        except Exception as e:
            pass

        return render (request, 'set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Podane hasła nie są takie same.")
            return render (request, 'set-new-password.html', context)

        if len(password) <= 7:
            messages.error(request, "Hasło musi się składać z conajmniej 8 znaków.")
            return render (request, 'set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Hasło zostało zmienione pomyślnie.")
            return redirect('login')

        except Exception as e:
            messages.info(request, "Coś poszło nie tak podczas zmiany hasła. Spróbuj ponownie. ")
            return render (request, 'set-new-password.html', context)

