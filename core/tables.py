from django_tables2.tables import Table
from .models import ObjectsFromCao

class TableConsolide(Table):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        for col_name, column in self.base_columns.items():
            column.attrs = {
                "th": {"id": col_name}
            }
    class Meta:
        model = ObjectsFromCao 