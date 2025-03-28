from django.contrib import admin
from .models import Regulation, RegulationFile

class RegulationFileInline(admin.TabularInline):
    model = RegulationFile
    extra = 1

@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    inlines = [RegulationFileInline]
