from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
from . forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'dashboard/home.html')


        # NOTES

@login_required
def notes(request):
    if request.method=="POST":
        form= NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f'Notes added by {request.user.username} successfully')
    else:
        form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_notes(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


class NotesView(generic.DetailView):
    model=Notes


        # Homework

@login_required
def homework(request):
    if request.method == "POST":
        form=HomeworkForm(request.POST)
        if form.is_valid():
                try:
                    finished = request.POST['is_finished']
                    if finished == "on":
                        finished =True
                    else:
                        finished=False
                except:
                    finished=False
                homeworks=Homework(
                    user=request.user,
                    subject=request.POST['subject'],
                    title=request.POST['title'],
                    description=request.POST['description'],
                    due=request.POST['due'],
                    is_finished=finished,
                )
                homeworks.save()
                messages.success(request,f'Homework added by {request.user.username} successfully')
    else:    
        form=HomeworkForm()
    homeworks=Homework.objects.filter(user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    context={'homeworks':homeworks,'homework_done':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context)

@login_required
def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')

@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


        # Youtube

def youtube(request):
    if request.method == "POST":
        form =SearchForm(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_lst=[]
        for i in video.result()['result']:
            result_dct={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel_name':i['channel']['name'],
                'link':i['link'],
                'viewcount':i['viewCount']['short'],
                'publishtime':i['publishedTime']
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dct['description']=desc
            result_lst.append(result_dct)

        context={
            'form':form,
            'results':result_lst
        }
        return render(request,'dashboard/youtube.html',context)                
    else:
        form = SearchForm()
    context= {'form':form}
    return render(request,'dashboard/youtube.html',context)

@login_required
def todo(request):
    if request.method == "POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                complete=request.POST['is_complete']
                if complete == 'on':
                    complete =True
                else:
                    complete=False
            except:
                complete=False
            todos= Todo(
                user=request.user,
                title=request.POST['title'],
                is_complete=complete
                )
            todos.save()
            messages.success(request,f'To-Do added by {request.user.username} successfully')
    else:
        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todo_done=True
    else:
        todo_done=False
    todos=Todo.objects.filter(user=request.user)
    context= {'form':form,'todo_done':todo_done,'todos':todos}
    return render(request,'dashboard/todo.html',context)

@login_required
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_complete==True:
        todo.is_complete=False
    else:
        todo.is_complete=True
    todo.save()
    return redirect('todo')

@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

def books(request):
    if request.method == "POST":
        form =SearchForm(request.POST)
        text=request.POST['text']
        url= 'https://www.googleapis.com/books/v1/volumes?q='+text
        r=requests.get(url)
        answer=r.json()
        result_lst=[]
        for i in range(10):
            result_dct={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'catagories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRatings'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_lst.append(result_dct)

        context={
            'form':form,
            'results':result_lst
        }
        return render(request,'dashboard/books.html',context)                
    else:
        form = SearchForm()
    context= {'form':form}
    return render(request,'dashboard/books.html',context)

def dictionary(request):
    if request.method == "POST":
        form =SearchForm(request.POST)
        input=request.POST['text']
        url='https://api.dictionaryapi.dev/api/v2/entries/en_US/'+input
        r=requests.get(url)
        answer=r.json()
        print(answer)
        try:
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context={
            'form':form,
            'input':input,
            'phonetics':phonetics,
            'audio':audio,
            'definition':definition,
            'example':example,
            'synonyms':synonyms,
            }
        except:
            context={
                'form':form,
                'input':''
            }
        return render(request,'dashboard/dictionary.html',context)
                      
    else:
        form = SearchForm()
        context= {'form':form}
    return render(request,'dashboard/dictionary.html',context)


def wiki(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        text = request.POST['text']
        search=wikipedia.page(text)
        context = {
                'form': form,
                'title': search.title,
                'link': search.url,
                'summary': search.summary,
            }
        
        return render(request, 'dashboard/wiki.html', context)
                      
    else:
        form = SearchForm()
        context = {'form': form}
    return render(request, 'dashboard/wiki.html', context)

def conversion(request):
    if request.method=="POST":
        form=ConversionForm(request.POST)
        if request.POST['measurement']=='length':
            m_form=LengthForm()
            context={'form':form,
                     'm_form':m_form,
                     'input':True}
            if 'input' in request.POST:
                first=request.POST['measur1']
                second=request.POST['measur2']
                input=request.POST['input']
                answer=''
                if input and int(input) >= 0:
                    if first=='yard' and second =='foot':
                        answer= f'{input} yard = {int(input)*3} foot'
                    if first=='foot' and second =='yard':
                        answer= f'{input} foot = {int(input)/3} yard'
                context={
                    'form':form,
                    'm_form':m_form,
                    'input':True,
                    'answer':answer
                }
        if request.POST['measurement']=='mass':
            m_form=MassForm()
            context={'form':form,
                     'm_form':m_form,
                     'input':True}
            if 'input' in request.POST:
                first=request.POST['measur1']
                second=request.POST['measur2']
                input=request.POST['input']
                answer=''
                if input and int(input) >= 0:
                    if first=='pound' and second =='kilogram':
                        answer= f'{input} pound = {int(input)*0.453} kilogram'
                    if first=='foot' and second =='yard':
                        answer= f'{input} kilogram = {int(input)/2.2062} pound'
                context={
                    'form':form,
                    'm_form':m_form,
                    'input':True,
                    'answer':answer
                }
        

    else:
        form=ConversionForm()
        context={
                    'form':form,
                    'input':False
            }
    return render(request,'dashboard/conversion.html',context)


def register(request):
    if request.method == "POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('login')
    else:
        form=UserRegistrationForm()
    context={'form':form}
    return render(request,'dashboard/register.html',context)

@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_complete=False,user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todos)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
    }

    return render(request,'dashboard/profile.html',context)