from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib import admin
from .models import *

class TextMedia:
    js = [
         '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class AnswerInline(admin.TabularInline):
    model = Answer
    exclude = ['feedback_initial']

class MCQuestionAdmin(admin.ModelAdmin):
    class Meta:
        model = JudgmentTask
        exclude = []
    list_display = ('name', )
    list_filter = ('name',)
    fields = ('name', 'description' )

    search_fields = ('name', )
    inlines = [AnswerInline]


class TopicAdmin (admin.ModelAdmin):
    class Meta:
        model = Topic
        exclude = []
    scenarios = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(),
                                               required=True,
                                               widget=FilteredSelectMultiple(
                                                   verbose_name='Scenarios',
                                                   is_stacked=False)
                                               )
    filter_horizontal = ('scenarios',)

    def get_queryset(self, request):
        profile = Profile.objects.get(user = request.user)
        if profile.language == 'L':
            return Topic.objects.all()
        else:
            return Topic.objects.filter(language= profile.language)


class ScenarioAdmin(admin.ModelAdmin):
    class Meta:
        model = Scenario
        exclude = []

    def get_queryset(self, request):
        profile = Profile.objects.get(user = request.user)
        if profile.language == 'L':
            return Scenario.objects.all()
        else:
            scenarios_topics = Topic.objects.filter(language= profile.language)
            scenario_ids = [scenario.pk  for topic in scenarios_topics for scenario in topic.scenarios.all()]
            return Scenario.objects.filter(id__in =scenario_ids)


admin.site.register(Module,  Media=TextMedia)
admin.site.register(Scenario,  ScenarioAdmin, Media=TextMedia)
admin.site.register(JudgmentTask, MCQuestionAdmin)
admin.site.register(Topic, TopicAdmin,  Media=TextMedia)
admin.site.register(Response)
admin.site.register(LearningObjectives, Media=TextMedia)
admin.site.register(Profile)
admin.site.register(FeedbackLabels)