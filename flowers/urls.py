from django.contrib import admin
from django.urls import path
from fapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.base),
    path('adbase',views.adbase),
    path('',views.index1),
    path('frreg',views.frreg),
    path('usrreg',views.usrreg),

    path('contact',views.contact),
    path('adlog',views.adlog),
    path('frview',views.frview,name='frview'),
    path('usrview',views.usrview,name='usrview'),
    path('adlogout',views.adlogout),

    path('farmlog',views.farmlog),
    path('forgotfarm',views.forgotfarm,name='forgotfarm'),
    path('frlogout',views.frlogout),
    path('usrlog',views.usrlog),
    path('forgotusr',views.forgotusr,name='forgotusr'),
    path('usrlogout',views.usrlogout),

    path('index',views.index),
    path('adindex',views.adindex),
    path('gallery',views.gallery),
    path('account',views.account,name='accont'),
    path('checkout',views.checkout),

    path('frbase',views.frbase),
    path('frindex',views.frindex),
    path('usrbase',views.usrbase),
    path('usrindex',views.usrindex,name='usrindex'),

    path('adpro',views.adpro),
    path('mngpro',views.mngpro),
    path('edit/<int:id>',views.edit),
    path('delete/<int:id>',views.delete),
    path('usrdisplay',views.usrdisplay,name='usrdisplay'),
    path('usrdisplay2/<int:id>',views.usrdisplay2,name='usrdisplay2'),

    path('addtocart/<int:id>',views.addtocart),
    path('buynow/<int:id>',views.buynow),
    path('mycart',views.mycart,name='mycart'),
    path('minuscart/<int:id>',views.minuscart),
    path('pluscart/<int:id>',views.pluscart),

    path('delete_c/<int:id>',views.delete_c),
    path('search',views.search),
    path('approve/<int:id>',views.approve,name='approve'),
    path('cancel/<int:id>',views.cancel,name='cacel'),

    path('rlyusr/<int:id>',views.rlyusr,name='rlyusr'),
    path('msg',views.msg,name='msg'),
    path('fmsg',views.fmsg,name='fmsg'),
    path('admsg',views.admsg,name='admsg'),
    path('adcon',views.adcon,name='adcon'),
    
    path('mybuy/<int:id>',views.mybuy,name='mybuy'),
    path('plusbuy/<int:id>',views.plusbuy,name='plusbuy'),
    path('minusbuy/<int:id>',views.minusbuy,name='minusbuy'),
    path('adshare/<int:id>',views.adshare,name='adshare'),
    path('prodisp',views.prodisp,name='prodisp'),
    path('aboutus',views.aboutus,name='aboutus'),

    path('create/', views.create_payment, name='create_payment'),
    # path('callback/', views.payment_callback, name='payment_callback'),
    path('success', views.success, name='success'),

    path('myacc',views.myacc,name='myacc'),
    path('edt/<int:id>',views.edt,name='edt'),
    path('order',views.order,name='order'),
    path('adpay',views.adpay,name='adpay'),
    path('fpay',views.fpay,name='fpay'),
    path('empty',views.empty,name='empty'),
    path('resetfarm/<token>',views.reset_passwordfarm,name='reset_passwordfarm'),
    path('resetuser/<token>',views.reset_passworduser,name='reset_passworduser'),
    path('delivery/<int:id>',views.delivery,name='delivery'),
    path('deliveries/<int:id>',views.deliveries,name='deliveries'),




    path('cart_payment', views.cart_payment, name='cart_payment'),
    path('csuccess', views.csuccess, name='csuccess'),









    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
