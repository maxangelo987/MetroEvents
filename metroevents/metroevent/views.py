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
		event = Event.objects.all()

		context = {
				'events' : event,
				}

		return render(request, 'homepage.html', context)

	def post(self,request):

		if 'joinEventBtn' in request.POST:
			eventid = request.POST.get('eventid')
			joinReq = Request.objects.create(user_id=request.user.id, request_type="Join event", event_id=eventid)
			print('saved')
			return HttpResponse('Request sent!')

		return redirect('metroevent:HomePageView')


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

	def post(self, request):
		if request.method == 'POST':	
			if 'btnUpdate' in request.POST:	
				print('Update Button Clicked')
				users = request.POST.get("user-id")
				first_name = request.POST.get("user-fname")
				last_name = request.POST.get("user-lname")
				email = request.POST.get("user-email")
				username = request.POST.get("user-username")
				date_joined = request.POST.get("user-dateJoined")
								
				update_user = User.objects.filter(id = users).update(first_name=first_name, last_name=last_name, email=email, 
								username=username)


				print(update_user)
		
				print('User Details Updated!')

			elif 'btnDelete' in request.POST:	

				print('Delete Button Clicked')
				users = request.POST.get("user-id")
				user = User.objects.filter(id = users).delete()
				print('Users Record Deleted')
		return redirect('metroevent:UsersAdminView')

class EventsAdminView(View):
	def get(self, request):
		event = Event.objects.all()

		context = {
				'events' : event,
				}
		return render(request, 'events.html', context)

class OrgAdminView(View):
	def get(self, request):
		return render(request, 'organizers.html')

class ProfileView(View):
	def get(self, request):
		user = User.objects.all()
		event = Event.objects.exclude(participants=request.user)
		joinedEvent = Event.objects.filter(participants=request.user)

		context = {
				'joinedEvents' : joinedEvent,
				'events' : event,
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
		reqs = Request.objects.all()

		context = {
				'reqs' : reqs,
				}
		return render(request, 'requests.html', context)

	def post(self,request):
		if 'EventReqAcceptBtn' in request.POST:
			event = Event.objects.get(id=request.POST.get('eventid'))
			req = Request.objects.get(id=request.POST.get('requestid'))
			user = User.objects.get(id=request.POST.get('userid'))
			event.participants(user)
			req.status = "Approved"
			req.save()
		return redirect('metroevent:RequestView')