from django.db import models
from simple_history.models import HistoricalRecords
from crum import get_current_user
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractUser):
    flottes = models.ManyToManyField('Flotte',  verbose_name = "Flottes authorisées", blank = True , limit_choices_to={'actif': True},  related_name="authaurized_users")
    
    # pass



class RelatedFlotteObjectsManager(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if not user or  user.is_anonymous :
            return super(RelatedFlotteObjectsManager, self).get_queryset().none()
        elif user and user.is_superuser:
            return super(RelatedFlotteObjectsManager, self).get_queryset()
        else:
            return super(RelatedFlotteObjectsManager, self).get_queryset().filter(flotte__authaurized_users= user )


class Societe(models.Model):
    FORMES = (
        ('sarl', 'SARL'),
        ('sarlau', 'SARL AU'),
        ('sa', 'SA'),
    )
    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Sociétés"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Société"
    nom = models.CharField(max_length = 30, verbose_name = "Raison sociale")
    phone = models.CharField(max_length = 16, verbose_name = "Téléphone",null = True, blank = True)
    adresse1 = models.CharField(max_length =30, verbose_name = "Adresse",null = True, blank = True)
    adresse2 = models.CharField(max_length =30, verbose_name = "Suite",null = True, blank = True)
    ville = models.CharField(max_length =15, verbose_name = "Ville")
    patente = models.CharField(max_length =15, verbose_name = "Patente",null = True, blank = True)
    rc = models.CharField(max_length =15, verbose_name = "Registre de commerce",null = True, blank = True)
    cnss = models.CharField(max_length =15, verbose_name = "Num CNSS",null = True, blank = True)
    idf = models.CharField(max_length =15, verbose_name = "Identifiant fiscal",null = True, blank = True)
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    ice = models.CharField(max_length =15, verbose_name = "ICE",null = True, blank = True)
    logo = models.ImageField(upload_to='logo',blank=True,null=True)
    forme = models.CharField(max_length = 10, verbose_name = "Type",choices=FORMES,null = True, blank = True)
    history = HistoricalRecords()
    def __str__(self):
        if self.forme:
            return "{0} {1}".format(self.nom, self.get_forme_display())
        else:
            return self.nom



class Flotte(models.Model):
    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Flottes"
        permissions = (
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Flotte"
    nom = models.CharField(max_length = 30, verbose_name = "Nom")
    phone = models.CharField(max_length = 16, verbose_name = "Téléphone",null = True, blank = True)
    adresse1 = models.CharField(max_length =30, verbose_name = "Adresse",null = True, blank = True)
    adresse2 = models.CharField(max_length =30, verbose_name = "Suite",null = True, blank = True)
    ville = models.CharField(max_length =15, verbose_name = "Ville",null = True, blank = True)
    patente = models.CharField(max_length =15, verbose_name = "Patente",null = True, blank = True)
    ref = models.CharField(max_length =10, verbose_name = "Ref",null = True, blank = True)
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    longitude = models.FloatField(verbose_name = "Longitude",null =True, blank = True)
    latitude = models.FloatField(verbose_name = "Latitude",null =True, blank = True)
    history = HistoricalRecords()
    societe_obj = models.ForeignKey(Societe, verbose_name = "Société",related_name="flottes",on_delete=models.PROTECT , limit_choices_to={'actif': True} )
    def __str__(self):
        return self.nom
    def invoice_footer(self, *args, **kwargs):
        return (u"{0} - Tél: {1} - ICE: {2}".format(self.societe, self.phone, self.ice),
        u"Identifiant Fiscal: {0} - Patente: {1} - RC: {2} - CNSS: {3}".format(self.idf, self.patente, self.rc , self.cnss),
        )
    @property
    def ice(self):
            return self.societe_obj.ice
    @property
    def rc(self):
            return self.societe_obj.rc
    @property
    def cnss(self):
            return self.societe_obj.cnss
    @property
    def societe(self):
            return str(self.societe_obj)
    @property
    def idf(self):
            return self.societe_obj.idf
    @property
    def logo(self):
            return self.societe_obj.logo



class Equipement(models.Model):
    ENSEMBLES = (
        ('porteur', 'Porteur'),
        ('tracteur', 'Tracteur'),
        ('remorque', 'Remorque'),
    )

    class Meta:
        ordering = ["external_id"]
        verbose_name_plural = "Equipements roulants"
        permissions = (
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Equipement roulant"
    matricule = models.CharField(max_length = 30, verbose_name = "Nom")
    external_id = models.CharField(max_length = 30, verbose_name = "Identifiant",null = True, blank = True)
    fabricant = models.CharField(max_length = 30, verbose_name = "Fabricant")
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    flotte = models.ForeignKey(Flotte, verbose_name = "Flotte",related_name="equipements",on_delete=models.PROTECT , limit_choices_to={'actif': True} )
    ensemble = models.CharField(max_length = 10, verbose_name = "Ensemble",choices=ENSEMBLES)
    tracteur = models.ForeignKey("Equipement", verbose_name = "Tracteur",related_name="remorques",on_delete=models.PROTECT , 
                        limit_choices_to={'actif': True, 'ensemble': 'tracteur'} ,null = True, blank = True)
    history = HistoricalRecords()
    def __str__(self):
        return self.matricule
    def clean(self):
        if not self.external_id :
            self.external_id = self.matricule
        if self.ensemble != 'remorque' and self.tracteur : 
            raise ValidationError({'tracteur': 'Le tracteur ne doit être défini que pour les remorques.'})
        # if self.ensemble == 'remorque' and not self.tracteur : 
        #     raise ValidationError({'tracteur': 'Le tracteur est obligatoire pour les remorques.'})



class Conducteur(models.Model):
    class Meta:
        ordering = ["external_id","nom","prenom"]
        verbose_name_plural = "Conducteurs"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Conducteur"
    nom = models.CharField(max_length = 30, verbose_name = "Nom")
    prenom = models.CharField(max_length = 30, verbose_name = "Prénom")
    phone = models.CharField(max_length = 16, verbose_name = "Téléphone")
    adresse = models.CharField(max_length =64, verbose_name = "Adresse",null = True, blank = True)
    external_id = models.CharField(max_length = 16, verbose_name = "Référence",unique=True)
    flotte = models.ForeignKey(Flotte, verbose_name = "Flotte" , limit_choices_to={'actif': True}, on_delete=models.PROTECT)
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    history = HistoricalRecords()

# def limit_tracteur_choices():
#     allowed_tracteur_ids = User.objects.filter(Q(group__name="contributor") | Q(group__name="Group")).values_list('id', flat=True)
#     return Q(id__in=allowed_user_ids)

class Tournee(models.Model):
    class Meta:
        verbose_name_plural = "Tournées"
    NEW = 'draft'
    ONGOING = 'ongoing'
    DONE = 'done'
    CANCEL = 'cancel'
    ETATS = (
        (NEW, 'Brouillon'),
        (CANCEL, 'Annulé'),
        (ONGOING, 'En cours'),
        (DONE, 'Terminé'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(verbose_name = "Heure de la validation" , null = True, blank = True)
    finished_at = models.DateTimeField(verbose_name = "Heure de la validation" , null = True, blank = True)
    accepted_at = models.DateTimeField(verbose_name = "Heure de la validation" , null = True, blank = True)
    created_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_tournees")
    started_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="started_tournees")
    finished_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="finished_tournees")
    accepted_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_tournees")
    #jour = models.DateField(verbose_name = "Date")
    verbose_name = "Tournée"
    conducteur = models.ForeignKey(Conducteur, verbose_name = "Conducteur" , limit_choices_to={'actif': True}, on_delete=models.PROTECT, db_index=True)
    tracteur = models.ForeignKey(Equipement, verbose_name = "Tracteur" , limit_choices_to={'actif': True, 'ensemble__in':('porteur','tracteur')}, on_delete=models.PROTECT, db_index=True)
    tracteur = models.ForeignKey(Equipement, verbose_name = "Remorque" , limit_choices_to={'actif': True, 'ensemble__in':('porteur','tracteur')}, on_delete=models.PROTECT, db_index=True)
    montant = models.FloatField(verbose_name = "Montant", null = False, blank = False, default = 0.0)
    external_id = models.CharField(max_length = 16, verbose_name = "Numéro")
    etat = models.CharField(max_length = 10, verbose_name = "Etat",choices=ETATS,default = "draft", db_index=True)
    tracteur =  models.ForeignKey(Equipement, verbose_name = "Camion" , limit_choices_to={'actif': True} , null = True, blank = True, on_delete=models.SET_NULL)
    flotte = models.ForeignKey(Flotte, verbose_name = "Flotte" , limit_choices_to={'actif': True}, on_delete=models.PROTECT, db_index=True)




class Etape(models.Model):
    class Meta:
        verbose_name_plural = "Etapes de tournée"
    NEW = 'draft'
    ONGOING = 'ongoing'
    DONE = 'done'
    CANCEL = 'cancel'
    ETATS = (
        (NEW, 'Brouillon'),
        (CANCEL, 'Annulé'),
        (ONGOING, 'En cours'),
        (DONE, 'Terminé'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(verbose_name = "Heure de la validation" , null = True, blank = True)
    finished_at = models.DateTimeField(verbose_name = "Heure de la validation" , null = True, blank = True)
    accepted_at = models.DateTimeField(verbose_name = "Heure de la validation" , null = True, blank = True)
    created_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_etapes")
    started_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="started_etapes")
    finished_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="finished_etapes")
    accepted_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_etapes")
    verbose_name = "Etape"
    tournee = models.ForeignKey(Tournee, verbose_name = "Tournée" , on_delete=models.PROTECT, db_index=True)
    conducteur = models.ForeignKey(Conducteur, verbose_name = "Conducteur" , limit_choices_to={'actif': True}, on_delete=models.PROTECT, db_index=True)
    client = models.ForeignKey("Client", verbose_name = "Client",related_name="ventes" , limit_choices_to={'actif': True}, on_delete=models.PROTECT, db_index=True)
    montant_ht = models.FloatField(verbose_name = "Montant HT", default = 0)
    montant_tva = models.FloatField(verbose_name = "Montant TVA", default = 0)
    montant_poids = models.FloatField(verbose_name = "Volume", default = 0)
    montant_ttc = models.FloatField(verbose_name = "Remise TTC", default = 0)
    facture = models.BooleanField(default=False, verbose_name = "Facturé?")
    reference_client = models.CharField(max_length = 64, verbose_name = "Référence client", null = True, blank = True)
    reference_externe = models.CharField(max_length = 64, verbose_name = "Référence externe", null = True, blank = True)
    external_id = models.CharField(max_length = 16, verbose_name = "Identifiant")
    etat = models.CharField(max_length = 10, verbose_name = "Etat",choices=ETATS,default = "draft", db_index=True)
    tracteur =  models.ForeignKey(Equipement, verbose_name = "Camion" , limit_choices_to={'actif': True} , null = True, blank = True, on_delete=models.SET_NULL)
    flotte = models.ForeignKey(Flotte, verbose_name = "Flotte" , limit_choices_to={'actif': True}, on_delete=models.PROTECT, db_index=True)



class Client(models.Model):
    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Clients"
        permissions = (
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nom = models.CharField(max_length = 30, verbose_name = "Nom")
    adresse1 = models.CharField(max_length = 30, verbose_name = "Adresse", blank = True)
    adresse2 = models.CharField(max_length =30, verbose_name = "Adresse (suite)", blank = True)
    ville = models.CharField(max_length =30, verbose_name = "Ville", blank = True)
    phone = models.CharField(max_length = 20, verbose_name = "Téléphone", blank = True)
    patente = models.CharField(max_length = 16, verbose_name = "Patente", blank = True)
    external_id = models.CharField(max_length = 16, verbose_name = "Tag", blank = True, unique = True)
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    ice = models.CharField(max_length =15, verbose_name = "ICE",null = True, blank = True)
    created_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_clients")
    updated_by_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_clients")
    delai_paiement = models.IntegerField(default = 0, verbose_name = "Délai de paiement (jours)",validators=[MinValueValidator(0)])
    history = HistoricalRecords()
    def __str__(self):
        return '[{0}] {1}'.format(self.external_id, self.nom)


    @property
    def has_open_paiements(self):
        return len(self.paiement.filter(etat='open')) > 0

    def formatted_phone(self):
        if len(self.phone.strip())==10:
            return "%s%s %s%s %s%s %s%s %s%s" % tuple(self.phone.strip())
        else:
            return self.phone.strip()

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk and user:
            self.created_by_user = user
            self.updated_by_user = user
        elif user:
            self.updated_by_user = user
        super(Client, self).save(*args, **kwargs)
