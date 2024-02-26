from django.shortcuts import render

def home_view(request):
    # Your view logic here
    return render(request, 'home.html', {})
