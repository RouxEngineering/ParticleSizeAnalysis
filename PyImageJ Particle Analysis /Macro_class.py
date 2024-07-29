'''
Macro functions to be called in PyImageJ
'''
class MacroFunctions:
    def __init__(self, image_path=None, results_path=None, output_path=None, threshold_min=None, threshold_max=None, scale=None, unit=None, pixels=None):
        #initalize variables 
        self.image_path = image_path
        self.results_path = results_path
        self.output_path = output_path
        self.threshold_min = threshold_min
        self.threshold_max = threshold_max
        self.scale = scale
        self.unit  = unit
        self.pixels = pixels

    def open_image(self): 
        '''macro function to open image based on image file path'''
        open_image_macro = f'''open("{self.image_path}");'''

        return open_image_macro
    
    def set_8bit(self):
        '''macro function to set image to 8bit image type'''
        macro_8bit = f'''run("8-bit");'''

        return macro_8bit
    
    def set_threshold(self):
        '''function to return macto for threshold based on user input'''
        macro_threshold = f'''setThreshold({self.threshold_min}, {self.threshold_max});'''

        return macro_threshold
    
    def binary_mask(self):
        '''macro function to apply binary mask onto image'''
        binary_mask = f'''
        run("Invert");
        run("Convert to Mask");'''

        return binary_mask
    
    def set_scale(self): 
        '''macro function to implement scale and units'''

        set_scale = f'''run("Set Scale...", "distance={self.pixels} known={self.scale} unit={self.unit}");'''

        return set_scale
    
    def set_measurements(self):
        '''macro function to set the measurements for analyzing particles'''
        set_measurements = f'''run("Set Measurements...", "area mean standard min centroid perimeter bounding box fit shape feret's integrated density median skewness kurtosis area_fraction stack position");'''
        
        return set_measurements
    
    def analyze_particles(self):
        '''macro function to analyze particles'''
        analyze_particles = f'''run("Analyze Particles...","size=0-Infinity");'''

        return analyze_particles
    
    def save_type(self, save_type, save_path):
        '''sunction to save results or preprocessed image'''
        return f'''saveAs("{save_type}", "{save_path}");'''