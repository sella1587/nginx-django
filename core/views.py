from rest_framework.views import APIView
from rest_framework.response import Response
from .outils import consolidate_data, merge_objects_from_json
from django_tenants.utils import schema_context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FileUploadParser,DjangoMultiPartParser
from .models import ConsolidatedObjects,ObjectsFromCao
from .serializers import SerialConsolidatedObject, SerialObjectFromCao
from .filter import ConsolidateFilter
from rest_framework import status

from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from .tables import TableConsolide
import pandas as pd

#for the login
class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    # def get_success_url(self):
    #     if self.request.user.is_staff:
    #         return '/admin/dashboard/'
    #     return '/menu/'

@login_required
def index(request):
    queryset = ConsolidateFilter(request.GET, queryset=ObjectsFromCao.objects.all())
    optionFacteurChoc = [element for element in ObjectsFromCao.objects.values('facteur_choc__etat', 'facteur_choc_id').distinct().order_by('-facteur_choc')]
    optionDegreChoc = [element for element in ObjectsFromCao.objects.values('degre_choc__etat', 'degre_choc_id').distinct().order_by('-degre_choc')]
    optionavec_plots = [element for element in ObjectsFromCao.objects.values('avec_plots__etat', 'avec_plots_id').distinct().order_by('-avec_plots')]
    optionaavec_carlingage = [element for element in ObjectsFromCao.objects.values('avec_carlingage__etat', 'avec_carlingage_id').distinct().order_by('-avec_carlingage')]
    dataOption = {
        "facteur_choc" : optionFacteurChoc,
        "degre_choc" : optionDegreChoc,
        "avec_plots" : optionavec_plots,
        "avec_carlingage" : optionaavec_carlingage
    }
    context = {
        "filtreform": queryset,
        "tables_consolide": TableConsolide(queryset.qs),
        "checkSelection":dataOption
    }
    return render(request, 'pages/home.html', context)

@login_required
def menu(request):
   
    context = {
        "datas": "consolidated_data",
        "formulaire": "si besoin"
    }
    return render(request, 'pages/menu.html', context)
#for api
class GetObjectConsolidated(ListAPIView):
    queryset = ConsolidatedObjects.objects.all()
    serializer_class = SerialObjectFromCao
    permission_classes = [IsAuthenticated]

#interne
class Getinfobrute(ListAPIView):
    queryset = ConsolidatedObjects.objects.all()
    serializer_class = SerialObjectFromCao
    permission_classes = [IsAuthenticatedOrReadOnly]

class ConsolidatedDataView(APIView):
    def get(self, request, *args, **kwargs):
        consolidated_df = consolidate_data()
        consolidated_data = consolidated_df.to_dict(orient="records")
        return Response(consolidated_data)

class ImportJsonView(APIView):
    parser_classes = [MultiPartParser] 
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)        
        file = request.FILES['file']
        try:
            import json
            data = json.load(file)            
            Project = str(data['Project']).lower()
            Source = data['Source']
            dt_processing = data['DateTraitement']
            # load datas sjon
            with schema_context(Project):
                df_raw = pd.DataFrame(data["Datas"])
                df_raw["source"] =  Source 
                df_raw["project"] = Project
                df_raw["dt_processing"] = dt_processing
                df_raw.rename(columns = {
                    "Oid": "uid",
                    "Name": "name",
                    "ComponentType": "component_type",
                    "Description": "description",
                    "Trade": "trade",
                    "Function": "function",
                    "Lot": "lot",
                    "Room": "room",
                    "CodeFournisseur": "code_fournisseur",
                    "FacteurChoc": "facteur_choc",
                    "DegreChoc":"degre_choc",
                    "AvecPlots":"avec_plots",
                    "AvecCarlingage": "avec_carlingage"
                }, inplace=True)            
                list_of_dicts = df_raw.to_dict(orient='records') 
                merge_objects_from_json(list_of_dicts)            
        except Exception as e:
            return Response({"error": "Invalid JSON file", "error_details": str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        return Response({"message": "Data imported and flagged successfully"}, status=status.HTTP_201_CREATED)