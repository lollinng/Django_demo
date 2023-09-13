from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Choice, Question


# to add the poll app to django admin
# admin.site.register(Question)
# admin.site.register(Choice)

# class QuestionAdmin(admin.ModelAdmin):
#     # fields = ['pub_date','question_text']

class ChoiceInline(admin.TabularInline):
    model = Choice
    # three extra slots to add choices in polls/question
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # The first element of each tuple in fieldsets is the title of the fieldset
    fieldsets = [
        (None,{'fields':['question_text']}),
        ("Data information",{"fields":["pub_date"]})
    ]
    # add choice to it
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date","was_published_recently"]
    # That adds a “Filter” sidebar that lets people filter the change list by the pub_date field:
    list_filter = ["pub_date"]
    search_fields = ["question_text"]


# This particular change above makes the “Publication date” come before the “Question” field:
admin.site.register(Question,QuestionAdmin)

