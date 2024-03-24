from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from collections import Counter
from django.core.paginator import Paginator

from itertools import islice

from .models import File, Word
from .forms import FileForm
from .utils import get_text_content


def index(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.save()
            return redirect('analysis:file_to_analysis', id=file.id)
    else:
        form = FileForm()
    files = File.objects.all()
    words = Word.objects.all()
    return render(request, 'analysis/index.html', {'form': form,
                                                   'files': files,
                                                   'words': words})


def file_to_analysis(request, id):
    documents_all = File.objects.count()
    file = get_object_or_404(File, id=id)
    text = get_text_content(file).split()
    text_counter = Counter(text).most_common(50)

    words = {}

    for word in text_counter:
        word_to_list = get_object_or_404(Word, word=word[0])
        word_idf = round(word_to_list.count_of_documents / documents_all, 4)
        words.update({word[0]: (word[1], word_idf)})

    sort_dict = sorted(words.items(), key=lambda dicx: dicx[1][1], reverse=True)
    sort_dict = dict(sort_dict)

    # return render(request, 'analysis/analysis.html', context={'words': sort_dict})

    page_size = 20
    page_num = int(request.GET.get('page', 1))
    start = (page_num - 1) * page_size
    end = int(page_num) * page_size
    start_index = (page_num - 1) * page_size

    context = {
        'words': dict(islice(sort_dict.items(), start, end)),
        'paginator': Paginator(sort_dict, page_size),
        'start_index': start_index,
        'page_num': page_num
    }

    return render(request, 'analysis/analysis.html', context=context)

def delete_all_data(request):
    Word.objects.all().delete()
    File.objects.all().delete()
    return HttpResponseRedirect(reverse("analysis:index")) 