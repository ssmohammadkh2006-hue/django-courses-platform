from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Home(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='carousel/')

class Courses(models.Model):
    images = models.ImageField(upload_to='courses/')
    name_courses = models.CharField(max_length=100)
    about_courses = models.TextField()

    instructor = models.CharField(max_length=100, blank=True, null=True)
    lessons = models.IntegerField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name_courses
   
   
   
class Lesson(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name="course_lessons")
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos/')
    duration = models.CharField(max_length=20)
    order = models.IntegerField()

    def __str__(self):
        return self.title
    

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.course.name_courses}"