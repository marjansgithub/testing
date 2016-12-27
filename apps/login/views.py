from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Quote, Fave


def index(request):
	return render(request, "login/index.html")

def quotes(request):
	excluded_list=[]
	if not 'id' in request.session :
		return redirect('/')
	else:
		first_name = request.session['first_name']
		user = User.objects.filter(first_name=first_name).get()
		print user.id,"user logged in"
		user_new = Fave.objects.filter(user_id=user.id)
		
		if user_new: 
			user_new_list = list(user_new)
			x= len(list(user_new))
			print x
			for i in range (0, len(list(user_new))):
				excluded_list.append(user_new[i].quote.id)
				print i, user_new[i].id, user_new[i].quote.id,excluded_list

		print user.id,"!!!!!!!!!!!!!!!!!!!!!!!!!"
		# new_quote = Quote.objects.exclude(id=user_new.user.id)
		new_quote = Quote.objects.exclude(id__in=excluded_list)
		print new_quote,"print user_new[0].quote_id"
		new_fave = Fave.objects.filter(user_id=user.id)
		print new_fave
		
		context = { 'user':user, 
				'new_quote':new_quote, 
				'new_fave':new_fave,}	
		return render(request, "login/quotes.html", context)

def add_my_quote_process(request):
	
	user = request.POST.get('id')
	quote_author = request.POST['quote_author']
	quote_text = request.POST['quote_text']
	result = Quote.objects.add_quote(quote_author, quote_text, user)
	if result[0]==True:
		# request.session['first_name'] = result[1][0].first_name
		print result
		return redirect('/quotes')
	else:
		messages.add_message(request, messages.WARNING, result[1][0])
		return redirect('/quotes')

def users(request, id):
	
	user = User.objects.get(id=id)
	quote = Quote.objects.filter(user_id=id)
	# print user_quote[0], "%%%%%%%%%%%%%%%%%"
	context = {'user':user, 'user_quote':quote }
	return render(request, "login/users.html", context)

def add_my_fave(request, id):
	# global id_to_be_removed
	first_name = request.session['first_name']
	user = User.objects.filter(first_name=first_name).get()
	print user.id, "yyyyyyyyyyyy"
	quote= Quote.objects.get(id=id)
	
	# print quote.id, quote.user.id, "llllllll"
	# print quote.user.id, quote.id, quote.quote_text,  "^^^^^^^^^^^^^^^^^"
	new_fave=Fave.objects.add_fave(user.id, quote.id, quote.quote_text,  quote.quote_author)
	
	# print new_fave.id, new_fave.user.id, new_fave.quote.id, new_fave.quote_text, new_fave.quote_author,"{{{{{{{{{{{{{{{{{{{{{{{{"
	return redirect('/quotes')

def remove_my_fave(request, id):
	Fave.objects.get(id=id).delete()
	return redirect('/quotes')

def logout(request)	:
	del request.session['first_name']
	return redirect ('/')	

def register_process(request):
	
	if request.method == "POST":
		result = User.objects.register(request.POST['first_name'],request.POST['last_name'],request.POST['email'],request.POST['password'], request.POST['confirm_password'])
	
		if result[0]==True:
			request.session['first_name'] = result[1].first_name
			print result, "*******************************************************"
			# request.session.pop('errors')
			return redirect('/quotes')
		else:
			messages.add_message(request, messages.WARNING, result[1][0])
			return redirect('/')
	else:

		return redirect ('/')

def login_process(request):
	print "------------ POST ----------------\n", request.POST
	result = User.objects.login(request.POST['email'],request.POST['password'])

	if result[0] == True:
		request.session['first_name'] = result[1][0].first_name
		request.session['id'] = result[1][0].id
		print request.session['id'],"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


		# We have result[1][0] this refers to the results of the query (user query returned) and index of zero which is what we just unwrapped.
		return redirect('/quotes')
	else:
		messages.add_message(request, messages.WARNING, result[1][0])

		# request.session['errors'] = result[1]
		return redirect('/')

