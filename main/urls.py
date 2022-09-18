from django.urls import path
from main import views

urlpatterns = [
    path('',views.home),
    path('compile',views.compile),
    path('open/<str:filename>',views.open_file),
    path('save',views.save),
    path('saveas/<str:filename>',views.save_saved)
]
