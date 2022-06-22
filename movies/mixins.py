from .models import UserProfile
from django import views

class ProfileMixin(views.generic.detail.SingleObjectMixin, views.View):
    def dispatch(self, request, *args, **kwargs ):
        if request.user.is_authenticated:
            userprofile=UserProfile.objects.filter(user=request.user).first()
            if not userprofile:
                userprofile=UserProfile.objects.create(user=request.user)
            userprofile.save()
        return super().dispatch(request, *args, **kwargs)
