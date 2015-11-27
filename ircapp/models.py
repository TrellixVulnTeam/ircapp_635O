from django.db import models


class Download_History(models.Model):
	filename = models.CharField(max_length=200)
	status = models.CharField(max_length=200)
	average = models.IntegerField(null=True)
	duration = models.DurationField(null=True)
	attempts = models.IntegerField(default=1)
	time = models.DateTimeField(null=True)
	sizeraw = models.IntegerField(null=True)
	
class Download_Queue(models.Model):
	title = models.CharField(max_length=200)
	sizeraw = models.IntegerField(null=True)
	network = models.CharField(max_length=200)
	channel = models.CharField(max_length=200)
	username= models.CharField(max_length=200)
	number = models.IntegerField(null=True)

class Resume_Backup(models.Model):
	title = models.CharField(max_length=200)
	sizeraw = models.IntegerField(null=True)
	network = models.CharField(max_length=200)
	channel = models.CharField(max_length=200)
	username= models.CharField(max_length=200)
	number = models.IntegerField(null=True)
	attempts = models.IntegerField(null=True)
	
class Download_Ongoing(models.Model):
	filename = models.CharField(max_length=200)
	status = models.CharField(max_length=200)
	speed = models.IntegerField(null=True)
	progress = models.IntegerField(null=True)
	completed = models.IntegerField(null=True)
	sizeraw = models.IntegerField(null=True)
	eta = models.DateTimeField(null=True)
	timeleft = models.IntegerField(null=True)
	active = models.BooleanField(default=True)	
	
class Download_Settings(models.Model):
	download_box = models.BooleanField(default=True)
	shutdown = models.BooleanField(default=False)
	
class Download_Path(models.Model):
	download_path = models.CharField(max_length=200)
	
class Quick_Download(models.Model):
    priority_choices = (
        ('MAXI', 'Maximum (BluRay)'),
        ('EXCE', 'Excellent (1080p)'),
        ('GOOD', 'Good (720p)'),
        ('NORM', 'Normal'),
    )
    priority = models.CharField('Prioritize', max_length=4, choices=priority_choices, default='NORM')
    
class Quick_Download_Contains(models.Model):
    contains = models.CharField(max_length=200)

class Quick_Download_Excludes(models.Model):
    excludes = models.CharField(max_length=200)  
    
    
    
    
    
