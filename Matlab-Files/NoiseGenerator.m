% Clear the command window
clc

% Define System Parameters
image_width = 224;
image_height = 224;
image_sample_count = 1000;
output_dir_n = fullfile(pwd(), 'Images-Test', 'Normal');
output_dir_a = fullfile(pwd(), 'Images-Test', 'Anomaly-A');
output_dir_b = fullfile(pwd(), 'Images-Test', 'Anomaly-B');
output_dir_c = fullfile(pwd(), 'Images-Test', 'Anomaly-C');
output_dir_d = fullfile(pwd(), 'Images-Test', 'Anomaly-D');

% Check that folders exist, and are empty
checkFolder(output_dir_n)
checkFolder(output_dir_a)
checkFolder(output_dir_b)
checkFolder(output_dir_c)
checkFolder(output_dir_d)

samples = image_sample_count / 5;

% Generate Base Samples
for n = 0:samples-1
    filename = string(n) + '.png';
    img_path = fullfile(output_dir_n, filename);
    base_img = zeros(image_width, image_height, 3);
    nois_img = imnoise(base_img, 'gaussian', 0.5, 0.5);
    %gray_img = rgb2gray(nois_img);
    imwrite(nois_img, img_path)
end
disp('Created ' + string(samples) + ' normal samples.')

% Generate anomaly A samples
for a = 0:samples-1
    filename =  string(a) + '.png';
    img_path = fullfile(output_dir_a, filename);
    base_img = zeros(image_width, image_height, 3);
    nois_img = imnoise(base_img, 'gaussian', 0.25, 0.25);
    %gray_img = rgb2gray(nois_img);
    imwrite(nois_img, img_path)   
end
disp('Generated ' + string(samples) + ' samples of anomaly type A.')

% Generate anomaly B samples
for b = 0:samples-1
    filename = string(b) + '.png';
    img_path = fullfile(output_dir_b, filename);
    base_img = zeros(image_width, image_height, 3);
    nois_img = imnoise(base_img, 'gaussian', 0.75, 0.25);
    %gray_img = rgb2gray(nois_img);
    imwrite(nois_img, img_path)   
end
disp('Generated ' + string(samples) + ' samples of anomaly type B.')

% Generate Anomaly C samples
for c = 0:samples-1
    filename = string(c) + '.png';
    img_path = fullfile(output_dir_c, filename);
    base_img = zeros(image_width, image_height, 3);
    nois_img = imnoise(base_img, 'gaussian', 0.5, 0.5);
    
    box_width = randi([5, 20]);
    box_height = randi([5, 20]);
    x_pos = randi(image_width - box_width);
    y_pos = randi(image_height - box_height);
    
    rect_img = insertShape(nois_img, 'FilledRectangle', [x_pos, y_pos, box_width, box_height], 'Color', 'black', 'Opacity', 1); 
    imwrite(rect_img, img_path);
end
disp('Generated ' + string(samples) + ' samples of anomaly type C.')

% Generate Anomaly D samples
for d = 0:samples-1
    filename = string(d) + '.png';
    img_path = fullfile(output_dir_d, filename);
    base_img = zeros(image_width, image_height, 3);
    nois_img = imnoise(base_img, 'gaussian', 0.5, 0.5);
    
    box_width = randi([5, 20]);
    box_height = randi([5, 20]);
    x_pos = randi(image_width - box_width);
    y_pos = randi(image_height - box_height);
    
    rect_img = insertShape(nois_img, 'FilledRectangle', [x_pos, y_pos, box_width, box_height], 'Color', 'white', 'Opacity', 1); 
    imwrite(rect_img, img_path);
end
disp('Generated ' + string(samples) + ' samples of anomaly type D.')


disp('Generated ' + string(image_sample_count) + ' total images.')


% Function that checks if the folder exists, and removes any pre-existing
% images from the folder. If the folder does not exist, it will create the
% folders.
function checkFolder(folderPath)
    if isfolder(folderPath)
        pattern = fullfile(folderPath, '*.png');
        files = dir(pattern);
    
        for f = 1:length(files)
            temp_name = fullfile(folderPath, files(f).name);
            delete(temp_name);
        end
        disp('Removed ' + string(length(files)) + ' images from' + folderPath)
        
    else
        mkdir(folderPath)
    end
end