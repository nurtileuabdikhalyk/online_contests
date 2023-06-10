from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone')
    list_display_links = ('id', 'first_name', 'last_name',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant', 'contest', 'score')
    list_display_links = ('id', 'participant', 'contest',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'created')
    list_display_links = ('id', 'name', 'phone')


@admin.register(Vote)
class VotingAdmin(admin.ModelAdmin):
    list_display = ('id', 'contest', 'participant')
    list_display_links = ('id', 'contest', 'participant')


@admin.register(Jury)
class JuryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'contest',)
    list_display_links = ('id', 'user', 'contest',)
