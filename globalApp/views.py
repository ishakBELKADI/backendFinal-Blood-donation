import datetime
import json
from time import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from globalApp.models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import logout


# Create your views here.
def custom_logout_view(request):
    request.method = 'POST'
    print("azdem")
    logout(request)
    return redirect('/')

@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        
     user= json.loads(request.body)
     print(user)
     try:
         usercreated= Utilisateur.objects.create(
         nom = user["nom"],
         prenom = user["prenom"],
         numtel = user["numtel"],
         groupSanguin= user["groupSanguin"],
         willaya = user["willaya"],
         daira = user["daira"],
         email = user["email"].lower(), 
       )
     except Exception as e :
         print(str(e))
         return JsonResponse({"message" : "erreur : " + str(e)})

     return JsonResponse({"message" : "utilisateur crée" })
    return JsonResponse(  {"messsage " : "Objet non  créé reqete get"} )


def getUser(request , email):
    if email == "":
        return JsonResponse({'error': 'Paramètre email manquant'}, status=400)
    else:
        utilisateur = Utilisateur.objects.get(email = email)
        print(utilisateur)
        user_data = {
                'id': utilisateur.id,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                'email': utilisateur.email,
                'numtel': utilisateur.numtel,
                'groupSanguin': utilisateur.groupSanguin,
                'willaya': utilisateur.willaya,
                'daira': utilisateur.daira,
            }
        return JsonResponse(user_data)
    
@csrf_exempt
def ajouterDonneur(request):
    if request.method == 'POST':
     user= json.loads(request.body)
     print(user["utilisateur"])
     usercreated = None
     try:
         usercreated= Utilisateur.objects.create(
         nom = user["utilisateur"]["nom"],
         prenom = user["utilisateur"]["prenom"],
         numtel = user["utilisateur"]["numtel"],
         groupSanguin= user["utilisateur"]["groupSanguin"],
         willaya = user["utilisateur"]["willaya"],
         daira = user["utilisateur"]["daira"],
         email = user["utilisateur"]["email"], 
       )
        #  usercreated.save()
         donneur = Donneur.objects.create(
             utilisateur = usercreated,
             statu = "Apte"
         )
         print(donneur)
     except Exception as e :
         print(str(e))
         return JsonResponse({"message" : "erreur : " + str(e)})

     return JsonResponse({"message" : "Donneur crée" })
    return JsonResponse(  {"messsage " : "Objet non  créé reqete get"} )

@csrf_exempt
def update_utilisateur(request, utilisateur_id):
    utilisateur = get_object_or_404(Utilisateur, pk=utilisateur_id)

    if request.method == 'PUT':
        utilisateurUpdated = json.loads(request.body)
        nom = utilisateurUpdated['nom']
        prenom = utilisateurUpdated['prenom']
        email = utilisateurUpdated['email'].lower()
        numtel = utilisateurUpdated['numtel']
        groupSanguin = utilisateurUpdated['groupSanguin']
        willaya = utilisateurUpdated['willaya']
        daira = utilisateurUpdated['daira']

        # Mettre à jour les champs de l'utilisateur
        utilisateur.nom = nom
        utilisateur.prenom = prenom
        # utilisateur.email = email
        utilisateur.numtel = numtel
        utilisateur.groupSanguin = groupSanguin
        utilisateur.willaya = willaya
        utilisateur.daira = daira

        # Enregistrer les modifications dans la base de données
        utilisateur.save()

        return JsonResponse({'success': 'Utilisateur mis à jour avec succès'})
    
    # Renvoyer les détails de l'utilisateur
    user_data = {
        'nom': utilisateur.nom,
        'prenom': utilisateur.prenom,
        'email': utilisateur.email,
        'numtel': utilisateur.numtel,
        'groupSanguin': utilisateur.groupSanguin,
        'willaya': utilisateur.willaya,
        'daira': utilisateur.daira,
    }
    return JsonResponse(user_data)

@csrf_exempt
def createAnounce(request , pk):
    if request.method == 'POST':
        try:
            
          info= json.loads(request.body)
          utilisateur = Utilisateur.objects.get(id = pk)
          date_objet = timezone.datetime.strptime(info["date_de_Don_max"], '%Y-%m-%dT%H:%M:%S.%f')
          date_aware = timezone.make_aware(date_objet)
          annonce = Annonce.objects.create(
            utilisateur = utilisateur,
            description = info["description"],
            groupSanguin=info["groupSanguin"],
            place=info["place"],
            type_de_don = info["type_de_don"],
            latitude = info["latitude"],
            longitude = info["longitude"],
            date_de_Don_max= date_aware,
            numerotelephone= info["numerotelephone"]
              )
          return JsonResponse({"message" : "annonce creé"})
        except Exception as e :
         print(str(e))
         return JsonResponse({"message :" : "erreur : " + str(e)}) 
    return JsonResponse({"message :" , "methode doit etre POST"})   
    

