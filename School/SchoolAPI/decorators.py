from django.http import HttpResponseForbidden

def grupo_requerido(nombre_grupo):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name=nombre_grupo).exists() and not request.user.is_superuser:
                return HttpResponseForbidden('No tienes permiso para realizar esta acción.')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
