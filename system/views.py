from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Person, Post, Comment, Like, Likecomments
from passlib.hash import pbkdf2_sha256
from usermanagement.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# Create your views here.
def registerusr(request):
    # form = Person(request.POST or None)
    form = request.POST or None
    if form != None:
        obj = Person.objects.create(
            fullname = request.POST['fname'],
            email = request.POST['email'],
            phone = request.POST['mobile'],
            password = pbkdf2_sha256.hash(request.POST['pass'], rounds=1200, salt_size=8)
        )
        obj.save()
        request.session['id'] = obj.id
        request.session['name'] = obj.fullname
        request.session['email'] = obj.email
        return redirect('/')
    return render(request, 'register.html')

def loginusr(request):
    if request.method == 'POST':
        try:
            if Person.objects.get(email = request.POST['mail']):
                # print(request.session['name'])
                obj = Person.objects.get(email = request.POST['mail'])
                if(pbkdf2_sha256.verify(request.POST['pass'], obj.password)):
                    request.session['id'] = obj.id
                    request.session['name'] = obj.fullname
                    request.session['email'] = obj.email
                    return redirect('/')
                else:
                    return render(request, 'login.html', {"login":'false'})
                # return render(request, 'userhome.html', {'uname':request.session['name'], 'loginstatus':'true'})
        except:
            return render(request, 'login.html', {"login":'false'})
    return render(request, 'login.html', {"login":'pending'})

def forgetpassword(request):
    if request.method == 'POST':
        #try:
        email = request.POST['email']
        print(email)
        message = 'http://127.0.0.1:8000/resetpassword/'+str(Person.objects.get(email = request.POST['email']).id)+"/"
        subject = "This is mail"
        send_mail(subject,message, EMAIL_HOST_USER, [email], fail_silently=False)
        return render(request, 'forgetpassword.html', {"status":'success', 'message': 'Please check your email for further instructions and reset password link'})
        #except:
        return render(request, 'forgetpassword.html', {'status': 'false', 'message': 'user does not Exists'})
    else:
        return render(request, 'forgetpassword.html')

def resetpassword(request, idd):
    print(idd)
    if request.method == "POST":
        personobj = Person.objects.get(id = int(idd))
        personobj.password = pbkdf2_sha256.hash(request.POST['newpass'], rounds=1200, salt_size=8)
        personobj.save()
        return redirect('/login')
        # personobj = Person.objects.get()
    return render(request, 'resetpassword.html')

def logout(request):
    try:
        del request.session['name']
    except:
        pass
    return redirect('/login')

def usrposts(request):
    objposts = Post.objects.all()
    userlen = len(Person.objects.all())
    try:
        usrsession = request.session['name']
        usrsessionid = request.session['id']
        return render(request, 'userhome.html', {'uname':usrsession, 'userlen':userlen, 'uid':usrsessionid, 'loginstatus':'true', 'posts':objposts})
    except:
        return render(request, 'userhome.html', {'uname':'Anonymous User', 'userlen':userlen, 'uid':'0', 'loginstatus':'false', 'posts':objposts})

def likepost(request):
    if request.method == 'GET':
        if request.GET['status'] == '1':
            likeobj = Like.objects.create(
                user = Person.objects.get(id = request.GET['posterid'])
            )
            postobj = Post.objects.get(id = request.GET['idd'])
            postobj.likes.append(likeobj)
            postobj.save()
            pass
        elif request.GET['status'] == '0':
            postobj = Post.objects.get(id = request.GET['idd'])
            likeobj = postobj.likes
            for obj in likeobj:
                if obj.user.id == int(request.GET['posterid']):
                    postobj.likes.pop(likeobj.index(obj))
            postobj.save()
        return HttpResponse()

def likecomment(request):
    if request.method == 'GET':
        if request.GET['status'] == '1':
            likecomobj = Likecomments.objects.create(
                user = Person.objects.get(id = request.GET['likerid'])
            )
            postobj = Post.objects.get(id = request.GET['posid'])
            for comment in postobj.comments:
                if comment.cid == int(request.GET['commid']):
                    comment.likes.append(likecomobj)
            postobj.save()
        if request.GET['status'] == '0':
            postobj = Post.objects.get(id = request.GET['posid'])
            for comment in postobj.comments:
                if comment.cid == int(request.GET['commid']):
                    for like in comment.likes:
                        if like.user.id == int(request.GET['likerid']):
                            comment.likes.pop(comment.likes.index(like))
            postobj.save()
    return HttpResponse()

def commentpost(request):
    likes = []
    if request.method == 'GET':
        commobj = Post.objects.get(id = request.GET['postid']).comments
        if commobj == []:
            cid = 1
        else:
            cid = commobj[len(commobj)-1].cid + 1
        commentobj = Comment.objects.create(
            cid = cid,
            user = Person.objects.get(id = request.GET['posterid']),
            comment = request.GET['comment'],
            likes = likes
        )
        postobj = Post.objects.get(id = request.GET['postid'])
        postobj.comments.append(commentobj)
        postobj.save()                
        print(Person.objects.get(id = request.GET['posterid']).fullname)
        print(Post.objects.get(id = request.GET['postid']).description)
        print(request.GET['comment'])
    return HttpResponse()

def editpost(request):
    try:
        if request.method == 'GET':
            postobj = Post.objects.get(id = request.GET['postid'])
            postobj.description = request.GET['data']
            postobj.save()
    except:
        print("id not found")
    return HttpResponse()

def deletepost(request):
    try:
        if request.method == 'GET':
            postobj = Post.objects.get(id = request.GET['postid'])
            postobj.delete()
            
    except:
        print("Id not found")
    return HttpResponse()

def ecposts(request):
    try:
        usrsession = request.session['name']
        usrid = request.session['id']
        likes = []
        comments = []
        print(Person.objects.get(id = request.session['id']))
        userobj = Post.objects.filter(user = Person.objects.get(id = request.session['id']))
        if request.method == 'POST':
            obj = Post.objects.create(
                user = Person.objects.get(email = request.session['email']),
                description = request.POST['desc'],
                likes = likes,
                comments = comments
            )
            obj.save()
            return redirect('/')
        return render(request, 'ecpost.html', {'uname':usrsession, 'uid': usrid, 'loginstatus':'true', 'posts':userobj})
    except:
        return redirect('/login')
