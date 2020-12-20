from django.shortcuts import render
from .models import Movie


# Create your views here.
def index(request):
    home_obj = Movie.objects.all()
    homeworks = []
    if home_obj:
        for item in home_obj:
            if item.star > 3:
                homeworks.append(item)
        return render(request, "algorithms/index.html", {"homeworks": homeworks})
    else:
        return render(request, "algorithms/index.html", {"homeworks": homeworks})
