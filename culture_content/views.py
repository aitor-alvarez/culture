from .models import *
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import simplejson
from django.http import JsonResponse

@login_required
def get_modules(request, lang):
    modules = Module.objects.filter(language= lang).order_by('module_number')
    return render(request, 'culture_content/modules.html', {'modules': modules})

@login_required
def get_topic_scenarios(request, top_id):
    topic = get_object_or_404(Topic, pk=top_id)
    return render(request, 'culture_content/topics.html', {'topic': topic})

@login_required
def get_scenario_detail(request, scenario_id):
    scenario = get_object_or_404(Scenario, pk=scenario_id)
    topic = Topic.objects.filter(scenarios__id =scenario_id)
    return render(request, 'culture_content/scenario.html', {'scenario': scenario, 'topic':topic})

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