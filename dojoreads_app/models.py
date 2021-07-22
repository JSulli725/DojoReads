from typing import Text
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, TextField, related
import re

class userManager(models.Manager):
    def userValidation(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name must be at least 2 characters"
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address")
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = "Passwords do not match"
        return errors

class bookManager(models.Manager):
    def bookValidation(self, postData):
        all_books = Book.objects.all()
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "Title must be 2 or more characters"
        if postData['title'] in all_books:
            errors['title'] = "That book already exists"
        return errors

class authorManager(models.Manager):
    def authorValidation(self, postData):
        errors = {}
        if len(postData['author_name']) < 2:
            errors['author_name']= "Author name must be 2 or more characters"
        author_in_db = Author.objects.filter(name=postData['author_name'])
        if len(author_in_db) >= 1:
            errors['duplicate'] = "Author already exists."
        return errors

class reviewManager(models.Manager):
    def reviewValidation(self, postData):
        errors = {}
        if postData['rating']:
            if len(postData['review']) == 0:
                errors['review'] = "Review must be at least 10 characters"
        if postData['review']:
            if len(postData['review']) < 10:
                errors['review'] = "Review must be at least 10 characters"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()


class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = bookManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    books = models.ForeignKey(Book, related_name = "authors", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = authorManager()

class Review(models.Model):
    body = models.TextField()
    rating = models.IntegerField()
    user_review = models.ForeignKey(User, related_name = "reviews", on_delete = models.CASCADE)
    reviewed_book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = reviewManager()