def recuperToutLesAnnonces(request , pk):
    annonces = Annonce.objects.all().order_by('-date_de_publication')
    user = Utilisateur.objects.get(id = pk)

    # Sérialiser les annonces en format JSON
    data = []
    for annonce in annonces:
        utilisateur = Utilisateur.objects.get(id = annonce.utilisateur.id)
        
        user_data = {
                'id': utilisateur.id,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                'email': utilisateur.email,
                'numtel': utilisateur.numtel,
                'groupSanguin': utilisateur.groupSanguin,
                'willaya': utilisateur.willaya,
                'daira': utilisateur.daira,
            }
        try:
             demande = Demande.objects.get(
             Q(utilisateur_src=utilisateur, utilisateur_dest=user) | 
             Q(utilisateur_src=user, utilisateur_dest=utilisateur)
                )
             data.append({
            'id':annonce.id,
            'utilisateur': user_data,
            'description': annonce.description,
            'groupSanguin': annonce.groupSanguin,
            'place': annonce.place,
            'date_de_publication': annonce.date_de_publication.isoformat(),
            'latitude' : annonce.latitude,
            'longitude': annonce.longitude,
            'date_de_Don_max': annonce.date_de_Don_max.isoformat() if annonce.date_de_Don_max else None,
            'numerotelephone': annonce.numerotelephone,
            'type_de_don' : annonce.type_de_don,
            'date_de_modification': annonce.date_de_modification.isoformat() if annonce.date_de_modification else None,
            'etat_demande' : demande.etat_demande
        })
        except Demande.DoesNotExist:
            data.append({
            'id':annonce.id,
            'utilisateur': user_data,
            'description': annonce.description,
            'groupSanguin': annonce.groupSanguin,
            'place': annonce.place,
            'latitude' : annonce.latitude,
            'longitude': annonce.longitude,
            'date_de_publication': annonce.date_de_publication.isoformat(),
            'date_de_Don_max': annonce.date_de_Don_max.isoformat() if annonce.date_de_Don_max else None,
            'numerotelephone': annonce.numerotelephone,
            'type_de_don':annonce.type_de_don,
            'date_de_modification': annonce.date_de_modification.isoformat() if annonce.date_de_modification else None,
            'etat_demande' : 'null'
               })        
    return JsonResponse(data, safe=False)


def recupererAnnoncesUser(request , pk):
    annonces = Annonce.objects.filter(utilisateur = Utilisateur.objects.get(id = pk))
    if annonces.exists():
            data = []
            for annonce in annonces:
                utilisateur = Utilisateur.objects.get(id = annonce.utilisateur.id)
                user_data = {
                'id': utilisateur.id,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                'email': utilisateur.email,
                'numtel': utilisateur.numtel,
                'groupSanguin': utilisateur.groupSanguin,
                'willaya': utilisateur.willaya,
                'daira': utilisateur.daira,
                   }     
                data.append({
                            'id': annonce.id,
                             'utilisateur': user_data,
                              'description': annonce.description,
                              'groupSanguin': annonce.groupSanguin,
                              'place': annonce.place,
                                'latitude' : annonce.latitude,
                                'longitude': annonce.longitude,
                                'type_de_don':annonce.type_de_don,
                                'date_de_publication': annonce.date_de_publication.isoformat(),
                                'date_de_Don_max': annonce.date_de_Don_max.isoformat() if annonce.date_de_Don_max else None,
                                'numerotelephone': annonce.numerotelephone,
                                'date_de_modification': annonce.date_de_modification.isoformat() if annonce.date_de_modification else None,
                                      })
            return JsonResponse(data , safe=False)
    else:
        return JsonResponse({"message":"Vous avez publier aucune annonce"})

        
@csrf_exempt
def supprimerAnnounce(request , pk):
    if request.method == 'DELETE':
        try :
            annonce = Annonce.objects.get(id = pk)
            annonce.delete()
            return JsonResponse({"message" : "annonce supprimé"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"message" : "erreur : " + str(e)}) 
    return JsonResponse({"message" : "requete non DELETE"})

