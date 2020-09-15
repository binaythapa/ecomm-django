from django.forms import forms, ModelForm
from review.models import Comment

class userReviewForm(ModelForm):

    class Meta:
        model= Comment
        fields=['userComment']