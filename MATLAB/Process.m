
clear all
close all
THR = 50;

files = dir('Pics/*.jpg');
figure;
hold off;
score = zeros(1,length(files) - 1);
labels = cell (1,length(files) - 1);
for ind = 2:length(files)
    %cla
    im_a = rgb2gray(imread(['Pics/' files(ind).name]));
    im_b = rgb2gray(imread(['Pics/' files(ind-1).name]));
    file_name_cell = regexpi(files(ind).name,'\s(.*).jpg','tokens');
    labels{ind-1} = file_name_cell{1};
    
    diff = abs(im_a - im_b);
    diff_bin = diff > THR;
    diff = diff .* uint8(diff_bin);
    imagesc(diff)
    local_score = sum(sum(diff));
    score(ind-1) = local_score;
    pause(0.1)
    
    
end
figure;
plot(score)
%set(gca, 'XTick',1:length(score),'XTickLabel', labels);
set(gca, 'XTickLabel', labels);
    



