import datetime

from django.http import HttpResponse
from django.shortcuts import render
from main.models import Votings, Complaints
from django.contrib import messages

from django.db import IntegrityError

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from main.forms import RegForm, LoginForm, CreateVoteForm, ComplainForm

from django.shortcuts import redirect

# def cookie_view(request):
#     response = HttpResponse("hello")
#     set_cookie(response, 'name', 'jujule')
#     return response
#
#
# def set_cookie(response, key, value, days_expire=7):
#     if days_expire is None:
#         max_age = 365 * 24 * 60 * 60  # one year
#     else:
#         max_age = days_expire * 24 * 60 * 60
#     expires = datetime.datetime.strftime(
#         datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
#         "%a, %d-%b-%Y %H:%M:%S GMT",
#     )
#     response.set_cookie(
#         key,
#         value,
#         max_age=max_age,
#         expires=expires,
#     )

# def get_menu_context():
#     return [
#         {'url_name': 'index', 'name': 'Главная'},
#         {'url_name': 'time', 'name': 'Текущее время'},
#     ]
#
#
# def index_page(request):
#     context = {
#         'pagename': 'Главная',
#         'author': 'Andrew',
#         'pages': 4,
#         'menu': get_menu_context()
#     }
#     return render(request, 'pages/index.html', context)
#
#
# def time_page(request):
#     context = {
#         'pagename': 'Текущее время',
#         'time': datetime.datetime.now().time(),
#         'menu': get_menu_context()
#     }
#     return render(request, 'pages/time.html', context)


def custom_404_page(request, exception):
    return render(request, 'custom_404.html')


def custom_403_page(request, exception):
    return render(request, 'custom_403.html')


def landing_page(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False

    return render(request, 'index.html', context)


def error_page(request):
    return render(request, 'error.html')


def votings_page(request):
    votings = Votings.objects.all()
    votings_dictlist = []

    for vote in votings:
        votings_dictlist.append({
            'id': vote.id,
            'name': vote.name,
            'about': vote.about,
        })
    context = {
        'votings': votings_dictlist,
    }

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False

    return render(request, 'votings.html', context)


def login_page(request):
    # username = request.GET.get('login', None)
    # password = request.GET.get('password', None)
    # context = {}
    #
    # if request.user.is_authenticated:
    #     return redirect('/')
    #
    # user = authenticate(request, username=username, password=password)
    #
    # if user is not None:
    #     login(request, user)
    #     return redirect('/')
    # else:
    #     return render(request, 'login.html')

    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            user = authenticate(request, username=loginform.data['username'], password=loginform.data['password'])

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.add_message(request, messages.ERROR, "Неправильное имя пользователя или пароль")
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
    else:
        pass

    context = {}
    context['loginform'] = LoginForm()
    return render(request, 'login.html', context)


def registration_page(request):
    # username = request.GET.get('login', None)
    # email = request.GET.get('email', None)
    # password = request.GET.get('password', None)

    # if request.user.is_authenticated:
    #     return redirect('/')
    #
    # if username is not None and email is not None and password is not None and \
    #    username is not "" and password is not "" and email is not "":
    #     user = User.objects.create_user(username=username, email=email, password=password)
    #     user.save()
    #     login(request, user)
    #     return redirect('/')
    if request.method == 'POST':
        regform = RegForm(request.POST)
        if regform.is_valid():
            try:
                user = User.objects.create_user(username=regform.data['username'], email=regform.data['email'], password=regform.data['password'])
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "Пользователь уже существует")
                return redirect('/registration/')
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
    else:
        pass

    context = {}
    context['regform'] = RegForm()

    return render(request, 'registration.html', context)


def logout_user(request):
    logout(request)
    return redirect('/')


