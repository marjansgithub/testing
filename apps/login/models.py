from __future__ import unicode_literals
from django.db import models
from django.db.models import F
import re, bcrypt

passRegex = re.compile(r'^(?=.{8,15}$)(?=.*[A-Z])(?=.*[0-9]).*$')
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameRegex = re.compile(r'^(?=.{2,})([a-zA-z]*)$')

class UserManager(models.Manager):

	def register(self, first_name, last_name, email, password, confirm_password ):
		errors = []
		if (len(first_name) == 0) or (len(last_name) == 0)  or (len(email) == 0) or (len(password) == 0):
			errors.append("Cannot be blank")

		if ((not nameRegex.match(first_name)) or (not nameRegex.match(last_name)) ):
		# elif (not emailRegex.match(email)) or (not nameRegex.match(first_name)) or (not nameRegex.match(last_name)):
			errors.append("Name must be at least 2 characters with no letters...")
		if (not emailRegex.match(email)):
			errors.append("Invalid email ....")
		else:
			email_registeres = User.objects.filter(email=email)
			print email_registeres,
			if (email_registeres):
				if (email==email_registeres[0].email):
					errors.append("Email exits in our system ")
		if (not passRegex.match(password)):
			errors.append("Password be at 8-15 characters with one capital letter...")
		if (not (password == confirm_password)):
			errors.append("Passwords don't match")	
		if len(errors) is not 0:
			return (False, errors)
		else:
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
			user_count=0
		return (True, new_user)

	def login(self, email, password):
		errors =[]

		user = User.objects.filter(email=email)
		# This query returns as an array, should always be unwrapped/unzipped in order to access the objects in the array!
		if user:
			print user,"user exist", user[0].password 
			compare_password = password.encode()
			if bcrypt.hashpw(compare_password, user[0].password.encode()) == user[0].password:
			# if (user[0].password == password):
				print user[0].password,"That is your password"
				return (True, user)
			else:
				errors.append("password didnt match")
				print "password didnt match"
				return (False, errors)
		else:
			print "no email found"
			errors.append("No email found in our system, please register dude!!!")
			return (False, errors)

class User(models.Model):
	first_name = models.CharField(max_length=45, blank=True, null=True)
	last_name = models.CharField(max_length=45, blank=True, null=True)
	email = models.EmailField(max_length = 255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user_count = models.IntegerField(default=0, blank=True)
	objects = UserManager()

class QuoteManager(models.Manager):
	def add_quote(self, quote_author, quote_text, user):
		errors=[]
		if (len(quote_author) < 4):
			errors.append("Quotes author name must be more than 3 characters")
		if (len(quote_text) < 11):
			errors.append("Text area needs to be more than 10 characters")
		if len(errors) is not 0:
			return (False, errors)
		else:
			new_quote = Quote.objects.create(quote_author=quote_author, quote_text=quote_text, user_id=user)
			new_count = User.objects.get(id=user)
			new_count.user_count = F('user_count') + 1
			new_count.save()
		return(True, new_quote)

class Quote(models.Model):
	quote_text = models.TextField(max_length=1000, blank=True, null=True)
	quote_author = models.CharField(max_length=45, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	objects = QuoteManager()
 
class FaveManager(models.Manager):
	def add_fave(self, user, quote, quote_text, quote_author):
		new_fave=Fave.objects.create(user_id=user, quote_id=quote, quote_text=quote_text, quote_author=quote_author)
		print new_fave.id, new_fave.user.id, new_fave.quote.id,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		return (new_fave)	

class Fave(models.Model):
	quote_text = models.TextField(max_length=1000, blank=True, null=True)
	quote_author = models.CharField(max_length=45, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
	objects = FaveManager()



# Create your models here.
