from django.db import models
from django.utils import timezone

# Create your models here.
class Worker(models.Model):
    nombre = models.TextField()

    def __str__(self):
        return self.nombre

# --- CLIENTS ---
class Client(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class Client_data(models.Model):
    data = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1,related_name="userData")
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.created_on

# --- SCHEDULE ---
class Cita(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1, related_name="citas")
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, default=1, related_name="citas")
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.client.nombre
