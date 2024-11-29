from django import forms

class BookForm(forms.ModelForm):
    class Meta:
        model = 'Book'
        fields = ['title', 'author']

    # Custom validation example
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if "<script>" in title:
            raise forms.ValidationError("Invalid input.")
        return title