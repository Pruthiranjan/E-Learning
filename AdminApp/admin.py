from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(UserDetail)
admin.site.register(Teacher_Request)
admin.site.register(UserOtp)
admin.site.register(Blog)
admin.site.register(Course)
admin.site.register(CourseVideo)
admin.site.register(VideoSection)
admin.site.register(Take_Course)
admin.site.register(Notes)
admin.site.register(Doubt)
admin.site.register(Answer)
