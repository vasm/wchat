from .models import Message, UserPresence, update_last_seen_time
from .forms import UserRegistrationForm

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.template import Context

from django.contrib.auth import logout as logout_session

from django.contrib.auth.models import User as User
from django.template.loader import get_template
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


@login_required
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/chat')


def get_contacts(exclude_user_id):
    return User.objects.filter(id__ne=exclude_user_id).\
        order_by('-userpresence__last_seen')


def get_contacts_as_html(exclude_user_id):
    tpl = get_template('user-list.html')
    return escape(tpl.render(
        Context({'user_list': get_contacts(exclude_user_id)})))


def get_new_messages_as_html(self_id, message_list):
    tpl = get_template('message-list.html')
    return escape(tpl.render({'messages': message_list,
                              'self_id': self_id}))


@login_required
def chat(request):
    current_user = User.objects.get(id=request.user.id)
    update_last_seen_time(current_user)

    message_list = Message.objects.order_by('id')

    return render(
        request,
        'chat.html',
        {
            'messages': message_list,
            'self_id': request.user.id,
            'user_list': get_contacts(request.user.id),
            'last_message':
                message_list.last().id if len(message_list) > 0 else 0
        }
    )


def contacts(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            update_last_seen_time(request.user)

            json_data = {
                'status': 'ok',
                'contact_list_html':
                    get_contacts_as_html(request.user.id)
            }

            return JsonResponse(json_data)
        else:
            return JsonResponse({
                    'status': 'error',
                    'error': 'Not authorized'
                },
                status_code=401)
    else:
        return HttpResponseRedirect('/chat')


def messages_from(request, message_id):
    if request.is_ajax():
        if request.user.is_authenticated():
            update_last_seen_time(request.user)
            message_list = Message.objects.filter(id__gt=message_id)
            json_data = {
                'status': 'ok',
                'messages_html': get_new_messages_as_html(
                    request.user.id, message_list),
                'last_message':
                    message_list.last().id
                    if len(message_list) > 0
                    else message_id
            }

            return JsonResponse(json_data)
        else:
            return JsonResponse({
                    'status': 'error',
                    'error': 'Not authorized'
                },
                status_code=401)
    else:
        return HttpResponseRedirect('/chat')


def send(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if not (request.method == 'POST'):
                return JsonResponse({
                    'status': 'error',
                    'error': 'Bad request:\
                        expected a POST request with form data'
                    },
                    status_code=400)
            # else:
            update_last_seen_time(request.user)
            new_message = Message(
                text=request.POST['message'],
                sender=request.user)
            new_message.save()
            message_list = Message.objects.filter(
                id__gt=request.POST['last_message'])
            return JsonResponse(
                {
                    'status': 'ok',
                    'message_list_html': get_new_messages_as_html(
                        request.user.id, message_list),
                    'last_message': message_list.last().id
                })
        else:
            return JsonResponse({
                    'status': 'error',
                    'error': 'Not authorized'
                },
                status_code=401)
    else:
        return HttpResponseRedirect('/chat')


#
# Auth views
#

def register(request):
    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if (reg_form.is_valid()):
            # TODO: collect user email via form
            new_user = User.objects.create_user(reg_form['username'].value(),
                                                '',
                                                reg_form['password1'].value())
            new_user.first_name = reg_form['first_name'].value()
            new_user.last_name = reg_form['last_name'].value()
            new_user.save()
            return HttpResponseRedirect(reverse('registered'))
        else:
            return render(request,
                          'registration/register.html',
                          {'form': reg_form})
    else:
        reg_form = UserRegistrationForm()
        return render(request,
                      'registration/register.html',
                      {'form': reg_form})


def reg_succeeded(request):
    return render(request, 'registration/registered.html')


@login_required
def logout(request):
    logout_session(request)
    return HttpResponseRedirect(reverse('login'))
