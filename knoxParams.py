"""
knoxParams.py 

netParams is a dict containing a set of network parameters using a standardized structure

simConfig is a dict containing a set of simulation configurations using a standardized structure

refs:
Z. F. Mainen and T. J. Sejnowski (1996) Influence of dendritic structure on 
firing pattern in model neocortical neurons. Nature 382: 363-366. 

Destexhe, A., Bal, T., McCormick, D.A. and Sejnowski, T.J. Ionic mechanisms 
underlying synchronized oscillations and propagating waves in a model of 
ferret thalamic slices. Journal of Neurophysiology	76: 2049-2070, 1996.

Bazhenov, M., Timofeev, I., Steriade, M., & Sejnowski, T. J. (2002). Model of 
thalamocortical slow-wave sleep oscillations and transitions to activated states. 
Journal of neuroscience, 22(19), 8691-8704.

Wei, Y., Krishnan, G. P., & Bazhenov, M. (2016). Synaptic mechanisms of memory 
consolidation during sleep slow oscillations. Journal of Neuroscience, 36(15), 4231-4247.

Contributors: xxx@xxxx.com
"""

from netpyne import specs
from netpyne import sim 

import random as rnd
import numpy as np

def smallWorldConn(NPre, NPost, p, K):
    ''' k is smallwordness parameters
    K is ratio of connections from each pre cell to post cells
    if p=0 regular network
    if p between 0 and 1 small-world network and
    if p=1 random network 
    '''
    connMat=[]
    for i in range(NPre):
        for j in np.arange(-1*int(NPost*K/2),int(NPost*K/2)+1):
            connMat.append([i,(NPost + i + j) % NPost])
    if p:
        connects = [x for x in range(len(connMat))]
        rnd_ind = rnd.sample(connects, int(len(connMat)*p))
        for i in rnd_ind:
            connMat[i][1]=rnd.randint(0,NPost-1)
    return connMat

"""
import matplotlib.pyplot as plt 
connMat=smallWorldConn(N_TC,N_IN,0.1,0.1)

for i in range(len(connMat)):
    plt.plot(connMat[i][0],connMat[i][1],'ro')

"""

netParams = specs.NetParams()   # object of class NetParams to store the network parameters
simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration

###############################################################################
#
# MPI HH TUTORIAL PARAMS
#
###############################################################################

###############################################################################
# NETWORK PARAMETERS
###############################################################################
N=100; N_PY=N; N_IN=N/2; N_TC=N/4; N_RE=N/4;
netParams.narrowdiam = 5
netParams.widediam = 10

netParams.xspacing = 20 # um
netParams.yspacing = 100 # um

netParams.axondelay = 0

###############################################################################
# Population parameters
###############################################################################
### Cortical Cells
netParams.popParams['PY'] = {'cellType': 'PY', 'numCells': N_PY, 'cellModel': 'HH_PY', 'ynormRange': [0.1, 0.3]} #, 'yRange': [1*netParams.yspacing,1*netParams.yspacing], 'gridSpacing': netParams.xspacing}
netParams.popParams['IN'] = {'cellType': 'IN', 'numCells': N_IN, 'cellModel': 'HH_IN', 'ynormRange': [0.35, 0.45]} #, 'yRange': [2*netParams.yspacing,2*netParams.yspacing], 'gridSpacing': netParams.xspacing} 

### Thalamic cells    
netParams.popParams['TC'] = {'cellType': 'TC', 'numCells': N_TC, 'cellModel': 'HH_TC', 'ynormRange': [0.65, 0.75]} #, 'yRange': [2+3*netParams.yspacing,2+3*netParams.yspacing], 'gridSpacing': netParams.xspacing}
netParams.popParams['RE'] = {'cellType': 'RE', 'numCells': N_RE, 'cellModel': 'HH_RE', 'ynormRange': [0.8, 0.9]} #, 'yRange': [2+4*netParams.yspacing,2+4*netParams.yspacing], 'gridSpacing': netParams.xspacing}


