from django_filters import FilterSet, BooleanFilter
from django.db import models
from django import forms
from .models import Post
from core.forms import floating_fields
from crispy_bootstrap5.bootstrap5 import Switch, FloatingField
from crispy_forms.layout import Layout, Div, Row, Column, HTML

class PostFilter(FilterSet):
    salvos = BooleanFilter(widget=forms.CheckboxInput, label='Meus Salvos', method='filter_salvo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        floating_fields(self.form)

        self.form.helper.disable_csrf = True

        self.form.fields['user'].label = 'Publicado por'
        self.form.fields['data'].label = 'Data exata'
        self.form.fields['data__gt'].label = 'Após a data'
        self.form.fields['data__lt'].label = 'Anterior a data'

        self.form.helper.layout = Layout(
            Div(
                FloatingField('user', css_class='form-primary')
            ),
            Div(
                HTML('<h6 class="mb-3">Data de Publicação:</h6>'),
                FloatingField('data', css_class='form-primary datepicker'),
                Row(
                    Column(
                        FloatingField('data__gt', css_class='form-primary datepicker')
                    ),
                    Column(
                        FloatingField('data__lt', css_class='form-primary datepicker')
                    )
                )
            ),
            Div(
                Switch('salvos')
            )
        )

    class Meta:
        model = Post
        fields = {
            'user': ['exact'],
            'data': ['lt', 'gt', 'exact']
        }

    def filter_salvo(self, queryset, name, value):
        if value:
            try:
                return queryset.filter(salvo__user=self.request.user).distinct()
            except AttributeError:
                return queryset.filter(salvo__isnull=False).distinct()
        return queryset