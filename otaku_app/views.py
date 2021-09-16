from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404


from .models import Title, Category, Subcategory
from .forms import TitleForm, CategoryForm, SubcategoryForm

def _check_owner(obj, request):
    if obj.owner != request.user:
        raise Http404

def index(request):
    """Widok głównej strony."""
    context = {}
    return render(request, 'index.html', context)


""" Widoki tablic. """

@login_required
def table_titles(request):
    """Widok tablicy z tytułami."""
    titles = Title.objects.filter(owner=request.user).order_by('name')

    context = {
        "titles": titles,
    }
    return render(request, 'table_titles.html', context)

@login_required
def table_category(request, title_id):
    """Widok tablicy z kategoriami wybranego tytułu."""
    title = get_object_or_404(Title, id=title_id)
    _check_owner(title, request)

    categories = title.category_set.all().order_by('name')

    context = {
        'title': title,
        'categories': categories,
    }
    return render(request, 'table_category.html', context)

@login_required
def table_subcategory(request, category_id):
    """Widok tablicy z podkategoriami wybranej kategorii wybranego tytułu."""
    category = get_object_or_404(Category, id=category_id)
    _check_owner(category, request)

    subcategories = category.subcategory_set.all().order_by('name')

    context = {
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'table_subcategory.html', context)


""" Widoki dodawania nowych obiektów. """


@login_required
def new_title(request):
    """Dodaj nowy tytuł."""
    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = TitleForm()

    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = TitleForm(data=request.POST)
        if form.is_valid():
            new_title = form.save(commit=False)
            new_title.owner = request.user
            new_title.save()
            return redirect('table_titles')

    # Wyświetlenie pustego formularza.
    context = {
        'form': form,
    }
    return render(request, 'new_title.html', context)

@login_required
def new_category(request, title_id):
    """Dodaj nową kategorię dla danego tytułu."""
    title = get_object_or_404(Title, id=title_id)
    _check_owner(title, request)

    if request.method != "POST":
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = CategoryForm()

    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.title = title
            new_category.owner = request.user
            new_category.save()
            return redirect('table_category', title_id=title_id)

    # Wyświetlanie pustego formularza.
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'new_category.html', context)

@login_required
def new_subcategory(request, category_id):
    """Dodaj nową podkategorię dla danej kategorii danego tytułu."""
    category = get_object_or_404(Category, id=category_id)
    _check_owner(category, request)

    if request.method != "POST":
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = SubcategoryForm()

    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = SubcategoryForm(data=request.POST)
        if form.is_valid():
            new_subcategory = form.save(commit=False)
            new_subcategory.category = category
            new_subcategory.owner = request.user
            new_subcategory.save()
            return redirect('table_subcategory', category_id=category_id)

    # Wyświetlanie pustego formularza.
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'new_subcategory.html', context)


""" Widoki edycji istniejących obiektów. """


@login_required
def edit_title(request, title_id):
    """Edytuj istniejący tytuł."""
    title = get_object_or_404(Title, id=title_id)
    _check_owner(title, request)

    if request.method != 'POST':
        # Ządanie początkowe, wypełnienie formularza aktualną treścią wpisu.
        form = TitleForm(instance=title)

    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = TitleForm(instance=title, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_titles')

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'edit_title.html', context)

@login_required
def edit_category(request, category_id):
    """Edytuj istniejącą kategorię."""
    category = get_object_or_404(Category, id=category_id)
    _check_owner(category, request)
    title = category.title

    if request.method != 'POST':
        # Ządanie początkowe, wypełnienie formularza aktualną treścią wpisu.
        form = CategoryForm(instance=category)

    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_category', title_id=title.id)

    context = {
        'category': category,
        'title': title,
        'form': form,
    }
    return render(request, 'edit_category.html', context)    

@login_required
def edit_subcategory(request, subcategory_id):
    """Edytuj istniejącą podkategorię."""
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    _check_owner(subcategory, request)
    category = subcategory.category

    if request.method != 'POST':
        # Ządanie początkowe, wypełnienie formularza aktualną treścią wpisu.
        form = SubcategoryForm(instance=subcategory)

    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = SubcategoryForm(instance=subcategory, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('table_subcategory', category_id=category.id)

    context = {
        'subcategory': subcategory,
        'category': category,
        'form': form,
    }
    return render(request, 'edit_subcategory.html', context)    


""" Widoki usunięcia istniejących obiektów. """


@login_required
def delete_title(request, title_id):
    """Usuń istniejący tytuł."""
    title = get_object_or_404(Title, id=title_id)
    _check_owner(title, request)

    if request.method == "POST":
        title.delete()
        return redirect('table_titles')

    context = {
        'title': title,
    }

    return render(request, 'delete_title.html', context)

@login_required
def delete_category(request, category_id):
    """Usuń istniejącą kategorię."""
    category = get_object_or_404(Category, id=category_id)
    _check_owner(category, request)
    title = category.title

    if request.method == "POST":
        category.delete()
        return redirect('table_category', title_id=title.id)

    context = {
        'category': category,
        'title': title,
    }

    return render(request, 'delete_category.html', context)

@login_required
def delete_subcategory(request, subcategory_id):
    """Usuń istniejącą podkategorię."""
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    _check_owner(subcategory, request)
    category = subcategory.category

    if request.method == "POST":
        subcategory.delete()
        return redirect('table_subcategory', category_id=category.id)

    context = {
        'subcategory': subcategory,
        'category': category,
    }

    return render(request, 'delete_subcategory.html', context)