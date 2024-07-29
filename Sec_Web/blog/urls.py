
from django.urls import include, path

from blog.views import NewPred, NewProduct, premierPage

urlpatterns = [

    path('', premierPage, name='home'),
    path('Update/', NewProduct.as_view(), name='new-product'),
    path('Update2/', NewPred.as_view(), name='preduction')
]