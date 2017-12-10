from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import label_image
from classify.forms import ImageForm

# Create your views here.

@csrf_exempt
def classify(request):
    if(request.method=='POST'):
        form = ImageForm(request.POST, request.FILES)
        if(form.is_valid):
            file_name = request.POST['file_name']
            form.save()    
            return HttpResponse(label_image.get_class(file_name))
    else:
        return HttpResponse('Expected POST request')
