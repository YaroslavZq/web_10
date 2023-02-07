from django.forms import ModelForm, CharField, TextInput
from .models import Tag, Quote, Author


class TagForm(ModelForm):
	name = CharField(min_length=3, max_length=30, required=True, widget=TextInput())

	class Meta:
		model = Tag
		fields = ['name']


class QuoteForm(ModelForm):

	text = CharField(min_length=5, max_length=250, required=True, widget=TextInput())

	class Meta:
		model = Quote
		fields = ['text']
		exclude = ['tags', 'author']


class AuthorForm(ModelForm):
	fullname = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
	born = CharField(min_length=3, max_length=50, required=True, widget=TextInput())
	description = CharField(min_length=3, max_length=5000, required=True, widget=TextInput())

	class Meta:
		model = Author
		fields = ['fullname', 'born', 'description']