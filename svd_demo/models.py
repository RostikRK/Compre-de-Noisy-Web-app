import os

from django.db import models
from .utils import load_image, svd_decomposition, compress_image, reconstruct_image, save_image, iterative_denoise, find_optimal_rank
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile





class CompressedImage(models.Model):
    original = models.ImageField(upload_to='originals/')
    compressed = models.ImageField(upload_to='compressed/', blank=True)

    def compress(self):
        img_path = self.original.path
        img_matrix = load_image(img_path)
        U, s, Vt = svd_decomposition(img_matrix)
        rank = find_optimal_rank(s)
        if rank < round(len(s) * 0.01):
            rank = round(len(s) * 0.05)
        U_compressed, s_compressed, Vt_compressed = compress_image(U, s, Vt, rank)
        img_compressed = reconstruct_image(U_compressed, s_compressed, Vt_compressed)

        temp_img = NamedTemporaryFile(suffix='.jpg', delete=True)
        save_image(img_compressed, temp_img.name)

        self.compressed.save('compressed_'+self.original.name, File(open(temp_img.name, 'rb')))

        temp_img.close()




class DenoisedImage(models.Model):
    original = models.ImageField(upload_to='originals/')
    denoised = models.ImageField(upload_to='denoised/', blank=True)

    def denoise(self):
        img_path = self.original.path
        img_matrix = load_image(img_path)
        img_denoised= iterative_denoise(img_matrix, 1, 0.5, 30, 0.005)
        temp_img = NamedTemporaryFile(suffix='.jpg', delete=True)
        save_image(img_denoised, temp_img.name)
        self.denoised.save('denoised_'+ self.original.name, File(open(temp_img.name, 'rb')))

        temp_img.close()

