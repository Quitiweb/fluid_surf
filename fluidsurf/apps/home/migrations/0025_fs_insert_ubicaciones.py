from django.db import connection
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20191029_1051'),
    ]
    operations = [

        migrations.RunSQL( "insert into home_ubicacion(spot, geoloc) values ('Europe', '36.557223,-6.303212')"),
        migrations.RunSQL( "insert into home_ubicacion(spot, geoloc) values ('Oceania', '-33.865143,151.2099')"),
        migrations.RunSQL( "insert into home_ubicacion(spot, geoloc) values ('Asia', '34.295833,132.319722')"),
        migrations.RunSQL( "insert into home_ubicacion(spot, geoloc) values ('Africa', '51.2099,33.865143')"),
        migrations.RunSQL( "insert into home_ubicacion(spot, geoloc) values ('North America', '34.42083,-119.69819')"),
        migrations.RunSQL( "insert into home_ubicacion(spot, geoloc) values ('South America', '-33.03553,-71.64182')"),
    ]
