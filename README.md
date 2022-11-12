# Fluid Surf

FluidSurf, es una plataforma online para fotógrafos y surferos.


## Puntos Pendientes

 - [ ] Para que el proyecto sea visiblemente aceptable, es necesaria la preparación de datos previos
     - Por lo tanto, lo ideal sería crear estos datos (aunq sean de prueba) vía `migrations`
 - [ ] Un `How to make it work` tb sería menester
 - [ ] El requirements.txt parece un copy paste de proyectos anteriores. Repasar los que no se usan


## How to run the project

 - Clone the repository
 - Create a venv using `python3 -m venv ~/venvs/fluid_surf`
 - Run `source ~/venvs/fluid_surf/bin/activate`
 - Go to your root project folder and run `pip install -r requirements.txt`
 - Then run `python manage.py migrate`
 - Run `python manage.py compilemessages`
 - Finally run `python manage.py runserver`
 - (here we need to create, at least, a super-user) `python manage.py createsuperuser`
 - After that, we need to create some records from `localhost:8000/admin/`
   - Country, surfer and photographer profiles, etc. (still pending)
 