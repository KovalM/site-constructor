import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
import watson
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.views.generic import FormView
from registration.backends.default.views import RegistrationView
from django.shortcuts import render_to_response
from django.contrib import auth
from article.forms import CreateProjectForm, CreatePageForm, GalleryImageForm
from article.models import Project, PageProject, Raitng, Like, Gallery
from django.template import RequestContext

cloudinary.config(
    cloud_name="dowzzsdtc",
    api_key="588197345913843",
    api_secret='MQgCAff-steIYQ3cKyb8L3m7_mM'
)

def view_site(request, id_project):
    if not valid_project(id_project):
        return redirect("/my_projects/")
    if request.method == 'POST':
        data = {'page': 'hui'}
        id_p = request.POST.get('id_return_page')
        if id_p:
            p = PageProject.objects.get(id=id_p)
            data['page'] = p.text
            return HttpResponse(json.dumps(data), content_type="application/json")
    pages = PageProject.objects.filter(project=Project.objects.get(id=id_project))
    project = Project.objects.get(id=id_project)
    return render_to_response('view_site_template.html',
                              {'project': project,
                               'pages': pages,
                               'user': request.user,
                               'url':request.META['HTTP_REFERER']}, RequestContext(request))

def valid_project(id_project):
    if not id_project.isnumeric() or len(Project.objects.filter(id=id_project))<1 or len(id_project) < 1:
        return False
    return True




def create_delete_rating(request):
    data = {}
    if request.method == 'GET':
        id_rating = request.GET.get('id_delete_rating')
        if id_rating:
            rating = Raitng.objects.filter(id=id_rating)
            rating.delete()
            data['response'] = 'success'
            return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == 'GET':
        id_project = request.GET.get('id_project_create_rating')
        if id_project:
            p = Raitng.objects.create(raiting_project=Project.objects.get(id=id_project))
            data['response'] = 'success'
            data['id_rating'] = p.id
    return HttpResponse(json.dumps(data), content_type="application/json")


def set_likes(request):
    data = {'response': 'hui'}
    if request.method == 'GET':
        id_rating = request.GET.get('id_rating')
        if id_rating and request.user.is_authenticated():
            like = Like.objects.filter(raiting=Raitng.objects.get(id=id_rating), user=request.user)
            if like:
                like.delete()
            else:
                Like.objects.create(raiting=Raitng.objects.get(id=id_rating), user=request.user)
            data['response'] = get_number_of_likes(id_rating)
        id_rating_get_likes = request.GET.get('id_rating_get_likes')
        if id_rating_get_likes:
            data['response'] = get_number_of_likes(id_rating_get_likes)
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_number_of_likes(id_rating):
    likes = Like.objects.filter(raiting=Raitng.objects.get(id=id_rating))
    return len(likes)


def get_main_page(request):
    total = Project.objects.filter().count()
    last_sites = Project.objects.filter()[total-5:total] if total > 5 else Project.objects.filter()[0:5]
    top_sites = get_top_sites()
    return render_to_response('index.html', {'user': request.user, 'last_sites': last_sites,
                                            'top_sites': top_sites},
                              RequestContext(request))
def get_top_sites():
    top_rating = []
    all_ratings = Raitng.objects.all()
    while len(top_rating) < 5:
        max = 0
        candidate = None
        for current_raiting in all_ratings:
            num = get_number_of_likes(current_raiting.id)
            if num > max and not found_in_list_of_dictionaries(current_raiting,top_rating):
                max = num
                candidate = current_raiting
        if candidate is None:
            break
        top_rating.append({'candidate': candidate, 'maximum': max})
    top_sites = []
    for raiting in top_rating:
        top_sites.append({'top_project': raiting['candidate'].raiting_project,
                          'number_of_likes': raiting['maximum']})
    return top_sites

def found_in_list_of_dictionaries(element, list_of_dictionaries):
    for current in list_of_dictionaries:
        if element.raiting_project.id is current['candidate'].raiting_project.id:
            return True
    return False

def logout(request):
    auth.logout(request)
    return redirect('/')


def create_project(form, request):
    if form.is_valid():
        Project.objects.create(project_name=form.cleaned_data['project_name'],
                               project_user=request.user)
        watson.update_index()

def add_images(request, form):
    if form.is_valid():
        Gallery.objects.create(user=request.user, image=form.cleaned_data['image'])

