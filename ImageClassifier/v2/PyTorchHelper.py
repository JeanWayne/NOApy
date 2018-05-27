import torch
from PIL import Image
from torch.autograd import Variable
from torchvision import models
from torchvision.transforms import transforms

names=['composite','diagramm','imaging','photos','vis']

def getLabelName(i):
    if i==0:
        return "composite"
    if i==1:
        return "diagramm"
    if i==2:
        return "imaging"
    if i==3:
        return "photos"
    if i==4:
        return "vis"

def getImageClass(path):
    img = Image.open(path)
    img_tensor = preprocess(img)
    img_tensor.unsqueeze_(0)
    input= Variable(img_tensor).type(torch.FloatTensor).cuda()
    output = model(input)
    _, preds = torch.max(output.data, 1)

    return getLabelName(preds[0])

use_gpu = torch.cuda.is_available()

model_ft = models.resnet18(pretrained=False)
num_ftrs = model_ft.fc.in_features
model_ft.fc = torch.nn.Linear(num_ftrs, 5)

if use_gpu:
    model_ft = model_ft.cuda()
    print("!!! Running with GPU POWER !!!")
else:
    print("??? Y NO GPU POWER ???")
model_ft.load_state_dict(torch.load("noa_image_model_v2.pt"))
model=model_ft
#model = torch.load('noa_image_model_v2.pt')

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
#photos=["/home/jean/Image_class_v2/val/photos/10.1100_2011_545421---1.jpg","/home/jean/Image_class_v2/val/photos/10.1100_2012_106429---5.jpg","/home/jean/Image_class_v2/val/photos/10.1100_2012_481584---1.jpg"]
#diagramm=["/home/jean/Image_class_v2/val/diagram/10.1093_ecam_nen040---3.jpg","/home/jean/Image_class_v2/val/diagram/10.1093_ecam_nen043---4.jpg","/home/jean/Image_class_v2/val/diagram/10.1093_ecam_nen061---3.jpg"]
#composite=["/home/jean/Image_class_v2/val/composite/10.1093_ecam_nep188---1.jpg","/home/jean/Image_class_v2/val/composite/10.1155_2011_346413---0.jpg","/home/jean/Image_class_v2/val/composite/10.1155_2010_635294---3.jpg"]
#imaging=["/home/jean/Image_class_v2/val/imaging/10.1100_2012_501751---12.jpg","/home/jean/Image_class_v2/val/imaging/10.1100_2012_537973---6.jpg","/home/jean/Image_class_v2/val/imaging/10.1155_2010_513461---6.jpg"]
#kl=0
#for k in [photos,diagramm,composite,imaging]:
 #   print("_____________")
  #  for i in k:



