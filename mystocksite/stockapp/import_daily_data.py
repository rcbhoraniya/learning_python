from django.db import connection
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'mystocksite.mystocksite.settings'
def my_custom_sql(id=1):

    with connection.cursor() as cursor:
        # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT * FROM stockapp_stock WHERE id = %s", [id])
        row = cursor.fetchone()
        print(row)

    return row


x=my_custom_sql(2)