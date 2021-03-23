from django.shortcuts import render
from django.views.generic import View
import datetime
from .forms import *
from .models import *
from .forms import CreateUserForm
from itertools import chain
from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def SignUpView(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(data=request.POST)
		# print(form.is_valid())
		# print(form.errors)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			# messages.success(request,'Account was created for '+user)
			messages.success(request, 'Registration Successful')
			return redirect('metroevent:LoginView')

	context = {'form':form}
	return render(request,'signup.html',context)

class LoginView(View):
	def get(self, request):
		return render(request, 'login.html')

	def post(self,request):
		# if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)
			print(user)

			if user is not None:
				login(request, user)
				# pass the name of the user to the base.html navbar
				request.session['username'] = username
				if request.user.is_superuser:
					return redirect('metroevent:AdminView')
				else:
					return redirect('metroevent:HomePageView')
			else:
				messages.info(request, 'Username or password is incorrect')
				
			# context = {} 
			return render(request, 'login.html')

def LogoutView(request):
	logout(request)
	return redirect('metroevent:IndexView')

class IndexView(View):
	def get(self, request):
		return render(request, 'index.html')

class HomePageView(View):
	def get(self, request):
		return render(request, 'homepage.html')

class AdminView(View):
	def get(self, request):
		user = User.objects.all()

		context = {
				'users' : user,
				}
		return render(request, 'admin_dashboard.html', context)


class UsersAdminView(View):
	def get(self, request):
		user = User.objects.all()

		context = {
				'users' : user,
				}
		return render(request, 'users.html', context)

class EventsAdminView(View):
	def get(self, request):
		return render(request, 'events.html')

class OrgAdminView(View):
	def get(self, request):
		return render(request, 'organizers.html')

class ProfileView(View):
	def get(self, request):
		user = User.objects.all()

		context = {
				'users' : user,
				}
		return render(request, 'profile.html', context)
			
class OrgProfileView(View):
	def get(self, request):
		return render(request, 'organizer_profile.html')

class AddEventView(View):
	def get(self, request):
		return render(request, 'addevent.html')

	def post(self,request):
		form = EventForm(request.POST, request.FILES)
		print('hh')
		if form.is_valid():
			name = request.POST.get('name')
			description = request.POST.get('description')
			datetime = request.POST.get('datetime')
			address = request.POST.get('address')
			event_pic = request.FILES['event_pic']
			print('hh')

			form = Event(name = name, datetime = datetime, address = address, description = description, event_pic=event_pic)
			form.save()
			print('hh')

			print('saved')
			return HttpResponse('Event added!')
		else:
			print(form.errors)
			print('wrong')
			return HttpResponse('Unsuccessful Save')

class RequestView(View):
	def get(self, request):
		return render(request, 'requests.html')