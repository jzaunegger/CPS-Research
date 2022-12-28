clc
clear

img_size = [256 256];
file_path = 'tanks-images';
out_folder = 'tanks-images-resized-256';

resizeImages(file_path, out_folder, img_size);


function resizeImages(file_path, out_folder, img_size)
    
    sub_data = dir(file_path);
    sub_data_size = size(sub_data,1);
    
    checkFolder(out_folder, true, true);
    
    disp('------------------------------------------------------------');
    fprintf('The main folder contains %d sub-folders. \n', sub_data_size);
    disp('------------------------------------------------------------');
    for i = 1:sub_data_size
       sub_entry = sub_data(i,:).name;
       if sub_entry ~= '.'
           disp(sub_entry);
           child_path = fullfile(file_path, sub_entry);
           child_out_path = fullfile(out_folder, sub_entry);
           child_path_img = fullfile(child_path, '/*.png');
           
           checkFolder(child_out_path, false, true) 
           
           child_files = dir(child_path_img);
           num_child_files = size(child_files, 1);
           fprintf('  - This folder contains %d files. \n', num_child_files);
           
           for j = 1:size(child_files, 1)
               filename = child_files(j, :).name;
               full_file_path = fullfile(child_path, filename);
               out_file_path = fullfile(child_out_path, filename);
        
               % Read in the file
               cur_img = imread(full_file_path);
               resized_img = imresize(cur_img, img_size);
               imwrite(resized_img, out_file_path);

           end
           fprintf('  - Sucessfully resized this folder. \n');
       end
      
    end
    disp('------------------------------------------------------------');
    disp('Resizing Complete!');
    disp('------------------------------------------------------------');
    
end

    
function checkFolder(folderPath, shouldLog, shouldClear)
    if isfolder(folderPath)
        if shouldClear == true
            pattern = fullfile(folderPath, '*.png');
            files = dir(pattern);
    
            for f = 1:length(files)
                temp_name = fullfile(folderPath, files(f).name);
                delete(temp_name);
            end
        
            if shouldLog == true
                disp('* Removed ' + string(length(files)) + ' images from ' + folderPath)
            end
        end     
    else
        mkdir(folderPath)
        if shouldLog == true
            sprintf('* Generated folder: %s', folderPath);
        end
    end
end
