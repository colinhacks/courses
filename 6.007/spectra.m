% Simple spectroscope script - imports image and converts to intensity vs.
% wavelength
% Created by: Michael Peng 6.007 SP13

clear;
clc;
close all;

%% SECTION A: Load your recorded diffraction image
fname = 'fluorescent_example.jpg'; % NEED TO CHANGE

%---Import JPG Image
    raw_image=imread(fname);  %import JPG image  
    
%---Convert RGB to grayscale intensity
    total_intensity = double(rgb2gray(raw_image));

%---Plot the uploaded image
    figure(1);
    pcolor(total_intensity), shading flat, colormap(gray);
    xlabel('Distance [pixel]');
    ylabel('Distance [pixel]');
    title('Loaded image');
    
%% SECTION B: Specify the y-coordinates for your diffraction pattern
lower_ylim = 326; % NEED TO CHANGE
upper_ylim = 370; % NEED TO CHANGE

%---Crops the image down to a horizontal slice of the diffraction pattern
    cropped_data = total_intensity(lower_ylim:upper_ylim,:,:);

%---Average in the y-dimension (assuming emission lines are vertical)
    spectrum_data = mean(cropped_data);
    
%---Re-plot image with cropped boundaries
    figure(1);
    pcolor(total_intensity), shading flat, colormap(gray);
    hold on;
    plot([1 length(spectrum_data)],[upper_ylim upper_ylim],'r');
    plot([1 length(spectrum_data)],[lower_ylim lower_ylim],'r');
    hold off;
    xlabel('Distance [pixel]');
    ylabel('Distance [pixel]');
    title('Cropped image');
    
%---Plot the intensity profile along the diffraction pattern.
    figure(2);
    subplot(2,1,1);imshow(raw_image(lower_ylim:upper_ylim,:,:));
    subplot(2,1,2);plot(spectrum_data);
    axis([1 length(spectrum_data) 0 inf]);
    xlabel('Distance [pixel]');
    ylabel('Intensity [a.u.]');
    title('Diffraction intensity profile');
%% SECTION C: Calibrate the x-axis from slit distance [pixels] to wavelength [nm]
cal_pixel_slit = 454;              % NEED TO CHANGE
cal_pixel_peaks = [230, 170, 130]; % NEED TO CHANGE
cal_wavelength = [436, 542, 612];
   
%---Create an x-array to represent distance from slit [in pixels]
    x = cal_pixel_slit-[1:length(spectrum_data)];
    
%---Calculates slit distance for the 3 calibration peaks [in pixels]
    cal_distance = cal_pixel_slit - cal_pixel_peaks;
    
%---Apply linear fit to the 3 calibration data points
    c = polyfit(cal_distance,cal_wavelength,1);
    a = c(1);
    b = c(2);
    
%---Convert the x-array to wavelength [nm] using y=a*x+b
    y = a*x+b;
    
%---Crop the data to 400-700nm range
    temp = (y>400) .* (y<700);
    I1 = find(temp,1,'first');
    I2 = find(temp,1,'last');
    
%---Plot the intensity profile with a calibrated x-axis
    figure;
    plot(y(I1:I2), spectrum_data(I1:I2));
    xlabel('Wavelength (nm)');
    ylabel('Intensity [a.u.]');
    title('Calibrated Spectrum');