import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

def calculate_face_similarity(image_path1, image_path2):
    # Load images
    image1 = Image.open(image_path1).convert('RGB')
    image2 = Image.open(image_path2).convert('RGB')

    # Initialize MTCNN and Inception Resnet V1 models
    mtcnn = MTCNN(keep_all=True)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    # Detect faces and get embeddings
    faces1 = mtcnn(image1)
    faces2 = mtcnn(image2)

    if faces1 is None or faces2 is None:
        print("Error: One or both faces not found.")
        return 0

    embeddings1 = resnet(faces1).detach().numpy()
    embeddings2 = resnet(faces2).detach().numpy()

    # Calculate cosine similarity between embeddings
    similarity = cosine_similarity(embeddings1, embeddings2)[0][0]

    return similarity

