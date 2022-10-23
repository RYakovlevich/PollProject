from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from .forms import SignupForm, ResetPassword
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

User = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Ссылка на активацию аккаунта' + current_site.domain
            message = render_to_string('registration/email_text_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(mail_subject, message, to=[to_email]
                                           )
            email.attach_alternative(message, 'text/html')
            email.send()

            return HttpResponse('На указанную почту было выслано письмо. Подтвердите вашу регистрацию.')
    else:
        form = SignupForm()

    return render(request, 'registration/sign_up.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Спасибо, что подтвердили регистрацию, теперь вы можете зайти на сайт')

    return HttpResponse('Ссылка активации аккаунта неверна!')


def reset_password(request):  # pylint: disable=R1710
    if request.method == 'GET':
        return render(request, 'registration/reset.html')

    if request.method == 'POST':
        to_email = request.POST.get('email')
        if not to_email:
            return render(request, 'registration/reset.html', {'error': 'Email не был указан'})

        try:
            user = User.objects.get(email=to_email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, 'registration/reset.html', {'error': 'Пользователь с таким email не существует!'})

        current_site = get_current_site(request)
        mail_subject = 'Ссылка на сброс пароля' + current_site.domain
        message = render_to_string('registration/email_reset_password.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        email = EmailMultiAlternatives(mail_subject, message, to=[to_email]
                                       )
        email.attach_alternative(message, 'text/html')
        email.send()

        return HttpResponse('Ссылка для сброса пароля была отправлена на указанную почту. ')


def new_password(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = ResetPassword(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password1'])
                user.save()
                return redirect('login')

            return render(request, 'registration/new_password.html', {'errors': form.errors})

        return render(request, 'registration/reset.html', {'error': 'Пользователь не найден!'})

    return render(request, 'registration/new_password.html')