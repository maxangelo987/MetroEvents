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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
			messages.success(request,'Account was created for '+user)
			#return HttpResponse('Registration Successful')
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
			#print(user)

			if user is not None:
				login(request, user)
				# pass the name of the user to the base.html navbar
				request.session['username'] = username
				if request.user.is_superuser:
					return redirect('metroevent:AdminView')
				if request.user.is_staff:
					return redirect('metroevent:OrgProfileView')
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

@method_decorator(login_required, name='dispatch')
class HomePageView(View):
	def get(self, request):
		event = Event.objects.all()
		totalparticipants = Event.objects.filter(participants=request.user).count()

		context = {
				'events' : event,
				'totalparticipants' : totalparticipants,
				}
		return render(request, 'homepage.html', context)

	def post(self,request):

		if 'joinEventBtn' in request.POST:
			eventid = request.POST.get('eventid')

			joinReqs = Request.objects.filter(user=request.user, request_type="Join event", event_id=eventid)

			if joinReqs:
				return HttpResponse('Request already submitted.')

			joinReq = Request.objects.create(user_id=request.user.id, request_type="Join event", event_id=eventid)
			return HttpResponse('Request sent! Please wait for the confirmation')

		elif 'requestOrgBtn' in request.POST:
			orgReqs = Request.objects.filter(user=request.user, request_type="Be an organizer")

			if orgReqs:
				return HttpResponse('Request already submitted.')
				return redirect('metroevent:HomePageView')

			orgReq = Request.objects.create(user=request.user, request_type="Be an organizer")
			return HttpResponse('Request sent! Please wait for the confirmation')

		return redirect('metroevent:HomePageView')

@method_decorator(login_required, name='dispatch')
class AdminView(View):
	def get(self, request):
		user = User.objects.all()

		context = {
				'users' : user,
				}
		return render(request, 'admin_dashboard.html', context)

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class EventsAdminView(View):
	def get(self, request):
		event = Event.objects.all()

		context = {
				'events' : event,
				}
		return render(request, 'events.html', context)
	def post(self, request):
		if request.method == 'POST':	
			if 'btnUpdate' in request.POST:	
				print('Update Button Clicked')
				events=request.POST.get("event-id")
				name = request.POST.get("event-name")
				description = request.POST.get("event-description")
				datetime = request.POST.get("event-datetime")
				address = request.POST.get("event-address")
						
				update_event = Event.objects.filter(id = events).update(name=name, description=description, address=address)


				print(update_event)
		
				print('Event Details Updated!')

			elif 'btnDelete' in request.POST:	

				print('Delete Button Clicked')
				events = request.POST.get("event-id")
				event = Event.objects.filter(id = events).delete()
				print('Events Record Deleted')
		return redirect('metroevent:EventsAdminView')

@method_decorator(login_required, name='dispatch')
class OrgAdminView(View):
	def get(self, request):
		organizer = Organizer.objects.all()

		context = {
				'organizers' : organizer,
				}

		return render(request, 'organizers.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		user = User.objects.filter(username=request.user)
		event = Event.objects.exclude(participants=request.user)
		joinedEvent = Event.objects.filter(participants=request.user)

		context = {
				'joinedEvents' : joinedEvent,
				'events' : event,
				'users' : user,
				}

		if request.user.is_staff:
			return redirect('metroevent:OrgProfileView')
		else:
			return render(request, 'profile.html', context)

@method_decorator(login_required, name='dispatch')			
class OrgProfileView(View):
	def get(self, request):
		organizer = request.user
		user = User.objects.filter(username=request.user)
		#event = Event.objects.exclude(organizer=organizer)
		#joinedEvent = Event.objects.filter(organizer=organizer)
		reqs = Request.objects.filter(request_type="Join event", status="Pending")

		context = {
				#'joinedEvent' : joinedEvent,
				#'events' : event,
				'users' : user,
				'reqs' : reqs,
				}
		return render(request, 'organizer_profile.html', context)

	def post(self,request):

		if 'EventReqAcceptBtn' in request.POST:
			event = Event.objects.get(id=request.POST.get('event_id'))
			req = Request.objects.get(id=request.POST.get('request_id'))
			user = User.objects.get(id=request.POST.get('user_id'))
			event.participants.add(user)
			req.status = "Approved"
			req.save()

		elif 'EventReqDeclineBtn' in request.POST:
			req = Request.objects.get(id=request.POST.get("requestid"))
			req.status = "Declined"
			req.save()
		return redirect('metroevent:OrgProfileView')


@method_decorator(login_required, name='dispatch')
class AddEventView(View):
	def get(self, request):
		if request.user.is_authenticated:
			if request.user.is_superuser or request.user.is_staff:
				return render(request, 'addevent.html')
			else:
				return HttpResponse("Error")
		return redirect('metroevent:LoginView')

	def post(self, request):
		organizer = Organizer.objects.get(organizer_id=request.user)
		name = request.POST.get('name')
		description = request.POST.get('description')
		datetime = request.POST.get('datetime')
		address = request.POST.get('address')
		event_pic = request.FILES['event_pic']
		event = Event.objects.create(name = name, datetime = datetime, address = address, description = description, event_pic=event_pic)
		organizer.event.add(event)

		return HttpResponse('Event added!')

		if request.user.is_superuser:
			return redirect('metroevent:EventsAdminView')
		elif request.user.is_staff:
			return redirect('metroevent:OrgProfileView')
		else:
			return redirect('metroevent:LoginView')

@method_decorator(login_required, name='dispatch')
class RequestView(View):
	def get(self, request): 
		reqs = Request.objects.filter(request_type="Be an Organizer", status="Pending")

		context = {
				'reqs' : reqs,
				}
		return render(request, 'requests.html', context)

	def post(self,request):
		if 'OrgReqAcceptBtn' in request.POST:
			req = Request.objects.get(id=request.POST.get('request_id'))
			userid = request.POST.get("user_id")
			organizer = Organizer.objects.create(organizer_id=userid)
			req.status = "Accepted"
			user = req.user
			user.is_staff = True
			organizer.save()
			req.save()
			user.save()

		elif 'OrgReqDeclineBtn' in request.POST:
			req = Request.objects.get(id=request.POST.get("request_id"))
			req.status = "Declined"
			req.save()

		return redirect('metroevent:RequestView')

