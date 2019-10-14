from django.shortcuts import render


def show_landing(request):
    context = {}
    return render(request, template_name='main/landing.html', context=context)
