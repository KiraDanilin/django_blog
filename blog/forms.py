from django import forms
from django.core.exceptions import ValidationError

from .models import Tag, Post


class TagForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # slug = forms.CharField(max_length=50)
    #
    # title.widget.attrs.update({'class': 'form-control'})
    # slug.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tag
        fields = ["title", "slug"]

        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "slug": forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data.get('slug').lower()

        if new_slug == 'create':
            raise ValidationError("Slug may not be 'Create'")  # is it right????

        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError(f"Slug '{new_slug}' already exist")

        return new_slug

    # def save(self):  # есть свой метод с большим функционалом
    #     new_tag = Tag.objects.create(**self.cleaned_data)
    #     return new_tag


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "slug", "body", "tags"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={'class': 'form-control'}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data.get('slug').lower()

        if new_slug == 'create':
            raise ValidationError("slug may not be 'Create'")

        # if Post.objects.filter(slug__iexact=new_slug).count():
        #     raise ValidationError("Post with passed slug already exist")

        return new_slug
