from django.urls import path

from . import views

app_name = 'dns_records'
urlpatterns = [
    path('', views.DnsRecordListView.as_view(), name='list'),
    path('export/', views.ZoneExportView.as_view(), name='zone_export'),
    path('import/', views.ZoneImportView.as_view(), name='zone_import'),
    path('create/', views.DnsRecordCreateView.as_view(), name='create'),
    path('<uuid:id>/', views.DnsRecordDetailView.as_view(), name='detail'),
    path('<uuid:id>/update/', views.DnsRecordUpdateView.as_view(), name='update'),
    path('<uuid:id>/delete/', views.DnsRecordDeleteView.as_view(), name='delete'),
]
