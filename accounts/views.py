from django.contrib.auth.views import LoginView

class AccountsLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        if self.request.user.is_staff:
            from django.urls import reverse_lazy
            return reverse_lazy('admin:index')
        from django.conf import settings
        return settings.LOGIN_REDIRECT_URL
