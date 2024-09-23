from django.contrib import admin
from django import forms
from .models import WeatherData
import json

class DynamicDataForm(forms.ModelForm):
    """Custom form to handle dynamic data as key-value pairs."""
    
    dynamic_data = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Dynamic weather data in key-value pairs (JSON format)."
    )

    class Meta:
        model = WeatherData
        fields = ['year', 'month', 'dynamic_data']

    def clean_dynamic_data(self):
        """Validate and return dynamic_data as a dict."""
        data = self.cleaned_data.get('dynamic_data')
        if data:
            try:
                json_data = json.loads(data)
                if not isinstance(json_data, dict):
                    raise forms.ValidationError("Dynamic data must be a valid JSON object.")
            except ValueError:
                raise forms.ValidationError("Invalid JSON format.")
            return json_data
        return {}

class DynamicDataSearchFilter(admin.SimpleListFilter):
    title = 'Dynamic Data Key'
    parameter_name = 'dynamic_data_key'

    def lookups(self, request, model_admin):
        keys = set()
        for weather_data in model_admin.model.objects.all():
            if weather_data.dynamic_data:
                keys.update(weather_data.dynamic_data.keys())
        return [(key, key) for key in keys]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(dynamic_data__has_key=self.value())
        return queryset

class WeatherAdmin(admin.ModelAdmin):
    form = DynamicDataForm
    list_display = ('year', 'month', 'formatted_dynamic_data')
    list_filter = ('year', DynamicDataSearchFilter)
    search_fields = ['year', 'month', 'dynamic_data']

    def formatted_dynamic_data(self, obj):
        """Format the dynamic_data for display in a table."""
        if obj.dynamic_data:
            return ", ".join(f"{key}: {value}" for key, value in obj.dynamic_data.items())
        return "No data"
    
    formatted_dynamic_data.short_description = 'Dynamic Data'

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        # Check if the search term is a digit and search in month
        if search_term.isdigit():
            queryset |= self.model.objects.filter(month=int(search_term))
        
        if search_term:
            queryset |= self.model.objects.filter(dynamic_data__icontains=search_term)
        
        return queryset, use_distinct

admin.site.register(WeatherData, WeatherAdmin)