@csrf_exempt
def modifierAnnounce(request , pk):
    if request.method == 'PUT':
        try :
            annonce = Annonce.objects.get(id = pk)
            annonce_updated = json.loads(request.body)
            print(annonce_updated['groupSanguin'])
            description = annonce_updated['description']
            group_sanguin = annonce_updated['groupSanguin']
            place = annonce_updated['place']
            date_de_don_max = annonce_updated['date_de_Don_max']
            numerotelephone = annonce_updated['numerotelephone']
    # date_de_modification = annonce_updated['date_de_modification']  # Si nécessaire

    # Mettre à jour les champs de l'annonce
            annonce.description = description
            annonce.groupSanguin = group_sanguin
            annonce.place = place
            annonce.date_de_Don_max = date_de_don_max
            annonce.numerotelephone = numerotelephone
            annonce.save()
            return JsonResponse({"message":"annonce mets a jour"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"message" : "erreur : " + str(e)})
    return JsonResponse({"message" : "requete doit etre PUT"})
    
            
            
        

@csrf_exempt
def signalerProbelem(request):
  if request.method == 'POST':
      data = json.loads(request.body)
      utilisateur = Utilisateur.objects.get(id = data["id"])
      probleme = Problems.objects.create(
        problem = data["problem"],
        utilisateur_src = utilisateur
       )
      return JsonResponse({"message" : "probleme signalé"})
  return JsonResponse({"message" : "requete doit etre post"})
   
@csrf_exempt   
def createDemande(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        utilisateurSrc =Utilisateur.objects.get(id = data['utilisateur_src']['id'])
        utilisateurDest = Utilisateur.objects.get(id = data["utilisateur_dest"] )
        demande = Demande.objects.create(
            utilisateur_dest = utilisateurDest,
            utilisateur_src = utilisateurSrc,
            type_demande= data["type_demande"],
            etat_demande = data["etat_demande"]
         )
        return JsonResponse({"message" : "Demande crée"})
        
    
    return request

@csrf_exempt   
def modifierEtatDemande(request , pkU , pkD):
    demande = get_object_or_404(
    Demande, 
    (Q(utilisateur_src_id=pkD, utilisateur_dest_id=pkU) | 
     Q(utilisateur_src_id=pkU, utilisateur_dest_id=pkD))
             )   
    data = json.loads(request.body)
    demande.etat_demande = data['etat_demande']
    demande.save()
    return JsonResponse({"message" : "etat Demande modifié"})

def recupererDonneurs(request):
    donneurs = Donneur.objects.all()
    if donneurs.exists():
            data = []
            for donneur in donneurs:
             utilisateur = Utilisateur.objects.get(id = donneur.utilisateur.id)
             user_data = {
                'id': utilisateur.id,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                'email': utilisateur.email,
                'numtel': utilisateur.numtel,
                'groupSanguin': utilisateur.groupSanguin,
                'willaya': utilisateur.willaya,
                'daira': utilisateur.daira,
             }
             data.append({
             'id':donneur.id,
             'utilisateur': user_data,
              'statu' : donneur.statu,
             'date_dernier_don' : donneur.date_dernier_don
               })
            return JsonResponse(data , safe=False)
    else:
        return JsonResponse({"message" : "pas de donneurs"})
    
    
@csrf_exempt
def recupererDonneursUserState(request, pk):
    donneurs = Donneur.objects.all()
    try:
        user = Utilisateur.objects.get(id=pk)
    except Utilisateur.DoesNotExist:
        return JsonResponse({"message": "Utilisateur introuvable"}, status=404)

    if donneurs.exists():
        data = []
        for donneur in donneurs:
            try:
                utilisateur = Utilisateur.objects.get(id=donneur.utilisateur.id)
            except Utilisateur.DoesNotExist:
                continue  # Skip this donor if the user does not exist

            user_data = {
                'id': utilisateur.id,
                'nom': utilisateur.nom,
                'prenom': utilisateur.prenom,
                'email': utilisateur.email,
                'numtel': utilisateur.numtel,
                'groupSanguin': utilisateur.groupSanguin,
                'willaya': utilisateur.willaya,
                'daira': utilisateur.daira,
            }

            try:
                demande = Demande.objects.filter(
                    Q(utilisateur_src=utilisateur, utilisateur_dest=user) | 
                    Q(utilisateur_src=user, utilisateur_dest=utilisateur)
                ).first()  # Get the first matching Demande or None
            except Demande.DoesNotExist:
                demande = None

            if demande:
                data.append({
                    'id': donneur.id,
                    'utilisateur': user_data,
                    'statu': donneur.statu,
                    'date_dernier_don': donneur.date_dernier_don,
                    'etat_demande': demande.etat_demande
                })
            else:
                data.append({
                    'id': donneur.id,
                    'utilisateur': user_data,
                    'statu': donneur.statu,
                    'date_dernier_don': donneur.date_dernier_don,
                    'etat_demande': 'null'
                })

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"message": "Pas de donneurs"}, status=404)    
    

