from django.contrib import admin
from django.urls import path
from gemini_app.views import generate_content, process_cheque ,predict_similarity,upload_cheque # Correctly import your views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel route
    path('', generate_content, name='home'),  # Route for the root path (optional)
    path('api/generate-content/', generate_content, name='generate_content'),  # Your API route
    path('api/process-cheque/', process_cheque, name='process_cheque'),  # Correct route for the process_cheque view
    path("api/predict_similarity/", predict_similarity, name="predict_similarity"),
    path("api/upload_cheque/", upload_cheque, name="upload_cheque"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