###############################################################################
# Cell parameters list
###############################################################################
"""
### PY (single compartment)
cellRule = netParams.importCellParams(label='PYrule', conds={'cellType': 'PY', 'cellModel': 'HH_PY'},	fileName='sPY.tem', cellName='sPY')
cellRule['secs']['soma']['mechs']['hh2']={'gnabar': 0.05, 'gkbar': 0.005, 'vtraub': -55.0}
cellRule['secs']['soma']['mechs']['pas']={'g': 1.0e-4, 'e': -70}
cellRule['secs']['soma']['mechs']['im']={'gkbar': 7e-5}
netParams.cellParams['PYrule'] = cellRule

### IN (single compartment)
cellRule = netParams.importCellParams(label='INrule', conds={'cellType': 'IN', 'cellModel': 'HH_IN'},	fileName='sIN.tem', cellName='sIN')
cellRule['secs']['soma']['mechs']['hh2']={'gnabar': 0.05, 'gkbar': 0.01, 'vtraub': -55.0}
cellRule['secs']['soma']['mechs']['pas']={'g': 1.5e-4, 'e': -70}

cellRule['secs']['soma']['vinit']=-80
netParams.cellParams['INrule'] = cellRule
"""

### mPY (multi compartment) (Mainen and Sejnowski, 1996)
cellRule = netParams.importCellParams(label='mPYrule', conds={'cellType': 'PY', 'cellModel': 'HH_PY'},	fileName='mPYr.tem', cellName='mPYr')
#cellRule = netParams.importCellParams(label='mPYrule', conds={'cellType': 'PY', 'cellModel': 'HH_PY'},	fileName='mPYr.py', cellName='mPYr')

"""
cellRule['secs']['dend']['mechs']['pas']={'g': 3.3e-5, 'e': -70}
cellRule['secs']['dend']['mechs']['kca']={'gmax': 3e-4}
cellRule['secs']['dend']['mechs']['na']={'gbar': 1.5e-3}
cellRule['secs']['dend']['mechs']['ca']={'gbar': 1e-5}
cellRule['secs']['dend']['mechs']['km']={'gmax': 1e-5}

cellRule['secs']['soma']['mechs']['na']={'gbar': 3}
cellRule['secs']['soma']['mechs']['kv']={'gmax': 0.2}
"""
netParams.cellParams['mPYrule'] = cellRule

### mIN (multi compartment) (Mainen and Sejnowski, 1996)
cellRule = netParams.importCellParams(label='mINrule', conds={'cellType': 'IN', 'cellModel': 'HH_IN'},	fileName='mINr.tem', cellName='mINr')
#cellRule = netParams.importCellParams(label='mINrule', conds={'cellType': 'IN', 'cellModel': 'HH_IN'},	fileName='mINr.py', cellName='mINr')

"""
cellRule['secs']['dend']['mechs']['pas']={'g': 3.3e-5, 'e': -70}
cellRule['secs']['dend']['mechs']['kca']={'gmax': 3e-4}
cellRule['secs']['dend']['mechs']['na']={'gbar': 1.5e-3}
cellRule['secs']['dend']['mechs']['ca']={'gbar': 1e-5}
cellRule['secs']['dend']['mechs']['km']={'gmax': 1e-5}

cellRule['secs']['soma']['mechs']['na']={'gbar': 3}
cellRule['secs']['soma']['mechs']['kv']={'gmax': 0.2}
"""
netParams.cellParams['mINrule'] = cellRule

### TC (Destexhe et al., 1996; Bazhenov et al.,2002)
cellRule = netParams.importCellParams(label='TCrule', conds={'cellType': 'TC', 'cellModel': 'HH_TC'}, fileName='TC.tem', cellName='sTC')
#cellRule = netParams.importCellParams(label='TCrule', conds={'cellType': 'TC', 'cellModel': 'HH_TC'}, fileName='TC.py', cellName='sTC')
"""
cellRule['secs']['soma']['mechs']['hh2']={'gnabar': 0.09, 'gkbar': 0.01, 'vtraub': -25.0}
cellRule['secs']['soma']['mechs']['pas']={'g': 1e-5, 'e': -70-20}
cellRule['secs']['soma']['mechs']['it']={'shift': 2.0, 'gcabar': 2.3e-3, 'q10': 3.0}
cellRule['secs']['soma']['mechs']['iar']={'shift': 0.0, 'ghbar': 1.5e-5}
cellRule['secs']['soma']['mechs']['cad']={'taur': 5.0, 'depth': 1.0, 'kt': 0.0, 'cainf': 2.4e-4, 'kd': 0.0}
cellRule['secs']['soma']['ions']['ca']={'e': 120}
cellRule['secs']['soma']['pointps']['kleak_0']['gmax']= 3e-5 # 0-0.03 mS/cm^2 for TC
"""
netParams.cellParams['TCrule'] = cellRule

