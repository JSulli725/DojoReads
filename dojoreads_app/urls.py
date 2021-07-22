from django.urls import path
from .views import *

urlpatterns = [
    path('', homePage),
    path('registration', registration),
    path('verify_login', verify_login),
    path('books', view_main),
    path('books/add', addBook),
    path('books/create_book', createBook),
    path('books/<int:id>', viewBook),
    path('addReview/<int:id>', addReview),
    path('books/deleteReview/<int:book_id>/<int:review_id>', deleteReview),
    path('users/<int:id>', loadUser),
    path('logout', logout),
]




# if request.POST['author_dropdown'] == "-1":
#             if request.POST['author_name'] ==  "":
#                 messages.error(request, "Please either choose an author from the dropdown or create a new one")
#             else:
#                 author_errors = Author.objects.author_validator(request.POST)
#                 errors+= list(author_errors.values())
        
#         if errors:
#             for error in errors:
#                 messages.error(request, error)
#             return redirect('/book/book_form')