def recupererDemande(request , pk):
    if request.method == 'GET':
        utilisateur = Utilisateur.objects.get(id = pk)
        demandesReçu = Demande.objects.filter(utilisateur_dest=utilisateur).exclude(etat_demande='Annulé').exclude(etat_demande='Accepté')
        globale = [{'Envoye' : [] } , {'Reçu' : []}]
        for demande in demandesReçu:
             user_data = {
                'id': demande.utilisateur_src.id,
                'nom': demande.utilisateur_src.nom,
                'prenom': demande.utilisateur_src.prenom,
                'email': demande.utilisateur_src.email,
                'numtel': demande.utilisateur_src.numtel,
                'groupSanguin': demande.utilisateur_src.groupSanguin,
                'willaya': demande.utilisateur_src.willaya,
                'daira': demande.utilisateur_src.daira,
               }

             demande_data = {
                'utilisateur_src': user_data,
                'date_de_demande': demande.date_de_demande.strftime('%Y-%m-%d %H:%M:%S'),
                'type_demande': demande.type_demande,
                'etat_demande': demande.etat_demande,
              }
             globale[1]['Reçu'].append(demande_data)
        demandesEnvoyé = Demande.objects.filter(utilisateur_src = utilisateur).exclude(etat_demande='Annulé').exclude(etat_demande='Accepté')
        for demande in demandesEnvoyé:
             user_data = {
                'id': demande.utilisateur_dest.id,
                'nom': demande.utilisateur_dest.nom,
                'prenom': demande.utilisateur_dest.prenom,
                'email': demande.utilisateur_dest.email,
                'numtel': demande.utilisateur_dest.numtel,
                'groupSanguin': demande.utilisateur_dest.groupSanguin,
                'willaya': demande.utilisateur_dest.willaya,
                'daira': demande.utilisateur_dest.daira,
               }

             demande_data = {
                'utilisateur_dest': user_data,
                'date_de_demande': demande.date_de_demande.strftime('%Y-%m-%d %H:%M:%S'),
                'type_demande': demande.type_demande,
                'etat_demande': demande.etat_demande,
              }
             globale[0]['Envoye'].append(demande_data)
        return JsonResponse(globale , safe= False)
             


@csrf_exempt
def creeDon(request):
    if request.method == 'POST':
        try:
          data = json.loads(request.body)
          date_objet = timezone.datetime.strptime(data["date_de_don"], '%Y-%m-%dT%H:%M:%S.%f')
          date_aware = timezone.make_aware(date_objet)
          donor = None
          donneurs = Donneur.objects.filter(utilisateur__id=data["donneur"]["utilisateur"]["id"]) 
          if donneurs.exists() == False:
             donneur = Donneur.objects.create(
                  utilisateur = Utilisateur.objects.get(id = data["donneur"]["utilisateur"]["id"]),
                  statu='Apte',
                  date_dernier_don = date_aware
                   )
             donor
          else:
              donor = donneurs.first()  
          don = EffectueDon.objects.create(
          donneur = donor,
          date_de_don =date_aware,
          type_de_don = data["type_de_don"],
          quantité = data["quantite"])
          return JsonResponse({"message" : "Un Don est crée et a été effectué"})
        except Exception as e:
            print(str(e))
            return JsonResponse({"message" : "erreur : " + str(e)})
        
def recupererDonUser(request , pk):
    try:
        
      donneur = Donneur.objects.get(utilisateur__id=pk) 
      dons = EffectueDon.objects.filter(donneur = donneur)
      if dons.exists():
           data = []
           for don in dons :
              don_data = {
              'id' : donneur.id,
              'date_de_don': don.date_de_don.strftime('%Y-%m-%d %H:%M:%S'),
              'type_de_don' : don.type_de_don,
              'quantité' : don.quantité
                }
              data.append(don_data)
           return JsonResponse(data , safe=False)
      return JsonResponse({"message" : "vous avez effectué aucun don"})
    except Donneur.DoesNotExist:
        return JsonResponse({"message" : "VOUS-Netes pas donneur"})
        
  
