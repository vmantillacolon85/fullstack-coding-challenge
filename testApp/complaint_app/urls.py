from django.urls import path
from rest_framework import routers
from .views import ComplaintViewSet, OpenCasesViewSet, ClosedCasesViewSet, TopComplaintTypeViewSet, ConstituentComplaintViewSet

router = routers.SimpleRouter()
router.register(r'', ComplaintViewSet, base_name='complaint')
router.register(r'openCases', OpenCasesViewSet, base_name='openCases')
router.register(r'closedCases', ClosedCasesViewSet, base_name='closedCases')
router.register(r'topComplaints', TopComplaintTypeViewSet, base_name='topComplaints')
router.register(r'constituentsComplaints', ConstituentComplaintViewSet, base_name='constituentsComplaints')
urlpatterns = [

    path('openCases/', OpenCasesViewSet.as_view({'get': 'list'}), name='openCases'),
    path('closedCases/', ClosedCasesViewSet.as_view({'get': 'list'}), name='closedCases'),
    path('topComplaints/', TopComplaintTypeViewSet.as_view({'get': 'list'}), name='topComplaints'),
    path('constituentsComplaints/', ConstituentComplaintViewSet.as_view({'get': 'list'}), name='constituentsComplaints'),
]

urlpatterns += router.urls
