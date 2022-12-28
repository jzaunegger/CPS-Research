% Clear the command window
clc

% Load the images into a datastore
imds = imageDatastore(fullfile(pwd(), 'tanks-images-resized-224'), ...
    'FileExtensions', '.png', ...
    'IncludeSubfolders', true, ...
    'LabelSource', 'foldernames');

% Split the dataset into training/validation set
[trainSet, validationSet] = splitEachLabel(imds, 0.7);

% Load googlenet
net = resnet50;

% Extract the Layers
if isa(net, 'SeriesNetwork')
    lgraph = layerGraph(net.Layers);
else
    lgraph = layerGraph(net);
end
figure('Units','normalized','Position',[0.1 0.1 0.8 0.8]);
plot(lgraph)

% Determine Input Size
inputSize = net.Layers(1).InputSize;

[learnableLayer,classLayer] = findLayersToReplace(lgraph);
numClasses = numel(categories(trainSet.Labels));
if isa(learnableLayer,'nnet.cnn.layer.FullyConnectedLayer')
    newLearnableLayer = fullyConnectedLayer(numClasses, ...
        'Name','new_fc', ...
        'WeightLearnRateFactor',10, ...
        'BiasLearnRateFactor',10);
    
elseif isa(learnableLayer,'nnet.cnn.layer.Convolution2DLayer')
    newLearnableLayer = convolution2dLayer(1,numClasses, ...
        'Name','new_conv', ...
        'WeightLearnRateFactor',10, ...
        'BiasLearnRateFactor',10);
end

lgraph = replaceLayer(lgraph,learnableLayer.Name,newLearnableLayer);
newClassLayer = classificationLayer('Name','new_classoutput');
lgraph = replaceLayer(lgraph,classLayer.Name,newClassLayer);

% Check new layer is being added properly
figure('Units','normalized','Position',[0.3 0.3 0.4 0.4]);
plot(lgraph)
ylim([0,10])

% Declare Training Parameters
options = trainingOptions('sgdm', ...
    'MiniBatchSize', 25, ...
    'MaxEpochs', 5, ...
    'ExecutionEnvironment', 'gpu', ...
    'InitialLearnRate',1e-4, ...
    'ValidationData',validationSet, ...
    'ValidationFrequency', 10, ...
    'ValidationPatience', Inf, ...
    'Verbose', false, ...
    'Plots', 'training-progress');

% Train the network
net = trainNetwork(trainSet,lgraph,options);

% Classify Validation Set
[YPred,probs] = classify(net,validationSet);
accuracy = mean(YPred == validationSet.Labels)

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

function [learnableLayer,classLayer] = findLayersToReplace(lgraph)

    if ~isa(lgraph,'nnet.cnn.LayerGraph')
        error('Argument must be a LayerGraph object.')
    end

    % Get source, destination, and layer names.
    src = string(lgraph.Connections.Source);
    dst = string(lgraph.Connections.Destination);
    layerNames = string({lgraph.Layers.Name}');

    % Find the classification layer. The layer graph must have a single
    % classification layer.
    isClassificationLayer = arrayfun(@(l) ...
        (isa(l,'nnet.cnn.layer.ClassificationOutputLayer')|isa(l,'nnet.layer.ClassificationLayer')), ...
        lgraph.Layers);

    if sum(isClassificationLayer) ~= 1
        error('Layer graph must have a single classification layer.')
    end
    classLayer = lgraph.Layers(isClassificationLayer);


    % Traverse the layer graph in reverse starting from the classification
    % layer. If the network branches, throw an error.
    currentLayerIdx = find(isClassificationLayer);
    while true

        if numel(currentLayerIdx) ~= 1
            error('Layer graph must have a single learnable layer preceding the classification layer.')
        end

        currentLayerType = class(lgraph.Layers(currentLayerIdx));
        isLearnableLayer = ismember(currentLayerType, ...
            ['nnet.cnn.layer.FullyConnectedLayer','nnet.cnn.layer.Convolution2DLayer']);

        if isLearnableLayer
            learnableLayer =  lgraph.Layers(currentLayerIdx);
            return
        end

        currentDstIdx = find(layerNames(currentLayerIdx) == dst);
        currentLayerIdx = find(src(currentDstIdx) == layerNames);

    end
end