from django.db import models
from django.contrib.auth.models import User


## Important things to know about the data
## The fields account and council_dist both refer to a council district. However, account refers to the district in which the complaint is being made, and council_dist refers to the district in which the person who is making the complaint lives. (i.e., John Doe is the Council Member for District 1, if a noise complaint labels account as NYCC01 and council_dist as NYCC34, that means the complaint is being made in his district 1, by a person who lives in district 34).
## All of the data are string data types except for the open and close dates. In addition, the data is NOT entirely clean; some fields will be empty strings or NULL.
## Single digit districts numbers are padded by a zero in the Complaint table, BUT single digit district numbers in the UserProfile table are NOT padded by a zero. You will need to take this into consideration when writing your code.


# Create your models here.
class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  full_name = models.CharField(max_length=150, blank=True, default="")
  district = models.CharField(max_length=5, blank=True, default="")
  party = models.CharField(max_length=50, blank=True, default="", null=True)
  borough = models.CharField(max_length=50, blank=True, default="")

  def __str__(self):
    return str(self.user)

class Complaint(models.Model):
  unique_key = models.CharField(max_length=150, blank=True, default="")
  account = models.CharField(max_length=10, blank=True, default="", null=True)
  opendate = models.DateField(blank=True, null=True)
  complaint_type = models.CharField(max_length=150, blank=True, default="", null=True)
  descriptor = models.CharField(max_length=150, blank=True, default="", null=True)
  zip = models.CharField(max_length=5, blank=True, default="", null=True)
  borough = models.CharField(max_length=50, blank=True, default="", null=True)
  city = models.CharField(max_length=50, blank=True, default="", null=True)
  council_dist = models.CharField(max_length=10, blank=True, default="", null=True)
  community_board = models.CharField(max_length=150, blank=True, default="", null=True)
  closedate = models.DateField(blank=True, null=True)

  def __str__(self):
    return str(self.unique_key)
