from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm
from .views import SearchResultsView
urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path("category/<slug:val>", views.CategoryView.as_view(),name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(),name="category-title"),
    path("productdetail/<int:pk>", views.ProductDetail.as_view(),name="product-detail"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    #cart 
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('removecart/', views.remove_cart, name='remove_cart'),
    path('pluswishlist/', views.plus_wishlist,name='plus_wishlist'),
    path('minuswishlist/', views.minus_wishlist,name='minus_wishlist'),

    #customer resistration
    path('resistration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='pages/login.html',authentication_form=LoginForm),name='login'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='pages/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange' ),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='pages/passwordchangedone.html'), name='passwordchangedone' ),
    path('logout/', views.custom_logout, name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='pages/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='pages/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='pages/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='pages/password_reset_complete.html'), name='password_reset_complete'),
    path('payment-success/', views.paymentSuccessful, name='payment-successful'), 
    path('payment-failed/', views.paymentFailed, name='payment-failed'),
    path('afterpayment/', views.afterpayment, name='afterpayment'),
    path('orders/',views.orders,name='orders'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
