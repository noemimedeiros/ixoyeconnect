from django.contrib import messages

def message_warning_generic(request, msg):
    messages.add_message(request, messages.WARNING, msg)

def message_success_generic(request, msg):
    messages.add_message(request, messages.SUCCESS, msg)

def message_error_generic(request, msg):
    messages.add_message(request, messages.ERROR, msg)

def message_info_generic(request, msg):
    messages.add_message(request, messages.INFO, msg)

def message_create_registro(request):
    messages.add_message(request, messages.SUCCESS, 'Registro criado com sucesso.')

def message_update_registro(request):
    messages.add_message(request, messages.SUCCESS, 'Registro atualizado com sucesso.')

def message_delete_registro(request):
    messages.add_message(request, messages.SUCCESS, 'Registro deletado com sucesso.')

def message_error_registro(request):
    messages.add_message(request, messages.SUCCESS, 'Ocorreu um erro durante a operação. Por favor, tente novamente.')