### RE (Destexhe et al., 1996; Bazhenov et al.,2002)
cellRule = netParams.importCellParams(label='RErule', conds={'cellType': 'RE', 'cellModel': 'HH_RE'}, fileName='RE.tem', cellName='sRE')
"""
cellRule['secs']['soma']['mechs']['hh2']={'gnabar': 0.1, 'gkbar': 0.01, 'vtraub': -55.0}
cellRule['secs']['soma']['mechs']['pas']={'g': 5e-5, 'e': -77}
cellRule['secs']['soma']['mechs']['it2']={'shift': 2.0, 'gcabar': 2.3e-3, 'qm': 5.0, 'qm': 3.0}
cellRule['secs']['soma']['mechs']['cad']={'taur': 5.0, 'depth': 1.0, 'kt': 0.0, 'cainf': 2.4e-4, 'kd': 0.0}
cellRule['secs']['soma']['ions']['ca']={'e': 120}
cellRule['secs']['soma']['pointps']['kleak_0']['gmax']= 5e-6  # 0.005 mS/cm^2 for RE
cellRule['secs']['soma']['vinit']=-80
"""
netParams.cellParams['RErule'] = cellRule

###############################################################################
# Synaptic mechanism parameters
###############################################################################
# AMPA
netParams.synMechParams['AMPA'] = {'mod': 'ExpSyn', 'tau': 0.1, 'e': 0}

# AMPA_S
#netParams.synMechParams['AMPA_S'] = {'mod': 'Exp2Syn', 'tau1': 0.05, 'tau2': 5.3, 'e': 0}  # AMPA
netParams.synMechParams['AMPA_S'] = {'mod': 'AMPA_S', 'Cmax': 0.5, 'Cdur': 0.3, 'Alpha': 0.94, 'Beta': 0.18, 'Erev': 0} #}

# NMDA
netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 0.15, 'tau2': 15, 'e': 0}  # NMDA
#netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cmax': 1.0, 'Cdur': 1.0, 'Alpha': 0.072, 'Beta': 0.0066, 'Erev': 0} #}

# GABAa_S
#netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAA
netParams.synMechParams['GABAA70'] = {'mod': 'GABAa_S', 'Cmax': 0.5, 'Cdur': 0.3, 'Alpha': 20, 'Beta': 0.162, 'Erev': -70} # }  # GABAA
netParams.synMechParams['GABAA80'] = {'mod': 'GABAa_S', 'Cmax': 0.5, 'Cdur': 0.3, 'Alpha': 20, 'Beta': 0.162, 'Erev': -80} # }  # GABAA
netParams.synMechParams['GABAA85'] = {'mod': 'GABAa_S', 'Cmax': 0.5, 'Cdur': 0.3, 'Alpha': 20, 'Beta': 0.162, 'Erev': -85} # }  # GABAA

# GABAb_S
#netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAB
netParams.synMechParams['GABAB'] = {'mod': 'GABAb_S', 'Cmax': 0.5, 'Cdur': 0.3, 'K1': 0.09, 'K2': 0.0012, 'K3': 0.18, 'K4': 0.034, 'KD': 100, 'Erev': -95} # }  # GABAB

###############################################################################
# Stimulation parameters
###############################################################################
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 0.2, 'noise': 0.5}
#netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'number': 10, 'noise': 0.1}

netParams.stimTargetParams['bgCrx'] = {'source': 'bkg', 'conds': {'cellType': ['PY', 'IN']}, 
                                            'weight': 0*2*0.5, 'delay': 'uniform(1,5)', 'synMech': 'AMPA_S'}  
netParams.stimTargetParams['bgThl'] = {'source': 'bkg', 'conds': {'cellType': ['TC'], 'cellList': [10]}, 
                                            'weight': 0*0.5, 'delay': 'uniform(1,5)', 'synMech': 'AMPA_S'}
#netParams.stimTargetParams['bg->sIN'] = {'source': 'bkg', 'conds': {'cellType': 'IN', 'cellModel': 'HH'}, 
#                                            'weight': 1, 'delay': 'uniform(1,5)', 'synMech': 'AMPA_S'}  

