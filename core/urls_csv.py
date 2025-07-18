from django.urls import path
from . import views, views_csv

# Choose between regular Django views or CSV-based views
# For CSV-based user management, use views_csv
# For regular Django ORM, use views

urlpatterns=[
    # CSV-based authentication (recommended for your use case)
    path('', views_csv.index, name='index'),
    path('hospital', views_csv.hospital, name='hos'),
    path('signup', views_csv.signup, name='signup'),
    path('login', views_csv.go, name='login'),
    path('prediction', views_csv.prediction, name='prediction'),
    path('out', views_csv.out, name='out'),
    path('profile', views_csv.profile, name='profile'),
    path('update_profile', views_csv.update_profile, name='update_profile'),
    path('admin_users', views_csv.admin_users, name='admin_users'),
    path('delete_user/<str:user_id>', views_csv.delete_user, name='delete_user'),
    
    # Alternative: Regular Django ORM-based views (uncomment to use)
    # path('', views.index, name='index'),
    # path('hospital', views.hospital, name='hos'),
    # path('signup', views.signup, name='signup'),
    # path('login', views.go, name='login'),
    # path('prediction', views.prediction, name='prediction'),
    # path('out', views.out, name='out'),
]
