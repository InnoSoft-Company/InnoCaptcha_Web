from django.shortcuts import render

def index(request): return render(request, "index.html")

def terms(request): return render(request, "terms.html")

def privacy(request): return render(request, "privacy.html")

def dashboard(request): return render(request, "dashboard.html")

def support(request): return render(request, "support.html")