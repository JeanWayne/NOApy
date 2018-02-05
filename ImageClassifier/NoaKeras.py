
# coding: utf-8

# In[2]:

import keras
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

pContent="/home/jean/Schreibtisch/Images/labeled/2class/"
pContent_val="/home/jean/Schreibtisch/Images/labeled/2class_val"


train_datagen = ImageDataGenerator()
        #rescale=1./255,
        #shear_range=0.2,
        #zoom_range=0.2,
        #horizontal_flip=True)

test_datagen = ImageDataGenerator()#rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        pContent,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        #save_to_dir='/home/jean/train',
        save_prefix="train_")

validation_generator = test_datagen.flow_from_directory(
        pContent_val,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        #save_to_dir='/home/jean/val',
        save_prefix="val_")


# In[3]:

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD


model = Sequential()
# input: 224x224 images with 3 channels -> (224, 224, 3) tensors.
# this applies 32 convolution filters of size 3x3 each.
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(BatchNormalization())
#model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.20))

model.add(Conv2D(64, (3, 3), activation='relu'))
#model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.20))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(2, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
adam= keras.optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

#model.compile(loss='binary_crossentropy', optimizer=sgd)
model.compile(loss='categorical_crossentropy', optimizer=adam)

#model.fit(x_train, y_train, batch_size=32, epochs=10)
#score = model.evaluate(x_test, y_test, batch_size=32)


# In[4]:

from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras import backend as K

# create pre-trained model
base_model = InceptionV3(weights='imagenet', include_top=False)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# add a fully-connected layer
x = Dense(1024, activation='relu')(x)
#  a logistic layer --  we have 2 classes
predictions = Dense(2, activation='softmax')(x)


model = Model(inputs=base_model.input, outputs=predictions)

# first: train only the top layers (which were randomly initialized)
# i.e. freeze all convolutional InceptionV3 layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model (should be done *after* setting layers to non-trainable)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')

# train the model on the new data for a few epochs
model.fit_generator(
        train_generator,
        steps_per_epoch=1000,
        epochs=4,
        verbose=2,
        validation_data=validation_generator,
        validation_steps=2)

# at this point, the top layers are well trained and we can start fine-tuning
# convolutional layers from inception V3. We will freeze the bottom N layers
# and train the remaining top layers.

# let's visualize layer names and layer indices to see how many layers
# we should freeze:
for i, layer in enumerate(base_model.layers):
   print(i, layer.name)

# we chose to train the top 2 inception blocks, i.e. we will freeze
# the first 249 layers and unfreeze the rest:
for layer in model.layers[:249]:
   layer.trainable = False
for layer in model.layers[249:]:
   layer.trainable = True

# we need to recompile the model for these modifications to take effect
# we use SGD with a low learning rate
from keras.optimizers import SGD
model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# we train our model again (this time fine-tuning the top 2 inception blocks
# alongside the top Dense layers
model.fit_generator(
        train_generator,
        steps_per_epoch=1000,
        epochs=4,
        verbose=2,
        validation_data=validation_generator,
        validation_steps=2)


# In[3]:

for i in range(1,4):
    model.fit_generator(
            train_generator,
            steps_per_epoch=2,
            epochs=2,
            verbose=2,
            validation_data=validation_generator,
            validation_steps=2)
    model.save("/home/jean/adam_"+str(i*2)+"_categorical_epochs_v1.h5")
    print("eval "+str(i))
    print(model.evaluate_generator(validation_generator, 2))


# In[8]:

#evals=model.evaluate_generator(validation_generator, 1000)
model.save("/home/jean/InceptionV3_0.06873_1000_4_1000_4.h5")


# In[5]:

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

import matplotlib.pyplot as plt
import numpy as np
#img_path = "/home/jean/Schreibtisch/download.png"
img_path="/home/jean/Bild_Classifier/mongoDB_toClassify/toDo/40/10.5194_tc-9-613-2015_863.jpg"
img = load_img(img_path, target_size=(224, 224))
plt.imshow(img)
plt.show()
x=img_to_array(img)
x.reshape((-1,) + x.shape)
x=np.reshape(x,(-1,224,224,3))
s=model.predict(x)
print(s)


# In[6]:

#### TEST CLASSIFY:
import os
for root, dirs, files in os.walk("/home/jean/toClassify"):
    for file in files:
        if file.endswith(".jpg"):
             #print(os.path.join(root, file))
            img = load_img(os.path.join(root, file), target_size=(224, 224))
            plt.imshow(img)
            plt.show()
            x=img_to_array(img)
            x.reshape((-1,) + x.shape)
            x=np.reshape(x,(-1,224,224,3))
            s=model.predict(x)
            print(s)


# In[ ]:



