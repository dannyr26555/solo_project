from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    if 'user_id' in request.session:
        return redirect('/home')
    return render(request, 'index.html')

def registerAttendee(request):
    if request.method == 'POST':
        errors = Attendee.objects.attendee_validator(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = Attendee.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['name'] = new_user.first_name + ' ' + new_user.last_name
        request.session['user_id'] = new_user.id
        request.session['att_id'] = new_user.id
        return redirect('/home')
    return redirect('/')

def registerOrganizer(request):
    if request.method == 'POST':
        errors = Organizer.objects.organizer_validator(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = Organizer.objects.create(org_name=request.POST['org_name'],first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['name'] = new_user.first_name + ' ' + new_user.last_name
        request.session['user_id'] = new_user.id
        request.session['org_id'] = new_user.id
        return redirect('/home')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        logged_attendee = Attendee.objects.filter(email=request.POST['email'])
        logged_organizer = Organizer.objects.filter(email=request.POST['email'])
        if len(logged_attendee) > 0:
            logged_attendee = logged_attendee[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_attendee.password.encode()):
                request.session['name'] = logged_attendee.first_name + ' ' + logged_attendee.last_name
                request.session['user_id'] = logged_attendee.id
                request.session['att_id'] = logged_attendee.id
                return redirect('/home')
        if len(logged_organizer) > 0:
            logged_organizer = logged_organizer[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_organizer.password.encode()):
                request.session['name'] = logged_organizer.first_name + ' ' + logged_organizer.last_name
                request.session['user_id'] = logged_organizer.id
                request.session['org_id'] = logged_organizer.id
                return redirect('/home')
    return redirect('/')

def home(request):
    if 'user_id' in request.session:
        if 'org_id' in request.session:
            logged_organizer = Organizer.objects.filter(id=request.session['org_id'])
            if len(logged_organizer) > 0:
                logged_organizer = logged_organizer[0]
                if request.session['user_id'] == logged_organizer.id:
                    context = {
                        'all_cons': Convention.objects.all(),
                        'logged_organizer': Organizer.objects.get(id=request.session['user_id'])
                    }
                    return render(request, 'home.html',context)
        if 'att_id' in request.session:
            logged_attendee = Attendee.objects.filter(id=request.session['att_id'])
            if len(logged_attendee) > 0:
                logged_attendee = logged_attendee[0]
                if request.session['user_id'] == logged_attendee.id:
                    context = {
                        'all_cons': Convention.objects.all(),
                        'logged_attendee': Attendee.objects.get(id=request.session['user_id'])
                    }
                    return render(request, 'home.html',context)
    return redirect('/')

def create_con(request):
    if request.method == 'POST':
        errors = Convention.objects.con_validator(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/quotes')
        new_con = Convention.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            con_type=request.POST['type'],
            date=request.POST['date'],
            location=request.POST['location'],
            created_by = Organizer.objects.get(id=request.session['user_id'])
        )
        return redirect('/home')
    return redirect('/')

def vieworg(request, id):
    if 'user_id' in request.session:
        if 'org_id' in request.session:
            logged_organizer = Organizer.objects.filter(id=request.session['org_id'])
            if len(logged_organizer) > 0:
                logged_organizer = logged_organizer[0]
                if request.session['user_id'] == logged_organizer.id:
                    org = Organizer.objects.get(id=id)
                    context = {
                        'logged_organizer': Organizer.objects.get(id=request.session['user_id']),
                        'clicked_org': org,
                        'all_org_cons': Convention.objects.filter(created_by=org.id)
                    }
                    return render(request, 'org.html',context)
        if 'att_id' in request.session:
            logged_attendee = Attendee.objects.filter(id=request.session['att_id'])
            if len(logged_attendee) > 0:
                logged_attendee = logged_attendee[0]
                if request.session['user_id'] == logged_attendee.id:
                    org = Organizer.objects.get(id=id)
                    context = {
                        'logged_attendee': Attendee.objects.get(id=request.session['user_id']),
                        'clicked_org': org,
                        'all_org_cons': Convention.objects.filter(created_by=org.id)
                    }
                    return render(request, 'org.html',context)
    return redirect('/')

# def viewatt(request, id):
#     if 'user_id' in request.session:
#         if 'org_id' in request.session:
#             logged_organizer = Organizer.objects.filter(id=request.session['org_id'])
#             if len(logged_organizer) > 0:
#                 logged_organizer = logged_organizer[0]
#                 if request.session['user_id'] == logged_organizer.id:
#                     att = Attendee.objects.get(id=id)
#                     context = {
#                         'logged_organizer': Organizer.objects.get(id=request.session['user_id']),
#                         'clicked_att': att,
#                         'all_liked_cons': Convention.objects.all(),
#                         'all_rsvpd_cons': Convention.objects.all()
#                     }
#                     return render(request, 'att.html',context)
#         if 'att_id' in request.session:
#             logged_attendee = Attendee.objects.filter(id=request.session['att_id'])
#             if len(logged_attendee) > 0:
#                 logged_attendee = logged_attendee[0]
#                 if request.session['user_id'] == logged_attendee.id:
#                     att = Attendee.objects.get(id=id)
#                     context = {
#                         'logged_attendee': Attendee.objects.get(id=request.session['user_id']),
#                         'clicked_att': att,
#                         'all_liked_cons': Convention.objects.all(),
#                         'all_rsvpd_cons': Convention.objects.all()
#                     }
#                     return render(request, 'att.html',context)
#     return redirect('/')

def viewaccount(request, id):
    if 'user_id' in request.session:
        if 'org_id' in request.session:
            logged_organizer = Organizer.objects.filter(id=request.session['org_id'])
            details = Organizer.objects.get(id=id)
            context = {
                'logged_organizer': Organizer.objects.get(id=request.session['user_id']),
                'details': details
            }
            return render(request, 'account.html', context)
        if 'att_id' in request.session:
            logged_attendee = Attendee.objects.filter(id=request.session['att_id'])
            details = Attendee.objects.get(id=id)
            context = {
                'logged_attendee': Attendee.objects.get(id=request.session['user_id']),
                'details': details
            }
            return render(request, 'account.html', context)
    return redirect('/')

def viewcon(request, id):
    if 'user_id' in request.session:
        if 'org_id' in request.session:
            logged_organizer = Organizer.objects.filter(id=request.session['org_id'])
            con = Convention.objects.get(id=id)
            context = {
                'logged_organizer': Organizer.objects.get(id=request.session['user_id']),
                'clicked_con': con
            }
            return render(request, 'con.html', context)
        if 'att_id' in request.session:
            logged_attendee = Attendee.objects.filter(id=request.session['att_id'])
            con = Convention.objects.get(id=id)
            context = {
                'logged_attendee': Attendee.objects.get(id=request.session['user_id']),
                'clicked_con': con
            }
            return render(request, 'con.html', context)
    return redirect('/')

def edit_att(request):
    if request.method == 'POST':
        myaccount = Attendee.objects.get(id=request.session['user_id'])
        myaccount.first_name = request.POST['first_name']
        myaccount.last_name = request.POST['last_name']
        myaccount.email = request.POST['email']
        myaccount.save()
        request.session['name'] = myaccount.first_name + ' ' + myaccount.last_name
        request.session['user_id'] = myaccount.id
    return redirect(f'/viewaccount/{str(myaccount.id)}')

def edit_org(request):
    if request.method == 'POST':
        myaccount = Organizer.objects.get(id=request.session['user_id'])
        myaccount.org_name = request.POST['org_name']
        myaccount.first_name = request.POST['first_name']
        myaccount.last_name = request.POST['last_name']
        myaccount.email = request.POST['email']
        myaccount.save()
        request.session['name'] = myaccount.first_name + ' ' + myaccount.last_name
        request.session['user_id'] = myaccount.id
    return redirect(f'/viewaccount/{str(myaccount.id)}')

def delete(request, id):
    con_to_delete = Convention.objects.get(id=id)
    con_to_delete.delete()
    return redirect('/home')

def rsvp(request, id):
    rsvpd_by = Attendee.objects.get(id=request.session['user_id'])
    rsvpd_con = Convention.objects.get(id=id)
    rsvpd_con.rsvps.add(rsvpd_by)
    return redirect('/home')

def unrsvp(request, id):
    unrsvpd_by = Attendee.objects.get(id=request.session['user_id'])
    unrsvpd_con = Convention.objects.get(id=id)
    unrsvpd_con.rsvps.remove(unrsvpd_by)
    return redirect('/home')

def like(request, id):
    liked_by = Attendee.objects.get(id=request.session['user_id'])
    liked_con = Convention.objects.get(id=id)
    liked_con.likes.add(liked_by)
    return redirect('/home')

def unlike(request, id):
    unliked_by = Attendee.objects.get(id=request.session['user_id'])
    unliked_con = Convention.objects.get(id=id)
    unliked_con.likes.remove(unliked_by)
    return redirect('/home')

def conrsvp(request, id):
    rsvpd_by = Attendee.objects.get(id=request.session['user_id'])
    rsvpd_con = Convention.objects.get(id=id)
    rsvpd_con.rsvps.add(rsvpd_by)
    return redirect(f'/viewcon/{str(rsvpd_con.id)}')

def conunrsvp(request, id):
    unrsvpd_by = Attendee.objects.get(id=request.session['user_id'])
    unrsvpd_con = Convention.objects.get(id=id)
    unrsvpd_con.rsvps.remove(unrsvpd_by)
    return redirect(f'/viewcon/{str(unrsvpd_con.id)}')

def conlike(request, id):
    liked_by = Attendee.objects.get(id=request.session['user_id'])
    liked_con = Convention.objects.get(id=id)
    liked_con.likes.add(liked_by)
    return redirect(f'/viewcon/{str(liked_con.id)}')

def conunlike(request, id):
    unliked_by = Attendee.objects.get(id=request.session['user_id'])
    unliked_con = Convention.objects.get(id=id)
    unliked_con.likes.remove(unliked_by)
    return redirect(f'/viewcon/{str(unliked_con.id)}')

def userrsvp(request, id):
    rsvpd_by = Attendee.objects.get(id=request.session['user_id'])
    rsvpd_con = Convention.objects.get(id=id)
    rsvpd_con.rsvps.add(rsvpd_by)
    return redirect(f'/vieworg/{str(rsvpd_con.created_by.id)}')

def userunrsvp(request, id):
    unrsvpd_by = Attendee.objects.get(id=request.session['user_id'])
    unrsvpd_con = Convention.objects.get(id=id)
    unrsvpd_con.rsvps.remove(unrsvpd_by)
    return redirect(f'/vieworg/{str(unrsvpd_con.created_by.id)}')

def userlike(request, id):
    liked_by = Attendee.objects.get(id=request.session['user_id'])
    liked_con = Convention.objects.get(id=id)
    liked_con.likes.add(liked_by)
    return redirect(f'/vieworg/{str(liked_con.created_by.id)}')

def userunlike(request, id):
    unliked_by = Attendee.objects.get(id=request.session['user_id'])
    unliked_con = Convention.objects.get(id=id)
    unliked_con.likes.remove(unliked_by)
    return redirect(f'/vieworg/{str(unliked_con.created_by.id)}')

def logout(request):
    request.session.flush()
    return redirect('/')