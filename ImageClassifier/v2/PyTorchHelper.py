import torch
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import transforms

model = torch.load('./model_resnet50.pth.tar')

normalize = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)
preprocess = transforms.Compose([
    transforms.Scale(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    normalize
])

img = Image.open(IMG_URL)
img_tensor = preprocess(img)
img_tensor.unsqueeze_(0)
output = model(Variable(img_tensor))