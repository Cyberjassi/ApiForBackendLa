
from django.contrib import admin
from django.urls import path,include

# for image-
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('main.urls')),
    #it is responstible for give login functionality in our rest_framework page
    # path('api-auth/',include('rest_framework.urls'))
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
