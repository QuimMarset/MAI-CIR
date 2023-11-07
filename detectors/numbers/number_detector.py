import os
import torch
from torch.optim import Adam
from torch.utils.data import DataLoader
from torch.nn import (Sequential, ReLU, Linear, Conv1d, 
    CrossEntropyLoss, MaxPool1d, Dropout, Flatten)
from detectors.numbers.custom_dataset import CustomDataset



class NumberDetector:


    def __init__(self, input_features, train_config, num_classes):
        self.batch_size = train_config.batch_size
        self.learning_rate = train_config.learning_rate
        self.l2_decay = train_config.l2_decay
        self.patience = train_config.patience
        self.epochs = train_config.epochs
        self.num_classes = num_classes
        
        self.init_device()
        self.create_model(input_features, train_config.dense_list)
        self.create_optimizer()


    def init_device(self):
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() 
            else 'cpu')


    def create_model(self, input_features, dense_list):
        layers = []
        for i, dense_units in enumerate(dense_list):
            if i == 0:
                linear = Linear(input_features, dense_units)
            else:
                linear = Linear(dense_list[i-1], dense_units)
            layers.append(linear)
            layers.append(ReLU())

        layers.append(Linear(dense_list[-1], self.num_classes))
        self.model = Sequential(*layers)
        self.model.to(self.device)
    
    
    def create_optimizer(self):
        self.loss_function = CrossEntropyLoss()
        self.optimizer = Adam(self.model.parameters(), self.learning_rate, 
            weight_decay=self.l2_decay)


    @classmethod
    def create_test_model(cls, input_features, num_classes, saved_config, load_path):
        instance = cls.__new__(cls)
        instance.num_classes = num_classes
        instance.init_device()
        instance.create_model(input_features, saved_config.dense_list)
        instance.load_model(load_path)
        return instance


    def load_model(self, load_path):
        self.model.load_state_dict(torch.load(load_path))


    def save_model(self, save_path):
        torch.save(self.model.state_dict(), os.path.join(save_path, 'model_checkpoint.pth'))


    def train_epoch(self, train_loader):
        running_loss = 0
        correct_predictions = 0

        for data in iter(train_loader):
            inputs, labels = data
            inputs = inputs.type(torch.FloatTensor)
            labels = torch.argmax(labels, dim=1)

            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.loss_function(outputs, labels)
            loss.backward()
            self.optimizer.step()

            correct_predictions += (torch.argmax(outputs, dim=1) == labels).float().sum()
            running_loss += loss

        epoch_loss = running_loss / len(train_loader)
        epoch_accuracy = correct_predictions / (len(train_loader) * train_loader.batch_size)

        return epoch_loss, epoch_accuracy


    def validate_epoch(self, val_loader):
        running_loss = 0
        correct_predictions = 0

        for data in iter(val_loader):
            inputs, labels = data
            inputs = inputs.type(torch.FloatTensor)
            labels = torch.argmax(labels, dim=1)
            outputs = self.model(inputs)
            loss = self.loss_function(outputs, labels)

            correct_predictions += (torch.argmax(outputs, dim=1) == labels).float().sum()
            running_loss += loss

        epoch_loss = running_loss / len(val_loader)
        epoch_accuracy = correct_predictions / (len(val_loader) * val_loader.batch_size)

        return epoch_loss, epoch_accuracy


    def perform_epoch(self, epoch_number, train_loader, val_loader):
        self.model.train(True)
        train_loss, train_accuracy = self.train_epoch(train_loader)
        self.model.train(False)
        val_loss, val_accuracy = self.validate_epoch(val_loader)
        print(f'Epoch {epoch_number}: train loss: {train_loss:.4f}, train accuracy: {train_accuracy:.4f}' + 
            f' val loss: {val_loss:.4f}, val accuracy: {val_accuracy:.4f}')
        return val_loss


    def create_loader(self, features, labels, shuffle=True):
        dataset = CustomDataset(features, labels, self.num_classes)
        data_loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=shuffle)
        return data_loader


    def train_model(self, train_features, train_labels, val_features, val_labels, save_path):
        best_val_loss = None
        non_improving_counter = 0

        train_loader = self.create_loader(train_features, train_labels)
        val_loader = self.create_loader(val_features, val_labels, shuffle=False)

        for epoch in range(self.epochs):

            val_loss = self.perform_epoch(epoch, train_loader, val_loader)

            if best_val_loss is None or val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_model(save_path)
                non_improving_counter = 0
            
            elif val_loss >= best_val_loss:
                non_improving_counter += 1
                if non_improving_counter >= self.patience:
                    break

        print('Finished Training!')


    def evaluate_model(self, test_features, test_labels, load_path):
        self.load_model(load_path)
        self.model.train(False)
        test_loader = self.create_loader(test_features, test_labels, shuffle=False)
        _, test_accuracy = self.validate_epoch(test_loader)
        print(f'Test accuracy: {test_accuracy}')


    def predict(self, features):
        self.model.eval()
        features = torch.tensor(features)
        features = features.type(torch.FloatTensor)
        outputs = self.model(features)
        predictions = torch.argmax(outputs, dim=1)
        return predictions.numpy()