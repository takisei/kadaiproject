from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'kadaiapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    path('photo_title/',views.PhotoTitleView.as_view(),name='photo_title'),
    
    
    path('post/', views.CreatePhotoView.as_view(), name='post'),
        
    #投稿完了ページへのアクセスはviewsモジュールのPostSuccessViewを実行
    path('post_done', views.PhotoSuccessView.as_view(), name='post_done'),
    
    path('photos/<int:category>',views.CategoryView.as_view(), name = 'photos_cat'),

    path('user_list/<int:user>',
        views.UserView.as_view(),
        name = 'user_list'
        ),

    path('detail/<int:pk>',
    views.DetailView.as_view(),
    name = 'detail'
    ),

    path('mypage/', views.MypageView.as_view(), name='mypage'),

    path('kadaiapp/<int:pk>/delete/',
        views.PhotoDeleteView.as_view(),
        name='delete'
        ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