def vote_page(request):
    vote_id = request.GET.get('id', None)
    type_of_values = request.GET.get('view', 'percent')

    context = {}

    if vote_id is None:
        return redirect('/error/')

    try:
        current_vote = Votings.objects.get(id=int(vote_id))
    except Votings.DoesNotExist:
        return redirect('/error/')

    variants_list = current_vote.variants.split(',.;:')
    variants_vals = current_vote.variants_values.split(' ')
    variants_dictlist = []
    for el in range(len(variants_list)):
        variants_dictlist.append({
            'text': variants_list[el],
            'val': str(int(int(variants_vals[el]) / int(current_vote.all_votes_quantity) * 100)) + "%" if type_of_values == "percent" and int(current_vote.all_votes_quantity) != 0 else variants_vals[el],
        })

    if current_vote is not None:
        context = {
            'name': current_vote.name,
            'author': current_vote.author,
            'all_votes_quantity': current_vote.all_votes_quantity,
            'about': current_vote.about,
            'vars': variants_dictlist,
            'vote_id': int(vote_id),
            'values_type': type_of_values,
        }
    else:
        return redirect('/error/')

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['user_logged_in'] = True
        history_pairs = [el.split('---') for el in (request.user.profile.history).split(',.;:')]
        for el in history_pairs:
            if el[0] == str(vote_id):
                context['already_voted'] = True
                context['green_var'] = str(el[1])
    else:
        context['user_logged_in'] = False

    return render(request, 'vote.html', context)


def user_voted_page(request):
    context = {}
    vote_id = request.GET.get('vote_id', None)
    var_text = request.GET.get('var_text', None)

    if request.user.is_authenticated:
        user_history = str(request.user.profile.history)
        history_pairs = [el.split('---') for el in user_history.split(',.;:')]
        for el in history_pairs:
            if el[0] == str(vote_id):
                return redirect('/votings/vote?id=' + vote_id + "&view=percent")
        if len(user_history) == 0:
            user_history += vote_id + "---" + var_text + '---' + Votings.objects.get(id=vote_id).name
        else:
            user_history += ",.;:" + vote_id + "---" + var_text + '---' + Votings.objects.get(id=vote_id).name
        request.user.profile.history = user_history
        request.user.save()

        voting = Votings.objects.get(id=int(vote_id))
        variants = voting.variants.split(',.;:')
        users_history = voting.participants
        if len(users_history) < 1:
            users_history = request.user.username
        else:
            users_history += ',.;:' + request.user.username
        voting.participants = users_history
        for el_num in range(len(variants)):
            if variants[el_num] == str(var_text):
                voting.all_votes_quantity = int(voting.all_votes_quantity) + 1
                new_vals = str(voting.variants_values).split(' ')
                new_vals[el_num] = str(int(new_vals[el_num]) + 1)
                new_vals = ' '.join(new_vals)
                voting.variants_values = new_vals
                voting.save()

        return redirect('/votings/vote?id=' + vote_id + "&view=percent")
    else:
        return redirect('/login')

    return redirect('/votings/vote?id=' + vote_id)


def user_profile_page(request):
    user_id = request.GET.get('id', request.user.id)

    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        if int(user_id) == request.user.id:
            context['can_edit'] = True
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False

    try:
        user_by_id = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('/error/')


    # if user_by_id is None:
    #     redirect('/error/')

    context['user_login'] = user_by_id.username
    context['firstname'] = user_by_id.first_name
    context['lastname'] = user_by_id.last_name
    context['email'] = user_by_id.email
    return render(request, 'user_profile.html', context)


