from django import forms
# from ckeditor.fields import RichTextEditor
class chatform(forms.Form):
    chat=forms.CharField(widget=forms.Textarea(attrs={"id":'chat-message-input','name':'chatmessage'}))