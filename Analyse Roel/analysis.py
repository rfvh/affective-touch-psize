# -*- coding: utf-8 -*-


# imports 
#############################
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.pylab as pylab
from scipy import stats, optimize
import blinkcorrection
import smoothing
import statistiek 
import csv 
import os
########################################### SETTINGS ##########
aantaltrials = 54 # default is 2x27 = 54

## make and prepare csv file to save data (needed for the statistics) 

output_file_lmer = open('csv_data/test_lmer.csv', 'wb')
output_writer_lmer = csv.writer(output_file_lmer)

timepoints = ['pp', 'conditie']
for i in range(1,451): 
    timepoints.append('ps' + str(i))

output_writer_lmer.writerow(timepoints)    



## empty lists which we need for plotting  
masssnelheid_3 = []
masssnelheid_0_3 = []
masssnelheid_30 = []

# setting for plots & data storage 
show_sem = True
data_opslaan = True

# make list of the data files 
root = os.getcwd() + "/data/"
participanten = os.listdir(root)

###########################################################################################
#################### loop voor de verschillende participanten begint hier ################
#########################################################################################
###################
### empty lists ###
###################
pupilsizestring = [] # data in strings  
pupilsize = []       # data in floats 
snelheid_0_3 = []    # data for the 0.3 cm stroking condition 
snelheid_3 = []      # data for the 3 cm stroking condition
snelheid_30 = []     # data for the 30cm stroking condition
starting_values = [] #  index where every trial begins 
velocity = []        # speed of stroking of every trial  
#############################

for participant in range(0,len(participanten)): 
    print 'working on participant ' + str(participant +1)
    f = open(root + participanten[participant])
    i_line = 0
    for line in f: 
        if len(line.split('\t')) > 12: # de regels die we nodig hebben zijn altijd langer dan 12 
            pupilsizestring.append(line.split('\t')[20]) # 8 = mean,  13 voor linkerpupil, 20 voor rechter
        else: 
            pupilsizestring.append(';')           # have to keep these in, otherwise indices are wrong 
            
        if "snelheid" in line:                         # what condition is this trial? 
            stuk= line.split('\t')[3]
            snelheid = stuk.split(' ')[2]
            snelheid = snelheid.strip()
            velocity.append(snelheid)
            
        if "start_trial" in line:                    # where does this trial begin? 
            starting_values.append(i_line)
        
        i_line = i_line + 1    
    
    pupilsizestring = pupilsizestring[1:len(pupilsizestring)+1]  # titles of the columns should be removed  
   
   ## convert to floats  
    for i in range(0,len(pupilsizestring)):
     if pupilsizestring[i] != ';' and pupilsizestring[i] != '': # voor dat ene .txt bestand 
             pupilsize.append(float(pupilsizestring[i]))
     else:
        pupilsize.append(';')  
                                                                            
    
    ## values needed for blinkcorrection ### 
    gemiddelde = numpy.mean([x for x in pupilsize if x != 0 and x != ';'])
    afwijking = numpy.std([x for x in pupilsize if x != 0 and x != ';'])
    afwijkend_hoog = (3*afwijking) + gemiddelde 
    afwijkend_laag =  gemiddelde - (3*afwijking)
   

    # blinkcorrectie voor data van één participant     
    pupilsize = blinkcorrection.correctiontotal(pupilsize, participant, afwijkend_hoog, afwijkend_laag, gemiddelde )
   
   
    ################################################################################
    ############### loop voor de trials begint hier ################################
    ##############################################################################
    # Hier wordt het signaal uit de data gehaald voor één trial ##
    for t in range(0,aantaltrials):
        
        
        
        ### baseline uit signaal halen: 40 metingen ############ 
        baseline = pupilsize[((50 + (starting_values[t]))):(90+(starting_values[t]))]
        
        ### signaal uit signaal halen: 450 metingen ############
        signal = pupilsize[((90 + (starting_values[t]))):((540 + starting_values[t]))]
        
        ## de baselinecorrectie uitvoeren voor één trial ##  
        signal = signal/numpy.mean(baseline)  
        
        
        ## elke trial opslaan in de bijbehorende categorie ##
        if velocity[t] == '3':
            snelheid_3.append(signal)
           
        elif velocity[t] == '0.3':
            snelheid_0_3.append(signal)
            
        elif velocity[t] == '30':
            snelheid_30.append(signal)
 
        
        ## empty singal and baseline so that they do not influence next trial ###
        signal = []   
        baseline = []   
        
        
        
        
   ########################################################################         
   ################### einde van de loop voor één trial ###################
   ########################################################################   
   
   
    if data_opslaan: # de individuele data (nodig voor de lmer). Dus alle trials per conditie 
         
         for item in snelheid_0_3: 
             output = [(participant +1 ), 1] + list(item)   # in file gecodeerd als conditie 1 
             output_writer_lmer.writerow(output)
             
         for item in snelheid_3: 
             output = [(participant +1 ), 2] + list(item)   # in file gecodeerd als conditie 2 
             output_writer_lmer.writerow(output)   
        
         for item in snelheid_30: 
             output = [(participant +1 ), 3] + list(item)  # in file gecodeerd als conditie 3 
             output_writer_lmer.writerow(output) 
    
    ## data smoothen 
    snelheid_30 = [sum(e)/len(e) for e in zip(*snelheid_30)]   
    snelheid_30_array = numpy.array(snelheid_30)
    snelheid_30 = smoothing.smooth(snelheid_30_array)
    
    snelheid_0_3 = [sum(e)/len(e) for e in zip(*snelheid_0_3)]
    snelheid_0_3array = numpy.array(snelheid_0_3)
    snelheid_0_3 = smoothing.smooth(snelheid_0_3array)
        
    snelheid_3 = [sum(e)/len(e) for e in zip(*snelheid_3)]
    snelheid_3array = numpy.array(snelheid_3)
    snelheid_3 = smoothing.smooth(snelheid_3array)
   
   ## de drie condities samenvoegen tot een lijn per conditie voor alle participanten, deze gebruiken we voor het plotten  ####     
    masssnelheid_3.append(snelheid_3)
    masssnelheid_0_3.append(snelheid_0_3)
    masssnelheid_30.append(snelheid_30)
    
    

   ## dingen leegmaken voor volgende participant 
    snelheid_3 = []
    snelheid_30 = []
    snelheid_0_3 = []
    velocity = []
    pupilsizestring = []
    pupilsize = []
    signal = []

  
    
    
