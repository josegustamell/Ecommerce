from django.http import HttpResponse
from django.shortcuts import redirect

# Um decorator é uma função que recebe outra função (nesse caso da minha view), e tem OUTRA FUNÇÃO dentro dela mesma que faz
# alguma coisa interessante, e então parece que essa outra função tem que retornar sempre a função de minha view que eu recebi,
# depois de fazer alguma coisa com ela. fácil.


def unauthenticated_user(view_func): # view_func é o nome da função (a minha view) que eu to recebendo.
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
    
    def decorator(view_func):
        
        def wrapper_func(request, *args, **kwargs): # É na wrapper que fazemos as coisas que precisamos.
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed to view this page.')
        
        return wrapper_func
    
    return decorator
        