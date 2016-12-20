from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book, Review

def index(request):
	return render(request, "login/index.html")

def success(request):
	if not 'first_name' in request.session :
		return redirect('/')
	else:
		first_name = request.session['first_name']
		user = User.objects.filter(first_name=first_name).get()
		all_review_3 = Review.objects.all().order_by('created_at').reverse()[:3]
		all_review = Review.objects.all()[:20]
		context = { 'user': user, 'all_review':all_review, 'all_review_3':all_review_3}	
		return render(request, "login/success.html", context)	

def add_book_review(request,id):
	user = User.objects.get(id=id)	
	context = { 'user': user}
	return render(request, "login/add_book_review.html", context)

def add_book_review_process(request, id):
	book_title = request.POST.get('book_title')
	print book_title, "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
	book_author = request.POST.get('book_author')
	
	user = User.objects.filter(id=id)
	print  "777777777777777777777777777777777"
	
	new_book = Book.objects.create(book_title=book_title, book_author=book_author, user_id=user[0].id)
	print "*********", new_book.book_title, new_book.book_author, new_book.id, new_book.user_id, user[0].id
	b = new_book.id
	u = user[0].id
	# book = Book.objects.filter(id=new_book.id)
	# new_review = Review.objects.create(review_text=review_text, rating=rating, user_id=user[0].id, book_id=b)
	# print "new_review",new_review.rating, new_review.review_text, new_review.id, new_review.user_id, new_review.book_id
	new_review = input_review(request, u, b)
	context = {'new_review': new_review, 'new_book':new_book}
	print new_book.id, "printing new_book id"
	return redirect('/each_book/{}'.format(b))

def input_review(request, user_id, book_id):
	review_text = request.POST.get('review_text')
	rating = request.POST.get('rating')
	new_review = Review.objects.create(review_text=review_text, rating=rating, user_id=user_id, book_id=book_id)
	print "new_review",new_review.rating, new_review.review_text, new_review.id, new_review.user_id, new_review.book_id
	return (new_review)

def add_review_each_book_process(request, id):
	print "iam here"
	book_user = Book.objects.get(id=id)
	print book_user,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", book_user.user_id
	u = book_user.user_id
	b = id
	new_review = input_review(request, u, b)
	return redirect('/each_book/{}'.format(b))


def each_book(request, id):
	book = Book.objects.get(id=id)
	# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",book.id
	all_review_one_book = Review.objects.filter(book_id=id)	

	all_review_except_one = Review.objects.exclude(book_id=id)[:3]	
	context = { 'book': book,
				 'all_review_one_book':all_review_one_book, 
				 'all_review_except_one':all_review_except_one}


	print all_review_except_one,"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	return render(request, "login/each_book.html", context)

def user_info(request,id):
	user = User.objects.get(id=id)

	print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",user.first_name
	user_book_reviewed = Book.objects.filter(user_id=id)
	
	# for i in  user_book_reviewed[0]:
	# 	print user_book_reviewed[0].book_title
	
	# all_review_one_book = Review.objects.filter(book_id=id)	
	context = { 'user': user, 'user_book_reviewed': user_book_reviewed }
	return render(request, "login/user_info.html", context)

def delete_review(request,id):
	print id,"((((((((((((((((((((((((((((("
	review_object = Review.objects.get(id=id)
	b = review_object.book_id
	Review.objects.get(id=id).delete()
	
	
	return redirect ('/each_book/{}'.format(b))

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
			return redirect('/success')
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
		# We have result[1][0] this refers to the results of the query (user query returned) and index of zero which is what we just unwrapped.
		return redirect('/success')
	else:
		messages.add_message(request, messages.WARNING, result[1][0])

		# request.session['errors'] = result[1]
		return redirect('/')


