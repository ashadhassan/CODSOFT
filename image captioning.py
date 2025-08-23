import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# -------------------
# 1. Encoder (ResNet50 feature extractor)
# -------------------
class EncoderCNN(nn.Module):
    def __init__(self, embed_size):
        super(EncoderCNN, self).__init__()
        resnet = models.resnet50(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad = False  # freeze ResNet
        modules = list(resnet.children())[:-1]  # remove last FC layer
        self.resnet = nn.Sequential(*modules)
        self.fc = nn.Linear(resnet.fc.in_features, embed_size)
        self.bn = nn.BatchNorm1d(embed_size, momentum=0.01)

    def forward(self, images):
        with torch.no_grad():
            features = self.resnet(images)  # (batch, 2048, 1, 1)
        features = features.view(features.size(0), -1)  # flatten
        features = self.fc(features)
        features = self.bn(features)
        return features  # (batch, embed_size)


# -------------------
# 2. Decoder (LSTM)
# -------------------
class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1):
        super(DecoderRNN, self).__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)

    def forward(self, features, captions):
        embeddings = self.embed(captions[:, :-1])  # exclude <end> token
        inputs = torch.cat((features.unsqueeze(1), embeddings), 1)
        hiddens, _ = self.lstm(inputs)
        outputs = self.linear(hiddens)
        return outputs


# -------------------
# 3. Putting it together
# -------------------
class ImageCaptioningModel(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size):
        super(ImageCaptioningModel, self).__init__()
        self.encoder = EncoderCNN(embed_size)
        self.decoder = DecoderRNN(embed_size, hidden_size, vocab_size)

    def forward(self, images, captions):
        features = self.encoder(images)
        outputs = self.decoder(features, captions)
        return outputs


# -------------------
# 4. Example usage
# -------------------
if __name__ == "__main__":
    embed_size = 256
    hidden_size = 512
    vocab_size = 5000  # (depends on dataset)
    model = ImageCaptioningModel(embed_size, hidden_size, vocab_size)

    # Dummy input (batch of 2 images, 3x224x224)
    images = torch.randn(2, 3, 224, 224)
    captions = torch.randint(0, vocab_size, (2, 20))  # dummy captions

    outputs = model(images, captions)
    print("Output shape:", outputs.shape)  # (batch, seq_len, vocab_size)
