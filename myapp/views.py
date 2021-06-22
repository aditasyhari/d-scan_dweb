from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, staff_required, superuser_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import resolve
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from wsgiref.util import FileWrapper
from zipfile import ZipFile
import urllib
import tempfile
import uuid
from math import *

import requests
from io import BytesIO
from PIL import Image
import numpy as np
import os
import shutil
from json import dumps 
import efficientnet.tfkeras
from tensorflow.keras.models import load_model

import random
from twilio.rest import Client

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Article
from .forms import *
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
import datetime

# parameters
input_size = (250, 250)
channel = (3,)
input_shape = input_size + channel
labels = ['Antraknosa', 'Bercak Merah', 'Busuk Batang', 'Busuk Hitam', 'Kudis', 'Mosaik']

# prepocessing function
def preprocess(img, input_size):
    nimg = img.convert('RGB').resize(input_size, resample = 0)
    img_arr = (np.array(nimg)) / 255
    return img_arr

def reshape(imgs_arr):
    return np.stack(imgs_arr, axis = 0)

# Load Model
MODEL_PATH = './models/pitaya/model10.h5'
model = load_model(MODEL_PATH, compile = False)

def index(request):
    return redirect('/home')

def homepage(request):
    return render(request,'index.html')

def statistik(request):
    return render(request,'statistik.html')

@superuser_required
def tambahDataset(request):
    return render(request,'tambah-dataset.html')

def scan(request):
    return render(request,'scan.html')





@superuser_required
def dashboard(request):
    import os

    n_listAntraks = os.listdir('./media/no-validate/antraknosa/')
    n_listBercakMerah = os.listdir('./media/no-validate/bercakMerah/')
    n_listBusukBatang = os.listdir('./media/no-validate/busukBatang/')
    n_listBusukHitam = os.listdir('./media/no-validate/busukHitam/')
    n_listKudis = os.listdir('./media/no-validate/kudis/')
    n_listMosaik = os.listdir('./media/no-validate/mosaik/')

    n_antraks = len(n_listAntraks)
    n_bercak_merah = len(n_listBercakMerah)
    n_busuk_batang = len(n_listBusukBatang)
    n_busuk_hitam = len(n_listBusukHitam)
    n_kudis = len(n_listKudis)
    n_mosaik = len(n_listMosaik)

    d_listAntraks = os.listdir('./media/done-validate/antraknosa/')
    d_listBercakMerah = os.listdir('./media/done-validate/bercakMerah/')
    d_listBusukBatang = os.listdir('./media/done-validate/busukBatang/')
    d_listBusukHitam = os.listdir('./media/done-validate/busukHitam/')
    d_listKudis = os.listdir('./media/done-validate/kudis/')
    d_listMosaik = os.listdir('./media/done-validate/mosaik/')

    d_antraks = len(d_listAntraks)
    d_bercak_merah = len(d_listBercakMerah)
    d_busuk_batang = len(d_listBusukBatang)
    d_busuk_hitam = len(d_listBusukHitam)
    d_kudis = len(d_listKudis)
    d_mosaik = len(d_listMosaik)

    total_novalidate = n_antraks + n_bercak_merah + n_busuk_batang + n_busuk_hitam + n_kudis + n_mosaik
    total_donevalidate = d_antraks + d_bercak_merah + d_busuk_batang + d_busuk_hitam + d_kudis + d_mosaik

    total_dataset = total_novalidate + total_donevalidate

    # total_article = Article.objects.count()
    # total_user = User.objects.count()
    # print(total_article)
    # print(total_user)

    data = [n_antraks + d_antraks, n_bercak_merah + d_bercak_merah, n_busuk_batang + d_busuk_batang, n_busuk_hitam + d_busuk_hitam, n_kudis + d_kudis, n_mosaik + d_mosaik]
    context = {'data':data, 'total_dataset':total_dataset, 'total_novalidate':total_novalidate, 'total_donevalidate':total_donevalidate}
    
    return render(request,'dashboard/index.html',context)

# ==================================================================
#                       ARTICLE
# ==================================================================

@login_required
def ArticleView(request):
    articles_list = Article.objects.all()
    paginator = Paginator(articles_list, 5)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'article/index.html', {'articles': articles})


# class ArticleDetailView(DetailView):
#     model = Article
#     template_name = 'article/article-detail.html'

@login_required
def article_create(request):
    if request.method == 'POST':
        article = Article(
            judul=request.POST['judul'],
            jenis_penyakit=request.POST['jenis_penyakit'],
            isi=request.POST['isi']
        )
        try:
            article.full_clean()
        except ValidationError as e:
            pass
        article.save()
        messages.success(request, 'Article was created successfully!')
        return redirect('article')
    else:
        return render(request, 'article/create.html')

@login_required
def article_edit(request, id):
    article = Article.objects.get(id=id)
    context = {'article': article}
    return render(request, 'article/edit.html', context)

@login_required
def article_update(request, id):
    article = Article.objects.get(id=id)
    context = {'article':article}
    if request.method == 'POST':
        article = Article(
            judul=request.POST['judul'],
            jenis_penyakit=request.POST['jenis_penyakit'],
            isi=request.POST['isi']
        )
        article.save()
        messages.success(request, 'Article was updated successfully!')
        return redirect('article')
    else:
        return render(request, 'article/edit.html', context)

