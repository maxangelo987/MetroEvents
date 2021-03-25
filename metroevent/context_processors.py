from django.contrib.auth.models import User
# add this in settings.py of the project under templates
def user(request):
	if 'username' in request.session:
		username = request.session.get('username')
		return{
			'username' : username
		}
	return{}