import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


def load_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return img.astype(np.float32) / 255.0


def power_iteration(A, num_iterations=1000, epsilon=1e-8):
    n, d = A.shape

    v = np.random.rand(d)
    v = v / np.linalg.norm(v)

    for _ in range(num_iterations):
        Av = np.dot(A, v)
        v_new = Av / np.linalg.norm(Av)
        if np.abs(np.dot(v, v_new)) > 1 - epsilon:
            break

        v = v_new

    return np.dot(Av, v), v


def svd_decomposition(img_matrix, num_iterations=50, epsilon=1e-8):
    A = img_matrix
    ATA = np.dot(A.T, A)
    n, m = A.shape
    U = np.zeros((n, m))
    S = np.zeros(m)
    Vt = np.zeros((m, m))

    for i in range(m):
        s, v = power_iteration(ATA, num_iterations, epsilon)
        if s < 0:
            break
        S[i] = np.sqrt(s)
        Vt[i] = v
        ATA = ATA - s * np.outer(v, v)
        if S[i] < epsilon:
            break
        u = np.dot(A, v) / S[i]
        U[:, i] = u
        A = A - np.outer(u, np.dot(S[i], v))

    return U, S, Vt


def compress_image(U, s, Vt, rank):
    s_compressed = s[:rank]
    U_compressed = U[:, :rank]
    Vt_compressed = Vt[:rank, :]
    return U_compressed, s_compressed, Vt_compressed


def denoise_image(U, s, Vt, threshold):
    s_denoised = np.where(s > threshold, s, 0)
    return U, s_denoised, Vt


def iterative_denoise(image, initial_threshold, threshold_step, max_iterations, target_mse):
    U, s, Vt = svd_decomposition(image)

    threshold = initial_threshold
    for iteration in range(max_iterations):
        U_denoised, s_denoised, Vt_denoised = denoise_image(U, s, Vt, threshold)
        denoised_image = reconstruct_image(U_denoised, s_denoised, Vt_denoised)

        mse = mean_squared_error(image.flatten(), denoised_image.flatten())
        print(mse)
        if mse >= target_mse:
            break
        threshold += threshold_step

    return denoised_image

def reconstruct_image(U, s, Vt):
    return np.dot(U, np.dot(np.diag(s), Vt))

def save_image(img_matrix, output_path):
    img_matrix = np.clip(img_matrix, 0, 1) * 255
    cv2.imwrite(output_path, img_matrix)




def find_optimal_rank(s, energy_fraction=0.9):
    s = np.sort(s)[::-1]

    plt.figure(figsize=(8, 6))
    plt.plot(s)
    plt.title("Singular values")
    plt.show()
    total_energy = np.sum(s**2)

    cumulative_energy = np.cumsum(s**2)

    rank = np.searchsorted(cumulative_energy, energy_fraction * total_energy)

    return rank