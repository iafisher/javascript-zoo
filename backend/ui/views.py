from django.shortcuts import render


def svelte_home(request):
    context = {"style": "ui/svelte.css", "script": "ui/svelte.js"}
    return render(request, "ui/home.html", context)
