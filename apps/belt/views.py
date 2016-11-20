from django.shortcuts import render, redirect
from django.contrib import messages
import models



def index(request):
    users = models.User.objects.all()
    context = {
        'users':users
    }
    try:
        if request.session['userID']:
            request.session.pop('userID')
    except KeyError:
        pass
    return render(request, 'belt/index.html', context)

def login(request):
    login = models.User.objects.login( request.POST )
    if not login[0]:
        errors = login[1]
        if 'no_entry' in errors:
            messages.error(request, 'Fill EVERYTHING out, you dunce.', extra_tags = 'login')
        if 'invalid_em' in errors:
            messages.error(request, 'Your email is broken, guy.', extra_tags = 'login')
        if 'short_pw' in errors:
            messages.error(request, 'Password is too short, dude.', extra_tags = 'login')
        if 'invalid_pw' in errors:
            messages.error(request, 'Weak password, brah.', extra_tags = 'login')
        if 'abs_em' in errors:
            messages.error(request, 'YOU DON\'T EXIST', extra_tags = 'login')
        if 'abs_pw' in errors:
            messages.error(request, 'Nice try, slick... wrong password!', extra_tags = 'login')
        return redirect('/')
    else:
        loggedUsr = models.User.objects.filter( email = request.POST['email'].lower() )
        request.session['userID'] = loggedUsr[0].id
        print request.session['userID']
        messages.success(request, "WOOHOO!... Now what...?")
        return redirect('/home')

def register(request):
    register = models.User.objects.register( request.POST )
    try:
        if not register[0]:
            errors = register[1]
            if 'no_entry' in errors:
                messages.error(request, 'Fill EVERYTHING out, you dunce.', extra_tags = 'register')
            if 'short_fn' in errors:
                messages.error(request, 'Don\'t be a hipster. You know your first name isn\t that short.', extra_tags = 'register')
            if 'short_ln' in errors:
                messages.error(request, 'Your last name isn\'t THAT short, dude...', extra_tags = 'register')
            if 'invalid_em' in errors:
                messages.error(request, 'Your email is broken, guy.', extra_tags = 'register')
            if 'short_pw' in errors:
                messages.error(request, 'Password is too short, dude.', extra_tags = 'register')
            if 'invalid_pw' in errors:
                messages.error(request, 'Weak password, brah.', extra_tags = 'register')
            if 'invalid_fn' in errors:
                messages.error(request, "Nuh-uh, for real? That's your name?! Letters only!", extra_tags = 'register')
            if 'invalid_ln' in errors:
                messages.error(request, "What kind of last name is that?! What\'re you a robot or something? Leters only!", extra_tags = 'register')
            if 'pwcnf_unmatch' in errors:
                messages.error(request, "You LITERALLY JUST TYPED your password. How could you get it wrong right after?!", extra_tags = 'register')
            return redirect('/')
    except:
        loggedUsr = models.User.objects.filter( email = request.POST['email'].lower() )
        request.session['userID'] = loggedUsr[0].id
        messages.success(request, 'Yay, you wasted your time and signed up.')
        print request.session['userID']
        return redirect('/home')

def home(request):
    userInfo = models.User.objects.filter(id = request.session['userID'])
    plans = models.Plan.objects.filter(user=userInfo).order_by('-start_date')
    other_plans = models.Plan.objects.exclude( user = userInfo[0] )
    context = {
        'user':userInfo[0],
        'plans':plans,
        'other_plans' : other_plans
    }

    return render(request, 'belt/home.html', context)


def add_plan(request):
    plans = models.Plan.objects.all()
    context = {
        'plans': plans,
    }
    return render(request, 'belt/add_plan.html', context)


def add_plan_process(request):
    add_plan = models.User.objects.add_plan( request.POST, request.session['userID'] )
    if not add_plan[0]:
        errors = add_plan[1]
        if 'no_entry' in errors:
            messages.error(request, 'ALL fields required')
        if 'past_date' in errors:
            messages.error(request, 'We\'re PLANNING trips here... y\'know... for the FUTURE.')
        if 'neg_trip' in errors:
            messages.error(request, 'What kind of trip has a start date AFTER IT ENDS?!')
        return redirect ('/add_plan')
    messages.success(request, 'You added '+'\"'+str(add_plan[1]).title()+'\"')
    return redirect('/add_plan')

def join_plan_process(request, plan_dest):
    join_plan = models.User.objects.join_plan( plan_dest, request.session['userID'] )
    messages.success(request, 'You joined '+'\"'+str(join_plan[1]).title()+'\"')
    return redirect('/home')

def delete_plan(request, plan_id):
    models.Plan.objects.filter(id=plan_id).delete()
    return redirect('/home')

def remove_plan(request, plan_id):
    user = models.User.objects.filter( id = request.session['userID'] )
    userremove = user[0]
    plan = models.Plan.objects.filter( id = plan_id )
    # models.Plan.objects.remove(user, plan_id)
    plan[0].user.remove(userremove)
    return redirect('/home')

def show_plan(request, plan_id):
    plan_to_show = models.Plan.objects.filter( id = plan_id )
    users = models.User.objects.filter(plan = plan_id)
    context = {
        'plan' : plan_to_show[0],
        'users' : users
    }
    return render(request, 'belt/show_plan.html', context)



def logout(request):
    request.session.flush()
    return redirect('/')
