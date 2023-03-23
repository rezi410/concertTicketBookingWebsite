from django.db import models


class GoldTicket(models.Model):
    name = models.CharField(max_length=120, unique=True)
    type = models.CharField(max_length=20, default="Gold", editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    numOfTicket = models.PositiveIntegerField()
    def __str__(self) -> str:
        return self.name

class SliverTicket(models.Model):
    name = models.CharField(max_length=120, unique=True)
    type = models.CharField(max_length=20, default="Sliver" ,editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    numOfTicket = models.PositiveIntegerField()
    def __str__(self) -> str:
        return self.name

class BronzeTicket(models.Model):
    name = models.CharField(max_length=120, unique=True)
    type = models.CharField(max_length=20, default="Bronze",editable=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    numOfTicket = models.PositiveIntegerField()
    def __str__(self) -> str:
        return self.name


class Concert(models.Model):
    title = models.CharField(max_length=40, unique=True)
    goldTicket = models.ForeignKey(GoldTicket, on_delete=models.CASCADE)
    sliverTicket = models.ForeignKey(SliverTicket, on_delete=models.CASCADE)
    bronzeTicket = models.ForeignKey(BronzeTicket, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    thumb = models.ImageField(default='default.png', blank=True, upload_to='images/')
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
    list_display = ('title', 'date')
    list_filter = ('date')
    def __str__(self) -> str:
        return f"{self.title} {self.date}"