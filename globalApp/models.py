from django.db import models

# Create your models here.

class Utilisateur(models.Model):
    nom = models.CharField(max_length=20)
    prenom = models.CharField(max_length=20)
    email = models.EmailField(unique=True , default='') 
    numtel = models.IntegerField()
    groupSanguin= models.CharField(max_length=2)
    willaya = models.CharField(max_length=20)
    daira = models.CharField(max_length=20)
        

class Donneur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur , on_delete=models.CASCADE, related_name='est_utilisateur')
    statu = models.CharField(max_length=8)
    date_dernier_don = models.DateField( null= True)



class Annonce(models.Model):
    utilisateur = models.ForeignKey(Utilisateur , on_delete=models.CASCADE, related_name='cree_annonce')
    description = models.CharField(max_length=100 , null=True )
    groupSanguin= models.CharField(max_length=2)
    place = models.CharField(max_length=30 , null=True)
    date_de_publication = models.DateTimeField(auto_now_add= True)
    date_de_Don_max = models.DateTimeField(null=True)
    numerotelephone= models.IntegerField(null=True)
    date_de_modification= models.DateTimeField(auto_now= True , null= True)
    type_de_don = models.CharField(max_length= 20 , null=True)

class Notification(models.Model):
    type_de_notif = models.CharField(max_length=15)
    titre = models.CharField(max_length=15)
    contenue = models.CharField(max_length=50)

class EffectueDon(models.Model):
    donneur = models.ForeignKey(Donneur , on_delete=models.CASCADE , related_name="effectue")
    date_de_don = models.DateField( null= False)
    type_de_don = models.CharField(max_length=15)
    quantité = models.IntegerField(null= True)
    def __str__(self):
      return f"{self.donneur.utilisateur.nom}-{self.donneur.utilisateur.prenom}-{self.date_de_don}"
    class Meta:
        unique_together = ['donneur', 'date_de_don']

class Demande(models.Model):
    utilisateur_dest = models.ForeignKey(Utilisateur , on_delete=models.CASCADE , related_name='recepteur' , default=None)
    date_de_demande = models.DateTimeField(auto_now_add= True)
    utilisateur_src = models.ForeignKey(Utilisateur ,on_delete=models.CASCADE , related_name='demandeur')
    type_demande= models.CharField(max_length=15)
    etat_demande = models.CharField(max_length=15)
    def __str__(self):
      return f"{self.utilisateur_dest.nom}-{self.utilisateur_src.nom}"
    class Meta:
        unique_together = ['utilisateur_dest', 'utilisateur_src']

class NotifEnvoyer(models.Model):
    utilisateur = models.ForeignKey(Utilisateur ,on_delete=models.CASCADE )
    notification = models.ForeignKey(Notification ,on_delete=models.CASCADE )

class Tokens(models.Model):
    token = models.CharField(max_length=100 , primary_key= True )
    utilisateur = models.ForeignKey(Utilisateur ,on_delete=models.CASCADE )

class Problems(models.Model):
    problem = models.CharField(max_length=100)
    utilisateur_src = models.ForeignKey(Utilisateur ,on_delete=models.CASCADE )

    