@login_required
def article_delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    messages.error(request, 'Article was deleted successfully!')
    return redirect('article')
# =================================================================


# =================================================================
#                               Users
# =================================================================
@login_required
def user(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'user/index.html', {'users': users})

def registerUser(request):
    return render(request, 'registration/register.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                # password=form.cleaned_data['password1'],
                is_staff=False,
                is_active=True,
                is_superuser=True,
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'User was added successfully!')
            return redirect('user')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})

@csrf_protect
def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                # password=form.cleaned_data['password1'],
                is_staff=False,
                is_active=True,
                is_superuser=True,
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Akun kontributor berhasil dibuat!')
            return redirect('register_user')
    else:
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.error(request, 'User was deleted successfully!')
    return redirect('user')

# ================================================================


# ================================================================
#                       PREDICT IMAGE
# ================================================================

def predictImage(request):
    if request.method == 'POST':
        print(request)
        print(request.POST.dict())

        fileObj = request.FILES['filePath']
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testimage = '.'+filePathName

        # predict the image
        img = Image.open(testimage)
        X = preprocess(img, input_size)
        X = reshape([X])
        y = model.predict(X)

        predictedLabel = labels[np.argmax(y)]
        predictedAcc = np.max(y)*100
        # print(labels[np.argmax(y)], np.max(y))

        # if (predictedLabel == 'Antraknosa'):
        #     shutil.copy2(testimage, './media/no-validate/antraknosa/'+fileObj.name)
        # elif (predictedLabel == 'Bercak Merah'):
        #     shutil.copy2(testimage, './media/no-validate/bercakMerah/'+fileObj.name)
        # elif (predictedLabel == 'Busuk Batang'):
        #     shutil.copy2(testimage, './media/no-validate/busukBatang/'+fileObj.name)
        # elif (predictedLabel == 'Busuk Hitam'):
        #     shutil.copy2(testimage, './media/no-validate/busukHitam/'+fileObj.name)
        # elif (predictedLabel == 'Kudis'):
        #     shutil.copy2(testimage, './media/no-validate/kudis/'+fileObj.name)
        # else:
        #     shutil.copy2(testimage, './media/no-validate/mosaik/'+fileObj.name)
        acc = floor(predictedAcc)

        context = {'filePathName':filePathName,'predictedLabel':predictedLabel,'acc':acc}
        return render(request,'scan.html',context)

    else:
        return redirect('/scan')




# Mobile
async def mobile(request) :
    fileObj = request.FILES['file']
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    testimage = '.'+filePathName

    # predict the image
    img = Image.open(testimage)
    X = preprocess(img, input_size)
    X = reshape([X])
    y = model.predict(X)

    predictedLabel = labels[np.argmax(y)]
    # print(labels[np.argmax(y)], np.max(y))

    return JsonResponse({'result': str(predictedLabel)})

# ====================================================================


# ====================================================================
#                                DATASET
# ====================================================================

imgs = []

@csrf_protect
def send_otp(request):
    if request.method == 'POST':

        id_user = request.POST['id_user']
        jenis_penyakit = request.POST['jenis_penyakit']
        img_data = request.FILES.getlist('dataset')
        phone = request.POST['phone']
        print(phone)
        print(id_user)
        print(img_data)

        user = User.objects.get(id=id_user)

        account_sid = "AC4688e7199d8e7c8b412fe609ba6167f0"
        auth_token = "3393672809410fa092f1c609c1e046bd"
        client = Client(account_sid, auth_token)

        # global imgs
        # imgs.append(img_data)

        # print(imgs)

        otp = random.randint(1000,9999)
        user.otp = otp
        user.save()

        message = client.messages.create(
                body='masukkan code otp '+str(otp),
                from_='+14154771214',
                to=phone
        )

        img_dir = './media/no-validate/'+jenis_penyakit+'/'

        for i in img_data:
            print(i)
            extension = os.path.splitext(i.name)
            file_name = '{}{}'.format(uuid.uuid4(), extension[1])
            with open(img_dir+ file_name, 'wb+') as destination:
                for chunk in i.chunks():#Prevent the file size from causing memory overflow
                    destination.write(chunk)

        context = {'jenis_penyakit':jenis_penyakit, 'img_data':img_data, 'id_user': id_user}

        # return render(request, 'send-otp.html')
        return render(request, 'send-otp.html', context)

@csrf_protect
def uploadDataset(request):
    if request.method == 'POST':
        id_user = request.POST['id_user']
        jenis_penyakit = request.POST['jenis_penyakit']
        otp = request.POST['otp']
        # img_data = request.FILES.getlist('dataset')
        print(jenis_penyakit)
        # print(img_data)

        user = User.objects.get(id=id_user)


        if otp == user.otp:
            # img_dir = './media/no-validate/'+jenis_penyakit+'/'
            # for i in imgs:
            #     print(i)
            #     extension = os.path.splitext(i.name)
            #     file_name = '{}{}'.format(uuid.uuid4(), extension[1])
            #     with open(img_dir+ file_name, 'wb+') as destination:
            #         for chunk in i.chunks():#Prevent the file size from causing memory overflow
            #             destination.write(chunk)
                # shutil.move('.'+i, './media/no-validate/'+jenis_penyakit+'/')

            messages.success(request, 'Terimakasih! Dataset berhasil diunggah!!')
            return redirect('/tambah-dataset')
        else:
            return render(request, 'tambah-dataset.html', {'pesan': 'Kode OTP salah!'})

    else:
        return redirect('/')

