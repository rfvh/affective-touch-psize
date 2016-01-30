# -*- coding: utf-8 -*-

def lmerTest(filename):
   import rpy2.robjects as ro
   import rpy2.robjects as robjects
   #ro.r('options(warn=-1)')
   
   # names of the timepoints in the csv data 
   tp = 450 # the number of timepoints we have 
   timepoints = []
   for i in range(1,tp+1): 
       timepoints.append('ps' + str(i))
   
  
   pvalues = [] # empty list where the pvalues are going to be stored 
   
   ro.r("psize = read.csv('csv_data/test_lmer.csv')") # reading the data 
   
    
    
        
   for i in range(0,len(timepoints)): # doing the test for every time point 
            
        tp = timepoints[i]
        formula_python = tp + ' ~ conditie + (1 + conditie|pp)'
        formula_r = robjects.r(formula_python)
        ro.globalenv['formula_r'] = formula_r
        ro.r("library(lmerTest)")
       
        try: 
            ro.r("ptest = lmer(formula= formula_r, data = psize)")
            pvalue = ro.r('summary(ptest)$coefficients[2,5]')
            pvalue = pvalue[-1]
            pvalue = float(pvalue)
            pvalues.append(pvalue)
        except: 
            pvalues.append(1.0)
        
   return pvalues 
        
