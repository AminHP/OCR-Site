from django.conf.urls import include, url
from django.contrib import admin

import polls

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', polls.views.home),
    url(r'^signup/', polls.views.signup),
    url(r'^forgot_password/', polls.views.forgot_password),
    url(r'^login/', polls.views.login),
    url(r'^logout/', polls.views.logout),
    url(r'^recognize/', polls.views.recognize),
    url(r'^ocr/', polls.views.ocr_handler),
    url(r'^ocr_train/', polls.views.ocr_train_handler),
    url(r'^ocr_get_error/', polls.views.ocr_get_error_handler),
]
