from .models import *
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import simplejson
from django.http import JsonResponse, HttpResponseForbidden
from course.models import Course

@login_required
def get_modules(request, lang):
    modules = Module.objects.filter(language=lang).order_by('module_number')
    return render(request, 'culture_content/modules.html', {'modules': modules})


@login_required
def get_topic_scenarios(request, top_id):
    topic = get_object_or_404(Topic, pk=top_id)
    module = Module.objects.get(topics__in=[top_id])
    scenario_results = get_scenarios_responses(top_id, request.user)
    return render(request, 'culture_content/topics.html', {'topic': topic, 'module': module, 'scenario_results': scenario_results})


@login_required
def get_scenario_detail(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    topic = Topic.objects.get(scenarios__in =[scenario_id])
    module = Module.objects.get(topics__in=[topic.id])
    return render(request, 'culture_content/scenario.html', {'scenario': scenario, 'topic':topic, 'module':module})


@login_required
def save_response(request, answer_id, response):
    if request.is_ajax() and request.method=='POST':
        answer = Answer.objects.get(pk=answer_id)
        response = Response.objects.create(answer=answer, response= response, user=request.user)
        expert ={}
        expert['answer_id'] = answer_id
        expert['content'] = answer.content
        expert['feedback'] = answer.feedback_final
        expert['from']=answer.rating_from
        expert['to'] = answer.rating_to
        expert['response_id'] = response.pk
        return JsonResponse(expert, content_type='application/json')


@login_required
def get_user_responses(request, lang):
    statistics = []
    user_profile = Profile.objects.get(user=request.user)
    modules = Module.objects.filter(language=lang)
    topics = Module.objects.filter(id__in=modules).values('topics')
    scenarios = Topic.objects.filter(id__in=topics).values('scenarios')
    scenarios = Scenario.objects.filter(id__in=scenarios)
    for scene in scenarios:
        options_stats, scenario_stats = get_scenario_results(scene.id)
        statistics.append([scene, scenario_stats])
    return render(request, 'culture_content/responses.html', {'stats': statistics, 'user_language': user_profile.language})


@login_required
def get_user_responses_in_course(request, course_id):
    statistics = []
    course = Course.objects.get(id=course_id)
    participants = Course.objects.filter(id=course_id).values_list('participants__user')
    print(participants)
    scenarios = Topic.objects.filter(language=course.language).values('scenarios')
    scenarios = Scenario.objects.filter (id__in=scenarios)
    for scene in scenarios:

        options_stats, scenario_stats = get_scenario_results (scene.id, participants)
        statistics.append ([scene, scenario_stats])
    return render (request, 'culture_content/responses_course.html',{'stats': statistics, 'course': course.name})


def get_scenarios_responses(topic_id, current_user):
    statistics = []
    scenarios = Topic.objects.filter(id=topic_id).values('scenarios')
    scenarios = Scenario.objects.filter(id__in=scenarios)
    for scene in scenarios:
        options_stats, scenario_stats = get_scenario_results(scene.id, current_user)
        statistics.append([scene, scenario_stats])
    print(statistics)
    return statistics


@login_required
def get_options_results(request, scenario_id):
    scenario = Scenario.objects.get (id=scenario_id)
    options_stats, scenario_stats = get_scenario_results(scenario_id)
    user_profile = Profile.objects.get (user=request.user)
    return render (request, 'culture_content/options_responses.html', {'stats': options_stats, 'user_language': user_profile.language, 'scenario_language': scenario.get_scenario_language()})


def get_scenario_results(scenario_id, users=None):
    scenario = Scenario.objects.get(pk=scenario_id)
    options = []
    attempts = []
    stats = []
    for answer in scenario.judgment_task.get_answers ():
        options.append (answer)
        results = []
        responses = 0
        if users:
            answer_responses=answer.get_user_responses(users)
        else:
            answer_responses=answer.get_responses()
        for res in answer_responses:
            responses += 1
            if res.response >= res.answer.rating_from and res.response <= res.answer.rating_to:
                results.append(1)
            else:
                results.append(0)
        attempts.append(round(len(results)))
        if len(results)>0:
            stats.append(round(100 * (sum (results)/len(results))))
        else:
            stats.append(0)
    output = zip (options, attempts, stats)
    scenario_stats=(attempts[0], round(sum(stats)/len(stats)))
    return(output, scenario_stats)


@login_required
def get_profile(request):
    if request.user.is_staff:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'culture_content/dashboard.html', {'profile': profile})
    else:
        return HttpResponseForbidden()




