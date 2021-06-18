import torch.nn as nn
from torchvision import transforms, models
from torch.autograd import Variable

"""
pre-trained ResNet
"""


class ResNet(nn.Module):
    """
    Args:
        fea_type: string, resnet101 or resnet 152
    """

    def __init__(self, fea_type='resnet152'):
        super(ResNet, self).__init__()
        self.fea_type = fea_type
        # rescale and normalize transformation
        # Transforms are common image transformations. They can be chained together using Compose
        # Tensor is n-d array with same dtype
        self.transform = transforms.Compose([
            transforms.ToTensor(),  # Convert PIL or numpy ndarray image to tensor
            # (image_pixel[channel] - mean[channel] )/ std[channel]
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            # recomended mean for resnet  - [0.485, 0.456, 0.406],
            # recomended std for resnet  - [0.229, 0.224, 0.225]
        ])

        """
        All pre-trained models expect input images normalized in the same way,
        i.e. mini-batches of 3-channel RGB images of shape (3 x H x W),
        where H and W are expected to be at least 224.
        The images have to be loaded in to a range of [0, 1] and then normalized using mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225].
        """

        # Downloading the pretrained model weights to a cache directory.
        # https://arxiv.org/pdf/1512.03385.pdf
        if fea_type == 'resnet101':
            resnet = models.resnet101(pretrained=True)  # dim of pool5 is 2048
        elif fea_type == 'resnet152':
            resnet = models.resnet152(pretrained=True)
        else:
            raise Exception('No such ResNet!')

        resnet.float()
        resnet.cuda()
        resnet.eval()

        module_list = list(resnet.children())
        self.conv5 = nn.Sequential(*module_list[: -2])
        self.pool5 = module_list[-2]

    # rescale and normalize image, then pass it through ResNet
    def forward(self, x):
        x = self.transform(x)
        x = x.unsqueeze(0)  # reshape the single image s.t. it has a batch dim
        # x = Variable(x).cuda()
        res_conv5 = self.conv5(x)
        res_pool5 = self.pool5(res_conv5)
        res_pool5 = res_pool5.view(res_pool5.size(0), -1)

        return res_pool5
