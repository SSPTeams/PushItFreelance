from django.http import HttpResponse
from django.shortcuts import render


def get_user(request, pk):
    return HttpResponse("Hello, world. You're at the users index.")

