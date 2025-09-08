from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Process, Favorite
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


@login_required
def home(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('cat', '')
    processes = Process.objects.filter(is_published=True)
    if q:
        processes = processes.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(steps_md__icontains=q)
        )
    if cat:
        processes = processes.filter(category__slug=cat)

    categories = Category.objects.all()
    favorites_ids = set()
    if request.user.is_authenticated:
        favorites_ids = set(Favorite.objects.filter(user=request.user).values_list('process_id', flat=True))

    return render(request, 'knowledge/home.html', {
        'processes': processes[:50],
        'categories': categories,
        'q': q,
        'cat': cat,
        'favorites_ids': favorites_ids,
    })

@login_required
def process_detail(request, slug):
    process = get_object_or_404(
        Process.objects.prefetch_related("steps", "attachments", "links"),
        slug=slug,
        is_published=True
    )
    is_fav = False
    if request.user.is_authenticated:
        is_fav = Favorite.objects.filter(user=request.user, process=process).exists()

    return render(request, 'knowledge/process_detail.html', {
        'process': process,
        'is_fav': is_fav,
    })



@login_required
def search(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('cat', '')
    processes = Process.objects.filter(is_published=True)
    if q:
        processes = processes.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(steps_md__icontains=q)
        )
    if cat:
        processes = processes.filter(category__slug=cat)
    return render(request, 'knowledge/partials/_process_cards.html', {'processes': processes[:50]})

@login_required
def autocomplete(request):
    term = request.GET.get('term', '')
    qs = Process.objects.filter(is_published=True, title__icontains=term).values_list('title', flat=True)[:10]
    return JsonResponse(list(qs), safe=False)

@login_required
def by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    processes = category.processes.filter(is_published=True)
    return render(request, 'knowledge/home.html', {
        'processes': processes,
        'categories': Category.objects.all(),
        'cat': slug,
        'q': '',
        'favorites_ids': set(Favorite.objects.filter(user=request.user).values_list('process_id', flat=True)),
    })

@login_required
def recent_updates(request):
    processes = Process.objects.filter(is_published=True).order_by('-updated_at')[:20]
    return render(request, 'knowledge/recent_updates.html', {'processes': processes})

@login_required
def toggle_favorite(request, pk):
    process = get_object_or_404(Process, pk=pk, is_published=True)
    fav, created = Favorite.objects.get_or_create(user=request.user, process=process)
    if not created:
        fav.delete()
        state = 'removed'
    else:
        state = 'added'
    return JsonResponse({'status': 'ok', 'state': state})


# Apenas usuários staff podem criar processos
@login_required
@user_passes_test(lambda u: u.is_staff)
def create_process(request):
    if request.method == 'POST':
        form = ProcessForm(request.POST)
        if form.is_valid():
            process = form.save()
            messages.success(request, f'Processo "{process.title}" criado com sucesso!')
            return redirect('knowledge:process_detail', slug=process.slug)
    else:
        form = ProcessForm()
    return render(request, 'knowledge/process_form.html', {'form': form, 'title': 'Novo Processo'})

 #Excluir processo (staff only)
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_process(request, pk):
    process = get_object_or_404(Process, pk=pk)
    if request.method == "POST":
        process.delete()
        messages.success(request, f'Processo "{process.title}" excluído com sucesso!')
        return redirect('knowledge:home')
    return render(request, 'knowledge/confirm_delete.html', {'process': process})