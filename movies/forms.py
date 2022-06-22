from django import forms


from .models import Reviews, Rating, RatingStar, UserProfile


class AddUserForm(forms.ModelForm, ):
    """ Форма изменения пользователя
    """
    class Meta:
        model = UserProfile
        model.podpiska=True
        fields = ("avatar","podpiska", "DateSubDie")

class SaveBuyForm (forms.ModelForm):
    """ Форма изменения пользователя после оплаты
        """
    class Meta:
        model = UserProfile
        fields = ( "podpiska", "DateSubDie")

class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")



class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)