def user_edit_profile_page(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['firstname'] = request.user.first_name
        context['lastname'] = request.user.last_name
        context['email'] = request.user.email
        context['userlogin'] = request.user.username
        context['user_logged_in'] = True
    else:
        return redirect('/login/')

    firstname = request.GET.get('firstname', None)
    lastname = request.GET.get('lastname', None)
    email = request.GET.get('email', None)
    userlogin = request.GET.get('userlogin', None)
    oldpassword = request.GET.get('oldpassword', None)
    newpassword = request.GET.get('newpassword', None)



    if request.user.is_authenticated:
        if str(firstname) is not "" and firstname is not None:
            request.user.first_name = str(firstname)
        if str(lastname) is not "" and lastname is not None:
            request.user.last_name = str(lastname)
        if str(email) is not "" and email is not None:
            request.user.email = str(email)
        if str(userlogin) is not "" and userlogin is not None and not any(user.username == userlogin for user in User.objects.all()):
            request.user.username = str(userlogin)
        if str(oldpassword) == str(newpassword) and str(oldpassword) is not "" and oldpassword is not None and str(newpassword) is not "" and newpassword is not None:
            request.user.set_password(newpassword)
            changed_password_user = authenticate(username=userlogin, password=newpassword)
            login(request, changed_password_user)

        request.user.save()

        if str(firstname) is not "" and firstname is not None or str(lastname) is not "" and lastname is not None or \
            str(email) is not "" and email is not None or str(userlogin) is not "" and userlogin is not None and \
            not any(user.username == userlogin for user in User.objects.all())\
            or str(oldpassword) == str(newpassword) and str(oldpassword) is not "" and oldpassword is not None \
            and str(newpassword) is not "" and newpassword is not None:
            return redirect('/user/')

    return render(request, 'edit_user.html', context)


def create_voting_page(request):
    context = {}
    context['createvoteform'] = CreateVoteForm()

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['author'] = request.user.username
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False
        return redirect('/login')

    if request.method == 'POST':
        createvoteform = CreateVoteForm(request.POST)
        if createvoteform.is_valid():
            variants = request.POST.getlist('variant', None)

            vars_in_str = ""
            for i in range(len(variants)):
                vars_in_str += str(variants[i]) + ",.;:"
            vars_in_str = vars_in_str[:-4]

            voting_name = createvoteform.data['votename']
            about = createvoteform.data['about']

            voting = Votings()

            voting.author = context['author']
            voting.about = about
            voting.participants = ''
            voting.name = voting_name
            voting.variants = vars_in_str
            tmp_vals = ""
            for i in range(len(variants)):
                tmp_vals += "0 "
            tmp_vals = tmp_vals[:-1]
            voting.variants_values = tmp_vals
            voting.all_votes_quantity = 0

            try:
                voting.save()
                return redirect('/votings/')
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "Голосование с таким названием уже существует")


            # try:
            #     user = User.objects.create_user(username=regform.data['username'], email=regform.data['email'],
            #                                     password=regform.data['password'])
            # except IntegrityError:
            #     messages.add_message(request, messages.ERROR, "Пользователь уже существует")
            #     return redirect('/registration/')
            pass
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
    else:
        pass

    # voting_name = request.GET.get('voting_name', None)
    # about = request.GET.get('about', None)
    # variants = request.GET.getlist('variant', None)

    # if str(voting_name) is not "" and voting_name is not None and str(about) is not "" and about is not None and len(variants) is not 0 and str(variants[0]) != "" and variants[0] is not None:
    #     voting = Votings()
    #
    #     voting.author = context['author']
    #     voting.about = about
    #     voting.name = voting_name
    #     voting.variants = vars_in_str
    #     tmp_vals = ""
    #     for i in range(len(variants)):
    #         tmp_vals += "0 "
    #     tmp_vals = tmp_vals[:-1]
    #     voting.variants_values = tmp_vals
    #     voting.all_votes_quantity = 0
    #
    #     voting.save()
    #     return redirect('/votings/')

    return render(request, 'add_votings.html', context)


def user_history_page(request):
    context = {}
    history_pairs = [el.split('---') for el in (request.user.profile.history).split(',.;:')]
    history_dictlist = []
    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False
        return redirect('/login/')
    for el in history_pairs:
        if len(el) > 1:
            history_dictlist.append({
                'id': el[0],
                'name': el[1],
                'vote_name': el[2],
            })
    context['history'] = history_dictlist
    print(context['history'])
    return render(request, 'history.html', context)


def complaints(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False

    compls = Complaints.objects.all()
    compllist = [{
        'author': el.author,
        'quote': el.message,
    } for el in compls]
    context['complaints'] = compllist

    return render(request, 'complaints.html', context)


def create_cas_page(request):
    context = {}
    context['complainform'] = ComplainForm()

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False

    if request.method == 'POST':
        complainform = ComplainForm(request.POST)
        if complainform.is_valid():
            textarea = complainform.data['textarea']
            user_id = 0
            username = 'Anonymous User'
            if request.user.is_authenticated:
                user_id = request.user.id
                username = request.user.username

            cas = Complaints()
            cas.author = username
            cas.message = textarea
            cas.user_id = user_id
            cas.save()
            return redirect('/complaints_&_suggestions/')

        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
    else:
        pass

    return render(request, 'create_complain.html', context)


def vote_users_page(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username.title()
        context['user_logged_in'] = True
    else:
        context['user_logged_in'] = False

    vote_id = request.GET.get('vote_id')
    vote_name = request.GET.get('vote_name')
    context['vote_name'] = vote_name

    users_history = Votings.objects.get(id=vote_id).participants.split(',.;:')
    print(len(users_history))
    if users_history[0] != '':
        users_history = [{
            'user_id': User.objects.get(username=el).id,
            'name': el if not request.user.is_authenticated or request.user.id != User.objects.get(username=el).id else el + ' (you)',
        } for el in users_history]

    context['users'] = users_history
    context['vote_id'] = vote_id

    return render(request, 'vote_users.html', context)
