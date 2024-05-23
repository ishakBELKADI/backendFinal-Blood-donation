from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import *

class InlineDonneur(admin.StackedInline):
     model = Donneur 


class UtilisateurAdmin(admin.ModelAdmin):
    inlines = [InlineDonneur]
    search_fields = ['id' ,'nom', 'prenom', 'email', 'numtel', 'groupSanguin', 'willaya', 'daira']
    list_display = ('nom', 'prenom', 'email', 'numtel', 'groupSanguin', 'willaya', 'daira')
    readonly_fields = ['nom', 'prenom', 'email', 'numtel', 'groupSanguin', 'willaya', 'daira']
    list_filter = ('willaya' , 'groupSanguin')
    
    
class DonneurAdmin(admin.ModelAdmin):
    search_fields = ['utilisateur__nom', 'utilisateur__prenom', 'statu', 'date_dernier_don' , 'utilisateur__groupSanguin' , 'utilisateur__willaya']
    list_display = ('utilisateur_nom', 'utilisateur_prenom', 'utilisateur_groupSanguin', 'statu', 'date_dernier_don')
    list_filter = ('utilisateur__groupSanguin','utilisateur__willaya' , 'statu' )
    readonly_fields = ('utilisateur', 'date_dernier_don')
   # Il faut accéder à utilisateur__groupSanguin

    def utilisateur_nom(self, obj):
        return obj.utilisateur.nom
    utilisateur_nom.admin_order_field = 'utilisateur__nom'  # Permet de trier par nom dans l'admin
    utilisateur_nom.short_description = 'Nom'

    def utilisateur_prenom(self, obj):
        return obj.utilisateur.prenom
    utilisateur_prenom.admin_order_field = 'utilisateur__prenom'  # Permet de trier par prénom dans l'admin
    utilisateur_prenom.short_description = 'Prénom'

    def utilisateur_groupSanguin(self, obj):
        return obj.utilisateur.groupSanguin
    utilisateur_groupSanguin.admin_order_field = 'utilisateur__groupSanguin'  # Permet de trier par groupe sanguin dans l'admin
    utilisateur_groupSanguin.short_description = 'Groupe Sanguin'
    def utilisateur_willaya(self, obj):
        return obj.utilisateur.groupSanguin
    utilisateur_groupSanguin.admin_order_field = 'utilisateur__willaya'  # Permet de trier par groupe sanguin dans l'admin
    utilisateur_groupSanguin.short_description = 'willaya'

    

class AnnonceAdmin(admin.ModelAdmin):
    search_fields = ['utilisateur__nom', 'utilisateur__prenom', 'description', 'groupSanguin', 'place', 'date_de_publication', 'date_de_Don_max', 'numerotelephone', 'type_de_don']
    list_display = ('utilisateur_info', 'date_de_publication', 'type_don_et_group_sanguin', 'date_de_Don_max' ,'numerotelephone')
    list_filter = ('type_de_don','groupSanguin' ,)
    readonly_fields = ('description', 'groupSanguin', 'place' ,'date_de_Don_max', 'numerotelephone', 'type_de_don' , 'latitude' , 'longitude' , 'utilisateur')# Il faut accéder à utilisateur__groupSanguin

    def utilisateur_info(self, obj):
        return f"{obj.utilisateur.nom} {obj.utilisateur.prenom}"
    utilisateur_info.short_description = 'Utilisateur'

    def type_don_et_group_sanguin(self, obj):
        return f"Type : {obj.type_de_don}, Groupe sanguin: {obj.groupSanguin}"
    type_don_et_group_sanguin.short_description = 'Type de don et Groupe sanguin'


class EffectueDonAdmin(admin.ModelAdmin):
    list_display = ('donneur_info', 'date_de_don', 'type_de_don', 'quantité')
    search_fields = ['donneur__utilisateur__nom', 'donneur__utilisateur__prenom', 'date_de_don', 'type_de_don', 'quantité']
    list_filter = ('type_de_don',) 
    readonly_fields = ('date_de_don', 'type_de_don', 'quantité' , 'donneur')# Il faut accéder à utilisateur__groupSanguin

    def donneur_info(self, obj):
        return f"{obj.donneur.utilisateur.nom} {obj.donneur.utilisateur.prenom}"
    donneur_info.short_description = 'Nom et prenom de donneur'

    


class DemandeAdmin(admin.ModelAdmin):
    search_fields = ['utilisateur_dest__nom', 'utilisateur_src__nom', 'date_de_demande', 'type_demande', 'etat_demande']
    list_display = ('utilisateur_src_nom' , 'utilisateur_dest_nom' , 'date_de_demande' , 'etat_demande')
    list_filter = ('etat_demande',)  # Il faut accéder à utilisateur__groupSanguin
    readonly_fields = ( 'date_de_demande', 'type_demande', 'etat_demande' , 'utilisateur_src' , 'utilisateur_dest')
    def utilisateur_src_nom(self, obj):
        return obj.utilisateur_src.nom
    utilisateur_src_nom.admin_order_field = 'utilisateur_src__nom'  
    utilisateur_src_nom.short_description = 'utilisateur source'

    def utilisateur_dest_nom(self, obj):
        return obj.utilisateur_dest.nom
    utilisateur_dest_nom.admin_order_field = 'utilisateur_dest__nom' 
    utilisateur_dest_nom.short_description = 'utilisateur destination'

    



class TokensAdmin(admin.ModelAdmin):
    search_fields = ['token', 'utilisateur__nom']

class ProblemsAdmin(admin.ModelAdmin):
    search_fields = ['problem', 'utilisateur_src__nom' , 'utilisateur_src__prenom']
    list_display = ('utilisateur_nom_prenom', 'problem')
    readonly_fields = ('problem' ,'utilisateur_src')

    def utilisateur_nom_prenom(self, obj):
        return f"{obj.utilisateur_src.nom} {obj.utilisateur_src.prenom}"
    utilisateur_nom_prenom.admin_order_field = 'utilisateur_src__nom'  # Permet de trier par nom dans l'admin
    utilisateur_nom_prenom.short_description = 'Signalé par'
    







# Register your models here.
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.unregister(Group)
admin.site.register(Donneur, DonneurAdmin)
admin.site.register(Annonce, AnnonceAdmin)
admin.site.register(EffectueDon, EffectueDonAdmin)
admin.site.register(Demande, DemandeAdmin)
admin.site.register(Tokens, TokensAdmin)
admin.site.register(Problems, ProblemsAdmin)
admin.site.site_header= "Admin interface grappgique"
admin.site.site_title= "le coté adminstrartion"
