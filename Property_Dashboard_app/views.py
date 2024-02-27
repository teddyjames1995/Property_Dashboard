from django.shortcuts import render

def home_view(request):
    # Updated template path
    return render(request, 'home.html', {})
