from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Toris Admin"
admin.site.site_title = "Toris Admin Portal"
admin.site.index_title = "Welcome to Toris Plant Portal"

urlpatterns = [
    path('', include('toris.urls')),
    path('admin/', admin.site.urls),



]
