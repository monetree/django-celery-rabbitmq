from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts
from django.http import JsonResponse
from celery import shared_task

class UsersListView(ListView):
    template_name = 'core/users_list.html'
    model = User


class GenerateRandomUserView(FormView):
    template_name = 'core/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')

@shared_task
def users(request):
    obj = list(User.objects.values())
    # create_random_user_accounts.delay(20)
    # return render()

    return JsonResponse(obj,safe=False)
