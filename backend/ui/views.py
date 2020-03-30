from django.shortcuts import render


def svelte_home(request):
    context = {"style": "ui/svelte.css", "script": "ui/svelte.js"}
    return render(request, "ui/home.html", context)

def vanilla_home(request):
    context = {"style": "ui/vanilla/css/vanilla.css", "script": "ui/vanilla/js/index.js"}
    return render(request, "ui/home.html", context)
