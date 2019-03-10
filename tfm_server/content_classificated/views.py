from django.shortcuts import render

# Create your views here.
from .models import ClasificationsContent
from .forms import ClasificationsContentForm, RawClasificationsContentForm
from django.core.serializers.json import DjangoJSONEncoder
import os
import sqlite3
import pandas as pd

def PreClassificationsContent_create_view(request):
    form = RawClasificationsContentForm()
    if request.method == 'POST':
        form = RawClasificationsContentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            ClasificationsContent.objects.create(**form.cleaned_data)
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

def ClasificationsContent_detail_view(request):
    obj = ClasificationsContent.objects.all()
#    context = {
#            'tittle': obj.title,
#            'description': obj.description}
#    djan_json = json.dumps(list(obj), cls=DjangoJSONEncoder)
    conn = sqlite3.connect(os.path.join('.', "..",
                                        "tfm_server", "db.sqlite3"))
    df = pd.read_sql_query("select * from content_classificated_clasificationscontent;",
                           conn)
    df = df.groupby('video_name').count()
    df.reset_index(level=0, inplace=True)
    told = df.to_dict('records')
    context = {
            'object': obj,
            'selector': told
            }
    return render(request, 'results.html', context)
