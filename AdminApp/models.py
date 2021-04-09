from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def course_directory_path(instance, filename):
    return 'courseVideo/user_{0}/{1}'.format(instance.user.id, filename)


class UserDetail(models.Model):
    choice = [
        ('student', 'student'),
        ('teacher', 'teacher'),
        ('admin', 'admin'),
    ]
    status = [
        ('allow', 'allow'),
        ('deny', 'deny'),
        ('pending', 'pending'),
        ('notsent', 'notsent'),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    contact = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=250, null=True)
    dob = models.CharField(max_length=50, null=True)
    usertype = models.CharField(
        max_length=10, choices=choice, default='student')
    Profile_img = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    status = models.CharField(
        max_length=30, choices=status, default='notsent')

    def __str__(self):
        """."""
        return self.user.username


class Teacher_Request(models.Model):
    status = [
        ('approve', 'approve'),
        ('rejected', 'rejected'),
        ('pending', 'pending'),
        ('notsent', 'notsent'),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(
        max_length=30, choices=status, default='notsent')
    skills = models.CharField(max_length=1000, null=True, blank=True)
    gcertificate = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    twocertificate = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    tencertificate = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    resume = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    demovideo = models.FileField(
        upload_to=user_directory_path, null=True, blank=True)
    why_teacher = models.CharField(max_length=1000, null=True, blank=True)
    experience = models.CharField(max_length=1000, null=True, blank=True)
    accomplishments = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        """."""
        return self.user.username


class UserOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now=True)
    otp = models.SmallIntegerField()

    def __str__(self):
        """."""
        return self.user.username


class Blog(models.Model):
    """."""
    title = models.CharField(max_length=255, null=True, blank=True)
    post_user = models.CharField(max_length=255, null=True)
    message = models.TextField(max_length=1000, null=True, blank=True)
    image = models.FileField(upload_to='blog_file', blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """."""

        return self.title


class Course(models.Model):
    """."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cname = models.CharField(max_length=255, null=True, blank=True)
    cabout = models.TextField(max_length=1000, null=True, blank=True)
    cimage = models.FileField(upload_to='courseimages',
                              blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """."""

        return self.cname


class VideoSection(models.Model):
    """."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    no_of_section = models.CharField(max_length=255, null=True)

    def __str__(self):
        """."""
        return self.no_of_section


class CourseVideo(models.Model):
    """."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(
        VideoSection, on_delete=models.CASCADE, null=True)
    ctitle = models.CharField(max_length=255, null=True)
    cvideo = models.FileField(upload_to=course_directory_path,
                              blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """."""
        return self.course.cname


class Take_Course(models.Model):
    """."""
    status = [
        ('complete', 'complete'),
        ('incomplete', 'incomplete'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30, choices=status, default='incomplete')
    certificate = models.FileField(upload_to='certificate',
                                   blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    teacher_id = models.CharField(max_length=250, null=True)

    def __str__(self):
        """."""
        return self.course.cname


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        """."""
        return self.title


class Doubt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    doubt = models.TextField(null=True)
    postby = models.CharField(max_length=255, null=True)

    def __str__(self):
        """."""
        return self.doubt


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doubt = models.ForeignKey(Doubt, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    answerby = models.CharField(max_length=255, null=True)
    ans = models.TextField()

    def __str__(self):
        """."""
        return self.ans
