"""
Definition of views.
"""
from django.template import loader
from django.shortcuts import render ,redirect
from django.http import HttpRequest,HttpResponse
from django.template import RequestContext
from datetime import datetime
from .models import Contact
from .forms import ContactForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def contact(request):
    searchKey=request.GET.get('keyword');
    if searchKey!=None and searchKey!="":
        contactList = Contact.objects.filter(FirstName__contains=searchKey)
    else:
        contactList = Contact.objects.all()

    count = Contact.objects.count()
    pageSize=request.GET.get('pageSize')
    try:
        paginator = Paginator(contactList, pageSize) 
    except:
         paginator = Paginator(contactList, 5) 

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'app/contact.html', {'contacts': contacts,'count':count})

def addContact(request):
    if request.method == 'GET':
        form=ContactForm()
        return render(request, 'app/addContact.html', {'form': form,'action':'Create Contact'})
    if request.method == 'POST':
        form=ContactForm(request.POST)
        if form.is_valid() or 1:
            contact=Contact()
            if form['id'].data!= "":
                contact.id = form['id'].data
            contact.FirstName=form['FirstName'].data
            contact.LastName=form['LastName'].data
            contact.Email=form['Email'].data
            contact.Mobile=form['Mobile'].data
            contact.save()
            return redirect('contact')

def editContact(request,id):
    contact = Contact.objects.get(pk=id)
    bindContact={'id':contact.id,'FirstName':contact.FirstName,'LastName':contact.LastName,'Email':contact.Email,'Mobile':contact.Mobile}
    form = ContactForm(initial = bindContact)
    return render(request, 'app/addContact.html', {'form': form,'action':'Edit Contact'})

def deleteContact(request,id):
    contact = Contact.objects.get(pk=id)
    contact.delete()
    return redirect('contact')