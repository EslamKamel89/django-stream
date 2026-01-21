from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request: HttpRequest):
        return render(request, "a_home/home.html")
