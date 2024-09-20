from django.contrib import admin
from .models import Tmax, Tmin, Tmean, Rainfall, Sunshine, Raindays1mm, AirFrost

class WeatherAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)
    
@admin.register(Tmax)
class TmaxAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)

@admin.register(Tmin)
class TminAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)

@admin.register(Tmean)
class TmeanAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)

@admin.register(Rainfall)
class RainfallAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)

@admin.register(Sunshine)
class SunshineAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)

@admin.register(Raindays1mm)
class Raindays1mmAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)

@admin.register(AirFrost)
class AirFrostAdmin(admin.ModelAdmin):
    list_display = ('year', 'month', 'value')
    list_filter = ('year',)
