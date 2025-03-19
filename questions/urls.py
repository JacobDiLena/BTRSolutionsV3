from .views import BusinessForm,BusinessResults,BusinessEditView,BusinessExportView,BusinessTemplateView,DriversLicenseListView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',BusinessResults.as_view(),name='business_form_input'),
    path('edit/<int:pk>/',BusinessEditView.as_view(),name='business_edit'),
    #path('export/',BusinessExportView.as_view(),name='business_export'),
    path('export/',BusinessTemplateView.as_view(),name='business_template'),
    path('drivers-licenses/',DriversLicenseListView.as_view(),name='drivers_licenses'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
