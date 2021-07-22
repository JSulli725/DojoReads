from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def homePage(request):
    return render(request, 'homePage.html')

def registration(request):
    errors = User.objects.userValidation(request.POST)
    user_email = User.objects.filter(email = request.POST['email'])
    if user_email:
        messages.error(request, "Email already exists")
        return redirect('/')
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    password = request.POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        name = request.POST['name'],
        alias = request.POST['alias'],
        email = request.POST['email'],
        password = hashed_password
        )
    request.session['logged_in_user'] = new_user.id
    return redirect('/books')

def verify_login(request):
    user = User.objects.filter(email=request.POST['login_email'])
    if user:
        login_user = user[0]
        if bcrypt.checkpw(request.POST['login_password'].encode(), login_user.password.encode()):
            request.session['logged_in_user'] = login_user.id
            return redirect('/books')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/')
    messages.error(request, "Invalid email address")
    return redirect('/')


def view_main(request):
    context = {
        "user": User.objects.get(id=request.session['logged_in_user']),
        "books": Book.objects.all(),
        "reviews": Review.objects.all(),
        "latest_reviews": Review.objects.order_by('-created_at')[:3],
        "remaining_reviews": Review.objects.order_by('-created_at')[3:]
        }
    return render(request, 'view_main.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')


def addBook(request):
    context = {
        "authors": Author.objects.all(),
    }
    return render(request, 'addBook.html', context)

def createBook(request):
    if 'logged_in_user' not in request.session:
        messages.error(request, "Please log in to add a book")
        return redirect('/books/add')
    if request.method == "POST":
        book_errors = Book.objects.bookValidation(request.POST)
        review_errors = Review.objects.reviewValidation(request.POST)
        errors = list(book_errors.values())+list(review_errors.values())

        if request.POST['author_select'] == "no_author_given":
            if len(request.POST['author_name']) == 0:
                messages.error(request, "You must add an author or choose one from the dropdown")
            else:
                author_errors = Author.objects.authorValidation(request.POST)
                errors+= list(author_errors.values())

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('/books/add')
        
        new_book = Book.objects.create(
        title = request.POST['title']
        )

        if request.POST['author_select'] == "no_author_given":
            author = Author.objects.create(
            name = request.POST['author_name'],
            books = new_book
            )
        else:
            author = Author.objects.get(id = request.POST['author_select'])
    
        new_book.authors.add(author)

        Review.objects.create(
            body = request.POST['review'],
            rating = int(request.POST['rating']),
            user_review = User.objects.get(id=request.session['logged_in_user']),
            reviewed_book = new_book
        )
        return redirect(f"/books/{new_book.id}")
    return redirect('/books/add')

def viewBook(request, id):
    if 'logged_in_user' not in request.session:
        messages.error(request, "You must be logged in to view this book")
        return redirect('/')
    book = Book.objects.get(id=id)
    rating = book.reviews.all()
    these_authors = book.authors.all()
    context = {
        "user": User.objects.get(id=request.session["logged_in_user"]),
        "authors": these_authors,
        "reviews": book.reviews.all(),
        "this_book": book,
        "ratings": rating
    }
    return render(request, 'view_book.html', context)


def addReview(request, id):
    this_book = Book.objects.get(id=id)
    reviews = this_book.reviews.all()
    this_user = User.objects.get(id=request.session['logged_in_user'])
    for review in reviews:
        if review.user_review.id == this_user.id:
            messages.error(request, "You have already reviewed/rated this book.")
            return redirect(f'/books/{this_book.id}')
    errors = Review.objects.reviewValidation(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/books/{id}')
    new_review = Review.objects.create(
        body = request.POST['review'],
        rating = request.POST['rating'],
        user_review = User.objects.get(id=request.session['logged_in_user']),
        reviewed_book = this_book
    )
    return redirect(f'/books/{id}')

def deleteReview(request, book_id, review_id):
    book = Book.objects.get(id=book_id)
    review = Review.objects.get(id=review_id)
    review.delete()
    return redirect(f'/books/{book.id}')

def loadUser(request, id):
    user = User.objects.get(id=id)
    context = {
        "user" : user,
        "total_reviews": user.reviews.all(),
        "books_reviewed": user.reviews.all()
    }
    return render(request, 'view_user.html', context)