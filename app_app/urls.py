from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name="home"),
    path('courses/',views.courses,name="courses"),
    path('courses_details/<int:id>/', views.courses_details, name='courses_details'),
    
    
    
    
    path('my_courses/<int:course_id>/',views.my_courses,name="my_courses"),
    path('course/<int:course_id>/', views.course_lessons, name='course_lessons'),
    
    path('login/',views.login_view,name="login"),
    
    
    
] 


