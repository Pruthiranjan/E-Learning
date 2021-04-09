from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import UserDetail, Teacher_Request, UserOtp, Blog, Course, Take_Course, Notes, Doubt, Answer, CourseVideo, VideoSection
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from PIL import Image, ImageDraw, ImageFont
import os
import pyttsx3
# Create your views here.
# login


def talk(data):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 130)
    engine.say(data)
    engine.runAndWait()


def Login(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    if request.method == "POST":
        user = request.POST["username"]
        password = request.POST["password"]
        data = authenticate(username=user, password=password)
        if data != None:
            login(request, data)
            if request.user.is_authenticated:
                talk("Login successfully welcome {}".format(
                    request.user.first_name))
                data = UserDetail.objects.get(pk=request.user)
                usertype = data.usertype
                if request.user.is_superuser:
                    return redirect("admin")
                elif request.user.userdetail.usertype == 'teacher':
                    return redirect("teacher")
                else:
                    return redirect("student")
        else:
            messages.warning(request, 'Invalid Credential !!!')
            talk("Invalid Credential Please try again")
    return render(request, "login.html")
# Signup


def Signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        password1 = request.POST["password"]
        password2 = request.POST["password2"]
        otp = 123456
        if password1 != password2:
            return redirect("signup")
        if User.objects.filter(username=email).exists():
            messages.warning(request,
                             'Email Already Exists Try Another One.')
            talk("Email Already Exists Try Another One.")
        else:
            user = User.objects.create_user(
                username=email, password=password2, first_name=first_name, last_name=last_name, email=email)
            UserDetail.objects.create(user=user, dob=dob, contact=contact)
            Teacher_Request.objects.create(user=user)
            UserOtp.objects.create(user=user, otp=otp)
            user.save()
            messages.success(
                request, 'Registration Successful Goto LogIn To Continue !!')
            talk("Registration Successfully Goto LogIn To Continue")
    return render(request, 'signup.html')

# student dashboard


def Student_Dashboard(request):
    if request.user.is_authenticated:
        data = User.objects.get(username=request.user)
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        courses = Course.objects.all()
        all_courses = Take_Course.objects.all()
        take_course = Take_Course.objects.filter(user_id=request.user.id)
        takec = 0
        c_complete = 0
        c_incomplete = 0
        if request.user.is_superuser:
            for c in all_courses:
                if c.status == "complete":
                    c_complete += 1
                elif c.status == "incomplete":
                    c_incomplete += 1
            takec = courses.count()
        else:
            for u in take_course:
                if u.status == "complete":
                    c_complete += 1
                elif u.status == "incomplete":
                    c_incomplete += 1
            takec = c_complete+c_incomplete
        return render(request, 'student.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1, 'courses': courses, "c_complete": c_complete, "c_incomplete": c_incomplete, "takec": takec})
    else:
        return HttpResponseRedirect('/login/')


def Logout(request):
    logout(request)
    talk("logout successfully.")
    return redirect("Home")


def Change_Password(request):
    if request.method == "POST":
        oldpass = request.POST["oldpass"]
        password1 = request.POST["password"]
        password2 = request.POST["password1"]
        uid = User.objects.get(username=request.user.username)
        check = uid.check_password(oldpass)
        if password1 != password2:
            return redirect("change_password")
        if check == True:
            uid.set_password(password1)
            uid.save()
            messages.success(request, 'Password SuccessFully Changed !!')
            login(request, uid)
            if request.user.is_authenticated:
                data = UserDetail.objects.get(pk=request.user)
                usertype = data.usertype
                if request.user.is_superuser:
                    return redirect("admin")
                elif request.user.userdetail.usertype == 'teacher':
                    return redirect("teacher")
                else:
                    return redirect("student")
        else:
            messages.warning(request, 'Old Password did not match !!')
            return redirect("change_password")
    else:
        if request.user.is_authenticated:
            data = User.objects.get(username=request.user)
            data1 = UserDetail.objects.get(pk=request.user)
            user = request.user.get_short_name()
            user1 = request.user.get_full_name()
            return render(request, 'change_password.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1})


def User_Profile(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        contact = request.POST["contact"]
        dob = request.POST["dob"]
        address = request.POST["address"]
        uid = User.objects.get(username=request.user.username)
        udata = UserDetail.objects.get(pk=request.user)
        uid.first_name = first_name
        uid.last_name = last_name
        udata.contact = contact
        udata.address = address
        udata.dob = dob
        uid.save()
        udata.save()
        if request.user.is_authenticated:
            return redirect("user_profile")
    else:
        if request.user.is_authenticated:
            data = User.objects.get(username=request.user)
            data1 = UserDetail.objects.get(pk=request.user)
            user = request.user.get_short_name()
            user1 = request.user.get_full_name()
            return render(request, 'user_profile.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1})
        else:
            return HttpResponseRedirect('/login/')


def Teacher_Dashboard(request):
    if request.user.is_authenticated:
        data1 = UserDetail.objects.get(pk=request.user)
        blogs = Blog.objects.all()
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        all_courses = Take_Course.objects.filter(teacher_id=request.user.id)
        tcourse = all_courses.count()
        return render(request, 'teacher.html', {'user': user, 'user1': user1, 'data1': data1, 'blogs': blogs, "tcourse": tcourse})
    else:
        return HttpResponseRedirect('/login/')


def Admin_Dashboard(request):
    if request.user.is_authenticated:
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        users = UserDetail.objects.all()
        blogs = Blog.objects.all()
        uc = 0
        tc = 0
        for u in users:
            if u.usertype == "student":
                uc += 1
            elif u.usertype == "teacher":
                tc += 1
        return render(request, 'admin.html', {'user': user, 'user1': user1, 'data1': data1, 'uc': uc, 'tc': tc, 'blogs': blogs})
    else:
        return HttpResponseRedirect('/login/')


def Teacher_Requset_View(request):
    if request.method == "POST":
        skills = request.POST["skills"]
        gcertificate = request.FILES["gcertificate"]
        twocertificate = request.FILES["twocertificate"]
        tencertificate = request.FILES["tencertificate"]
        Resume = request.FILES["Resume"]
        demovideo = request.FILES["demovideo"]
        why_teacher = request.POST["why_teacher"]
        experience = request.POST["experience"]
        accomplishments = request.POST["accomplishments"]
        data1 = UserDetail.objects.get(pk=request.user)
        data = Teacher_Request.objects.get(pk=request.user)
        data.skills = skills
        data.gcertificate = gcertificate
        data.tencertificate = tencertificate
        data.twocertificate = twocertificate
        data.resume = Resume
        data.demovideo = demovideo
        data.experience = experience
        data.why_teacher = why_teacher
        data.accomplishments = accomplishments
        data.status = "pending"
        data.save()
        data1.status = 'pending'
        data1.save()
        return redirect("student")
    if request.user.is_authenticated:
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        return render(request, 'become_Teacher.html', {'user': user, 'user1': user1, 'data1': data1})
    else:
        return HttpResponseRedirect('/login/')


def Profile_pic(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            profile_pic = request.FILES["profilepic"]
            udata = UserDetail.objects.get(pk=request.user)
            udata.Profile_img = profile_pic
            udata.save()
            return redirect("profile_pic")
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        return render(request, 'profile_pic.html', {'user': user, 'user1': user1, 'data1': data1})
    else:
        return HttpResponseRedirect('/login/')


def VerifyUser(request):
    if request.method == 'POST':
        email = request.POST["email"]
        if User.objects.filter(username=email).exists():
            try:
                u = User.objects.get(username=email)
                userotp = random.randint(100000, 999999)
            except:
                return render(request, 'User.html')
            body = f"Forgot Password!!Here is your OTP {userotp}"
            subject = f"Welcome to E-Learning!! OTP for user {u.username}"
            uotp = UserOtp.objects.get(user=u)
            uotp.otp = userotp
            uotp.save()
            send_mail(subject, body, settings.EMAIL_HOST_USER, [u.email])
            return render(request, 'forgot.html', {'email': email})
    return render(request, 'User.html')


def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST["email"]
        uotp = request.POST.get('userotp')
        pass1 = request.POST.get('npassword')
        pass2 = request.POST.get('cpassword')
        u = User.objects.get(username=email)
        otp = UserOtp.objects.get(user=u)
        if uotp != otp and pass1 != pass2:
            return render(request, 'forgot.html', {'email': email})
        else:
            u.set_password(pass1)
            u.save()
            return redirect("login")
    return render(request, 'forgot.html')


def Add_Subject(request):
    if request.user.is_authenticated:
        data = User.objects.get(username=request.user)
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        if request.method == "POST":
            cname = request.POST["cname"]
            cabout = request.POST["cabout"]
            cimage = request.FILES["cimage"]
            Course.objects.create(user=data, cname=cname, cabout=cabout,
                                  cimage=cimage)
            return HttpResponseRedirect('/teacher_dashboard/')
        return render(request, 'addsub.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1})
    else:
        return HttpResponseRedirect('/login/')


def Delete_Course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return HttpResponseRedirect('/manage_view/')


def Edit_Course(request, id):
    course = Course.objects.get(id=id)
    return render(request, 'editsub.html', {"course": course})


def Request_View(request):
    if request.user.is_authenticated:
        data = User.objects.get(username=request.user)
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        return render(request, 'request_view.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1})
    else:
        return HttpResponseRedirect('/login/')


def Manage_View(request):
    if request.user.is_authenticated:
        data = User.objects.get(username=request.user)
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        courses = Course.objects.all()
        return render(request, 'manage-view.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1, 'courses': courses})
    else:
        return HttpResponseRedirect('/login/')


def Manage_upload(request):
    if request.user.is_authenticated:
        data = User.objects.get(username=request.user)
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        return render(request, 'manage-upload.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1})
    else:
        return HttpResponseRedirect('/login/')


def Blog_Posting(request):
    if request.user.is_authenticated:
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        if request.method == "POST":
            btitle = request.POST["title"]
            bmessage = request.POST["message"]
            bimage = request.FILES["filename2"]
            uid = User.objects.get(username=request.user.username)
            bname = uid.first_name
            Blog.objects.create(title=btitle, message=bmessage,
                                image=bimage, post_user=bname)
            return HttpResponseRedirect('/teacher_dashboard/')
        return render(request, 'blogposting.html', {'user': user, 'user1': user1})
    else:
        return HttpResponseRedirect('/login/')


def Blog_show(request):
    data1 = UserDetail.objects.get(pk=request.user)
    user = request.user.get_short_name()
    user1 = request.user.get_full_name()
    blogs = Blog.objects.all()
    return render(request, 'blogshow.html', {'user': user, 'user1': user1, 'data1': data1, 'blogs': blogs})


def Upate_Profile_Pic(request):
    if request.user.is_authenticated:
        data = User.objects.get(username=request.user)
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        return render(request, 'update_Profile_Pic.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1})
    else:
        return HttpResponseRedirect('/login/')


def Student_Course(request):
    if request.user.is_authenticated:
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        taken_course = Take_Course.objects.filter(user_id=request.user.id)
        return render(request, 'student_course.html', {'user': user, 'user1': user1, 'data1': data1, 'taken_course': taken_course})
    else:
        return HttpResponseRedirect('/login/')


def Doubt_Post(request):
    if request.user.is_authenticated:
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        if request.method == "POST":
            doubt = request.POST["doubt"]
            d = Doubt(user=request.user, doubt=doubt,
                      postby=user)
            d.save()
            return redirect('doubt_show1')
        return render(request, 'doubt_post.html', {'user': user, 'user1': user1, 'data1': data1})
    else:
        return HttpResponseRedirect('/login/')


def Show_doubt(request):
    data1 = UserDetail.objects.get(pk=request.user)
    user = request.user.get_short_name()
    user1 = request.user.get_full_name()
    s = Doubt.objects.all()
    a = Answer.objects.all()
    return render(request, 'doubt_show1.html', {'s': s, 'a': a, 'user': user, 'user1': user1, 'data1': data1})


def Edit_doubt(request, id):
    data1 = UserDetail.objects.get(pk=request.user)
    user = request.user.get_short_name()
    user1 = request.user.get_full_name()
    d = Doubt.objects.get(id=id)
    if request.method == "POST":
        answer = request.POST["answer"]
        Answer.objects.create(user=request.user, doubt=d,
                              ans=answer, answerby=request.user.first_name)
        return redirect('doubt_show')
    return render(request, 'edit_doubt.html', {'d': d, 'user': user, 'user1': user1, 'data1': data1})


def Delete_doubt(request, id):
    d = Doubt.objects.get(id=id)
    d.delete()
    return redirect('doubt_show')


def Note(request):
    if request.user.is_authenticated:
        n = Notes.objects.filter(user_id=request.user.id)
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        return render(request, 'notes.html', {'user': user, 'user1': user1, 'data1': data1, 'n': n})
    else:
        return HttpResponseRedirect('/login/')


def Add_note(request):
    data1 = UserDetail.objects.get(pk=request.user)
    user = request.user.get_short_name()
    user1 = request.user.get_full_name()
    if request.method == "POST":
        ntitle = request.POST["title"]
        ndescription = request.POST["message"]
        Notes.objects.create(user=request.user, title=ntitle,
                             description=ndescription)
        return redirect('note')
    return render(request, 'addnote.html', {'user': user, 'user1': user1, 'data1': data1})


def Edit_note(request, id):
    data1 = UserDetail.objects.get(pk=request.user)
    user = request.user.get_short_name()
    user1 = request.user.get_full_name()
    n = Notes.objects.get(id=id)
    if request.method == "POST":
        ntitle = request.POST["title"]
        ndescription = request.POST["message"]
        n = Notes.objects.get(id=id)
        n.title = ntitle
        n.description = ndescription
        n.save()
        return redirect('note')
    return render(request, 'edit_note.html', {'n': n, 'user': user, 'user1': user1, 'data1': data1})


def Delete_note(request, id):
    n = Notes.objects.get(id=id)
    n.delete()
    return redirect('note')


def Teacher_rqst(request):
    if request.user.is_authenticated:
        data = User.objects.get(username=request.user)
        data1 = UserDetail.objects.get(pk=request.user)
        user_list = Teacher_Request.objects.filter(status="pending")
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        return render(request, 'teacher_rqst.html', {'user': user, 'user1': user1, 'data': data, 'data1': data1, 'users': user_list})
    else:
        return HttpResponseRedirect('/login/')


def Reject_Teacher(request, id):
    data = Teacher_Request.objects.get(user_id=id)
    u = UserDetail.objects.get(user_id=id)
    data.status = "rejected"
    u.user.userdetail.usertype = "student"
    u.user.userdetail.status = "notsent"
    u.save()
    data.save()
    return redirect('techer_rqst')


def Accept_Teacher(request, id):
    data = Teacher_Request.objects.get(user_id=id)
    u = UserDetail.objects.get(user_id=id)
    data.status = "approve"
    u.user.userdetail.usertype = "teacher"
    u.user.userdetail.status = "allow"
    u.save()
    data.save()
    return redirect('techer_rqst')


def Add_To_Acc(request, id, tid):
    if request.user.is_authenticated:
        data1 = UserDetail.objects.get(pk=request.user)
        user = request.user.get_short_name()
        user1 = request.user.get_full_name()
        take_course = Take_Course.objects.create(
            user_id=request.user.id, course_id=id, teacher_id=tid)
        return HttpResponseRedirect('/student_course/')
    else:
        return HttpResponseRedirect('/login/')


def Gen_Cert(request, id, tid):
    course = Course.objects.get(pk=tid)
    date = Take_Course.objects.get(id=id)
    font = ImageFont.truetype('KaushanScript-Regular.otf', 60)
    font1 = ImageFont.truetype('KaushanScript-Regular.otf', 30)
    font3 = ImageFont.truetype('KaushanScript-Regular.otf', 15)
    img = Image.open('certificate.jpg')
    draw = ImageDraw.Draw(img)
    uid = request.user.id
    text = request.user.get_full_name().title()
    iname = course.user.get_full_name().title()
    cname = course.cname.title()
    sdate = str(date.created).split(" ")
    edate = str(date.updated).split(" ")
    draw.text((580, 450), iname, fill="red", font=font1, align="right")
    draw.text((170, 385), cname, fill="red", font=font3, align="right")
    draw.text((330, 385), sdate[0], fill="green", font=font3, align="right")
    draw.text((460, 385), edate[0], fill="green", font=font3, align="right")
    # drawing text size
    if len(text) < 10:
        draw.text((350, 270), text, fill="red", font=font, align="right")
    else:
        draw.text((170, 270), text, fill="green", font=font, align="right")
    import time
    di = os.getcwd()
    img.save("{}/media/certificate/certificate{}{}.png".format(di, cname, uid))
    empPhoto = 'certificate/certificate{}{}.png'.format(cname, uid)
    course = Take_Course.objects.get(id=id)
    course.certificate = empPhoto
    course.save()
    return HttpResponseRedirect('/student_course/')


def Course_content(request, id):
    data1 = UserDetail.objects.get(pk=request.user)
    user = request.user.get_short_name()
    user1 = request.user.get_full_name()
    cv = CourseVideo.objects.filter(course_id=id)
    course = Course.objects.get(id=id)
    cs = VideoSection.objects.filter(course_id=id)
    if request.method == "POST":
        ctitle = request.POST["ctitle"]
        secid = request.POST["section"]
        video = request.FILES["Video"]
        cv = VideoSection.objects.get(id=secid)
        CourseVideo.objects.create(
            user=request.user, course=course, section=cv, ctitle=ctitle, cvideo=video)
        return redirect('manage_view')
    return render(request, 'course_content.html', {'user': user, 'user1': user1, 'data1': data1, 'cv': cv, 'cs': cs})


def New_section(request, id):
    cv = CourseVideo.objects.filter(course_id=id)
    course = Course.objects.get(id=id)
    vc = VideoSection.objects.filter(course_id=id)
    count = len(vc)
    count += 1
    VideoSection.objects.create(
        user=request.user, course=course, no_of_section=count)
    return redirect('manage_view')


def Del_section(request, id):
    vc = VideoSection.objects.get(id=id)
    vc.delete()
    return redirect('manage_view')