@login_required(login_url="/")
def get_user_projects(request):
    if request.method == 'POST':
        idr = request.POST.get('proj_id')
        if idr:
            p = Project.objects.get(id=idr)
            if p.project_user == request.user:
                p.delete()
    form = CreateProjectForm(request.POST)
    form_image = GalleryImageForm(request.POST, request.FILES)
    add_images(request, form_image)
    create_project(form, request)
    projects = Project.objects.filter(project_user=request.user)
    return render_to_response("user_projects.html", {'user': request.user,
                                                     'projects': projects,
                                                     'images': Gallery.objects.filter(user=request.user),
                                                     'img_form': form_image,
                                                     'form': form}, RequestContext(request))

class UserCreateProject(FormView):
    form_class = CreateProjectForm
    template_name = 'user_projects.html'
    success_url = '/'

class RegisterFormView(RegistrationView):
    template_name = "registration.html"

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/my_projects/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

@login_required(login_url='/')
def edit_view(request, ids):
    if not valid_project(ids):
        return redirect("/my_projects/")
    current_project =Project.objects.get(id=ids)
    if current_project.project_user != request.user and not request.user.is_staff:
        return redirect("/my_projects")
    page_form = CreatePageForm(request.POST)
    requests_editor(request, page_form, current_project)
    save_pages(request)
    if request.method == 'POST':
        data = {'page': 'error'}
        id_p = request.POST.get('id_return_page')
        if id_p:
            p = PageProject.objects.get(id=id_p)
            data['page'] = p.text
            return HttpResponse(json.dumps(data), content_type="application/json")
    pages = PageProject.objects.filter(project=current_project)
    return render_to_response('editor.html', {'user': request.user,
                                              'project': current_project,
                                              'pages': pages,
                                              'page_form': page_form,
                                              'images': Gallery.objects.filter(user=request.user)},
                              RequestContext(request))

def save_pages(request):
    if request.method == 'POST':
        id_page = request.POST.get('id_page')
        if id_page:
            p = PageProject.objects.get(id=id_page)
            p.text = request.POST.get('content')
            p.save()

def requests_editor(request, form, current_project):
    if form.is_valid():
        PageProject.objects.create(project=current_project, page_name=form.cleaned_data['page_name'])

def search_form(request):
    return render_to_response('search_form.html', {'user': request.user})

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        search_results = watson.search(str(q))
        projects = []
        users = []
        for result in search_results:
            if type(result.object) is User:
                users.append(result.object)
            elif type(result.object) is Project and result.object not in projects:
                projects.append(result.object)
            elif type(result.object) is PageProject and result.object.project not in projects:
                projects.append(result.object.project)
        return render_to_response('search_form.html',
                                  {'query': q, 'user': request.user, 'users': users, 'projects': projects},
                                  RequestContext(request))
    else:
        return render_to_response('search_form.html', {'user': request.user}, RequestContext(request))

def change_theme(request):
    if request.method == 'GET':
        id_p = request.GET.get('proj_id')
        value = request.GET.get('is_dark')
        if id_p:
            p = Project.objects.get(id=id_p)
            p.project_is_dark = True if value == 'True' else False
            p.save()
    return HttpResponse(json.dumps({}), content_type="application/json")


def change_menu(request):
    if request.method == 'GET':
        id_p = request.GET.get('proj_id')
        value = request.GET.get('is_horizontal')
        if id_p:
            p = Project.objects.get(id=id_p)
            if request.user == p.project_user or request.user.is_staff:
                p.project_menu_is_horizontal = True if value == 'True' else False
                p.save()
    return HttpResponse(json.dumps({}), content_type="application/json")



def change_site_name(request):
    new_site_name = []
    if request.method == 'GET':
        id_p = request.GET.get('proj_id')
        new_site_name = request.GET.get('new_site_name')
        if id_p:
            p = Project.objects.get(id=id_p)
            if request.user == p.project_user or request.user.is_staff:
                p.project_name = new_site_name
                p.save()
    return HttpResponse(json.dumps({'newName': new_site_name}), content_type="application/json")

def remove_page(request):
    if request.method == 'POST':
        idr = request.POST.get('page_id')
        if idr:
            p = PageProject.objects.get(id=idr)
            if p.project.project_user == request.user:
                p.delete()
    return HttpResponse(json.dumps({}), content_type="application/json")

def view_another_user(request, id_user):
    if not id_user.isnumeric() or len(User.objects.filter(id=id_user))<1 or len(id_user) < 1:
        return redirect("/")
    currrent_user = User.objects.get(id=id_user)
    projects = Project.objects.filter(project_user=currrent_user)
    return render_to_response('view_user.html',
                              {'user_of_projects': currrent_user,'projects': projects,
                               'user': request.user}, RequestContext(request))
