from django.db import models
import bcrypt, re

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        all_users = User.objects.all()
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be atleast 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be atleast 2 characters long"
        UserRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')
        if not UserRegex.match(postData['email']):
            errors['email'] = "This is not a valid email"
        for user in all_users:
            if user.email == postData['email']:
                errors['unique_email'] = "This email is already taken"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password and Confirm PW must match"
        return errors
    def login_validator(self, postData):
        errors = {}
        login_user = User.objects.filter(email=postData['log_email'].lower())
        if len(login_user) > 0:
            if bcrypt.checkpw(postData['log_password'].encode(), login_user[0].password.encode()):
                print('password matches')
            else:
                errors['log_password'] = "That username and or password is incorrect"
        else:
            errors['log_username'] = "That username and or password is incorrect"
        return errors
    def update_validator(self, postData):
        errors = {}
        all_users = User.objects.all()
        current_user = User.objects.get(id=postData['current_user_id'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be atleast 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be atleast 2 characters long"
        UserRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')
        if not UserRegex.match(postData['email']):
            errors['email'] = "This is not a valid email"
        for user in all_users:
            if postData['email'] == current_user.email:
                pass
            elif postData['email'] == user.email:
                errors['unique_email'] = "This email is already in use"
            
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) < 4:
            errors['author'] = "Must be more than 3 characters"
        if len(postData['quote']) < 11:
            errors['quote'] = "Quote must be more than 10 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField() 
    uploaded_by = models.ForeignKey(User, related_name="quotes_uploaded", on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()