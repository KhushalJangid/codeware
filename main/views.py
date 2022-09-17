from urllib import response
from django.shortcuts import render,HttpResponse
import subprocess
from os import path,remove
from pathlib import Path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from uuid import uuid4
# Create your views here.

def home(request):
    return render(request,'')

@api_view(['POST'])
def compile(request):   
    lang = request.POST.get('lang')
    code = request.POST.get('code')
    BASE = Path(path.abspath(__file__)).parent.parent
    _filename = f'test_{uuid4()}.{lang}'
    _fileloc = path.join(BASE,"media",_filename)
    with open(_fileloc, 'wb') as fp:
        # fp.write(code)
        fp.write(code.encode('utf-8'))
        fp.close()
    _output  = subprocess.run(["python",_fileloc],capture_output=True)
    ctx = _output.stdout.decode('utf-8')
    if _output.returncode != 0:
        ctx = _output.stderr.decode('utf-8')
    remove(_fileloc)
    print(_output.stdout.decode('UTF-8'))
    return Response(ctx)


@api_view(['POST'])
def save(request):   
    lang = request.POST.get('lang')
    code = request.POST.get('code')
    filename = request.POST.get('file-name')
    BASE = Path(path.abspath(__file__)).parent.parent
    _filename = f'{filename}.{lang}'
    _fileloc = path.join(BASE,"media",_filename)
    with open(_fileloc, 'wb') as fp:
        # fp.write(code)
        fp.write(code.encode('utf-8'))
        fp.close()
    _output  = subprocess.run(["python",_fileloc],capture_output=True)
    ctx = _output.stdout.decode('utf-8')
    if _output.returncode != 0:
        ctx = _output.stderr.decode('utf-8')
    remove(_fileloc)
    print(_output)
    return Response(ctx)
