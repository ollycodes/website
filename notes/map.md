# Django Production Map

* starting a project environment
    1. create project folder
    2. setup venv: `python3 -m venv .venv`
    3. activate venv: `source .venv/bin/activate`
    4. install django: `pip install django`
    5. save version: `pip -m freeze > requirements.txt`

* Creating a view (Part 1 & 3)
    1. create function in **app/views.py**
        - each func must have:
            * a `(request)` parameter
            * a `return HttpResponse()` or `return render()`
    2. tie views.function to url path in **app/urls.py** (create file if absent)
        - before urlpatterns: `from . import views`
        - in urlpatterns: `path('url_string', views.function, name='function')`
            * variables can be assigned via 'url_string': `'<int:pk>/'`
    3. append app app.urls to **core/urls.py** (only needs to be done once per app)
        - in urlpatterns: `path('app/', include('app.urls')),`
    4. `python manage.py runserver`

* app database setup
    1. in **core/settings.py**:
        * edit TIME_ZONE (only needs to be done once per project)
        * add apps to INSTALLED_APPS with either:
            - `app.apps.appConfig`: app/apps.py -> appConfig class
            - `app`: app folder
    2. migrate: `python manage.py migrate`

* Models
    1. change models in **app/models.py**
        - add __str__() to your models!
    2. `python manage.py makemigrations`
    3. `python manage.py migrate`

* Creating an admin user
    1. `python manage.py createsuperuser`
    2. enter username
    3. enter email (optional)
    4. enter pw

* make an app's model modifiable to the admin
    - in **app/admin.py** register:
        * import: `from .models import Model_Name`
        * register: `admin.site.register(Model_Name)`


* Creating a Template
    1. create **templates/app/** directories in **app/** directory
    2. create .html templates in **app/template/app/**
        - python code can be injected with `{%%}`
        - variables can be called with `{{}}`
        - use url tags: `<a href="{% url 'app_name:view_name' url.variable %}">`
    3. namespace url tags in **app/urls.py**:
        - add `app_name = app` above urlpatterns
        - `url.variable` depends on if said url is assigned at URLconfs
    4. update view in **app/views.py**
        - `from django.template import loader`
        - `return render(request, 'app/view_template.html', context)`
        - context: dict of variables available to the code in the .html template
        - raise 404 with: `context = get_object_or_404(Model_Name, pk=Model_id)`




* Flow
    - "ollys.com/blog/1"
    - **core/urls.py**:
        ```python3
        from django.contrib import admin
        from django.url import include, path
        urlpatterns = [
            path('', include('site.urls')),
            # goto blog/urls.py
            path('blog/', include('blog.urls')),
            path('admin/', admin.site.urls),
        ]
        ```
    - **blog/urls.py**:
        ```python3
        from django.urls import path
        
        from . import views

        urlpatterns = [
            path('', views.index, name='index'),
            # goto entry function in views.py with blog_id as keyword argument
            path('<int:blog_id>/', views.entry, name='entry')
        ]
        ```
    - **app/views.py**:
        ```python3
        from django.shortcuts import render

        from . import models

        def index(request):
            posts = models.Post.objects.all()
            # goto template/blog/index.html with context dict(posts=posts)
            # and user's request info
            return render(request, 'blog/index.html', dict(posts=posts))
        ```



* start development server
    1. `python manage.py runserver`
    2. http://127.0.0.1:8000/admin/

[index](index.md)
