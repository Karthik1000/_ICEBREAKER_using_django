from django.shortcuts import render
from .models import Testimony
from django.http import HttpResponse
from .forms import TestimonyForm
from django.db.models import Q
# Create your views here.
def all_profiles(request):
    all_profiles = Testimony.objects.all()
    query = request.GET.get('q')
    if query:
        all_profiles = Testimony.objects.filter(
        Q(name__icontains=query)|
        Q(to_name__icontains=query)

        )
    context = {
        'all_profiles': all_profiles
    }
    # return render(request, 'proj/detail.html')
    return render(request, 'testimony/search.html', {'all_profiles': all_profiles})


def Home_view(request):
    return render(request,'testimony/pa.html')
def Testimony_view(request):
    if request.method == 'POST':

        testimony_form = TestimonyForm(data=request.POST)
        if testimony_form.is_valid():
            prof=testimony_form.save(commit=False)


            prof.save()

            all_profiles = Testimony.objects.all().order_by('timestamp')
            context = {
                'all_profiles': all_profiles
            }
            #return render(request, 'proj/detail.html')
            return render(request, 'testimony/home.html',context)
            #return HttpResponse('successfully done')
            #messages.error(request, ('Please correct the error below.'))
    else:

        testimony_form = TestimonyForm()
    return render(request, 'testimony/testimony.html', {'testimony_form': testimony_form})
