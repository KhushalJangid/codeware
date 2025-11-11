from django.shortcuts import render,redirect
import subprocess
from os import path,remove,listdir
from pathlib import Path
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from uuid import uuid4
# from accounts.models import User
# Create your views here.

BASE = Path(path.abspath(__file__)).parent.parent

def writeFile(request,filename):
    code = request.POST.get('code')
    _fileloc =  path.join(BASE,"media",filename)
    with open(_fileloc, 'w') as fp:
        fp.write(r'{}'.format(code))
        fp.close()
    return _fileloc

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
        BASE = Path(path.abspath(__file__)).parent.parent
        user = request.user
        user_files = path.join(BASE,'media',user.email)
        ctx['username'] = f'{user.first_name} {user.last_name}'
        ctx["user_files"] = listdir(user_files)
        return render(request,'index(1).html',ctx)

@api_view(['POST'])
def compile(request):   
    lang = request.POST.get('lang')
    stdin = request.POST.get('stdin')
    # lang = request.POST.get('lang')
    # code = request.POST.get('code')
    # stdin = request.POST.get('stdin')
    # _filename = f'test_{uuid4()}.{lang}'
    # _fileloc = path.join(BASE,"media",_filename)
    # with open(_fileloc, 'w') as fp:
    #     fp.write(r'{}'.format(code))
    #     fp.close()
    try :
        if lang == "py": 
            _fileloc = writeFile(request,f'test_{uuid4()}.{lang}')
            _output  = subprocess.run(["python",_fileloc],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
            remove(_fileloc)
        elif lang == "js": 
            _fileloc = writeFile(request,f'test_{uuid4()}.{lang}')
            _output  = subprocess.run(["node",_fileloc],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
            remove(_fileloc)
        elif lang == "cpp": 
            _fileloc = writeFile(request,f'test_{uuid4()}.{lang}')
            _output  = subprocess.run(["g++",_fileloc],timeout=5,capture_output=True)
            remove(_fileloc)
            if _output.returncode != 0:
                ctx = _output.stderr.decode('utf-8')
                return Response(ctx,status=status.HTTP_400_BAD_REQUEST)
            _output = subprocess.run([f'./a.out'],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
            remove('./a.out')
        elif lang == "c": 
            _fileloc = writeFile(request,f'test_{uuid4()}.{lang}')
            _output  = subprocess.run(["gcc",_fileloc],timeout=5,capture_output=True)
            remove(_fileloc)
            if _output.returncode != 0:
                ctx = _output.stderr.decode('utf-8')
                return Response(ctx,status=status.HTTP_400_BAD_REQUEST)
            _output = subprocess.run([f'./a.out'],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
            remove('./a.out')
        elif lang == "java":
            _fileloc = writeFile(request,'Main.java')
            _output  = subprocess.run(["javac",_fileloc],timeout=5,capture_output=True)
            remove(_fileloc)
            if _output.returncode != 0:
                ctx = _output.stderr.decode('utf-8')
                return Response(ctx,status=status.HTTP_400_BAD_REQUEST)
            _output = subprocess.run(['java',"Main"],input=stdin.encode('utf-8'),timeout=5,
                                     capture_output=True,cwd=path.join(BASE,"media"))
            remove(f'{_fileloc[:-5]}.class')
        elif lang == "dart": 
            _fileloc = writeFile(request,f'test_{uuid4()}.{lang}')
            _output  = subprocess.run(["dart",_fileloc],input=stdin.encode('utf-8'),timeout=5,capture_output=True)
            remove(_fileloc)
        else:
            return Response('Language not supported.',status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        print("Error : ",e.__str__())
        return Response(f'Error : {e.__str__()}',status=status.HTTP_400_BAD_REQUEST)
    ctx = _output.stdout.decode('utf-8')
    if _output.returncode != 0:
        ctx = _output.stderr.decode('utf-8')
        return Response(ctx,status=status.HTTP_400_BAD_REQUEST)
    return Response(ctx)

@login_required()
@api_view(['POST'])
def save(request):   
    lang = request.POST.get('lang')
    code = request.POST.get('code')
    print(code)
    filename = request.POST.get('filename')
    BASE = Path(path.abspath(__file__)).parent.parent
    _filename = f'{filename}.{lang}'
    _fileloc = path.join(BASE,"media",request.user.email,_filename)
    if path.isfile(_fileloc):
        _filename = f'{filename}(1).{lang}'
        _fileloc = path.join(BASE,"media",request.user.email,_filename)
    with open(_fileloc, 'w') as fp:
        fp.write(code)
        fp.close()
    return redirect(f'/open/{_filename}')

@login_required()
@api_view(['POST'])
def save_saved(request,filename):   
    lang = request.POST.get('lang')
    code = request.POST.get('code')
    filename = filename.split('.')[0]
    BASE = Path(path.abspath(__file__)).parent.parent
    _filename = f'{filename}.{lang}'
    _fileloc = path.join(BASE,"media",request.user.email,_filename)
    # if path.isfile(_fileloc):
    #     _filename = f'{filename}(1).{lang}'
    #     _fileloc = path.join(BASE,"media",request.user.email,_filename)
    with open(_fileloc, 'w') as fp:
        fp.write(code)
        fp.close()
    return redirect(f'/open/{_filename}')

@login_required()
def open_file(request,filename):
    ctx = isAuthenticated(request)
    BASE = Path(path.abspath(__file__)).parent.parent
    _fileloc = path.join(BASE,"media",request.user.email,filename)
    file = open(_fileloc, 'r')
    code = file.read()
    ctx["code"] = code
    user = request.user
    user_files = path.join(BASE,'media',user.email)
    lst = listdir(user_files)
    lst.remove(filename)
    ctx["user_files"] = lst
    ctx["active"] = filename
    ctx["filetype"] = filename.split(".")[-1]
    return render(request,'open.html',ctx)


