image resized to optimise feature extraction 
the images go through a pipeline  
 - bin the files into subject folders: bin.py  
- resize: resize.py  
- remove background: removeBg.py  
- remove the backgrounds from all the images in working.py before processing them: remove_background_batch.py  

simplified the algorithm to make the mask binary and check the edges  
 - made the program modular,  
 - moved config to its own file  
 - moved code into mothods and created main loop  

changed fill algorithm to simple check for non zero  
check border algorithm  
