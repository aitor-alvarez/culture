"""culture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from culture_content.views import *
from course.views import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('accounts/', include(('django.contrib.auth.urls','django.contrib.auth'), namespace='auth')),

    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', login_required(TemplateView.as_view(template_name="culture_content/home.html")), name="home"),
    path('mod/<str:lang>/', get_modules, name='modules'),
    path('top/<int:top_id>/', get_topic_scenarios, name='topic-scenarios'),
    path('scenario/<int:scenario_id>/', get_scenario_detail, name='scenario'),
    path('course_results/<int:course_id>/', get_user_responses_in_course, name='responses_course'),
    path('save_response/<int:answer_id>/<str:response>', save_response, name='save_response'),
    path('responses/<str:lang>/', get_user_responses, name='responses'),
    path('responses/scenario/<int:scenario_id>/', get_options_results, name='responses'),
    path('dashboard', get_profile, name='profile'),
    path('profile', get_user_data, name='user_profile')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
