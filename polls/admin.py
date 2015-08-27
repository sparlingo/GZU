from django.contrib import admin

from .models import Question, Choice

class ChoiceInLine(admin.TabularInline):
	model = Choice
	extra = 3
	
class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
	('Question to ask', {'fields': ['question_text', 'question_reference']}),
	('Date information', {'fields': ['pub_date']}),
	]
	inlines = [ChoiceInLine]

	
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)