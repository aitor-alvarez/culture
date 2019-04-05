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
    module = Module.objects.get(topics__in=[top_id])
    return render(request, 'culture_content/topics.html', {'topic': topic, 'module': module})


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
    users = User.objects.exclude(id__in=(1, 2, 3))
    modules = Module.objects.filter(language=lang)
    topics = Module.objects.filter(id__in=modules).values('topics')
    scenarios = Topic.objects.filter(id__in=topics).values('scenarios')
    tasks = Scenario.objects.filter(id__in=scenarios).filter(judgment_task__answer__response__user_id__in=users).values('judgment_task')
    tasks = JudgmentTask.objects.filter(id__in=tasks)
    statistics = get_task_statistics(tasks)
    return render(request, 'culture_content/responses.html', {'stats': statistics, 'modules': modules, 'topics': topics})


def get_task_statistics(tasks):
    stats={}
    for task in tasks:
        results=[]
        for response in task.get_answers():
            for res in response.get_responses():
                if res.response >= res.answer.rating_from and res.response <= res.answer.rating_to:
                    results.append(1)
                else:
                    results.append(0)
        stats[task.name]= 100*(sum(results)/len(results))
    return(stats)






