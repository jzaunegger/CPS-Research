%{
    This script is intended to function as a pre-processor for the Tanks
    Dataset. This dataset contains date/time values, register numbers, and
    sensor readings for various sensors in a automatic water balancing
    system. 
%}

% Main Script
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc
tanks_dir = 'tanks-dataset/*.csv';
tanks_files = dir(tanks_dir);
num_files = length(tanks_files);
full_file_paths = strings(0);

names_array = strings(0);
stats_array = [];

disp('------------------------------------------------------------------------------------------------')
disp('There are csv files in the tanks directory.')
disp('------------------------------------------------------------------------------------------------')

% Loop through files
for k=1:length(tanks_files)
    % Determine file paths
    full_path = fullfile(tanks_files(k).folder, tanks_files(k).name);
    full_file_paths(end+1) = full_path;
    
    % Process a table
    current_values = processTable(full_path, false);
    
    % Determine the Output Folder
    output_folder = dir('tanks-images');
    cur_file_name = getFilename(full_path);
    cur_file_name = replace(cur_file_name, ' ', '-');
    
    tanks_dir = fullfile(pwd, 'tanks-images', cur_file_name);
    
    % Log Information
    fprintf('* %s\n', tanks_files(k).name);
    fprintf('   > Parent Folder: %s\n', tanks_files(k).folder);
    fprintf('   > File Path: %s\n', full_path);
    
    % Calculate stats, generate values, convert2images
    [averages, mins, maxs] = calcStats(current_values, false);
    
    %table_obj = [cur_file_name; ' ' ; ' '; ' '; ' '; ' '; ' '; ' '; ' '; ' ';];
    col1 = [1; 2; 3; 4; 5; 6; 7; 8; 9; 10;];
    curr_stats_table = table(col1, averages', mins', maxs');
    curr_stats_table.Properties.VariableNames = {'Register', 'Avgs', 'Mins', 'Maxs'}; 
    curr_table_arr = table2array(curr_stats_table);
    
    names_array(end+1) = cur_file_name;
    stats_array = [stats_array curr_table_arr];
    
    convertToImages(current_values, 20, 10, 10, tanks_dir)
    disp(' ');
end

% Determine the parent path to the dataset
image_ds_path = 'tanks-images';
balanceImageDataset(image_ds_path, stats_array, names_array)
disp('------------------------------------------------------------------------------------------------')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%{
    This function processes a file and converts the data to a table, and
    optionally lets you plot the data.

    * Input
        - file_path
            * A path to the input file.
        - should_plot
            * A boolean value that determines if the function generates a
            plot of the input data
    
    * Output
        - values
            * The matrix of data from the original input source.
            * Returns with a shape of NUM_REGISTERS X NUM_ENTRIES
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Extract the table from the file, and return the formatted register data
% Optionally allows you to plot the values
function values = processTable(file_path, should_plot)

    % Extract the current table
    opts = detectImportOptions(file_path);
    opts = setvaropts(opts, 'TimeStamp', 'InputFormat', 'MM/dd/uuuu HH:mm:ss.SSS');
    
    % 'PreserveVariableNames', true
    current_table = readtable(file_path, opts);
    current_table.Properties.VariableNames = {'TimeStamp', 'Register', 'Value'};
    
    % Extract Registers Numbers and Values
    current_regs = current_table.Register;
    current_vals = current_table.Value;
    valSize = size(current_vals,1);
    
    % Create Column of Register Numbers
    col1 = [1; 2; 3; 4; 5; 6; 7; 8; 9; 10;];

    values = reshape(current_vals, 10, []);
    sub_values = [col1, values];
    data_size = size(values);

    
    if should_plot == true
         plot(vals2')
        xlabel('Sensor Readings') 
        ylabel('Sensor Values') 
        title(getFilename(full_file_paths(1)) + ' Sensor Values')
        sensor_names = {'Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5','Sensor 6', 'Sensor 7', 'Sensor 8', 'Sensor 9', 'Sensor 10'};
        legend(sensor_names, 'Location', 'eastoutside')
    end

end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{
    This function determines the number of files in each class, and
    generates samples to make all of the classes file count even.

    * Input
        - folder_path
            * A path to the image dataset.
        - stats_array
            A 10xN matrix, where the rows represent various registers,
            and columns are statistical data. The data is all file stats
            with each entry containing 4 columns. The columns match the
            output listed below.
        - names_array
            * A 1xN row vector of file names.

%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Balance the number of images in the classification folders to be equal,
% according to the folder with the largest amount. 
function balanceImageDataset(folder_path, stats_array, names_array)
    disp('Balancing Dataset');
    data = dir(folder_path);
    size_x = size(data, 1);
    fprintf('There are %d subfolders. \n', size_x-2);
    disp('------------------------------------------------------------------------------------------------')
    
    max_file_size = 0;
    
    % Determine the largest file size
    for i = 1:size_x
        filename = data(i,:).name;
        if filename ~= '.'
            sub_folder_path = fullfile(folder_path, filename);
            file_size = getFileSize(sub_folder_path);
            if file_size > max_file_size
                max_file_size = file_size;
            end    
        end
    end
    
    % Calculate the size differences, and generate the samples
    for j = 1:size_x
         filename = data(j,:).name;
         if filename ~= '.'
            sub_folder_path = fullfile(folder_path, filename);
            
            % Get file size and compute difference
            file_size = getFileSize(sub_folder_path);
            diff = max_file_size - file_size;
            
           %fprintf('The maximum file size is %d.\n', max_file_size);
           %fprintf('This folder contains %d images. \n', file_size);
           %fprintf('The difference is %d. \n', diff);
            
            if diff == 0
                sprintf('Dataset Already Balanced');
                
            else
                % Get Stats for Image Generation
                stats = retrieveStatsFromName(stats_array, names_array, filename);
                mins = stats(:,3)'; 
                maxs = stats(:,4)'; 

                % Generate the Images
                generated_data = generateValues(diff, mins, maxs, false);
            
                % Save The Images
                y_idx = 1;
                for i = file_size: diff+file_size
                   img_name = sprintf('Img-%d.png', i);
                   file_path = fullfile(sub_folder_path, img_name);
                   matrix_data = generated_data(:, y_idx:y_idx+9);
                   new_mat = constrainMatrix(matrix_data, 0, 9000 , 0, 255);
                   rgb_img = gray2rgb(new_mat);
                   imwrite(rgb_img, file_path);
                end

                % Log Info
                new_size = getFileSize(sub_folder_path);
                fprintf('* Folder: %s \n', filename);
                fprintf('   > This folder has %d files. \n', file_size);
                fprintf('   > This folder needed %d more files. \n', diff);
                fprintf('   > This folder now contains %d files. \n', new_size);
            end
        end
    end
    
    disp('------------------------------------------------------------------------------------------------')
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{
    This function returns a matrix of statistics from a given array of
    stats, names, and name.

    * Input
        - stats_array
            * A 10xN matrix, where the rows represent various registers,
            and columns are statistical data. The data is all file stats
            with each entry containing 4 columns. The columns match the
            output listed below.
        - names_array
            * A 1xN row vector of file names.
        - name
            * The given filename to find statistics for.

    * Outuput
        - Stats Matrix 
           * Col1 - Register ID Numbers
           * Col2 - Average Register Values
           * Col3 - Minimum Register Values
           * Col4 - Maximum Register Values
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Retrieve the stats from a given name
function stats = retrieveStatsFromName(stats_array, names_array, name)
    for idx = 1:length(names_array)
       if name == names_array(idx) 
            if idx > 1  
                stats_end_idx = idx * 4;
                stats_start_idx = stats_end_idx - 3;
            else
                stats_end_idx = 4;
                stats_start_idx = 1;
            end
            
            stats = stats_array(:, stats_start_idx:stats_end_idx);
       end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{
    This function returns the number of files found in a given path.

    * Input
        - folder_path
            * The path of the folder to count files in.

    * Outuput
        - file_Size
            * The number of files found in that folder.
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Calculate the number of child elements a given path has
function file_size = getFileSize(folder_path)
    folder_data = dir(folder_path);
    file_size = size(folder_data, 1);
    file_size = file_size - 2;
end

%{
    This function takes statistical data, and generates N images of IxJ
    dimension to a given path.

    Input
        - value_data
        - amountOfSyntheticData
            * The number of extra images to generate when writing the
            original data.
        - imageX
            * The X dimension of the image.
        - imageY
            * The Y dimension of the image.
        - imagePath
            * The path to the folder to save the images in.
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Convert Data into Images
function convertToImages(valueData, amountOfSyntheticData, imageX, imageY, imagePath)

    % Calculate data statistics
    [averages, mins, maxs] = calcStats(valueData, false);
    [size_X, size_Y] = size(valueData);
    
    % Determine the number of images to make
    new_samples_needed =  10 - mod(size_Y, 10);
    
    if new_samples_needed > 0
        total_gen_size = new_samples_needed + amountOfSyntheticData;
    else
        total_gen_size = amountOfSyntheticData;
    end
    
    % Log the number total number of samples to generate
    genData = generateValues(total_gen_size, mins, maxs, false);
    
    % Log the number total number of samples
    totalData = [valueData genData];
    [tot_X, tot_Y] = size(totalData);
    
    disp('   > Conversion Data')
    fprintf('      o The input data has %d samples. \n', size_X, size_Y);
    fprintf('      o The %d will be generated to balance the dataset. \n', total_gen_size);
    fprintf('      o The size of the total image dataset is %d x %d. \n', tot_X, tot_Y);
    
    % Check if output folder exists
    checkFolder(imagePath, false, true)
    
    % Convert to Images
    if mod(tot_Y, imageY) == 0
       num_images = tot_Y / 10;
       fprintf('      o Generating %d images with size %d x %d. \n', num_images, imageX, imageY) 
       disp('      o Saving Images to: ' + string(imagePath));


       y_idx = 1;
       for img_num = 1:num_images
           img_name = sprintf('Img-%d.png', img_num);
           file_path = fullfile(imagePath, img_name);
           matrix_data = totalData(:, y_idx:y_idx+9);
           new_mat = constrainMatrix(matrix_data, 0, 9000 , 0, 255);
           rgb_img = gray2rgb(new_mat);
           imwrite(rgb_img, file_path);
       end
        
    else
        error('Error: There is a size mismatch. The width of the images should evenly divide the size of the image data matrix.')  
    end
   
end

%{
    This function checks if a given path is a folder that exists, and makes
    it if it does not exist, or clears it if it does exist. 

    * Input
        - folder_path
            * The path of the folder to check.
        - shouldLog
            * A boolean variable to set if the function should log data or
            not.
%}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Check if a folder exists, if it does removes all png files, if not it
% creates the folder
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
                disp('   > Removed ' + string(length(files)) + ' images from ' + folderPath)
            end
        end     
    else
        mkdir(folderPath)
        if shouldLog == true
            disp('   > Generated folder: ' + folderPath)
        end
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{
    Generate register signals that match the statistical information
    gathered from the original dataset.

    * Input
        - N
            * The number of sample entries to generate.
        - mins
            * A column array of minimum register values.
        - maxs
            * A column array of maximum register values.
        - log
            * A boolean variable to set if the function should log data or
            not.


    * Outuput
        - new_files
            * The generated signal data.
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generate N number of sensor values
function new_values = generateValues(N, mins, maxs, log)
    if size(mins) == size(maxs)
        sizeX = size(mins, 2);
        new_values = zeros(10, N);

        % Loop Through Each Row
        for i = 1:sizeX
           cur_min = mins(1, i);
           cur_max = maxs(1, i);

           % Loop Through Each Column
           for j = 1:N
               
              rand_val = randi([cur_min,cur_max],1,1);
               
              %rand_val = cur_min + rand*(cur_max-cur_min);
              new_values(i,j) =  rand_val;
           end
        end
        
        [n_x, n_y] = size(new_values);
        if log == true
            fprintf('A Synthetic Matrix of size %d x %d was generated. \n', n_x, n_y);
        end
    else
        error('Error: The sizes of avgs, mins, and maxes must match.')
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{
    This function takes in the input data and calculates the average,
    minimum, and maximum values for each register in the data.

    * Input
        - data
            * The table generated by matlab from a input file.
        - log
            * A boolean variable that determines if the function logs data
            or not.


    * Outuput
        - aves
            * A array of average register values.
        - mins
            * A array of minimum register values.
        - maxs
            * A array of maximum register values.
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generate the averages, mins, and maxes of data
function [aves, mins, maxs] = calcStats(data, log)

    data(isnan(data))=0;
    aves = zeros(1, 10);
    mins = zeros(1, 10);
    maxs = zeros(1, 10);

    % Log Header
    if log == true
        disp('--------------------------------------------')
        disp('Statistical Data for')
        disp('--------------------------------------------')
    end

    % Calc Stats
    for k = 1:10
       x_avg = mean(data(k, :));  
       aves(1, k) = round(x_avg);

       x_min = min(data(k, :));  
       mins(1, k) = round(x_min);

       x_max = max(data(k, :));  
       maxs(1, k) = round(x_max); 
       
       if log == true
          fprintf('Sensor %d Avg.: %d \n', k, x_avg);
          fprintf('Sensor %d Max.: %d \n', k, x_max);
          fprintf('Sensor %d Min.: %d \n', k, x_min);
          disp('--------------------------------------------')     
       end
    end
end

function [Image]= gray2rgb(Image)
%Gives a grayscale image an extra dimension
%in order to use color within it
[m n]=size(Image);
rgb=zeros(m,n,3);
rgb(:,:,1)=Image;
rgb(:,:,2)=rgb(:,:,1);
rgb(:,:,3)=rgb(:,:,1);
Image=rgb/255;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function mat = constrainMatrix(old_mat, old_min, old_max, new_min, new_max)
    mat = old_mat;
    
    [mat_x, mat_y] = size(old_mat);
    for i = 1:mat_x
       for j = 1:mat_y
          cur_val = mat(i,j);
          new_val = (cur_val - old_min) / (old_max - old_min) * (new_max - new_min) + new_min;
          mat(i,j) = round(new_val);
       end
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%{
    This function takes a filepath and returns just the filename.

    * Input
        - path
            * The path to the file.


    * Outuput
        - name
            * The name of the file.
%}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Returns the file name given the full path
function name = getFilename(path)
    [filepath,name,ext] = fileparts(path) ;
    name = replace(name, '_', ' ');   
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%