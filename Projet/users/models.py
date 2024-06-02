from django.contrib.auth.models import AbstractUser 
from django.db import models

from users.managers import CustomUserManager
#import pycountry


# Create your models here.
class CustomUser(AbstractUser):
    nom = models.CharField(max_length=50, null=False)
    prenom = models.CharField(max_length=60)
    organisation = models.CharField(max_length=50)
    #pays_choices = [(country.alpha_2, country.name) for country in pycountry.countries]
    pays = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField(unique=True)
    motDePasse = models.CharField(max_length=50)
    password_conf = models.CharField(max_length=50, default='')
    username = None

    objects = CustomUserManager()


    USERNAME_FIELD = 'email'  # Identifiant principal de l'utilisateur
    EMAIL_FIELD = 'email'  # Champ de l'adresse email
    REQUIRED_FIELDS = ['nom', 'prenom', 'organisation']  # Champs requis lors de la création d'un superutilisateur
    
    def __str__(self):
        return self.email
    