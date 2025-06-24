from django.shortcuts import render,redirect
#from django.http import HttpResponse
from . models import MovieInfo
from . forms import MovieForm
#Authentication..........
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def create(request):
    frm=MovieForm()
    if request.POST:
        # print(request.POST)
        # print(request.POST.get('year'))
        
        # title = request.POST.get('title')
        # year = request.POST.get('year')
        # desc = request.POST.get('description')
        # movie_obj=MovieInfo(title=title, year=year, description=desc)
        # movie_obj.save()

        frm=MovieForm(request.POST, request.FILES)
        if frm.is_valid():
            frm.save()
            return redirect('list')
        else:
            frm=MovieForm()

    return render(request, 'create.html',{'frm':frm})

@login_required(login_url='/login/')
def list(request):
    #print(request.session)
    #print(request.COOKIES)

    ##visits counts using cookies.........
    # visits = int(request.COOKIES.get('visits',0))
    # visits=visits+1
    # movie_set=MovieInfo.objects.all()

    ##Recent Visits.........
    recent_visits=request.session.get('recent_visits',[])

    ##visits counts usings sessions..........
    count = request.session.get('count',0)
    count = int(count)
    count = count+1
    request.session['count']=count
    ##Recent Visits................
    recent_movie_set = MovieInfo.objects.filter(pk__in=recent_visits)

    ##ORM Queries.........
    #movie_set=MovieInfo.objects.filter(year=2023,title='Jailer')
    #movie_set=MovieInfo.objects.exclude(year=2023).order_by('-year')
    #movie_set = MovieInfo.objects.filter(year__gt=2023)
    #movie_set = MovieInfo.objects.filter(actors__name='Mohanlal')
    movie_set = MovieInfo.objects.all()

    response = render(request, 'list.html', {
        'recent_movies':recent_movie_set,
        'movies':movie_set,'visits':count })
    #response.set_cookie('visits',visits)
    return response

@login_required(login_url='/login/')
def edit(request,pk):
    instance_to_be_edited=MovieInfo.objects.get(pk=pk)
    if request.POST:
        # title=request.POST.get('title')
        # instance_to_be_edited.title=title
        # instance_to_be_edited.save()
        frm=MovieForm(request.POST,request.FILES, instance=instance_to_be_edited)
        if frm.is_valid():
            instance_to_be_edited.save()
            return redirect('list')
    else:
        #recent visits.............
        recent_visits=request.session.get('recent_visits',[])
        recent_visits.insert(0,pk)
        request.session['recent_visits']=recent_visits

        frm=MovieForm(instance=instance_to_be_edited)
        
    frm=MovieForm(instance=instance_to_be_edited)
    return render(request, 'create.html',{'frm':frm})

def home(request):  #  HOME VIEW
    return render(request, 'home.html')

@login_required(login_url='/login/')
def delete(request,pk):
    instance=MovieInfo.objects.get(pk=pk)
    instance.delete()
    movie_set=MovieInfo.objects.all()
    return render(request, 'list.html', {'movies':movie_set })
