


def correctiontotal(signal,participant, afwijkend_hoog, afwijkend_laag, gemiddelde):
 import numpy
 import scipy as sp
 from scipy.interpolate import interp1d
 from scipy.interpolate import UnivariateSpline 
 f = 0
 
    
 ## velocity ###   
 velocity = [] # hier is velocity de verandering van de lijn ten opzichte van het vorige punt 
 velocity.append(0.0) # de allereerste waarde kan je niet uitrekenen dus dat wordt even 0
 for i in range(1,len(signal)): # de allereerste wordt er op deze manier dus niet uitgehaald
    if signal[i-1] == ';':
        velocity.append(0.0)
    else: 
        try: 
            velocity.append((signal[i]-signal[i-1]))  
        except: 
            velocity.append(0.0) # als de vorige ; was
     
    
    
  ## correct for blinks ###   
 for i in range(0,(len(signal))):
     
     if velocity[i] < (-4.0) or velocity[i] > 4.0 or signal[i] == 0 or signal[i] >= afwijkend_hoog or signal[i] <= afwijkend_laag:  # hier ga je de knippers eruit halen en het signaal herstellen

        # DETERMING ONSET 

        onset = (signal[i-1]) #  onset is the point just before velocity started dropping
        g = 1
        while onset == ';' and g < i: # as long as the onset is ; (so not really signal, go back until you can find the signal just before the velocity started dropping
            onset = signal[i-g]
            g = g +1 
        
        if onset == ';': # if g >1, we could find a value so we take the average 
            onset = gemiddelde
            
        # DETERMINE OFFSET     
            
        if i >=(len(signal)-1): # if this is true, the end of the signal has been reached and you cannot select an offset from the signal    
            if onset != ';': 
                 offset = onset
                 f =1
            else: 
                 print 'einde signaal bereikt voor het kiezen van een goede offset '
           
        else: 
            offset = (signal[i+1])
            f = 1
            while velocity[i+f] < -4.0 or velocity[i+f] >4.0 or velocity[i+f] == 0.0 or offset == ';' or signal[i+f] >= afwijkend_hoog or signal[i+f] <= afwijkend_laag:    # hier stond eerst afwijkend 
                if (i+f) == (len(signal)-1): # einde bereikt 
                    offset = onset
                    if onset != ';': 
                        signal[(len(signal)-1)] = onset 
                        break
                    else: 
                        print 'onset is ;'
                else: 
                    offset = (signal[i+f])
                    f = f +1   
      

         
        filling = numpy.linspace(onset,offset,f) # signaal wordt een lineaire lijn tussen het eerste en laatste punt 
        
        
        
       
        # things for the cubic spline thing  
        t2 = i -1
        t3 = i +f  
        t1= t2-t3+t2
        t4= t3-t2+t3
       
        # see if we can use the cubic spline method, otherwise it'll just be the lineair line 
        if signal[t2] == ';' or signal[t3] == ';':
            pass
            
        elif signal[t1] != ';' and t4 < len(signal)  and signal[t4] != ';' : # omdat je t1 en t4 berekent ten opzichte van de onset en de offset, zouden dit eventueel ; kunnen zijn. in dat geval kan je deze manier dus niet gebruiken
            x1 = [t1,t2,t3,t4]
            y1 = [signal[t1], signal[t2], signal[t3], signal[t4]]
            
            x = numpy.array(x1)
            y = numpy.array(y1)
           
            f1 = interp1d(x, y)
            f2 = interp1d(x, y, kind='cubic')
    
            xnew = numpy.linspace(x.min(), x.max() ,f)
            filling = f2(xnew)
      
      
        
         
        if f == 1: 
            signal[i] = numpy.mean([onset,offset]) # alleen als er maar een waarde met een afwijkende velocity is
        else: 
            signal[i:i+f] = filling
            
     elif velocity[i] >= (-4.0) and velocity[i] <= 4.0 or signal[i] == ';': # no blinks were found in this signal point 
        signal[i] = signal[i]
        
     
         
 return signal
 
 
