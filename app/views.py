from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import QuestionForm, SignUpForm, LoginForm, ResultForm
from .models import Contest, Category, Participant, Result, Vote


def index(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('home')
    form = QuestionForm()
    teacher_contests = Contest.objects.filter(category_id=Category.objects.get(name='Ұстаздар арасында байқау').id) \
                           .filter(status=True)[:3]

    suret = Contest.objects.filter(category_id=Category.objects.get(name='Сурет салу байқауы').id) \
                .filter(status=True)[:3]
    horse_racing = Contest.objects.filter(category_id=Category.objects.get(name='Ат бәйгесі').id) \
                       .filter(status=True)[:3]
    mushaira = Contest.objects.filter(category_id=Category.objects.get(name='Мүшәйра').id) \
                   .filter(status=True)[:3]

    context = {
        'title': 'Онлайн байқау',
        'form': form,
        'teacher_contests': teacher_contests,
        'suret': suret,
        'horse_racing': horse_racing,
        'mushaira': mushaira,
    }
    return render(request, 'app/index.html', context)


# admin
# samal
# samal123

@login_required
def contest_detail(request, slug):
    contest = get_object_or_404(Contest, slug=slug)
    results = Result.objects.filter(contest=contest).order_by('-score')
    v = Vote.objects.filter(contest=contest).filter(user=request.user)

    if not v:
        v = True
    else:
        v = False

    if contest.category.name == 'Ат бәйгесі' or contest.category.name == 'Мүшәйра':
        c = False
    else:
        c = True
    question = Result.objects.filter(participant=request.user.participant).filter(contest=contest)
    jury = False
    for j in request.user.jury_set.all():
        if j.contest == contest:
            jury = True
            break

    if not question:
        question = ['', ]
    context = {'title': contest.title, 'contest': contest, 'c': c, 'question': question[0], 'results': results,
               'vote': v,'jury':jury}
    return render(request, 'app/contest_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    contests = Contest.objects.filter(category=category)
    context = {
        'title': category.name,
        'contests': contests,

    }
    return render(request, 'app/category_detail.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            Participant.objects.create(user=user,
                                       first_name=form.cleaned_data['first_name'],
                                       last_name=form.cleaned_data['last_name'],
                                       phone=form.cleaned_data['phone'],

                                       )
            return redirect('home')

    else:
        form = SignUpForm()
    context = {'title': 'Тіркелу', 'form': form}
    return render(request, 'account/signup.html', context)


def loginView(request):
    messages = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['login']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            try:
                login(request, user)
            except:
                context = {'title': 'Кіру', 'form': form, 'messages': 'Логин немесе пароль қате!'}
                return render(request, 'account/login.html', context)
            return redirect('home')
    else:
        form = LoginForm()
    context = {'title': 'Кіру', 'form': form, 'messages': messages}
    return render(request, 'account/login.html', context)


def contest_register(request, slug):
    contest = get_object_or_404(Contest, slug=slug)
    if request.method == 'POST':
        form = ResultForm(request.user, contest, request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect(f'/contest/{contest.slug}/')
    else:
        form = ResultForm(request.user, contest)
    context = {'title': 'Тіркелу', 'form': form, 'contest_slug': contest.slug}
    return render(request, 'app/contest_register.html', context)


def contest_update(request, slug, pk):
    result = Result.objects.get(id=pk)

    contest = get_object_or_404(Contest, slug=slug)
    if request.method == 'POST':
        form = ResultForm(request.user, contest, request.POST, request.FILES, instance=result)

        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('home')
    else:
        form = ResultForm(request.user, contest, instance=result)

    context = {'form': form, 'title': 'Өңдеу'}
    return render(request, 'app/contest_update.html', context)


def guest_list(request):
    contests = Contest.objects.exclude(category_id=Category.objects.get(name='Мүшәйра').id) \
        .exclude(category_id=Category.objects.get(name='Ат бәйгесі').id).filter(open_close=False)
    if request.user.jury_set.all().count() != 0:
        contests2 = Contest.objects.order_by('-created').order_by('category') \
            .exclude(category_id=Category.objects.get(name='Мүшәйра').id) \
            .exclude(category_id=Category.objects.get(name='Ат бәйгесі').id).filter(open_close=True)
        c = []
        for con in request.user.jury_set.all():
            c.append(con.contest.id)
        contests = contests.union(contests2.filter(id__in=c))
    contests = contests.order_by('-created').order_by('category')
    context = {'title': 'Байқаулар', 'contests': contests}
    return render(request, 'app/guest_list.html', context)


def choice(request, slug):
    contest = get_object_or_404(Contest, slug=slug)
    results = Result.objects.filter(contest=contest).order_by('-score')
    v = Vote.objects.filter(contest=contest).filter(user=request.user)

    if not v:
        v = True
    else:
        v = False
    context = {'title': 'Дауыс беру', 'results': results, 'contest': contest, 'vote': v}

    return render(request, 'app/choice_participant.html', context)


@login_required
def vote(request, slug):
    contest = get_object_or_404(Contest, slug=slug)
    results = Result.objects.filter(contest=contest).order_by('-score')

    context = {'title': 'Дауыс беру', 'results': results, 'contest': contest}
    try:
        selected = contest.result_set.get(pk=request.POST['choice'])
        Vote.objects.create(contest=contest, user=request.user, participant=selected.participant)

    except:
        return render(request, 'app/choice_participant.html', context)
    else:
        if contest.open_close:
            selected.score += int(request.POST['score'])
        else:
            selected.score += 1
        selected.save()
        return redirect(f'/guest_list/{contest.slug}/choice_participant/')


def results(request, slug):
    contest = get_object_or_404(Contest, slug=slug)
    results = Result.objects.filter(contest=contest).order_by('-score')[:3]
    context = {
        'title': 'Нәтижелер',
        'results': results
    }
    return render(request, 'app/results.html', context)
