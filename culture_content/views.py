from .models import *
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def get_modules(request, lang):
    modules = Module.objects.filter(language= lang)
    return render(request, 'culture_content/modules.html', {'modules': modules})


def get_topic_scenarios(request, top_id):
    topic = get_object_or_404(Topic, pk=top_id)
    return render(request, 'culture_content/topics.html', {'topic': topic})


def get_scenario_detail(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    topic = Topic.objects.filter(scenarios__id =scenario_id)
    return render (request, 'culture_content/scenario.html', {'scenario': scenario, 'topic':topic})


def save_response(request, answer_id, response):
    if request.is_ajax() and request.method=='POST':
        answer = Answer.objects.get(pk=answer_id)
        response = Response.objects.create(answer=answer, response= response, user=request.user)
        return HttpResponse("Saved")