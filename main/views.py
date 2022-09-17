from django.shortcuts import render,HttpResponse
import subprocess
from os import path
from pathlib import Path
# Create your views here.

def home(request):
    file = str(Path(path.abspath(__file__)).parent.parent)+"/media/" + "tests.py"
    exec = f"python -u {file}"
    out  = str(subprocess.check_output(["python",file]))
    print(out)
    return HttpResponse(request,out)