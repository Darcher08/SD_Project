from django.db import models
from django.contrib.auth.models import User

# viewSet

# ---
class Departamento(models.Model):
    nombre = models.CharField(max_length=150)
    clave = models.CharField(max_length=15, unique=True)
    
    """
    Dado que Django no soporte claves primarias compuestas, una
    forma de lograr un  efecto similar es con unique_together

    """

    class Meta:
        unique_together = ('nombre', 'clave')

    def __str__(self):
        return self.nombre

# ---
class Carrera(models.Model):
    nombre = models.CharField(max_length=150)
    clave = models.CharField(max_length=15, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL,null=True, related_name='carreras')
    
    class Meta:
        unique_together = ('nombre', 'clave')

    def __str__(self):
        return f"{self.nombre} ({self.clave})"


# ---
# endpoints personalizados
class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula_profesional = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=150)
    apellidoPaterno = models.CharField(max_length=150)
    apellidoMaterno = models.CharField(max_length=150)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, related_name='profesores')
    urlFoto = models.URLField(blank=True)
    es_director = models.BooleanField(default=False)  # Para identificar directores de departamento
    salario = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidoPaterno} {self.apellidoMaterno}"


# ---
class Alumno(models.Model):
    #utilizar el id como si fuera la matricula de la persona
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=150)
    apellidoPaterno = models.CharField(max_length=150)
    apellidoMaterno = models.CharField(max_length=150)
    curp = models.CharField(max_length=45, unique=True)
    promedio = models.FloatField(blank=True, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True, related_name='alumnos')
    semestre_actual = models.PositiveSmallIntegerField(default=1)
    urlFoto = models.URLField(blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidoPaterno} {self.apellidoMaterno}"


# ---
class Materia(models.Model):
    nombre = models.CharField(max_length=125)
    codigo = models.CharField(max_length=30, unique=True)
    creditos = models.IntegerField()
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True, related_name='materias')
    
    
    class Meta:
        unique_together = ('nombre', 'codigo')


    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
# ---
class Curso(models.Model):
    DIAS_CHOICES = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    
    TIPOS_SALON = [
        ('AULA', 'Aula regular'),
        ('LAB', 'Laboratorio'),
        ('TALLER', 'Taller'),
        ('AUDITORIO', 'Auditorio')
    ]
    
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='cursos')
    profesor = models.ForeignKey(Profesor, on_delete=models.SET_NULL, null=True, related_name='cursos')
    nombre_periodo = models.CharField(max_length=50)  # Ej: "Semestre Primavera 2025"
    activo = models.BooleanField(default=True)
    grupo = models.CharField(max_length=5)  # Ej: "A", "B", "001", etc., bajo decision propia
    cupo_maximo = models.PositiveIntegerField(default=30)
    # Información del horario
    dia = models.CharField(max_length=3, choices=DIAS_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    # Información del salón
    edificio = models.CharField(max_length=50)
    numero_salon = models.CharField(max_length=10)
    tipo_salon = models.CharField(max_length=30, choices=TIPOS_SALON, default='AULA')
    
    class Meta:
        unique_together = [
            ('materia', 'grupo', 'nombre_periodo'),
            ('edificio', 'numero_salon', 'dia', 'hora_inicio')
        ]
    
    def __str__(self):
        return f"{self.materia.nombre} - Grupo {self.grupo} ({self.nombre_periodo})"


# ---
class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    calificacion = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('alumno', 'curso')
    
    def __str__(self):
        return f"{self.alumno.nombres} - {self.curso.materia.nombre}"


# ---
class Asistencia(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(auto_now_add=True)
    presente = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('inscripcion', 'fecha')
    
    def __str__(self):
        return f"{self.inscripcion.alumno.nombres} - {self.fecha}"