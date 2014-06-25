# Create your views here.

from django.http import HttpResponse
from django.template import loader,RequestContext

from django.shortcuts import redirect,render_to_response

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from notes_forms import LoginForm
from models import Note,NoteForm



@login_required(login_url="/notes/index/")
def dashboard(request):
    from django.forms.models import inlineformset_factory
    # InlineFormSet with parent_model=User and model=Note
    NoteFormSet=inlineformset_factory(User,Note,can_delete=True,extra=1,form=NoteForm)
    if request.method=="POST":
        formset=NoteFormSet(request.POST,request.FILES,instance=request.user)
        if formset.is_valid():
            # updates and deletes Note objects based on user inputs
            formset.save()
        return redirect("dashboard")
    else:
        qs = Note.objects.order_by('-createTime')
        formset=NoteFormSet(instance=request.user, queryset=qs)
        return render_to_response("dashboard.html",
        {'form':NoteForm(),'formset':formset},RequestContext(request))

@login_required(login_url="/notes/index/")
def dashboard_old(request):
    if request.method=="POST":
        d=request.POST.copy()
        d.update({'owner':request.user.id})
        form=NoteForm(d)
        if not form.is_valid():
            # if form is not valid, return the dashboard template with errors
            template=loader.get_template("dashboard.html")
            rc=RequestContext(request,{'form':form})
            return HttpResponse(template.render(rc))
        # save the note to the database
        note=form.save(commit=False)
        note.owner=request.user
        note.save()
        return render_to_response("dashboard.html",
            {'notes':Note.objects.filter(owner=request.user),'form':form})
    else:
        template=loader.get_template("dashboard.html")
        from django.forms.models import modelformset_factory
        NoteFormSet=modelformset_factory(Note,can_delete=True,extra=0)
        formset=NoteFormSet(queryset=Note.objects.all())
        rc=RequestContext(request,{'form':NoteForm(),'formset':formset,
        'notes':Note.objects.filter(owner=request.user)})
        return HttpResponse(template.render(rc))

def index(request):    
    if request.method=="POST":
        print "Received POST"
        form=LoginForm(request.POST)
        if form.is_valid():
            print "FORM is Valid"
            # user registration or login code
            username,pwd=request.POST.get("username",None),request.POST.get("password")
            if not username or not pwd:
                return HttpResponse("Username or password not present")
            try:
                user=User.objects.get(username__exact=username)
            except ObjectDoesNotExist,ex:
                print "Creating new user..."
                user=User.objects.create_user(username,username,pwd)
            if user:
                print "Authenticating..."
                user=authenticate(username=username,password=pwd)
            print "Logging in user"
            login(request,user)
            return redirect("dashboard")
        else:
            print "FORM is NOT VALID"
            template=loader.get_template("index.html")
            rc=RequestContext(request,{'username':'Sid Azad','form':form})
            return HttpResponse(template.render(rc))
    else:
        template=loader.get_template("index.html")
        rc=RequestContext(request,{'username':'Sid Azad','form':LoginForm()})
        return HttpResponse(template.render(rc))

def dologout(request):
    logout(request)
    return redirect("index")
    


def example(request):
    template=loader.get_template("examples.html")
    temp=72
    rc=RequestContext(request,{
    'fruits':["bananas","berries","kiwis"],
    'username':'Sid Azad',
    'temp':temp})
    return HttpResponse(template.render(rc))
    