import pandas as pd
from questions.models import Business
from django_pandas.io import read_frame
import os
import django


# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btr.config.settings')
django.setup()

businesses = Business.objects.all()
df = read_frame(businesses)
print(df)