from django.http import HttpResponse
from django.shortcuts import render
from .models import Freelancer

'''
def get_user(request, pk):
    freelancer = Freelancer.objects.get(pk=pk)
    return render(request, "users/user_detail.html", {"freelancer": freelancer})
'''

def get_user(request, pk):
    return HttpResponse("Hello, world. You're at the users index.")


print(588 / 28 + 7 - 728 / 26)