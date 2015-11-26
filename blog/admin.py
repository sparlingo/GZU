from django.contrib import admin
from .models import Post, Comment, Feedback, Question, Choice, Vote

class ChoiceInLine(admin.TabularInline):
	model = Choice
	extra = 3
	
class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
	('Question to ask', {'fields': ['question_text', 'question_reference']}),
	('Date information', {'fields': ['pub_date']}),
	]
	inlines = [ChoiceInLine]

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Feedback)
admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)