from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/generate-content/', views.generate_content, name='generate_content'),
    path('api/process-cheque/', views.process_cheque, name='process_cheque'),
    path("api/predict_similarity/", views.predict_similarity, name="predict_similarity"),
    path("api/upload_cheque/", views.upload_cheque, name="upload_cheque"),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

