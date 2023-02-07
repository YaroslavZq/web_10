from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Quote, Author

# Create your views here.


def main(request):
    quotes = Quote.objects.all()
    return render(request, 'quote_app/index.html', {"quotes": quotes})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quote_app:main')
        else:
            return render(request, 'quote_app/add_author.html', {'form': form})

    return render(request, 'quote_app/add_author.html', {'form': AuthorForm()})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            author = Author.objects.filter(fullname__in=request.POST.getlist('authors'))
            new_note.author = author[0]
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='quote_app:main')
        else:
            return render(request, 'quote_app/add_quote.html', {"tags": tags, "authors": authors, 'form': form})

    return render(request, 'quote_app/add_quote.html', {"tags": tags, "authors": authors, 'form': QuoteForm()})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quote_app:main')
        else:
            return render(request, 'quote_app/add_tag.html', {'form': form})

    return render(request, 'quote_app/add_tag.html', {'form': TagForm()})


@login_required
def delete_quote(request, quote_id):
    Quote.objects.get(pk=quote_id).delete()
    return redirect(to='quote_app:main')


def detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quote_app/detail.html', {"author": author})