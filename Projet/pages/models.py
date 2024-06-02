from django.db import models
import pycountry
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser 
# Create your models here.
class Evénement(models.Model):
   x=[
      ('Séminaire' , 'Séminaire' ),
      ('Stand' , 'Stand'),
      ('Symposium' ,'Symposium'),
      ('Colloque' , 'Colloque'),
      ('Congrès' , 'Congrès') ,
     ( 'Convention', 'Convention'),
      ('Atelier' ,'Atelier'),
      ('Journée détude', 'Journée détude'),
      ('Conférence', 'Conférence'),
   ]

   nom_evnt=models.CharField(max_length=30,null=False)
   acronym=models.CharField(max_length=30)
   type=models.CharField(max_length=30,null=True,blank=True,choices=x)
   date_debut_evnt=models.DateField(max_length=30, null=True, blank=True)
   date_fin_evnt=models.DateField(max_length=30, null=True, blank=True)
   description =models.CharField(max_length=100, default='')
   pays_choices = [(country.alpha_2, country.name) for country in pycountry.countries]
   pays = models.CharField(max_length=40, null=True, blank=True )
   ville = models.CharField(max_length=40 , null=True, blank=True)
   addresse = models.CharField(max_length=40,default='')
   date_debut_soumission=models.DateField(null=True, blank=True)
   heure_debut_soumission=models.TimeField(null=True, blank=True)
   date_fin_soumission=models.DateField(null=True, blank=True)
   heure_fin_soumission=models.TimeField(null=True, blank=True)
   date_debut_enchere=models.DateField(null=True, blank=True)
   heure_debut_enchere=models.TimeField(null=True, blank=True)
   date_fin_enchere=models.DateField(null=True, blank=True)
   heure_fin_enchere=models.TimeField(null=True, blank=True)

   def __str__(self):
      return self.nom_evnt

class participation(models.Model):
   organisateur=models.BooleanField(default=False)
   evaluateur=models.BooleanField(default=False)
   auteur=models.BooleanField(default=False)
   speaker=models.BooleanField(default=False)
   editeur=models.BooleanField(default=False)  
   evenement=models.ForeignKey(Evénement, on_delete=models.CASCADE)
   user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class soumission(models.Model):
   titre=models.CharField(max_length=3000,null=False)
   resume=models.TextField(max_length=6000)
   status=models.BooleanField(default=False)
   accept=models.BooleanField(default=False)
   contrat=models.FileField(upload_to='documents/', verbose_name='Article')
   attestation=models.FileField(upload_to='documents/', verbose_name='Attestation')
   prestation=models.FileField(upload_to='documents/', verbose_name='Presentation')
   evenement=models.ForeignKey(Evénement, on_delete=models.CASCADE , null=True)
   user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   camera_ready_pdf = models.FileField(upload_to='documents/', verbose_name='Camera ready PDF',null=True)
   camera_ready_zip = models.FileField(upload_to='documents/', verbose_name='Camera ready ZIP', blank=True, null=True)
   
   def __str__(self):
      return self.titre

class CoAuteur(models.Model):
   email_co_auteur=models.EmailField()
   nom_coauteur=models.CharField(max_length=30,null=True)
   prenom_coauteur=models.CharField(max_length=30 ,null=True)
   soumission=models.ForeignKey(soumission, on_delete=models.CASCADE)

   def __str__(self):
      return self.email_co_auteur

class Evaluation(models.Model):

   d=[
      ('Rejet catégorique' , 'Rejet catégorique' ),
      ('Rejet' , 'Rejet' ),
      ('Rejet modéré' , 'Rejet modéré'),
      ('Neutre' , 'Neutre' ),
      ('Acceptation modérée ' ,'Acceptation modérée'),
      ('Acceptation' , 'Acceptation'),
      ('Acceptation catégorique ' , 'Acceptation catégorique') ,
   ]

   commentaire=models.TextField(max_length=5000)
   commentaire_confidentiel=models.TextField(max_length=5000,null=True)
   maitrise = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
   note=models.CharField(max_length=30,null=True,blank=True,choices=d)
   user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   soumission=models.ForeignKey(soumission, on_delete=models.CASCADE ,null=True)


class Invitation(models.Model):
   o=[
     ('evaluateur','evaluateur'),
     ('speaker', 'speaker'),
      ('editeur', 'editeur'),
        ]
   email_invitation=models.CharField(max_length=30, null=True,blank=True)
   user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   evenement=models.ForeignKey(Evénement, on_delete=models.CASCADE,null=True)
   role=models.CharField(max_length=30,null=True,blank=True,choices=o)
   accepted=models.BooleanField(default=False)


class Affectation(models.Model):
   user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   soumission=models.ForeignKey(soumission, on_delete=models.CASCADE)


class Encheres(models.Model):
  e=[
     ('Je peux','Je peux'),
     ('Peut etre', 'Peut etre'),
     ('Je ne peux pas', 'Je ne peux pas'),
      ('Conflit', 'Conflit'),
    ]
  user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  soumission=models.ForeignKey(soumission, on_delete=models.CASCADE)
  enthousiasme=models.CharField(max_length=30,null=True,blank=True,choices=e)


class Presentation(models.Model):
   user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   titre_pres=models.CharField(max_length=90)
   affiliation_pres=models.CharField(max_length=90)
   biographie_pres=models.CharField(max_length=90)
   evenement=models.ForeignKey(Evénement, on_delete=models.CASCADE,null=True)

class Guide(models.Model):
   user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   guide_soumission=models.CharField(max_length=150)
   evenement=models.ForeignKey(Evénement, on_delete=models.CASCADE,null=True)
