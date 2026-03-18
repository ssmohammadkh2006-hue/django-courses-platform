from django.shortcuts import render, redirect
from .models import *
from .models import Enrollment
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Home Page
def home(request):
    images = Home.objects.all()
    return render(request,'pages/home.html',{'images': images})


# All Courses Page
def courses(request):
    all_courses = Courses.objects.all()
    return render(request, 'pages/courses.html', {'courses': all_courses})

# Course Details Page
def courses_details(request, id):
    course = Courses.objects.get(id=id)
    return render(request, 'pages/courses_details.html', {'course': course})




@login_required
def my_courses(request, course_id):
    course = get_object_or_404(Courses, id=course_id)

    # 🔥 تحقق إذا المستخدم مشترك
    enrollment = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).first()

    if not enrollment:
        return redirect('courses')  # أو صفحة "غير مصرح"

    lessons = course.course_lessons.all().order_by('order')

    lesson_id = request.GET.get('lesson')

    if lesson_id:
        current_lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    else:
        current_lesson = lessons.first()

    lesson_list = list(lessons)

    # 🔴 حماية إضافية (إذا ما في دروس)
    if not lesson_list:
        return render(request, 'pages/my_courses.html', {
            'lessons': [],
            'current_lesson': None,
            'progress': 0,
        })

    index = lesson_list.index(current_lesson)

    prev_lesson = lesson_list[index - 1] if index > 0 else None
    next_lesson = lesson_list[index + 1] if index < len(lesson_list) - 1 else None

    progress = int((index + 1) / len(lesson_list) * 100)

    return render(request, 'pages/my_courses.html', {
        'lessons': lessons,
        'current_lesson': current_lesson,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'progress': progress,
    })
    
@login_required
def course_lessons(request, course_id):
    course = get_object_or_404(Courses, id=course_id)

    # 🔥 تحقق سريع وأقوى
    if not Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists():
        messages.error(request, "You are not enrolled in this course")
        return redirect('courses')

    # جلب الدروس
    lessons = course.course_lessons.all().order_by('order')

    # 🔴 إذا ما في دروس
    if not lessons.exists():
        messages.warning(request, "No lessons available for this course yet")
        return redirect('courses')

    return render(request, 'course_lessons.html', {
        'course': course,
        'lessons': lessons
    })
    
    
# Login Page

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'courses')
            return redirect(next_url)
        else:
            return render(request, 'pages/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'pages/login.html')