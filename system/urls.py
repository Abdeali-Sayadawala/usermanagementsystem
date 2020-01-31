from django.urls import path, include
from .views import registerusr, loginusr, logout, usrposts, ecposts, likepost, commentpost, forgetpassword, resetpassword, editpost, deletepost

urlpatterns = [
    path('register/', registerusr),
    path('login/', loginusr),
    path('forgetpassword/', forgetpassword),
    path('resetpassword/<str:idd>/', resetpassword),
    path('', usrposts),
    path('commentpost/', commentpost),
    path('likepost/', likepost),
    path('deletepost/', deletepost),
    path('editpost/', editpost),
    path('logout/', logout),
    path('profile/', ecposts)
]