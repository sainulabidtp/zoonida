from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL
from .forms import URLForm
import qrcode


# Create your views here.
def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('list_url')
        else:
            messages.info(request,"invalid credentials")
            return redirect('login')
    return render(request, "signin.html")
def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
                return  redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Taken")
                return  redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password not matching")
            return redirect('register')
        return redirect('/')
    return render(request, 'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('credentials:login')

def shorten_url(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            shortend_url = form.save()

            qr = qrcode.QRCode(version=1,
                               error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=10,
                               border=4,
                               )
            qr.add_data(shorten_url.short_code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black",back_color="white")
            img.save(f'static/qrcodes/{shortend_url.short_code}.png')
            return render(request, 'shortened_url.html',{'shortened_url':shortend_url})
    else:
        form = URLForm(request.POST)
    return render(request, 'shortened_url.html', {'form': form})


def redirect_original(request,short_code):
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    shortened_url.visits +=1
    shortened_url.save()
    return redirect(shortened_url.original_url)

def view_url(request,short_code):
    shortened_url = get_object_or_404(ShortenedURL,short_code=short_code)
    return render(request,'view_url.html',{'shortened_url':shortened_url})

def list_urls(request):
    shortened_url = ShortenedURL.objects.all()
    for x in shortened_url:
        print(x)
    return  render(request,'list_urls.html', {'shortenend_urls':shortened_url})

def edit_url(request, short_code):
    shortened_url = get_object_or_404(ShortenedURL,short_code=short_code)
    print("bbbbbb", shortened_url)
    if request.method == 'POST':
        print("aaaa")
        form = URLForm(request.POST,instance=shortened_url)
        if form.is_valid():
            form.save()
            return  redirect('list_url')
        else:
            form = URLForm(instance=shortened_url)
        return render(request,'edit_url.html',{'form':form,'shortened_url':shortened_url})

def delete_url(request, short_code):
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    if request.method == 'POST':
        shortened_url.delete()
        return  redirect('list_urls')
    return  render(request, 'delete_url.html',{'shortened_url':shortened_url})