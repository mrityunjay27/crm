from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records


def home(request):
    records = Records.objects.all()

    # check to see if logging in
    # user is trying to fill the form
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In!')
            return redirect('home')  # view name is passed
        else:
            messages.success(request, 'There Was an error Logging In, Please try again...')
            return redirect('home')

    else:
        column_to_sort = request.GET.get('sort', 'first_name')  # Default to a column
        records = Records.objects.all().order_by(column_to_sort)
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        #  whatever coming from register Form pass that to the constructor
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # After filling out the form, authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered....")
            return redirect('home')
    else:  # user has opened to register.
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up record
        cus_record = Records.objects.get(id=pk)
        return render(request, "record.html", {"cus_record": cus_record})
    else:
        messages.success(request, "You must be logged to view that page")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Records.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged to delete")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)  # other method of handling Form Class
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Added a new Record!")
                return redirect('home')
        return render(request, "add_record.html", {"form": form})
    else:
        messages.success(request, "You must be logged to add")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated!")
            return redirect('home')
        return render(request, "update_record.html", {"form": form})
    else:
        messages.success(request, "You must be logged to update")
        return redirect('home')
