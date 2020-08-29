from django.forms import forms, ModelForm

from review.models import userReview


class userReviewForm(ModelForm):

    class Meta:
        model= userReview
        fields=['userComment']