from django.shortcuts import render

# Create your views here.
import sqlite3
import pandas as pd
import os
from .models import Resumen
from .forms import ResumenForm, RawResumenForm


def resumen_create_view(request):
    form = RawResumenForm()
    if request.method == 'POST':
        form = RawResumenForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Resumen.objects.create(**form.cleaned_data)
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

def resumen_detail_view(request):
    obj = Resumen.objects.all()
    conn = sqlite3.connect(os.path.join('.', "..",
                                        "tfm_server", "db.sqlite3"))
    df = pd.read_sql_query("select * from political_clasification_politicalclasification;",
                           conn)
    df.sort_values(by='content', inplace=True)
    told = df.to_dict('records')
    context = {
            'object': obj,
            'another_metrics': told
            }
    return render(request, 'detail.html', context)