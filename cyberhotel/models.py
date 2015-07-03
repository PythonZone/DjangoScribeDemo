# coding=utf-8

from import_export import resources
import polymorphic
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils.translation import ugettext as _


import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('computed_fields',)

CATEGORIE = (
    ('economique', 'economique'),
    ('standard', 'standard'),
    ('premium', 'premium'),
    ('prestige', 'prestige'),
)

class Residence(models.Model):
  class Meta:
    computed_fields = ['chambres','nbDeChambres','chambresUtiles','sallesDeBain','salles','nbDeSalles']
  nom         = models.CharField(max_length=60)
  etageMin	  = models.IntegerField(default=0)
  etageMax    = models.IntegerField()
  categorie   = models.CharField(max_length=10, choices=CATEGORIE)
  nbPlacesMax = models.IntegerField(blank=True,null=True)   # TODO
  tarifMoyen  = models.FloatField(blank=True,null=True)     # TODO 
  def chambres(self):
    return self.salles().instance_of(Chambre)
  def nbDeChambres(self):
    return len(self.chambres())
  def chambresUtiles(self):
    return  [ s for s in self.chambres() if not s.enTravaux ]
  def sallesDeBain(self):
    return self.salles().instance_of(SalleDeBain)
  def salles(self):
    return self._salles.all()
  def nbDeSalles(self):
    return len(self.salles())
  def __unicode__(self):
    return self.nom 
  # for validating entity constraint
  def validateOrdreEtages(self):
    if not (self.etageMin <= self.etageMax):
       raise ValidationError(_(u"etage minimum est plus haut que l'etage max"),code="ordreEtages")
  def clean(self):
    self.validateOrdreEtages() 
  
class Salle(polymorphic.PolymorphicModel):
  residence   = models.ForeignKey(Residence,related_name="_salles")
  etage	      = models.IntegerField()
  enTravaux	  = models.BooleanField()
  numero      = models.IntegerField()
  def __unicode__(self):
    return str(self.numero)
  def validateEtageEntreMinEtMax(self):
    if not(self.residence.etageMin <= self.etage and self.etage<=self.residence.etageMax):
      raise ValidationError(
        _(u"l'etage doit etre entre %i et %i, les etages de la residences") % (self.residence.etageMin,self.residence.etageMax),code="validateEtageEntreMinEtMax")
  def clean(self):
    self.validateEtageEntreMinEtMax()
    
class SalleDeBain(Salle):
  estSurLePallier = models.BooleanField()
  chambre         = models.ForeignKey('Chambre',related_name="_sallesDeBains",blank=True,null=True)
  def __unicode__(self):
    return str(self.numero)
    
class Chambre(Salle):
  class Meta:
    computed_fields = ['nbDePlaces','occupants','nbDeOccupants','occupantsList']
  nbLitsSimples = models.IntegerField(default=1,verbose_name='nb de lits simples')
  nbLitsDoubles	= models.IntegerField(default=0)
  prix	        = models.FloatField(blank=True,null=True)
  estNonFumeur  = models.BooleanField() 
  def nbDePlaces(self):
    return self.nbLitsSimples+self.nbLitsDoubles*2
  def occupants(self):
    return list(self._occupants.all())
  def nbDeOccupants(self):
    return len(self.occupants())
  def occupantsList(self):
    return ",".join(str(o) for o in self.occupants())
  def __unicode__(self):
    return str(self.numero)

    
GENRE = {
    ('homme', 'homme'),
    ('femme', 'femme'),
}

class Personne(models.Model):
  class Meta:
    abstract = True
  nom    = models.CharField(max_length=40)
  age    = models.IntegerField()
  genre  = models.CharField(max_length=5, choices=GENRE)
  
class Resident(Personne):
  estFumeur      = models.NullBooleanField()
  chambreOccupee = models.ForeignKey(Chambre,related_name="_occupants")
  conjoint       = models.OneToOneField("self",related_name="+",blank=True,null=True)
  tuteurs        = models.ManyToManyField("self",symmetrical=False,related_name='tutores',blank=True,null=True)
  def __unicode__(self):
    return self.nom
  def residence(self):
    return self.chambreOccupee.residence
    
class ResidenceResource(resources.ModelResource):
    class Meta:
        model = Residence
    
class Locataire(Resident):
  def prixPaye(self):
    return 0  # TODO
  def __unicode__(self):
    return self.nom
    
class Location(models.Model):
  chambreLouee    = models.ForeignKey(Chambre,related_name="_locations")   # TODO plural +s -e  to be resolved
  locataire       = models.ForeignKey(Locataire,related_name="_locations")
  dateDepart      = models.DateField()
  dateFin         = models.DateField()
  def reduction(self):
    return 0  # TODO
  def prix(self):
    return 0  # TODO
  def __unicode__(self):
    return str(self.chambreLouee.numero)+"/"+self.locataire.nom



        
class Reduction(models.Model):
  location   = models.ForeignKey(Location,related_name="_reductions")
  def validate_taux(taux):
    if  not (0<=taux and taux<=100):
        raise ValidationError(_(u"%s is not a percentage")% taux,code="tauxPercentage")  
  taux     = models.IntegerField(validators=[validate_taux])
  #  taux  = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
  label      = models.CharField(max_length=10)

  
    
#  def user_link(self):
#    return '<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)) , escape(self.user))
#
#  user_link.allow_tags = True
#  user_link.short_description = "User" 
