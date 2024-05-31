from django.db import models

class Redditdatabase(models.Model):
     redditlink=models.TextField()
     wordcloud=models.TextField()
     emotiongraph=models.TextField()
     bargraph=models.TextField()