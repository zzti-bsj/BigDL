#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import pytest
from unittest import TestCase

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from test.pytorch.utils._train_torch_lightning import create_data_loader, data_transform

from bigdl.nano.pytorch import TorchNano
from bigdl.nano.pytorch.vision.models import vision

batch_size = 256
num_workers = 0
data_dir = os.path.join(os.path.dirname(__file__), "../data")


class ResNet18(nn.Module):
    def __init__(self, num_classes, pretrained=True, include_top=False, freeze=True):
        super().__init__()
        backbone = vision.resnet18(pretrained=pretrained, include_top=include_top, freeze=freeze)
        output_size = backbone.get_output_size()
        head = nn.Linear(output_size, num_classes)
        self.model = nn.Sequential(backbone, head)

    def forward(self, x):
        return self.model(x)

    def do_nothing(self):
        # test whether we can access this method after calling `self.setup`
        pass


class MyNano(TorchNano):
    def train(self):
        model = ResNet18(10, pretrained=False, include_top=False, freeze=True)
        loss_func = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        train_loader = create_data_loader(data_dir, batch_size, num_workers, data_transform)

        model, optimizer, train_loader = self.setup(model, optimizer, train_loader)

        model.train()

        num_epochs = 1
        for _i in range(num_epochs):
            total_loss, num = 0, 0
            for X, y in train_loader:
                optimizer.zero_grad()
                loss = loss_func(model(X), y)
                self.backward(loss)
                optimizer.step()
                
                total_loss += loss.sum()
                num += 1
            print(f'avg_loss: {total_loss / num}')


class LinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(1, 1, bias=False)
        self.fc1.weight.data.fill_(1.0)

    def forward(self, input_):
        return self.fc1(input_)


class MyNanoCorrectness(TorchNano):
    def train(self, lr):
        dataset=TensorDataset(
            torch.tensor([[0.0],[0.0],[1.0],[1.0]]),
            torch.tensor([[0.0],[0.0],[0.0],[0.0]]),
        )
        train_loader = DataLoader(dataset=dataset, batch_size=2, shuffle=False)
        origin_model = LinearModel()
        loss_func = nn.MSELoss()
        optimizer = torch.optim.SGD(origin_model.parameters(), lr=lr)

        model, optimizer, train_loader = self.setup(origin_model, optimizer, train_loader)

        model.train()

        num_epochs = 2
        for _i in range(num_epochs):
            for X, y in train_loader:
                optimizer.zero_grad()
                loss = loss_func(model(X), y)
                self.backward(loss)
                optimizer.step()

        assert origin_model.fc1.weight.data == 0.25, \
            f"wrong weights: {origin_model.fc1.weight.data}"


class MyNanoAccess(TorchNano):
    def train(self):
        model = ResNet18(10, pretrained=False, include_top=False, freeze=True)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        train_loader = create_data_loader(data_dir, batch_size, num_workers, data_transform)
        model, optimizer, train_loader = self.setup(model, optimizer, train_loader)

        # access a custom attribute
        model.do_nothing()


class MyNanoMultiOptimizer(TorchNano):
    def train(self):
        model = ResNet18(10, pretrained=False, include_top=False, freeze=True)
        loss_func = nn.CrossEntropyLoss()
        optimizers = [torch.optim.Adam(model.parameters(), lr=0.005),
                      torch.optim.Adam(model.parameters(), lr=0.01)]
        train_loader = create_data_loader(data_dir, batch_size, num_workers, data_transform)

        model, optimizers, train_loader = self.setup(model, optimizers, train_loader)

        model.train()

        num_epochs = 1
        for _i in range(num_epochs):
            total_loss, num = 0, 0
            for X, y in train_loader:
                for optimizer in optimizers:
                    optimizer.zero_grad()
                loss = loss_func(model(X), y)
                self.backward(loss)
                for optimizer in optimizers:
                    optimizer.step()
                
                total_loss += loss.sum()
                num += 1
            print(f'avg_loss: {total_loss / num}')


class TestLite(TestCase):
    def setUp(self):
        test_dir = os.path.dirname(__file__)
        project_test_dir = os.path.abspath(
            os.path.join(os.path.join(os.path.join(test_dir, ".."), ".."), "..")
        )
        os.environ['PYTHONPATH'] = project_test_dir

    def test_torch_nano(self):
        MyNano().train()

    def test_torch_nano_spawn(self):
        MyNano(num_processes=2, strategy="spawn").train()

    def test_torch_nano_subprocess(self):
        MyNano(num_processes=2, strategy="subprocess").train()

    def test_torch_nano_correctness(self):
        MyNanoCorrectness().train(0.25)

    def test_torch_nano_spawn_correctness(self):
        MyNanoCorrectness(num_processes=2, strategy="spawn").train(0.5)

    def test_torch_nano_subprocess_correctness(self):
        MyNanoCorrectness(num_processes=2, strategy="subprocess").train(0.5)

    def test_torch_nano_attribute_access(self):
        MyNanoAccess().train()

    def test_torch_nano_multi_optimizer(self):
        MyNanoMultiOptimizer().train()


if __name__ == '__main__':
    pytest.main([__file__])
