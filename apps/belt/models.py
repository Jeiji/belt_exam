from __future__ import unicode_literals
import re, datetime, bcrypt
from django.db import models

class UserManager(models.Manager):
    def login(self, guest):
        echeck = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = []
        if not guest['email'] or not guest['password']:
            errors.append('no_entry')
            return ( False , errors )
        if not echeck.match(guest['email']):
            errors.append('invalid_em')
            return ( False , errors )

        try:
            dbUser = User.objects.filter( email = guest['email'].lower() )
            dbPass = str(dbUser[0].password)
            guestPass = str(guest['password'])
            if bcrypt.hashpw(guestPass, dbPass) == dbPass :

                return ( True , dbUser )
            else:
                errors.append('abs_pw')
                return (False, errors)
        except:
            errors.append('abs_em')
            return (False, errors)

        # if not errors == []:
        #     return ( False , errors )

    def register(self, guest):
        echeck = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        pwccheck = re.compile(r'.*\d.*[A-Z].*|.*[A-Z].*\d.*')
        fncheck = re.compile(r'[a-zA-Z-]')
        lncheck = re.compile(r'[a-zA-Z-]')
        dbUsers = User.objects.all()

        errors = []
        dbEmailCheck = User.objects.filter( email = guest['email'].lower() )
        if dbEmailCheck :
            errors.append('invalid_em')
            return (False , errors)
        if not guest['first_name'] or not guest['last_name'] or not guest['email'] or not guest['password'] or not guest['confirm']:
            errors.append('no_entry')
            return ( False , errors )
        if not fncheck.match(guest['first_name']) :
            errors.append('invalid_fn')
        if len(guest['first_name']) < 3 :
            errors.append('short_fn')
        if len(guest['last_name']) < 3 :
            errors.append('short_ln')
        if not lncheck.match(guest['last_name']) :
            errors.append('invalid_ln')
        if not echeck.match(guest['email']):
            errors.append('invalid_em')
        if len(guest['password']) < 8 :
            errors.append('short_pw')
        if not pwccheck.match(guest['confirm']):
            errors.append('invalid_pw')
        if not guest['password'] == guest['confirm']:
            errors.append('pwcnf_unmatch')
        if errors == []:
            hashedpw = bcrypt.hashpw(guest['password'].encode(),bcrypt.gensalt())
            User.objects.create( first_name = guest['first_name'].lower(), last_name = guest['last_name'].lower(), email = guest['email'].lower(), password = hashedpw )
            return (True)
        else:
            print '********'
            return (False, errors)
        return (False, errors)

    def add_plan(self, planEntry, userID):
        user = User.objects.filter( id = userID )
        errors = []
        dbPlanCheck = Plan.objects.filter( destination = planEntry['destination'].lower() )
        if not planEntry['destination'] or not planEntry['start_date'] or not planEntry['end_date'] or not planEntry['plan'] :
            errors.append('no_entry')
            return ( False , errors )
        if datetime.datetime.strptime(planEntry['start_date'], '%Y-%m-%d') < datetime.datetime.today():
            errors.append('past_date')
        if datetime.datetime.strptime(planEntry['start_date'], '%Y-%m-%d') > datetime.datetime.strptime(planEntry['end_date'], '%Y-%m-%d'):
            errors.append('neg_trip')
        if not errors:
            if dbPlanCheck :
                PlanToEnter = dbPlanCheck[0]
            else:
                PlanToEnter = Plan.objects.create( destination = planEntry['destination'], start_date = planEntry['start_date'], end_date = planEntry['end_date'], plan = planEntry['plan'], created_by = user[0])
            PlanToEnter.user.add( user[0] )

            return (True, planEntry['destination'])
        return ( False , errors )

    def join_plan(self, planEntryDestination, userID):
        user = User.objects.filter( id = userID )
        dbPlanCheck = Plan.objects.filter( destination = planEntryDestination )
        print ('%'*400) ,dbPlanCheck
        planToJoin = dbPlanCheck[0]
        print ('?'*400) ,planToJoin, type(planToJoin)
        planToJoin.user.add( user[0] )


        return (True, planEntryDestination)




class User(models.Model):
    first_name = models.CharField( max_length = 50 )
    last_name = models.CharField( max_length = 50 )
    email = models.EmailField( max_length = 50 )
    password = models.CharField( max_length = 255, default = 0 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    objects = UserManager()



class Plan(models.Model):
    created_by = models.ForeignKey(User, related_name = "creator")
    name = models.CharField( max_length = 50 )
    user = models.ManyToManyField(User)
    destination = models.CharField( max_length = 50 )
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField( max_length = 2000 )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
