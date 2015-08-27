__author__ = 'amin'

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.core.mail import send_mail

from mysite.settings import EMAIL_HOST_USER
import basic_funcs
import ocr
import forms
import models


def home(request):
    return redirect('/login')

@csrf_exempt
def signup(request):
    if request.method == 'POST' and not request.is_ajax():
        form = forms.SignupForm(data=request.POST)
        if form.is_valid():
            models.User.save_form(form)
            send_mail('IUST Ocr Site', 'Thanks you for registering.\n\nYour username is %s\nYour password is %s' % (form.username, form.password), EMAIL_HOST_USER, [form.email], fail_silently=False)
            return redirect('/login/')
        else:
            return render_to_response("signup.html", {'captcha_error': form.captcha_errors(form.captcha)})
    elif request.method == 'POST' and request.is_ajax():
        if request.POST['input'] == 'username' and request.POST['value'] != '':
            return HttpResponse(forms.SignupForm.username_errors(request.POST['value']))
        if request.POST['input'] == 'email'    and request.POST['value'] != '':
            return HttpResponse(forms.SignupForm.email_errors(request.POST['value']))
        if request.POST['input'] == 'password' and request.POST['value'] != '':
            return HttpResponse(forms.SignupForm.password_errors(request.POST['value']))
        if request.POST['input'] == 'confpass' and request.POST['value2'] != '':
            return HttpResponse(forms.SignupForm.confpass_errors(request.POST['value1'], request.POST['value2']))
        return HttpResponse('NULL')

    return render_to_response("signup.html")

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST' and not request.is_ajax():
        username = request.POST['username']
        if not models.User.objects.filter(username=username):
            return render_to_response('forgot_password.html', {'res': 'Username not found'})
        email = models.User.objects.get(username=username).email
        password = models.User.objects.get(username=username).password
        send_mail('IUST Ocr Site', 'Your password is %s' % (password), EMAIL_HOST_USER, [email], fail_silently=False)
        return render_to_response('forgot_password.html', {'res': 'Your password sent to your email'})

    return render_to_response('forgot_password.html')

@csrf_exempt
def login(request):
    response = {}

    if login in request.session and request.session['login']:
        return redirect('/recignize')

    if request.method =='POST' and not request.is_ajax():
        user = request.POST['username']
        if not models.User.objects.filter(username=user):
            response.update({'error': mark_safe('<li class="text-error">Username does not exist</li>')})
        else:
            if not check_password(request.POST['password'], models.User.objects.get(username=user).password):
                response.update({'error': mark_safe('<li style=\"color="red"\">Password is wrong</li>')})
            else:
                request.session['login'] = True
                request.session['username'] = user
                request.session['userid'] = models.User.objects.get(username=user).id
                return redirect('/recognize')

    return render_to_response("login.html", response)

@csrf_exempt
def logout(request):
    request.session.clear()
    request.session.delete()
    return redirect('/login')


def recognize(request):
    if 'login' in request.session and request.session['login']:
        return render(request, 'recognize.html', {'user_login': request.session['username']})
    return redirect('/login')


@csrf_exempt
def ocr_handler(request):
    response = 'NULL'

    if request.method == 'POST' and request.is_ajax():
        userid = request.session['userid']
        action = request.POST['action']

        if action == 'check':
            image = basic_funcs.canvas2image(request.POST['canvas'])
            response = ocr.check(userid, image)
        elif action == 'add':
            image = basic_funcs.canvas2image(request.POST['canvas'])
            char = request.POST['char']
            response = ocr.add(userid, image, char[0])
        else:
            response = 'invalid'

    return  HttpResponse(response)


@csrf_exempt
def ocr_train_handler(request):
    response = 'NULL'
    if request.method == 'POST' and request.is_ajax():
        action = request.POST['action']
        userid = request.session['userid']

        if action == 'train':
            max_error = request.POST['max_error']
            response = ocr.train(userid, max_error)
        elif action == 'reset':
            response = ocr.reset(userid)

    return HttpResponse(response)


@csrf_exempt
def ocr_get_error_handler(request):
    response = 'NULL'
    if request.method == 'POST' and request.is_ajax():
        userid = request.session['userid']
        response = ocr.get_error(userid)

    return HttpResponse(response)