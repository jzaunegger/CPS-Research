% Clear the command window
clc

% Load the images into a datastore
imds = imageDatastore(fullfile(pwd(), 'tanks-images-resized-224'), ...
    'FileExtensions', '.png', ...
    'IncludeSubfolders', true, ...
    'LabelSource', 'foldernames');

% Split the dataset into training/validation set
[trainSet, validationSet] = splitEachLabel(imds, 0.7);

% Load VGG16
net = vgg19;

% Extract Layer Graph
lgraph = layerGraph(net.Layers());
figure('Units','normalized','Position',[0.1 0.1 0.8 0.8]);
plot(lgraph)

% Determine Input Size
inputSize = net.Layers(1).InputSize;
disp(inputSize)

% Remove the last layer, and replace with new layer
lgraph = removeLayers(lgraph, {'fc8','prob','output'});

numClasses = numel(categories(trainSet.Labels));
newLayers = [
    fullyConnectedLayer(numClasses,'Name','fc','WeightLearnRateFactor',10,'BiasLearnRateFactor',10)
    softmaxLayer('Name','softmax')
    classificationLayer('Name','classoutput')];
lgraph = addLayers(lgraph,newLayers);

% Check new layer is being added properly
lgraph = connectLayers(lgraph,'drop7','fc');

figure('Units','normalized','Position',[0.3 0.3 0.4 0.4]);
plot(lgraph)
ylim([0,10])

% Declare Training Parameters
options = trainingOptions('sgdm', ...
    'MiniBatchSize', 25, ...
    'MaxEpochs',5, ...
    'ExecutionEnvironment', 'gpu',...
    'InitialLearnRate',1e-4, ...
    'ValidationData',validationSet, ...
    'ValidationFrequency', 10, ...
    'ValidationPatience',Inf, ...
    'Verbose',false ,...
    'Plots','training-progress');

% Train the network
net = trainNetwork(trainSet,lgraph,options);

% Classify Validation Set
[YPred,probs] = classify(net,validationSet);
accuracy = mean(YPred == validationSet.Labels);

% Display sample images with predicted labels, and probabilities
idx = randperm(numel(validationSet.Files),36);
figure
for i = 1:36
    subplot(6,6,i)
    I = readimage(validationSet,idx(i));
    imshow(I)
    label = YPred(idx(i));
    title(string(label) + ", " + num2str(100*max(probs(idx(i),:)),3) + "%");
end