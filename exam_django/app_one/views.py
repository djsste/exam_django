from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render (request, 'index.html')

def create_user(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.registration_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'].lower(),
            password = hashedpw,
        )
        request.session['user_id'] = new_user.id
        return redirect('/quotes')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        current_user = User.objects.get(email=request.POST['log_email'].lower())
        request.session['user_id'] = current_user.id
        return redirect('/quotes')

def logout(request):
    request.session.flush()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'current_user': current_user,
        'quotes': Quote.objects.all(),
    }
    return render(request, 'quotes.html', context)

def upload_quote(request):
    errors = Quote.objects.quote_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        current_user = User.objects.get(id=request.session['user_id'])
        new_quote = Quote.objects.create(
            author = request.POST['author'],
            quote = request.POST['quote'],
            uploaded_by = current_user
        )
    
        return redirect('/quotes')

def delete_quote(request,id):
    Quote.objects.get(id=id).delete()
    return redirect('/quotes')

def like_quote(request, id):
    current_user = User.objects.get(id=request.session['user_id'])
    current_user.liked_quotes.add(Quote.objects.get(id=id))
    return redirect('/quotes')

def view_user(request,id):
    context = {
        'user': User.objects.get(id=id),
    }
    return render(request, 'view_user.html', context)

def edit_account_page(request,id):
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        'current_user': current_user,
    }
    return render(request, 'edit_account.html', context)

def edit_account(request, id):
    errors = User.objects.update_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/myaccount/{id}')
    else:
        updated_account = User.objects.get(id=id)
        updated_account.first_name=request.POST['first_name']
        updated_account.last_name=request.POST['last_name']
        updated_account.email=request.POST['email']
        updated_account.save()
        return redirect(f'/myaccount/{id}')