def recupererAllUsers(request):
    utilisateurs = Utilisateur.objects.all()
    data = []
    for utilisateur in utilisateurs:
        user = {
            'id' : utilisateur.id,
            'nom' : utilisateur.nom,
            'prenom' : utilisateur.prenom,
            'groupSanguin' : utilisateur.groupSanguin,
            'email' : utilisateur.email,
            'numtel' : utilisateur.numtel,
         }
        data.append(user)
    return JsonResponse(data , safe=False)

@csrf_exempt
def createToken(request ):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
         utilisateur = Utilisateur.objects.get(id = data["utilisateur"]["id"])
         token = Tokens.objects.create(
         token = data['token'],
         utilisateur =  utilisateur
          )
         return JsonResponse({"message" : "token enregistré"})
        except Exception as e :
            return JsonResponse({"message" : "erreur "+ str(e)})
        
def recupereTokenUser(reqeust , pk):
    tokens = Tokens.objects.filter(utilisateur__id = pk)
    data = []
    for token in tokens :
        data.append({
            'token' : token.token,
        })
    return JsonResponse(data , safe=False)

@csrf_exempt
def deleteDon(request , pk  , date ):
    if request.method == 'DELETE':
        try:
           date_objet = timezone.datetime.strptime(date,  '%Y-%m-%d %H:%M:%S')
           date_aware = timezone.make_aware(date_objet)
           EffectueDon.objects.filter(donneur__utilisateur_id=pk, date_de_don=date_aware).delete()
           return JsonResponse({"message":"Don supprimé"})
        except Exception as e :
            return JsonResponse({"message" : "error " + str(e)})
    

def demandesAccepter(request, pk):
    if request.method == 'GET':
        demandes = Demande.objects.filter(Q(utilisateur_src__id=pk) | Q(utilisateur_dest__id=pk) , etat_demande='Accepté')        
        pk = int(pk)
        data = []
        print(demandes)
        for demande in demandes:
            if demande.utilisateur_src.id == pk:
                user_data = {
                'id': demande.utilisateur_dest.id,
                'nom': demande.utilisateur_dest.nom,
                'prenom': demande.utilisateur_dest.prenom,
                'email': demande.utilisateur_dest.email,
                'numtel': demande.utilisateur_dest.numtel,
                'groupSanguin': demande.utilisateur_dest.groupSanguin,
                'willaya': demande.utilisateur_dest.willaya,
                'daira': demande.utilisateur_dest.daira,
               }
            else :
                user_data = {
                'id': demande.utilisateur_src.id,
                'nom': demande.utilisateur_src.nom,
                'prenom': demande.utilisateur_src.prenom,
                'email': demande.utilisateur_src.email,
                'numtel': demande.utilisateur_src.numtel,
                'groupSanguin': demande.utilisateur_src.groupSanguin,
                'willaya': demande.utilisateur_src.willaya,
                'daira': demande.utilisateur_src.daira,
               }
            demande_data = {
                'utilisateur_dest': user_data,
                'date_de_demande': demande.date_de_demande.strftime('%Y-%m-%d %H:%M:%S'),
                'type_demande': demande.type_demande,
                'etat_demande': demande.etat_demande,
            }
            data.append(demande_data)
        print(data)
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def changeretatdonneur(request , pk):
  if request.method == 'PUT':
      
     donneur = Donneur.objects.get(utilisateur__id = pk)
     if donneur.statu == 'Apte':
        donneur.statu = 'inapte'
     else: donneur.statu='Apte'
     donneur.save()
     return JsonResponse({"message" : "Statu changé"})
 
def getstatu(request , pk):
    try :
        donneur = Donneur.objects.get(utilisateur__id = pk)
        return JsonResponse({"message" : donneur.statu})
    except Donneur.DoesNotExist:
        return JsonResponse({"message" : "non donneur"})

@csrf_exempt
def supprimerDemande(request, pk1, pk2):
    if request.method == 'DELETE':
        try:
            demande = Demande.objects.get(
                Q(utilisateur_src_id=pk1, utilisateur_dest_id=pk2) | 
                Q(utilisateur_src_id=pk2, utilisateur_dest_id=pk1)
            )
            demande.delete()
            return JsonResponse({"message": "Demande supprimée"})
        except Demande.DoesNotExist:
            return JsonResponse({"message": "Demande introuvable"}, status=404)
    else:
        return JsonResponse({"message": "Méthode non autorisée"}, status=405)
     
    
  
                    
    

        
        
    
    
        

    

            

        
            
        

        
        
        

    

    