#######################################################################
###################### einde participant-loop #########################
######################################################################
output_file_lmer.close()


## pvalues uitrekenen voor de 450 datapunten 
pvalues = statistiek.lmerTest('csv_data/test_lmer.csv')    
sigvalues = []
for i in range(0,len(pvalues)): 
    if pvalues[i] < 0.05: 
        sigvalues.append(i)

## plotten van de drie condities voor alle participanten         
# de sems uitrekenen per lijn, er één lijn van maken en deze lijn smoothen   

# lijn 1 : 30 cm per seconde wordt oranje
zipped = zip(*masssnelheid_30)
errors_30 = numpy.array([stats.sem(x) for x in zipped])
errors_30 = smoothing.smooth(errors_30)
masssnelheid_30 = [sum(e)/len(e) for e in zip(*masssnelheid_30)] 
x = range(450)
y3 = masssnelheid_30
plt.plot(x,y3,'#FE8702');
if show_sem: 
    plt.fill_between(x, y3-errors_30, y3+errors_30, alpha = 0.2, facecolor='#FE8702'); # oranje


# lijn 2: 0.3 cm per seconde wordt groen
zipped = zip(*masssnelheid_0_3)
errors_0_3 = numpy.array([stats.sem(x) for x in zipped])
errors_0_3 = smoothing.smooth(errors_0_3)
masssnelheid_0_3 = [sum(e)/len(e) for e in zip(*masssnelheid_0_3)] 
x = range(450)
y1 = masssnelheid_0_3
plt.plot(x,y1,'#31B404');
if show_sem: 
    plt.fill_between(x, y1-errors_0_3, y1+errors_0_3, alpha = 0.2, facecolor='#31B404'); # groen



# lijn 3: 3 cm per seconde wordt blauw 
zipped = zip(*masssnelheid_3)
errors_3 = numpy.array([stats.sem(x) for x in zipped])
errors_3 = smoothing.smooth(errors_3)
masssnelheid_3 = [sum(e)/len(e) for e in zip(*masssnelheid_3)] 
x = range(450)
y2 = masssnelheid_3
plt.plot(x,y2,'#2E64FE');
if show_sem: 
    plt.fill_between(x, y2-errors_3, y2+errors_3, alpha = 0.2, facecolor='#2E64FE'); # blauw





        
## plotting the vertical lines for the timepoints where the data sig differs 
for point in sigvalues:
    plt.plot([point, point], [0.90,1.1], color = '#D8D8D8', alpha = 0.1, linewidth=7.0);


## legend and other fancy stuff ###
blue_patch = mpatches.Patch(color='#2E64FE', alpha = 0.2)
green_patch = mpatches.Patch(color='#31B404', alpha = 0.2)
orange_patch = mpatches.Patch(color ='#FE8702', alpha = 0.2)
plt.legend([orange_patch,blue_patch,green_patch],['30 cm/s','3 cm/s','0.3 cm/s'], fontsize = 16)
plt.grid(False)
plt.axis([0,450,0.93,1.03])
pylab.xticks(range(0,480,30),range(0,16),fontsize = 16)
pylab.yticks(fontsize = 16)
plt.xlabel('Time in seconds', fontsize = 20)
plt.ylabel('Pupilsize relative to baseline', fontsize = 20)
figure = plt.gcf() # get current figure
figure.set_size_inches(20, 10)
# saving the figure in the folder plots     
name = 'plot_lmer_' + str(participant+1) + '_participants.png'
plt.savefig('figures/' + name, dpi = 100)