#netParams.stimTargetParams['bg->PYR_HH'] = {'source': 'bkg', 'conds': {'cellType': 'PYR', 'cellModel': 'HH'}, 
#                                            'weight': 1, 'synMech': 'AMPA', 'sec': 'dend', 'loc': 1.0, 'delay': 'uniform(1,5)'}

###############################################################################
# Connectivity parameters
###############################################################################
####################### intra cortikal projections ############################
p=1.0 # small-world-ness param
K=0.1 # connectivity param

netParams.connParams['PY->PY'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0.1,            # 0.08 - 0.15 uS (Bazhenov et al.,2002)
    #'weight': 0.08,            # (Wei et al., 2016)
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'AMPA_S',
    'sec': 'dend',                          # section to connect to
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.05} # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_PY,N_PY,p,K)}   

netParams.connParams['PY->PY'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0*0.01,           # (Bazhenov et al.,2002)         
    #'weight': 0*0.006,            # (Wei et al., 2016)           
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'NMDA',
    'sec': 'dend',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.05}  # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_PY,N_PY,p,K)}   

netParams.connParams['PY->IN'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'IN'},
    'weight': 0.05,           # (Bazhenov et al.,2002)         
    #'weight': 0.08,         # (Wei et al., 2016)           
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'AMPA_S',
    'sec': 'dend',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.02} # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_PY,N_IN,p,K)}  

netParams.connParams['PY->IN'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'IN'},
    'weight': 0*0.008,           # (Bazhenov et al.,2002)         
    #'weight': 0*0.005,        # (Wei et al., 2016)               
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'NMDA',
    'sec': 'dend',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.02} # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_PY,N_IN,p,K)}  

netParams.connParams['IN->PY_GABAA'] = {
    'preConds': {'popLabel': 'IN'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0.05,        # (Bazhenov et al.,2002) 
    #'weight': 0.25,         # (Wei et al., 2016)  
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'GABAA70',
    'sec': 'dend',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.05} # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_IN,N_PY,p,K)}  


###################### intra thalamic projections #############################
netParams.connParams['TC->RE'] = {
    'preConds': {'popLabel': 'TC'}, 
    'postConds': {'popLabel': 'RE'},
    'weight': 0.5*0.4,         # (Bazhenov et al.,2002)            
    #'weight': 0.35,         # (Wei et al., 2016)             
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    'sec': 'soma',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.4}  # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}  

netParams.connParams['RE->RE'] = {
    'preConds': {'popLabel': 'RE'}, 
    'postConds': {'popLabel': 'RE'},
    'weight': 0.1*0.2,            # (Bazhenov et al.,2002)         
    #'weight': 0.125,            # (Wei et al., 2016)        
    'delay': netParams.axondelay, 
    'synMech': 'GABAA80',
    'sec': 'soma',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.4}   # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}  

netParams.connParams['RE->TC_GABAA'] = {
    'preConds': {'popLabel': 'RE'}, 
    'postConds': {'popLabel': 'TC'},
    'weight': 0.1*0.2,         # (Bazhenov et al.,2002)              
    #'weight': 0.15,         # (Wei et al., 2016)               
    'delay': netParams.axondelay, 
    'synMech': 'GABAA85',
    'sec': 'soma',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.4}   # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}  

netParams.connParams['RE->TC_GABAB'] = {
    'preConds': {'popLabel': 'RE'}, 
    'postConds': {'popLabel': 'TC'},
    'weight': 0.04,         # (Bazhenov et al.,2002)             
    #'weight': 0.04,         # (Wei et al., 2016)             
    'delay': netParams.axondelay, 
    'synMech': 'GABAB',
    'sec': 'soma',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0.4}  # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}  

################# thalamo-cortical projections ################################
netParams.connParams['PY->RE'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'RE'},
    'weight': 0.05,           # (Bazhenov et al.,2002)     
    #'weight': 0.05,           # (Wei et al., 2016)      
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'AMPA_S',
    'sec': 'soma',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0*0.4} # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_PY,N_RE,p,K)}  

netParams.connParams['PY->TC'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'TC'},
    #'weight': 0.025,           # 0.08-0.025 uS (Bazhenov et al.,2002)     
    'weight': 0.005,       # (Wei et al., 2016)  
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'AMPA_S',
    'sec': 'soma',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0*0.4}  # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_PY,N_TC,p,K)} 

