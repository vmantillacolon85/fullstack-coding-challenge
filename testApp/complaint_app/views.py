from rest_framework import viewsets, status
from .models import UserProfile, Complaint
from .serializers import UserSerializer, UserProfileSerializer, ComplaintSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count

## Important things to know about the data
## The fields account and council_dist both refer to a council district. However, account refers to the district in which the complaint is being made, and council_dist refers to the district in which the person who is making the complaint lives. (i.e., John Doe is the Council Member for District 1, if a noise complaint labels account as NYCC01 and council_dist as NYCC34, that means the complaint is being made in his district 1, by a person who lives in district 34).
## All of the data are string data types except for the open and close dates. In addition, the data is NOT entirely clean; some fields will be empty strings or NULL.
## Single digit districts numbers are padded by a zero in the Complaint table, BUT single digit district numbers in the UserProfile table are NOT padded by a zero. You will need to take this into consideration when writing your code.

def updatedpadDistrict(dist):

    dist = dist if len(dist) > 1 else '0' + dist

    return "New York City Council" + dist

def ComplaintDataset(request):
    distNumber = renderDistNumber(request)
    complaints = Complaint.objects.filter(account_exact =distNumber)
    return complaints

# Create your views here.

class ComplaintViewSet(viewsets.ModelViewSet):
  http_method_names = ['get']
  serializer_class = ComplaintSerializer
  queryset = Complaint.objects.all()

  def list(self, request):
    # Get all complaints from the user's district
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    complaints = self.queryset.filter(
        account_exact = updatedpadDistrict(userProfile.district)
    )

    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)

class OpenCasesViewSet(viewsets.ModelViewSet):
  http_method_names = ['get']
  serializer_class = ComplaintSerializer
  queryset = Complaint.objects.filter(closedate_isnull=True)

  def list(self, request):
    # Get only the open complaints from the user's district
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    openCases = self.queryset.filter(
        account_exact = updatedpadDistrict(userProfile.district)
    )

    serializer = ComplaintSerializer(openCases, many=True)
    return Response(serializer.data)


class ClosedCasesViewSet(viewsets.ModelViewSet):
  http_method_names = ['get']
  serializer_class = ComplaintSerializer
  queryset = Complaint.objects.filter(closedate_isnull=False)

  def list(self, request):
    # Get only complaints that are close from the user's district
    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    complaints = self.queryset.exclude(closedate=None)
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)



class TopComplaintTypeViewSet(viewsets.ModelViewSet):
  http_method_names = ['get']

  def list(self, request):
      complaintsSearchset = ComplaintDataset(request)
    # Get the top 3 complaint types from the user's district
    top_complaints = complaintsSearchset.values('complaint_type').annotate(count=Count('complaint_type')).order_by('-count')[:3]

    print(type(top_complaints))
    for in in top_complaints:
        print(i)
    return Response(top_complaints)

## Create new endpoint and viewset that should return all complaints that were made by constituents that live in the logged in council member’s district. (i.e., John Doe is the Council Member for District 1, and he clicks on the new button. His dashboard table now only shows complaints where conucil_dist is NYCC01).##

class ConstituentComplaintViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.exclude(council_dist_isnull=True).exclude(council_dist='')

    def list(self, request):

    user = request.user
    userProfile = UserProfile.objects.get(user=user)
    constituentsComplaints = self.queryset.filter (council_dist=updatedpadDistrict(userProfile.district))

    serializer = ComplaintSerializer(constituentsComplaints, many=True)
    return Response(serializer.data)
