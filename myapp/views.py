from django.shortcuts import render
from django.views.static import serve

import shutil
from zipfile import ZipFile
import os
import re
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import PyPDF2
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError

from Myproject import test


# Create your views here.

def user_login(request):
    context={}
    if request.method =='POST':
        username= request.POST['username']
        password=request.POST['password']
        user=authenticate(request, username=username,password=password)
        if user:
            login(request, user)
            return redirect('/upload/')
        else:
            context["error"]= "provide valid credentials !!"
            return render(request,'index.html',context)


    else:
        return render(request,'index.html',context)

def register(request):
    return render(request,'singup.html')

def upload(request):
    if request.method=='POST' and 'resume' in request.POST:
        try:
            uploaded_file = request.FILES['document']
        except MultiValueDictKeyError:
            print("please select a file")
            return render(request, 'upload.html')
        if uploaded_file:
            if re.match(r'^.*\.pdf$',uploaded_file.name):
                fs = FileSystemStorage()
                fs.save(uploaded_file.name, uploaded_file)
                name = "media/" + str(uploaded_file.name)
                newfile = open('res.txt', 'w')
                file = open(name, 'rb')
                pdfreader = PyPDF2.PdfFileReader(file)
                # print(pdfreader.getNumPages())
                pageobj = pdfreader.getPage(0)
                newfile.write(pageobj.extractText())
                file.close()
                newfile.close()
                text_file = open('res.txt', 'r')
                resume = text_file.readlines()
                makeitastring = ''.join(map(str, resume))
                test.predict(makeitastring)
                return render(request, 'upload.html')
            elif re.match(r'^.*\.zip$',uploaded_file.name):
                context={}
                posts=[]
                os.mkdir('download_folder')
                fs=FileSystemStorage()
                fs.save(uploaded_file.name,uploaded_file)
                file_name=str(uploaded_file.name)
                with ZipFile(("media/" + file_name), 'r') as zip:
                    # extracting all the files
                    print('Extracting all the files now...')
                    zip.extractall()
                    print('Done!')
                new_name = re.sub(r'.zip$', "", file_name)
                for files in os.listdir(new_name):
                    filename = os.fsdecode(files)
                    if filename.endswith(".pdf"):
                        newfile = open('res.txt', 'w')
                        file = open((new_name+'/'+filename), 'rb')
                        pdfreader = PyPDF2.PdfFileReader(file)
                        # print(pdfreader.getNumPages())
                        pageobj = pdfreader.getPage(0)
                        newfile.write(pageobj.extractText())
                        file.close()
                        newfile.close()
                        text_file = open('res.txt', 'r')
                        resume = text_file.readlines()
                        makeitastring = ''.join(map(str, resume))
                        post=test.predict(makeitastring)
                        print(posts)
                        if post in posts:
                            shutil.copy((new_name+'/'+filename),("download_folder/"+str(post)))
                        else:
                            os.mkdir("download_folder/"+str(post))
                            shutil.copy((new_name + '/' + filename), ("download_folder/" + str(post)))
                            posts.append(post)
                    else:
                        continue
                print("folder upload worked")
                # shutil.rmtree('resumes')
                # os.remove("media/"+file_name)
                # print("delete successful")
                shutil.make_archive('folder', 'zip', 'download_folder')
                shutil.move('folder.zip','media')
                link=fs.url('folder.zip')
                context['url']=link
                return render(request, 'upload.html',context)
            else:
                print("please upload pdf or zip file")
                return render(request,'upload.html')

    else:
        context={}
        context['user']= request.user
        return render(request,'upload.html',context)
