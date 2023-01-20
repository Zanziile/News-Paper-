from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
                 'author',
                 'title',
                 'post_choice',
                 'category',
                 'body'
                  ]

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get("body")
        title = cleaned_data.get("title")

        if body is not None and len(title) < 20:
            raise ValidationError({
                "body": "Заголовок должен содержать больше 20 символов и контент не может быть пустым"
            })

        if title == body:
            raise ValidationError(
                "Описание не должно быть идентично названию"
            )

        return cleaned_data
