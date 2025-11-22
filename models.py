from django.db import models
from django.contrib.auth.models import User
import numpy as np
import pickle
import json
from PIL import Image
import joblib
import numpy as np


svm = pickle.load(open(r'C:\Users\Mothilal Chowdary\Desktop\DRUGS\FRONTEND\rf_drug.pkl', 'rb'))
xgb = pickle.load(open(r'C:\Users\Mothilal Chowdary\Desktop\DRUGS\FRONTEND\x_gb_drug.pkl', 'rb'))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

def predict(lst,algo):
	test = np.array(lst)
	test = np.reshape(test, (1, -1))
	print(test.shape)
	if algo=='svm':
		y_pred=svm.predict(test)
		return y_pred
	else:
		y_pred=xgb.predict(test)
		return y_pred