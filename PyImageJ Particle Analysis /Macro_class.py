# creating macro class functions to be called 

class MacroFunctions:
    def __init__(self, image_path, results_path, output_path, threshold_min, threshold_max, scale, unit, save_type, pixels):
        #initalize variables 
        self.image_path = image_path
        self.results_path = results_path
        self.output_path = output_path
        self.threshold_min = int(threshold_min)
        self.threshold_max = int(threshold_max)
        self.scale = float(scale)
        self.unit  = unit
        self.save_type = save_type
        self.pixels = int(pixels)

    def open_image(image_path): 
        '''macro function to open image based on image file path'''
        open_image_macro = f'''open("{image_path}");'''

        return open_image_macro
    
    def set_8bit():
        '''macro function to set image to 8bit image type'''
        macro_8bit = f'''run("8-bit");'''

        return macro_8bit
    
    def set_threshold(threshold_min, threshold_max):
        '''macro function to set image threshold and invert image'''
        macro_threshold = f'''setThreshold({threshold_min}, {threshold_max});'''

        return macro_threshold
    
    def binary_mask():
        '''macro function to apply binary mask onto image'''
        binary_mask = f'''
        run("Invert");
        run("Convert to Mask");'''

        return binary_mask
    
    def set_scale(scale, unit, pixels): 
        '''macro function to implement scale and units'''
        set_scale = f'''run("Set Scale...", "distance={pixels}, known={scale} unit={unit}");'''

        return set_scale
    
    def set_measurements():
        '''macro function to set the measurements for analyzing particles'''
        set_measurements = f'''run("Set Measurements...", "area mean standard min centroid perimeter bounding box fit shape feret's integrated density median skewness kurtosis area_fraction stack position");'''
        
        return set_measurements
    
    def analyze_particles():
        '''macro function to analyze particles'''
        analyze_particles = f'''run("Analyze Particles...","size=0-Infinity");'''

        return analyze_particles
    
    def save_type(save_type, results_path):
        ''' function to save results or preprocessed image'''
        save_as = f'''saveAs("{save_type}", "{results_path}");'''