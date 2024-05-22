from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {

    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    upload_success = False
    if request.POST and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        try:
            if myfile.size > 1048576:
                raise Exception('Слишком большой файл')
            filename = fs.save(myfile.name, myfile)
            upload_success = True
            print('Файл сохранен', filename)
        except Exception as exc:
            print('Ошибка:', exc)
    context = {
        'upload_success': upload_success
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)