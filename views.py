from django.shortcuts import render, redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.views.generic import TemplateView, DeleteView, UpdateView
from django import forms
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Recipe, Review
from .forms import ReviewForm, RecipeForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404


class Register(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8)
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8)
    
def home(request):
    return render(request, 'index.html', {
        'title' : 'Home'
    })
    

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home:recipes')  
        else:
            messages.error(request, "Invalid credentials!")
    return render(request, 'login.html', {'title': 'Login'})

    
def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            password2 = form.cleaned_data["password2"]

            if password != password2:
                messages.error(request, "Passwords do not match!")
                return redirect("home:register")

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect("home:register")

            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            auth_login(request, user)  
            return HttpResponseRedirect(reverse("home:index"))
        else:
           form = Register()
           return render(request, "register.html", {"form": form})

    else:
        form = Register()
        return render(request, "register.html", {"form": form})    

def recipe_list(request):
    if not request.user.is_authenticated:
        return redirect('home:login')
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    review_form = ReviewForm()

    if request.method == 'POST':
        
        if 'add_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.recipe = recipe
                review.user = request.user
                review.save()
                return redirect('home:recipe_detail', recipe_id=recipe_id)

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'review_form': review_form,
        'is_owner': request.user == recipe.created_by
    })

def add_recipe(request):
    if not request.user.is_authenticated:
        return redirect('home:login')
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            return redirect('home:recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    
    return render(request, 'add_recipe.html', {'form': form})


def test_func(self):
        return self.request.user == self.get_object().user
        
def update_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('home:recipe_detail', recipe_id=recipe.id)  
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'update_recipe.html', {'form': form, 'recipe': recipe})


def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        recipe.delete()  
        return redirect('home:recipes')  

    return render(request,'recipe_confirm_delete.html', {'recipe': recipe})  
    