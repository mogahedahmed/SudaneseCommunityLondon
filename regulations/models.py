from django.db import models

class Regulation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class RegulationFile(models.Model):
    regulation = models.ForeignKey(Regulation, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='regulations/files/')

    def __str__(self):
        return f"ملف: {self.file.name}"
