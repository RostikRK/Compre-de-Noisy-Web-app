from django.shortcuts import render
from django import forms
from django.shortcuts import render, redirect
from .models import CompressedImage, DenoisedImage
from django.http import JsonResponse
from django.urls import reverse


def home(request):
    return render(request, 'svd_demo/home.html')



class ImageForm(forms.Form):
    image = forms.ImageField()

def compress(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('image')
            print(f"Number of images: {len(images)}")  # Debug print
            compressed_image_ids = []
            for image in images:
                compressed_image = CompressedImage(original=image)
                compressed_image.save()
                compressed_image.compress()
                compressed_image_ids.append(str(compressed_image.id))
            print(f"Compressed image ids: {compressed_image_ids}")  # Debug print
            image_ids = '-'.join(compressed_image_ids)
            return JsonResponse({'redirect_url': reverse('svd_demo:result_compre', args=(image_ids,))})
    else:
        form = ImageForm()
    return render(request, 'svd_demo/compress.html', {'form': form})


def result_compre(request, image_ids):
    image_ids_list = list(map(int, image_ids.split('-')))
    compressed_images = CompressedImage.objects.filter(id__in=image_ids_list)
    return render(request, 'svd_demo/result_compre.html', {'compressed_images': compressed_images})


def result_denoise(request, image_ids):
    image_ids_list = list(map(int, image_ids.split('-')))
    denoised_images = DenoisedImage.objects.filter(id__in=image_ids_list)
    return render(request, 'svd_demo/result_denoise.html', {'denoised_images': denoised_images})





def denoise(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('image')
            print(f"Number of images: {len(images)}")  # Debug print
            denoised_image_ids = []
            for image in images:
                denoised_image = DenoisedImage(original=image)
                denoised_image.save()
                denoised_image.denoise()
                denoised_image_ids.append(str(denoised_image.id))
            print(f"denoise image ids: {denoised_image_ids}")  # Debug print
            image_ids = '-'.join(denoised_image_ids)
            return JsonResponse({'redirect_url': reverse('svd_demo:result_denoise', args=(image_ids,))})
    else:
        form = ImageForm()
    return render(request, 'svd_demo/denoise.html', {'form': form})
