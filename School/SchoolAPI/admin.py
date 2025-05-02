from django.contrib import admin
from .models import (

    Departamento,
    Alumno,
    Profesor,
    Carrera,
    Materia,
    Curso,    
    Inscripcion,
    Asistencia,
)

admin.site.register(Alumno)
admin.site.register(Profesor)
admin.site.register(Carrera)
admin.site.register(Departamento)
admin.site.register(Curso)
admin.site.register(Inscripcion)
admin.site.register(Asistencia)
admin.site.register(Materia)
