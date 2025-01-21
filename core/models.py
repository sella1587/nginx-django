from django.db import models
from django_tenants.models import TenantMixin

class FacteurChoc(models.Model):
    etat = models.CharField(max_length=5, unique=True)  
    class Meta:
        db_table = '"projet"."facteur_choc"'
        # managed = False
    def __str__(self):
        return self.etat

class DegreChoc(models.Model):
    etat  = models.CharField(max_length=50)    
    class Meta:
        db_table = '"projet"."degre_choc"'
        # managed = False
    def __str__(self):
        return self.etat

class AvecPlot(models.Model):
    etat = models.CharField(max_length=150, unique=True)   
    class Meta:
        db_table = '"projet"."avec_plots"'
        # managed = False
    def __str__(self):
        return self.etat
    
    
class AvecCarlingage(models.Model):
    etat = models.CharField(max_length=75)    
    class Meta:
        db_table = '"projet"."avec_carlingage"'
        # managed = False
    def __str__(self):
        return self.etat

class ProprieteDc(models.Model):
    property = models.CharField(max_length=50)
    sourcespriorities = models.CharField(max_length=250)
    displaymode = models.CharField(max_length=50)   
    class Meta:
        db_table = '"projet"."proriete_dc"'
        # managed = False

class Ouvrage(TenantMixin):
    name = models.CharField(max_length=25, unique=True)
    type = models.CharField(max_length=50)
    schema_name = models.CharField(max_length=50)
    code_client = models.CharField(max_length=150)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True
    class Meta:
        db_table = '"public"."ouvrage"'
        # managed = False
 

class ObjectsFromCao(models.Model):
    uid = models.CharField(max_length=75, null=False)
    source = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=255, null=False)
    component_type = models.CharField(max_length=75, null=True)
    description = models.CharField(max_length=254, null=True)
    trade = models.CharField(max_length=100, null=True)
    function = models.CharField(max_length=50, null=True)
    lot = models.CharField(max_length=50, null=True)
    room = models.CharField(max_length=50, null=True)
    code_client_ouvrage = models.CharField(max_length=75, null=True)
    code_client_object = models.CharField(max_length=50, null=True)
    code_fournisseur = models.CharField(max_length=50, null=True)
    facteur_choc = models.ForeignKey(FacteurChoc, db_column='facteur_choc', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    degre_choc = models.ForeignKey(DegreChoc, db_column='degre_choc', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    avec_plots = models.ForeignKey(AvecPlot, db_column='avec_plots', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    avec_carlingage = models.ForeignKey(AvecCarlingage, db_column='avec_carlingage', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    creation_date = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(blank=True, null=True)
    archived_date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = "objects_from_cao"
    

class ConsolidatedObjects(models.Model):
    uid = models.CharField(max_length=75, null=False)
    source = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=255, null=False)
    component_type = models.CharField(max_length=75,null=True)
    description = models.CharField(max_length=254, null=True)
    trade = models.CharField(max_length=100,null=True)
    function = models.CharField(max_length=50,null=True)
    lot = models.CharField(max_length=50, null=True)
    room = models.CharField(max_length=50, null=True)
    code_client_ouvrage = models.CharField(max_length=75, null=True)
    code_client_object = models.CharField(max_length=50, null=True)
    code_fournisseur = models.CharField(max_length=50, null=True)
    facteur_choc = models.ForeignKey(FacteurChoc, db_column='facteur_choc', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    degre_choc = models.ForeignKey(DegreChoc, db_column='degre_choc', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    avec_plots = models.ForeignKey(AvecPlot, db_column='avec_plots', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    avec_carlingage = models.ForeignKey(AvecCarlingage, db_column='avec_carlingage', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    date_last_modified = models.DateField(blank=True, null=True)
    archived_date = models.DateField(blank=True, null=True)
    class Meta:
        db_table = "objects_consolidate"
    


class OwnerCodeDetails(models.Model):
    objconso_id  = models.IntegerField(null=False)
    fieldorder = models.IntegerField(null=False, unique=True)    
    fieldvalue = models.CharField(max_length=50)
    class Meta:
        db_table =  "owner_code_details"

class OwnerCodeProperties(models.Model):
    fieldorder = models.IntegerField(null=False, unique=True)
    fieldtype = models.IntegerField(null=False)
    fieldvalue = models.CharField(max_length=50)
    fieldlabel = models.CharField(max_length=50)
    def __str__(self):
        return self.fieldlabel
    class Meta:
        db_table =  "owner_code_properties"   

class ConsolidationRule(models.Model):
    property_name = models.CharField(max_length=255)
    sources_priorities = models.TextField(null=True, blank=True)  # Ex: "PID;SPEL;SM3D;USER"
    display_mode = models.CharField(max_length=50, choices=[("First", "First"), ("All", "All")])
    ouvrage = models.ForeignKey(Ouvrage, db_column='ouvrage', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    def __str__(self):
        return self.property_name
    class Meta:
        db_table = '"public"."consolidation_rule"'
        # managed = False
   

class TmpObjectsFromCao(models.Model):
    uid = models.CharField(max_length=75, null=False)
    source = models.CharField(max_length=150, null=False)
    name = models.CharField(max_length=255, null=False)
    component_type = models.CharField(max_length=75, null=True)
    description = models.CharField(max_length=254, null=True)
    trade = models.CharField(max_length=100, null=True)
    function = models.CharField(max_length=50, null=True)
    lot = models.CharField(max_length=50, null=True)
    room = models.CharField(max_length=50, null=True)
    code_client_ouvrage = models.CharField(max_length=75, null=True)
    code_client_object = models.CharField(max_length=50, null=True)
    code_fournisseur = models.CharField(max_length=50, null=True)
    facteur_choc = models.CharField(max_length=20, null=True)
    degre_choc = models.CharField(max_length=20, null=True)
    avec_plots = models.CharField(max_length=20, null=True)
    avec_carlingage = models.CharField(max_length=20, null=True)
    creation_date = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(blank=True, null=True)
    archived_date = models.DateField(blank=True, null=True)
    flag_events = models.CharField(max_length=20, null=True)
    class Meta:
        db_table = "Tmp_objects_from_cao"
