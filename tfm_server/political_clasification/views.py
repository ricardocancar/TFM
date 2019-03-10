from django.shortcuts import render

# Create your views here.
from .models import PoliticalClasification
from .forms import PoliticalClasificationForm, RawPoliticalClasificationForm


def clasifications_create_view(request):
    form = RawPoliticalClasificationForm()
    if request.method == 'POST':
        form = RawPoliticalClasificationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            PoliticalClasification.objects.create(**form.cleaned_data)
        else:
            print(form.errors)
    context = {
            'form': form}
    return render(request, 'product_create.html', context)


#def product_create_view(request):
#    if request.method == 'POST':
#        my_new_title = request.POST.get('title')
#    # Product.objects.create(title=my_new_title)
#    context = {}
#    return render(request, 'product_create.html', context)

#def product_create_view(request):
#    form = ProductForm(request.POST or None)
#    if form.is_valid():
#        form.save()
#        form = ProductForm()
#    context = {
#            'form': form
#            }
#    return render(request, 'product_create.html', context)

def political_clasification_detail_view(request):
    obj = PoliticalClasification.objects.all()
#    context = {
#            'tittle': obj.title,
#            'description': obj.description}
    context = {
            'object': obj
            }
    return render(request, 'results.html', context)