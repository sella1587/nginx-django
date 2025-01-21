import pandas as pd
from .models import ObjectsFromCao, ConsolidationRule, Ouvrage
from datetime import date
from django.utils.timezone import now

def getListCategorie():
    listcat = Ouvrage.objects.values("ouvrage","id").distinct()
    return [(c['ouvrage'], c['id']) for c in listcat]

def loadConsolidatepara(ouvrage):
    NormalizeOuvrage = int(ouvrage)
    rules = ConsolidationRule.objects.filter(ouvrage__id = NormalizeOuvrage)
  
    config = [
        {
            "property": rule.property_name,
            "sourcespriorites": rule.sources_priorities,
            "DisplayMode": rule.display_mode,
            
        }
        for rule in rules
    ]        
    return config



def consolidate_data():
    # Charger les objets actifs (non archivés)
    objects = ObjectsFromCao.objects.filter(archived_date__isnull=False)
    data = pd.DataFrame.from_records(objects.values())
  

    # Charger les règles de consolidation
    rules = ConsolidationRule.objects.all()
    config = [
        {
            "property": rule.property_name,
            "sourcespriorites": rule.sources_priorities,
            "DisplayMode": rule.display_mode,
        }
        for rule in rules
    ]

    # Initialiser le DataFrame consolidé
    consolidated_rows = []

    # Regrouper les données par 'name'
    for name, group in data.groupby("name"):
        consolidated_row = {"name": name}

        for rule in config:
            property_name = rule["property"]
            sources_priorities = rule.get("sourcespriorites")
            display_mode = rule.get("DisplayMode", "All")

            if property_name not in group.columns:
                consolidated_row[property_name] = None
                continue

            # Si SourcesPriorites est défini, filtrer les sources par priorité
            if sources_priorities:
                sources_priorities = sources_priorities.split(";")
                valid_sources = [s for s in sources_priorities if s in group["source"].values]
            else:
                valid_sources = group["source"].unique()

            # Si aucune source valide n'est trouvée, prendre les valeurs restantes
            if not valid_sources:
                group_sorted = group
            else:
                group_sorted = group.sort_values(
                    by="source", key=lambda x: x.map({s: i for i, s in enumerate(valid_sources)}).fillna(len(valid_sources))
                )

            if display_mode == "First":
                consolidated_row[property_name] = group_sorted.iloc[0][property_name]
            elif display_mode == "All":
                consolidated_row[property_name] = "; ".join(group_sorted[property_name].astype(str).unique())
            consolidated_rows.append(consolidated_row)
    consolidated_data = pd.DataFrame(consolidated_rows)    
    return pd.DataFrame(consolidated_data)

def merge_objects_from_json(source_data):
    """
    Fonction qui effectue le traitement de fusion :
    - Met à jour les objets existants
    - Insère les nouveaux objets
    - Flague les objets absents
    """

    # Récupérer les UIDs de la source
    source_uids = {item['uid'] for item in source_data}

    # Récupérer les objets existants dans la base
    existing_objects = ObjectsFromCao.objects.filter(uid__in=source_uids)

    # Mise à jour des objets existants
    for obj in existing_objects:
        data = next(item for item in source_data if item['uid'] == obj.uid)
        obj.source = data['source']
        obj.name = data['name']
        obj.component_type = data.get('component_type')
        obj.description = data.get('description')
        obj.trade = data.get('trade')
        obj.function = data.get('function')
        obj.lot = data.get('lot')
        obj.room = data.get('room')
        obj.code_client_ouvrage = data.get('code_client_ouvrage')
        obj.code_client_object = data.get('code_client_object')
        obj.code_fournisseur = data.get('code_fournisseur')
        obj.date_last_modified = now()
        obj.save()

    # Insérer les nouveaux objets
    existing_uids = {obj.uid for obj in existing_objects}
    new_objects = [
        ObjectsFromCao(
            uid=item['uid'],
            source=item['source'],
            name=item['name'],
            component_type=item.get('component_type'),
            description=item.get('description'),
            trade=item.get('trade'),
            function=item.get('function'),
            lot=item.get('lot'),
            room=item.get('room'),
            code_client_ouvrage=item.get('code_client_ouvrage'),
            code_client_object=item.get('code_client_object'),
            code_fournisseur=item.get('code_fournisseur'),
            creation_date=now(),
        )
        for item in source_data
        if item['uid'] not in existing_uids
    ]
    ObjectsFromCao.objects.bulk_create(new_objects)
    all_uid2_flaged_as_deleted = existing_uids - source_uids
    # Flager les objets absents dans la source
    ObjectsFromCao.objects.filter(
        uid__in=all_uid2_flaged_as_deleted
    ).update(archived_date=date.today())
    return {"list_of_delete": list(all_uid2_flaged_as_deleted)}