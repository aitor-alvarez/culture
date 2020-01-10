from django.shortcuts import render
from culture_content.models import *
from culture_content.views import get_scenario_results
from .models import Course
from django.contrib.auth.decorators import login_required


@login_required
def get_user_data(request):
    user_profile = Profile.objects.get(user=request.user)
    if user_profile.type=='I':
        courses = Course.objects.filter(instructor=request.user)
        return render(request, 'course/instructor.html', {'courses': courses})
    elif user_profile.type=='S':
        user_scenarios = Response.objects.filter(user=request.user).values('answer__task__scenario')
        scenarios =set([scenario['answer__task__scenario'] for scenario in user_scenarios])
        statistics=[]
        for scene in scenarios:
            if scene is not None:
                options_stats, scenario_stats = get_scenario_results(scene)
                scenario = Scenario.objects.get(id=scene)
                statistics.append ([scenario, scenario_stats])

        return render(request, 'course/student.html', {'results': statistics})





