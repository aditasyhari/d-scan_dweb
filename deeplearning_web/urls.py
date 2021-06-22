from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include
# from django.views.generic import ListView, DetailView
# from myapp.views import ArticleView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # Url Article
    path('article/', views.ArticleView, name='article'),
    # path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('article/create/', views.article_create, name='create'),
    path('article/edit/<int:id>/', views.article_edit, name='edit'),
    path('article/edit/<int:id>/update/', views.article_update, name='update'),
    path('article/delete/<int:id>/', views.article_delete, name='delete'),

    # Url User
    path('user',views.user,name='user'),
    path('user/register',views.register,name='register'),
    path('user/delete/<int:id>',views.user_delete,name='user_delete'),

    # Url Dataset
    path('dataset',views.dataset,name='dataset'),
    path('dataset/crawling',views.crawling,name='crawling'),
    path('dataset/novalidate',views.novalidate,name='novalidate'),
    path('dataset/validate',views.validate,name='validate'),

    path('dataset/novalidate/antraknosa',views.dataset_novalidate,name='no_antraknosa'),
    path('dataset/novalidate/bercakMerah',views.dataset_novalidate,name='no_bercakMerah'),
    path('dataset/novalidate/busukBatang',views.dataset_novalidate,name='no_busukBatang'),
    path('dataset/novalidate/busukHitam',views.dataset_novalidate,name='no_busukHitam'),
    path('dataset/novalidate/kudis',views.dataset_novalidate,name='no_kudis'),
    path('dataset/novalidate/mosaik',views.dataset_novalidate,name='no_mosaik'),

    path('dataset/validate/antraknosa',views.dataset_validate,name='val_antraknosa'),
    path('dataset/validate/bercakMerah',views.dataset_validate,name='val_bercakMerah'),
    path('dataset/validate/busukBatang',views.dataset_validate,name='val_busukBatang'),
    path('dataset/validate/busukHitam',views.dataset_validate,name='val_busukHitam'),
    path('dataset/validate/kudis',views.dataset_validate,name='val_kudis'),
    path('dataset/validate/mosaik',views.dataset_validate,name='val_mosaik'),

    path('validasiDataset',views.validasiDataset,name='validasiDataset'),
    path('hapusDataset',views.hapusDataset,name='hapusDataset'),
    path('downloadDataset',views.downloadDataset,name='downloadDataset'),

    path('tambah-dataset/', views.tambahDataset, name='tambahDataset'),
    path('tambah-dataset/send-otp/',views.send_otp,name='send_otp'),

    url(r'^$',views.index,name='index'),
    url('home',views.homepage,name='homepage'),
    url('statistik',views.statistik,name='statistik'),
    url('scan',views.scan,name='scan'),
    # url('tambah-dataset',views.tambahDataset,name='tambahDataset'),
    url('upload-dataset',views.uploadDataset,name='uploadDataset'),
    url('predictImage',views.predictImage,name='predictImage'),
    url('mobile',views.mobile,name='mobile'),
    url('dashboard',views.dashboard,name='dashboard'),
    url('register',views.register_user,name='register_user'),

    # otp
    #  url('viewDataBase',views.viewDataBase,name='viewDataBase'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)