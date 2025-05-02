# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'departamentos', views.DepartamentoViewSet)
router.register(r'carreras', views.CarreraViewSet)
router.register(r'profesores', views.ProfesoresViewSet)
router.register(r'alumnos', views.AlumnosViewSet)
router.register(r'materias', views.MateriaViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'inscripciones', views.InscripcionViewSet)
router.register(r'asistencias', views.AsistenciaViewSet)

urlpatterns = [ 
    # Los endpoints de los modelos
    path('api/', include(router.urls)),
]

