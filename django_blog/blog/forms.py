from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Tag
from taggit.forms import TagWidget

# create forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Enter tags separated by commas")
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags separated by commas'}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tags = self.cleaned_data['tags']
            if tags:
                tag_names = [t.strip() for t in tags.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
        return instance
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here..'})}
    