@login_required
def dataset(request):
    return render(request,'dataset/index.html')

@login_required
def crawling(request):
    from bs4 import BeautifulSoup

    GOOGLE_IMAGE = \
        'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

    imagelinks = []
    if request.method == 'GET':
        if 'status_check' in request.GET:

            data = request.GET['keyword']
            n_images = int(request.GET['jumlah'])
            data_lower = data.lower()

            print('Start searching...')
            
            katakunci = urllib.parse.quote_plus(data_lower)
            # print(keyword)

            searchurl = GOOGLE_IMAGE + 'q=' + katakunci
            print(searchurl)

            def getdata(url): 
                r = requests.get(url) 
                return r.text 
            
            htmldata = getdata(searchurl) 
            soup = BeautifulSoup(htmldata, 'html.parser')

            results = soup.find_all('img', limit=n_images+1)
            
            for i, re in enumerate(results):
                if i == 0:
                    continue

                imagelinks.append(re['src'])

    return render(request,'dataset/crawling/index.html', {'results': imagelinks})

@login_required
def novalidate(request):
    return render(request,'dataset/no_validate/index.html')

@login_required
def validate(request):
    return render(request,'dataset/done_validate/index.html')


# dataset belum divalidasi
@login_required
def dataset_novalidate(request):
    url_name = resolve(request.path).url_name
    print(url_name)
    if(url_name == 'no_antraknosa'):
        folder = 'antraknosa'
        nama = 'Antraknosa'
    elif(url_name == 'no_bercakMerah'):
        folder = 'bercakMerah'
        nama = 'Bercak Merah'
    elif(url_name == 'no_busukBatang'):
        folder = 'busukBatang'
        nama = 'Busuk Batang'
    elif(url_name == 'no_busukHitam'):
        folder = 'busukHitam'
        nama = 'Busuk Hitam'
    elif(url_name == 'no_kudis'):
        folder = 'kudis'
        nama = 'Kudis'
    elif(url_name == 'no_mosaik'):
        folder = 'mosaik'
        nama = 'Mosaik'

    listImages=os.listdir('./media/no-validate/'+folder+'/')
    listImagesPath=['/media/no-validate/'+folder+'/'+i for i in listImages]
    total = len(listImages)
    # print(total)

    context = {'listImagesPath':listImagesPath, 'nama_penyakit':nama, 'total':total}
    return render(request,'dataset/no_validate/dataset_novalidate.html',context)

# dataset sudah divalidasi
@login_required
def dataset_validate(request):
    url_name = resolve(request.path).url_name
    print(url_name)
    if(url_name == 'val_antraknosa'):
        folder = 'antraknosa'
        nama = 'Antraknosa'
    elif(url_name == 'val_bercakMerah'):
        folder = 'bercakMerah'
        nama = 'Bercak Merah'
    elif(url_name == 'val_busukBatang'):
        folder = 'busukBatang'
        nama = 'Busuk Batang'
    elif(url_name == 'val_busukHitam'):
        folder = 'busukHitam'
        nama = 'Busuk Hitam'
    elif(url_name == 'val_kudis'):
        folder = 'kudis'
        nama = 'Kudis'
    elif(url_name == 'val_mosaik'):
        folder = 'mosaik'
        nama = 'Mosaik'

    listImages=os.listdir('./media/done-validate/'+folder+'/')
    listImagesPath=['/media/done-validate/'+folder+'/'+i for i in listImages]
    total = len(listImages)
    # print(total)

    context = {'listImagesPath':listImagesPath, 'nama_penyakit':nama, 'total':total}
    return render(request,'dataset/done_validate/dataset_donevalidate.html',context)


def validasiDataset(request):
    print(request)
    jenis_penyakit = request.POST['jenis_penyakit']
    img_data = request.POST.getlist ('cbdata')
    print(jenis_penyakit)

    for i in img_data:
        print(i)
        shutil.move('.'+i, './media/done-validate/'+jenis_penyakit+'/')

    # return redirect('no_'+jenis_penyakit)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def hapusDataset(request):
    print(request)
    img_data = request.POST.getlist ('cbdata')

    for i in img_data:
        print(i)
        os.remove('.'+i)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def downloadDataset(request):
    temp = tempfile.TemporaryFile()
    zip = ZipFile(temp, 'w')

    images = request.POST.getlist('cbdata')

    for img in images:
        zip.write('.'+img)

    zip.close()
    temp.seek(0)
    wrapper = FileWrapper(temp)

    response = HttpResponse(wrapper, content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename=dataset-download.zip'
    return response

# ===================================================================================