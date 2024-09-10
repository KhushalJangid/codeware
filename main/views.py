from django.shortcuts import render,redirect
import subprocess
from os import path,remove,listdir,makedirs
from django.http.response import HttpResponseNotAllowed,HttpResponse,HttpResponseForbidden,HttpResponseBadRequest
# from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
# from rest_framework.response import Response
# from rest_framework import status
from uuid import uuid4
from codeware.settings import BASE_DIR
# from accounts.models import User
# Create your views here.

def isAuthenticated(request):
    if request.user.is_anonymous:
        return {"auth":False}
    else :
        return {"auth":True}

def home(request):
    ctx = isAuthenticated(request)
    if ctx["auth"] == False:
        return render(request,'index(1).html',ctx)
    else:
        user = request.user
        user_files = path.join(BASE_DIR,'media',user.email)
        # print(listdir(user_files))
        if path.exists(user_files):
            ctx["user_files"] = listdir(user_files)
            return render(request,'index(1).html',ctx)
        else:
            makedirs(user_files)
            ctx["user_files"] = []
            return render(request,'index(1).html',ctx)
            

# @api_view(['POST'])
def compile(request): 
    if request.method == 'POST':
        lang = request.POST.get('lang')
        code = request.POST.get('code')
        stdin = request.POST.get('stdin')
        _filename = f'test_{uuid4()}.{lang}'
        _fileloc = path.join(BASE_DIR,"media",_filename)
        with open(_fileloc, 'w') as fp:
            # fp.write(code)
            fp.write(r'{}'.format(code))
            fp.close()
        try :
            if lang == "py": 
                _output  = subprocess.run(["python",_fileloc],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
                remove(_fileloc)
            elif lang == "js": 
                _output  = subprocess.run(["node",_fileloc],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
                remove(_fileloc)
            elif lang == "cpp": 
                _output  = subprocess.call(["g++",_fileloc],timeout=5)
                _output = subprocess.run([f'./a.out'],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
                remove(_fileloc)
                remove('./a.out')
            elif lang == "c": 
                _output  = subprocess.call(["gcc",_fileloc],timeout=5)
                _output = subprocess.run([f'./a.out'],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
                remove(_fileloc)
                remove('./a.out')
            elif lang == "dart": 
                _output  = subprocess.run(["dart",_fileloc],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
                remove(_fileloc)
            else:
                # return Response('Language not supported.',status=status.HTTP_403_FORBIDDEN)
                return HttpResponseForbidden('Language not supported.')
        except Exception as e:
            print(e.__str__())
            # return Response(e.__str__(),status=status.HTTP_400_BAD_REQUEST)
            return HttpResponseBadRequest(str(e))
        ctx = _output.stdout.decode('utf-8')
        if _output.returncode != 0:
            ctx = _output.stderr.decode('utf-8')
            # return Response(ctx,status=status.HTTP_400_BAD_REQUEST)
            return HttpResponseBadRequest(ctx)
        # return Response(ctx)
        return HttpResponse(ctx)
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required()
# @api_view(['POST'])
def save(request):  
    if request.method == 'POST': 
        lang = request.POST.get('lang')
        code = request.POST.get('code')
        print(code)
        filename = request.POST.get('filename')
        _filename = f'{filename}.{lang}'
        _fileloc = path.join(BASE_DIR,"media",request.user.email,_filename)
        if path.isfile(_fileloc):
            _filename = f'{filename}(1).{lang}'
            _fileloc = path.join(BASE_DIR,"media",request.user.email,_filename)
        with open(_fileloc, 'w') as fp:
            fp.write(code)
            fp.close()
        return redirect(f'/open/{_filename}')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required()
# @api_view(['POST'])
def save_saved(request,filename): 
    if request.method == 'POST':  
        lang = request.POST.get('lang')
        code = request.POST.get('code')
        filename = filename.split('.')[0]
        _filename = f'{filename}.{lang}'
        _fileloc = path.join(BASE_DIR,"media",request.user.email,_filename)
        with open(_fileloc, 'w') as fp:
            fp.write(code)
            fp.close()
        return redirect(f'/open/{_filename}')
    else:
        return HttpResponseNotAllowed(['POST'])

@login_required()
def open_file(request,filename):
    ctx = isAuthenticated(request)
    _fileloc = path.join(BASE_DIR,"media",request.user.email,filename)
    file = open(_fileloc, 'r')
    code = file.read()
    ctx["code"] = code
    user = request.user
    user_files = path.join(BASE_DIR,'media',user.email)
    lst = listdir(user_files)
    lst.remove(filename)
    ctx["user_files"] = lst
    ctx["active"] = filename
    ctx["filetype"] = filename.split(".")[-1]
    return render(request,'open.html',ctx)


