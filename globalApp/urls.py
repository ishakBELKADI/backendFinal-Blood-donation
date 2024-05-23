from . import views
from django.urls import path 

urlpatterns = [
path('createUser/' , views.createUser),
path('ajouterDonneur/' , views.ajouterDonneur),
path('getUser/<str:email>' , views.getUser),
path('updaterUser/<str:utilisateur_id>' , views.update_utilisateur),
path('createAnounce/<str:pk>' , views.createAnounce),
path('updateAnnounce/<str:pk>' , views.modifierAnnounce),
path('deleteAnnonce/<str:pk>' , views.supprimerAnnounce),
path('getAllAnnounces/<str:pk>' , views.recuperToutLesAnnonces),
path('getAllAnnouncesUser/<str:pk>' , views.recupererAnnoncesUser),
path('SignalerProbleme/' , views.signalerProbelem),
path('recupererDonneurs/' , views.recupererDonneurs),
path('recupererDemande/<str:pk>' , views.recupererDemande),
path('recupererDonneursUserState/<str:pk>' , views.recupererDonneursUserState),
path('createDemande/' , views.createDemande),
path('modifierEtatDemande/<str:pkU>/<str:pkD>' , views.modifierEtatDemande),
path('creeDon/' , views.creeDon),
path('recupererDonUser/<str:pk>' , views.recupererDonUser),
path('recupererAllUsers/' , views.recupererAllUsers),
path('createToken/' , views.createToken),
path('recupereTokenUser/<str:pk>' , views.recupereTokenUser),
path('deleteDon/<str:pk>/<str:date>' , views.deleteDon),
path('demandesAccepter/<str:pk>' , views.demandesAccepter),






















    # <str:pk> means pk est un string
]  
    
