from webapp.models import predict
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from webapp.models import UserProfile
from django.contrib import messages
import requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()

def age_encoder(x):
    if x == '18-24':
        return "young"
    elif x == '25-34':
        return "middle young"
    elif x == '35-44':
        return "early middle"
    elif x == '45-54':
        return "middle age"
    elif x == '55-64':
        return "adults"
    else:
        return "old adults"

class_names = ['Never Used','Used over a Decade Ago','Used in Last Decade','Used in Last Year','Used in Last Month','Used in Last Week','Used in Last Day']
# Create your views here.

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if the email already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Create the new user
        user = User.objects.create_user(username=email, email=email, password=password)

        # Optionally create a UserProfile or other related models
        UserProfile.objects.create(user=user, full_name=name)

        messages.success(request, "Registration successful. Please login.")
        return redirect('home')

    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('name')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log the user in
            return redirect('input')  # Redirect to the input page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to login page if authentication fails

    return render(request, 'index.html')


@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def input(request):
	return render(request,'input.html')

@login_required
def output(request):
    # Initialize a LabelEncoder for preprocessing
    le = LabelEncoder()

    # Extract and preprocess the "AGE" field
    AGE = request.POST.get("AGE")
    AGE = age_encoder(AGE)  # Assuming you have an 'age_encoder' function
    AGE = le.fit_transform([AGE])

    # Extract and preprocess the "Gender" field
    Gender = request.POST.get("Gender")
    Gender = le.fit_transform([Gender])

    # Extract and preprocess the "Education" field
    Education = request.POST.get("Education")
    Education = le.fit_transform([Education])

    # Extract and preprocess the "Country" field
    Country = request.POST.get("Country")
    Country = le.fit_transform([Country])

    # Extract and preprocess the "Ethnicity" field
    Ethnicity = request.POST.get("Ethnicity")
    Ethnicity = le.fit_transform([Ethnicity])

    # Extract the other fields without preprocessing
    Nscore = request.POST.get("Nscore")
    Escore = request.POST.get("Escore")
    Oscore = request.POST.get("Oscore")
    AScore = request.POST.get("AScore")
    Cscore = request.POST.get("Cscore")
    Impulsive = request.POST.get("Impulsive")
    SS = request.POST.get("SS")
    lst = [float(AGE), float(Gender), float(Education), float(Country), float(Ethnicity), float(Nscore), float(Escore), float(Oscore), float(AScore), float(Cscore), float(Impulsive), float(SS)]

    algo = request.POST.get('algo')
    out = predict(lst, algo)
    # classes = class_names[int(out)]
    if out == 0:
        class_name = 'Never Used'
    elif out == 1:
        class_name = 'Used over a Decade Ago'
    elif out == 2:
        class_name = 'Used in Last Decade'
    elif out == 3:
        class_name = 'Used in Last Year'
    elif out == 4:
        class_name = 'Used in Last Month'
    elif out == 5:
        class_name = 'Used in Last Week'
    else:
        class_name = "Used in Last Day"
    print(class_name)  # This print statement is optional for debugging purposes
    return render(request, 'output.html', {'out': class_name})



