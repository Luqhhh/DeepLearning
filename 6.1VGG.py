import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn

cfg=[64, 64, 'M', 128, 128, 'M', 256, 256, 256, 'M', 512, 512, 512, 'M', 512, 512, 512, 'M']

class VGG(nn.Module):
    def __init__(self,features,num_classes,init_weight):
        super().__init__()
        self.features=features
        self.avgpool=nn.AdaptiveAvgPool2d((7,7))
        self.classifier=nn.Sequential(
                nn.Linear(512*7*7,4096),
                nn.ReLU(True),
                nn.Dropout(),
                nn.Linear(4096,4096),
                nn.ReLU(True),
                nn.Dropout(),
                nn.Linear(4096,num_classes))
    def forward(self,x):
        out1=self.features(x)
        out2=self.avgpool(out1)
        out3=self.classifier(out2.view(-1,512*7*7))
        return out3
    def initialize_weight(self):
        for m in self.modules():
            if isinstance(m,nn.Conv2d):
                nn.init.kaiming_normal_(m.weight,mode='fan_out',nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias,0)
            elif isinstance(m,nn.BatchNorm2d):
                nn.init.constant_(m.weight,1)
                nn.init.constant_(m.bias,0)
            elif isinstance(m,nn.Linear):
                nn.init.normal_(m.weight,0,0.01)
                nn.init.constant_(m.bias,0)
def make_layers(cfg,batch_norm):
    layers=[]
    in_channel=3
    for v in cfg:
        if v=='M':
            layers+=[nn.MaxPool2d(kernel_size=2,stride=2)]
        else:
            conv=nn.Conv2d(in_channel,v,kernel_size=3,padding=1)
            if batch_norm:
                layers+=[conv,nn.BatchNorm2d(v),nn.ReLU(True)]
            else:
                layers+=[conv,nn.ReLU(True)]
            in_channel=v
    return nn.Sequential(*layers)
model=VGG(make_layers(cfg,batch_norm=True),num_classes=10,init_weight=True)
a=torch.zeros(100,3,32,32)
out=model(a)
print(out.shape)
print(model)
