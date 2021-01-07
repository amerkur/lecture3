from django import forms
from django.http import request
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

class NewTaskForm(forms.Form):
    form_task = forms.CharField(label="New Task")
    form_num = forms.IntegerField(label="Priority", min_value=1, max_value=10)

# Create your views here.

def index(request):
    if "task_list" not in request.session:
        request.session["task_list"] = []  ## using sessions so nobody else access this list
        ## replaced global variable task_list = []
    return render(request, "tasks/index.html", {
        "todos": request.session["task_list"] ## rendered in index.html in {% for todo in todos %}
    } )

def add(request):
    if request.method == "POST":
        formed = NewTaskForm(request.POST)  #POSTed data + form stored in formed
        if formed.is_valid(): # if all 'formed' fields correct ie. text=text, etc
            clean_form_task = formed.cleaned_data["form_task"] # Calling NewTaskForm() stores function in 'form_task'
            clean_form_num = formed.cleaned_data["form_num"]
            request.session["task_list"] += [clean_form_task, clean_form_num]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": formed ## rendered in add.html {{ form }}
            })

    # first visit as HTTP GET and not POST
    return render(request, "tasks/add.html", {
        "form": NewTaskForm() ## rendered in add.html {{ form }}
    })