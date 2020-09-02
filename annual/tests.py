from django.test import TestCase
from accounts.models import Profile, Team, Position
from commute.models import Commute
from django.utils import timezone
from datetime import *
from dateutil.relativedelta import relativedelta
from .models import AnnualDate, MinusData
# Create your tests here.

#class AnnualDateTests(TestCase):
#    def test_recent_pub(self):