netParams.connParams['TC->PY'] = {
    'preConds': {'popLabel': 'TC'}, 
    'postConds': {'popLabel': 'PY'},
    #'weight': 0.1,        # (Bazhenov et al.,2002)     
    'weight': 1.5*0.1,        # (Wei et al., 2016)      
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'AMPA_S',
    'sec': 'dend',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0*0.1} # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_TC,N_PY,p,K)}

netParams.connParams['TC->IN'] = {
    'preConds': {'popLabel': 'TC'}, 
    'postConds': {'popLabel': 'IN'},
    #'weight': 0.1,        # (Bazhenov et al.,2002)  
    'weight': 2*0.05,        # (Wei et al., 2016)  
    'delay': netParams.axondelay, 
    'loc': 0.5,
    'synMech': 'AMPA_S',
    'sec': 'dend',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    #'probability': 0*0.04} # (Bazhenov et al.,2002; Wei et al., 2016)
    'probability': 0.1}
    #'connList': smallWorldConn(N_TC,N_IN,p,K)}   



###############################################################################
# SIMULATION PARAMETERS
###############################################################################

#------------------------------------------------------------------------------
# SIMULATION CONFIGURATION
#------------------------------------------------------------------------------

# Simulation parameters
simConfig.trans = 10000
simConfig.Dt = 0.1
simConfig.steps_per_ms = 1/simConfig.Dt
simConfig.npoints = 30000

simConfig.duration = 20*1000 # simConfig.trans + simConfig.npoints * simConfig.Dt # Duration of the simulation, in ms
simConfig.dt = 0.1 # Internal integration timestep to use
simConfig.hParams['celsius'] = 36
simConfig.hParams['v_init'] = -70
simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
simConfig.verbose = False  # show detailed messages 

# Recording 
simConfig.recordCells = []  # which cells to record from
"""
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'},
                          'V_dend':{'sec':'dend','loc':0.5,'var':'v'},
                          'AMPA_i': {'sec':'soma', 'loc':'0.5', 'synMech':'AMPA', 'var':'AMPA_i'}}
"""
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}

simConfig.recordStim = True  # record spikes of cell stims
simConfig.recordStep = 0.1 # Step size in ms to save data (eg. V traces, LFP, etc)

# Saving
simConfig.simLabel = "trial1"
simConfig.saveFolder = "data_knox_v1"
simConfig.filename = 'knox_v1'  # Set file output name
simConfig.saveFileStep = 1000 # step size in ms to save data to disk
#simConfig.savePickle = True # Whether or not to write spikes etc. to a .mat file
#simConfig.saveJson = True
#simConfig.saveMat = True
#simConfig.saveDpk = False

# Analysis and plotting 
simConfig.analysis['plotRaster'] = {'include': ['PY', 'IN', 'TC', 'RE'], 'orderInverse': True} #True # Whether or not to plot a raster
#simConfig.analysis['plotRaster'] = True  # Plot raster
simConfig.analysis['plotTraces'] = {'include': [('PY',0),('IN',0),('TC',10),('RE',10)]} # plot recorded traces for this list of cells

simConfig.analysis['plotRatePSD'] = {'include': ['PY', 'IN', 'TC', 'RE'], 'Fs': 50, 'smooth': 10} # plot recorded traces for this list of cells

simConfig.addAnalysis('plot2Dnet', {'include': ['PY', 'IN', 'TC', 'RE'],  'showConns': True, 'saveFig': './images/plot2Dnet.png', 'showFig': False})
#simConfig.addAnalysis('plotShape', {'showSyns': True})
#simConfig.addAnalysis('plotConn', {'include': ['allCells'], 'feature': 'strength'})
#simConfig.analysis.plotConn(include=['allCells'], feature='strength', groupBy='pop', figSize=(9,9), showFig=True)

# netParams
simConfig.stimtime = 10050
simConfig.randomstim = 0

simConfig.field = 0
simConfig.fieldg = 0
simConfig.ampafield = 0
simConfig.gabaafield = 0
simConfig.gababfield = 0
simConfig.gababTCfield = 0

simConfig.runStopAt = simConfig.duration

sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)

