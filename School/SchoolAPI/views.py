from django.shortcuts import (
    render,
    get_object_or_404,
)

from rest_framework.response import Response

from rest_framework.decorators import (
    api_view,
    permission_classes,
    action,
)
from rest_framework import (
    status,
    viewsets,
    )

from rest_framework.exceptions import (
    MethodNotAllowed,
)

from .serializers import *
from .models import *

"""

viewset crea las siguientes rutas:

    Listar todos los departamentos: GET /departamento/
    Crear un nuevo departamento: POST /departamento/
    Obtener un departamento específico: GET /departamento/<pk>/
    Actualizar un departamento específico: PUT /departamento/<pk>/
    Eliminar un departamento específico: DELETE /departamento/<pk>/
"""

class Detector:
    def camposVacios(self, camposRequeridos, data):

        camposVacios = [ campo for campo in camposRequeridos if not data.get(campo)]
        
        if camposVacios:
            return Response(
                {"error": f"Favor de revisar su entrada. Los siguientes campos son obligatorios:{''.join(camposVacios)}"},
                status=status.HTTP_400_BAD_REQUEST
            )    
        return None
    
class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class CarreraViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer

class ProfesoresViewSet(viewsets.ModelViewSet, Detector):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

    #! para que los profesores puedan ser registrados en el sistema

    def create(self, request, *args, **kwargs):

        """
        Campos que se tomaran en consideracion durante la crecion 
        de los profesores: 
        Json (del request)

        nombreUsuario (str),
        password (str),
        
        cedulaProfesional(str),

        nombres (str),
        apellidoPaterno (str), 
        apellidoMaterno (str),

        departamento (str), 
        salario (float)

        """

        try:
            #! Manejo de malos request
            if request.method != 'POST':
                raise MethodNotAllowed(str(request.method))


            #! Manejo del request
            data = request.data

            #checar campos vacios
            camposUsuario = ['nombreUsuario','password']
            responseError = self.camposVacios(camposRequeridos=camposUsuario, data=data)
            if responseError:
                 return responseError
                
            elif User.objects.filter(username=data.get('nombreUsuario')).exists():
                return Response(
                    {"error": "El nombre de usuario ingresado ya se encuentra en uso."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # manejon de registro de contrasenia muuuuuy basico
            elif len(data.get('password')) < 8: 
                return Response(
                    {"error": "La longitud de la contraseña debe ser de almenos 8 caracteres"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            #! Verificar que no haya ningun campo vacio

            camposRequeridos = ['cedulaProfesional', 'email', 'nombres', 'apellidoPaterno', 'apellidoMaterno', 'departamento', 'salario']
            responseError = self.camposVacios(camposRequeridos, data)
            if responseError:
                 return responseError

            nmbUsuario = data.get('nombreUsuario')
            password = data.get('password')
            nmbs = data.get('nombres')
            apellidoPat = data.get('apellidoPaterno')
            apellidoMat = data.get('apellidoMaterno')
            departamento  = data.get('departamento')
            cedulaProfesional = data.get('cedulaProfesional')
            email = data.get('email')
            salario = data.get('salario')

            #*Crear Usuario
            user = User.objects.create_user(
                username=nmbUsuario,
                password=password,
                email=email
            )

            #*Prepara los datos del alumno
            profesorData = {
                'user': user.id,
                'nombres': nmbs,
                'apellidoPaterno': apellidoPat,
                'apellidoMaterno': apellidoMat,
                'departamento': departamento,
                'cedulaProfesional': cedulaProfesional,
                'salario': salario

            }
            
            serializer = self.get_serializer(data=profesorData) #mejor practica
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": f"Registro del usuario {nmbUsuario} realizado con exito"},
                    status=status.HTTP_201_CREATED
                )
            
                """
                Si el seralizador no fueera valido, seria necesario
                reahacer nuevamente el procedimiento. Por lo tanto, 
                habria que borrar el usuario (User) que fue creado.
                """

            else:
                user.delete()
                return Response(
                    {"error" : serializer.errors},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except MethodNotAllowed as e:
            return Response(
                {"error": f"El metodo que se esta intentando utilizar {e} no esta permitido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e: 
            return Response(
                {"error" : f"Ha ocurrido un error inesperado {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class AlumnosViewSet(viewsets.ModelViewSet, Detector):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

    #! para que los alumnos se puedan inscribir a la escuela

    def create(self, request, *args, **kwargs):

        """
        Campos que se esperan que se ingresen para hacer el procesamiento
        (La relacion de nombres es del JSON del request):
        Aunque el modelo tiene mas campos, no todos se usan para crear el alumno para el endpoint
        nombreUsuario (str),
        password (str),
        nombres (str),
        apellidoPaterno (str), 
        apellidoMaterno (str),
        curp (str),
        carrera (int), 
        email (str)
        """

        #verificar el nombre de usuario y password antes de proceder
        try:
            #! Manejo de malos request
            if request.method != 'POST':
                raise MethodNotAllowed(str(request.method))
            
            data = request.data
            
            nmbUsuario = data.get('nombreUsuario')
            password = data.get('password')
           
            
            #checar campos vacios
            camposUsuario = ['nombreUsuario','password']
            responseError = self.camposVacios(camposRequeridos=camposUsuario, data=data)
            if responseError:
                 return responseError

            elif User.objects.filter(username=nmbUsuario).exists():
                return Response(
                    {"error": "El nombre de usuario ingresado ya se encuentra en uso."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # manejon de registro de contrasenia muuuuuy basico
            elif len(password) < 8: 
                return Response(
                    {"error": "La longitud de la contraseña debe ser de almenos 8 caracteres"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            


            # Verificar que no haya ningun campo vacio
            camposRequeridos = ['nombres', 'apellidoPaterno', 'apellidoMaterno', 'curp', 'carrera','email']
            responseError = self.camposVacios(camposRequeridos, data)
            if responseError:
                 return responseError

            nmbs = data.get('nombres')
            apellidoPat = data.get('apellidoPaterno')
            apellidoMat = data.get('apellidoMaterno')
            curp  = data.get('curp')
            carrera = data.get('carrera')
            email = data.get('email')

            #*Crear Usuario
            user = User.objects.create_user(
                username=nmbUsuario,
                password=password,
                email=email
            )

            #*Prepara los datos del alumno
            alumnoData = {
                'user': user.id,
                'nombres': nmbs,
                'apellidoPaterno': apellidoPat,
                'apellidoMaterno': apellidoMat,
                'curp': curp,
                'carrera': carrera
            }

            
            serializer = self.get_serializer(data=alumnoData) #mejor practica
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": f"Registro del usuario {nmbUsuario} realizado con exito"},
                    status=status.HTTP_201_CREATED
                )
            
                """
                Si el seralizador no fueera valido, seria necesario
                reahacer nuevamente el procedimiento. Por lo tanto, 
                habria que borrar el usuario (User) que fue creado.
                """

            else:
                user.delete()
                return Response(
                    {"error" : serializer.errors},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except MethodNotAllowed as e: 
            return Response(
                {"Error": f"El metodo que se esta intentando utilizar {e} no esta permitido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e: 
            return Response({"error": str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)       


    
class MateriaViewSet(viewsets.ModelViewSet, Detector):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

    # agregar el post modificado

    def create(self, request, *args, **kwargs): 
        """
            Campos que se esperan que se ingresen para el procesamiento
            (relacion de nombres es del JSON del request): 

            nombre, 
            codigo, 
            creditos, 
            carrera(fk)
        """
        
        try:
            
            if request.method != 'POST':
                raise MethodNotAllowed(str(request.method))
            
            data = request.data
            camposRequeridos = ['nombre', 'codigo', 'creditos', 'carrera']
            responseError = self.camposVacios(camposRequeridos, data)
            
            if responseError:
                return responseError
            
            #! Verificador de carrera
            # Si no existe la carrera se sale del metodo
            if not Carrera.objects.filter(pk=(data.get('carrera'))):
                return Response(
                    {"error": f"El id de la carrera que ha sido ingresada no es correcta"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            #* Obtener toda la informacion proporcionada por el request

            nombre = data.get('nombre')
            codigo = data.get('codigo')
            creditos = data.get('creditos')
            carrera = data.get('carrera')


            pass
        except MethodNotAllowed as e:
            return Response(
                {"Error": f"El metodo {e} que se esta intentado utilizar no esta permitido"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

class Curso(viewsets.ModelViewSet, Detector):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    def create(self, request, *args, **kwargs):

        try:
            #! Manejo de metodo
            if request.method != 'POST':
                raise MethodNotAllowed(str(request.method))


            #! Manejo del request
            data = request.data

            #checar campos vacios
            campos = ['materia','profesor', 'nombrePeriodo', 'grupo', 'cupoMax', 'dia', 'horaInicio', 'horaFin',
                             'edificio', 'numeroSalon', 'tipoSalon']
            
            responseError = self.camposVacios(camposRequeridos=campos, data=data)

            if responseError:
                 return responseError
                
            elif not Profesor.objects.filter(pk=data.get('profesor')).exists():
                return Response(
                    {"error": "El profesor que ha ingresado no existe. Verifique sus entradas."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            elif not Materia.objects.filter(pk=data.get('materia')).exists():
                return Response(
                    {"error": "La materia que fue ingresada no existe. Verifique sus entradas."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            



            #*Prepara los datos del alumno
            cursoData = {
                'materia': data.get('materia'),
                'profesor': data.get('profesor'),
                'nombre_periodo': data.get('nombrePeriodo'), 
                'grupo': data.get('grupo'),
                'cupo_maximo': data.get('cupoMax'),
                'dia': data.get('dia'),
                'hora_inicio': data.get('horaInicio'),
                'hora_fin': data.get('horaFin'),
                'edificio': data.get('edificio'),
                'numero_salon': data.get('numeroSalon'),
                'tipo_salon': data.get('tipoSalon'),
                }
            
            serializer = self.get_serializer(data=cursoData) #mejor practica
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": f"Registro del curso realizado con exito"},
                    status=status.HTTP_201_CREATED
                )
            
                """
                Si el seralizador no fuera valido, seria necesario
                reahacer nuevamente el procedimiento. Por lo tanto, 
                habria que borrar el usuario (User) que fue creado.
                """
            
        except MethodNotAllowed as e:
            return Response(
                {"error": f"El metodo que se esta intentando utilizar {e} no esta permitido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e: 
            return Response(
                {"error" : f"Ha ocurrido un error inesperado {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

class Inscripcion(viewsets.ModelViewSet, Detector):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

    def create(self, request, *args, **kwargs):

        try:
            #! Manejo de metodo
            if request.method != 'POST':
                raise MethodNotAllowed(str(request.method))


            #! Manejo del request
            data = request.data

            #checar campos vacios
            campos = ['alumno','curso']
            responseError = self.camposVacios(camposRequeridos=campos, data=data)

            if responseError:
                 return responseError
                
            elif not Alumno.objects.filter(pk=data.get('alumno')).exists():
                return Response(
                    {"error": "El alumno que ha ingresado no existe. Verifique sus entradas."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            elif not Curso.objects.filter(pk=data.get('curso')).exists():
                return Response(
                    {"error": "El curso que fue ingresado no existe. Verifique sus entradas."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            



            #*Prepara los datos del alumno
            cursoData = { 
                'alumno': data.get('alumno'), 
                'curso': data.get('curso')
                }
            
            serializer = self.get_serializer(data=cursoData) #mejor practica
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": f"La inscripcion del alumno se ha realizado con exito"},
                    status=status.HTTP_201_CREATED
                )
            

        except MethodNotAllowed as e:
            return Response(
                {"error": f"El metodo que se esta intentando utilizar {e} no esta permitido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e: 
            return Response(
                {"error" : f"Ha ocurrido un error inesperado {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


class Asistencia(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer

    def create(self, request, *args, **kwargs):

        try:
            #! Manejo de metodo
            if request.method != 'POST':
                raise MethodNotAllowed(str(request.method))


            #! Manejo del request
            data = request.data

            #checar campos vacios
            campos = ['inscripcion']
            responseError = self.camposVacios(camposRequeridos=campos, data=data)

            if responseError:
                 return responseError
                
            elif not Inscripcion.objects.filter(pk=data.get('inscripcion')).exists():
                return Response(
                    {"error": "El alumno que ha ingresado no existe. Verifique sus entradas."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            



            #*Preparar los datos
            cursoData = { 
                'inscripcion': data.get('inscripcion')
                }
            
            # en caso que se incluyera el valor presente, sino se maneja su default -> false
            if data.get('presente'):
                cursoData['presente'] = data.get('presente')


            serializer = self.get_serializer(data=cursoData) #mejor practica
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": f"La inscripcion del alumno se ha realizado con exito"},
                    status=status.HTTP_201_CREATED
                )
            

        except MethodNotAllowed as e:
            return Response(
                {"error": f"El metodo que se esta intentando utilizar {e} no esta permitido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e: 
            return Response(
                {"error" : f"Ha ocurrido un error inesperado {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        