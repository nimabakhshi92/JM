from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import pyodbc
import pandas as pd
import numpy as np
import json

# DESKTOP-EO1NKE0
# HYPERSIGNAL\SQLEXPRESS
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-EO1NKE0;'
                      'Database=JanatolMava;'
                      'UID=MYLOGIN;'
                      'PWD=MYLOGIN;'
                      'Trusted_Connection=yes;')
