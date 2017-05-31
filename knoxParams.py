"""
knoxParams.py 

netParams is a dict containing a set of network parameters using a standardized structure

simConfig is a dict containing a set of simulation configurations using a standardized structure

refs:
Bazhenov, M., Timofeev, I., Steriade, M., & Sejnowski, T. J. (2002). Model of 
thalamocortical slow-wave sleep oscillations and transitions to activated states. 
Journal of neuroscience, 22(19), 8691-8704.


Contributors: xxx@xxxx.com
"""

from netpyne import specs

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

### PY (single compartment)
cellRule = netParams.importCellParams(label='PYrule', conds={'cellType': 'PY', 'cellModel': 'HH_PY'},	fileName='sPY.tem', cellName='sPY')
cellRule['secs']['soma_0']['mechs']['hh2']={'gnabar': 0.05, 'gkbar': 0.005, 'vtraub': -55.0}
cellRule['secs']['soma_0']['mechs']['pas']={'g': 1.0e-4, 'e': -70}
cellRule['secs']['soma_0']['mechs']['im']={'gkbar': 7e-5}
netParams.cellParams['PYrule'] = cellRule

### IN (single compartment)
cellRule = netParams.importCellParams(label='INrule', conds={'cellType': 'IN', 'cellModel': 'HH_IN'},	fileName='sIN.tem', cellName='sIN')
cellRule['secs']['soma_0']['mechs']['hh2']={'gnabar': 0.05, 'gkbar': 0.01, 'vtraub': -55.0}
cellRule['secs']['soma_0']['mechs']['pas']={'g': 1.5e-4, 'e': -70}
netParams.cellParams['INrule'] = cellRule
"""

### mPY (multi compartment)
cellRule = netParams.importCellParams(label='mPYrule', conds={'cellType': 'PY', 'cellModel': 'HH_mPY'},	fileName='mPYr.tem', cellName='mPYr')
cellRule['secs']['dend_0']['mechs']['pas']={'g': 3.3e-5, 'e': -70}
cellRule['secs']['dend_0']['mechs']['kca']={'gbar': 3e-4}
cellRule['secs']['dend_0']['mechs']['na']={'gbar': 1.5e-3}
cellRule['secs']['dend_0']['mechs']['ca']={'gbar': 1e-5}
cellRule['secs']['dend_0']['mechs']['km']={'gbar': 1e-5}

cellRule['secs']['soma_0']['mechs']['na']={'gbar': 3}
cellRule['secs']['soma_0']['mechs']['kv']={'gbar': 0.2}

netParams.cellParams['mPYrule'] = cellRule

### mIN (multi compartment)
cellRule = netParams.importCellParams(label='mINrule', conds={'cellType': 'IN', 'cellModel': 'HH_mIN'},	fileName='mINr.tem', cellName='mINr')
cellRule['secs']['dend_0']['mechs']['pas']={'g': 3.3e-5, 'e': -70}
cellRule['secs']['dend_0']['mechs']['kca']={'gbar': 3e-4}
cellRule['secs']['dend_0']['mechs']['na']={'gbar': 1.5e-3}
cellRule['secs']['dend_0']['mechs']['ca']={'gbar': 1e-5}
cellRule['secs']['dend_0']['mechs']['km']={'gbar': 1e-5}

cellRule['secs']['soma_0']['mechs']['na']={'gbar': 3}
cellRule['secs']['soma_0']['mechs']['kv']={'gbar': 0.2}

netParams.cellParams['mINrule'] = cellRule
"""
### TC (Bazhenov et al.,2002)
cellRule = netParams.importCellParams(label='TCrule', conds={'cellType': 'TC', 'cellModel': 'HH_TC'}, fileName='TC.tem', cellName='sTC')
cellRule['secs']['soma_0']['mechs']['hh2']={'gnabar': 0.09, 'gkbar': 0.01, 'vtraub': -25.0}
cellRule['secs']['soma_0']['mechs']['pas']={'g': 1e-5, 'e': -70}
cellRule['secs']['soma_0']['mechs']['it']={'shift': 2.0, 'gcabar': 0.0022}
cellRule['secs']['soma_0']['mechs']['iar']={'shift': 0.0, 'ghbar': 1.7e-5}
cellRule['secs']['soma_0']['mechs']['cad']={'taur': 5.0, 'depth': 1.0, 'kt': 0.0, 'cainf': 2.4e-4, 'kd': 0.0}
cellRule['secs']['soma_0']['ions']['ca']={'e': 120}
cellRule['secs']['soma_0']['pointps']['kleak_0']['gmax']= 0.003 # 0-0.03 mS/cm^2 for TC

netParams.cellParams['TCrule'] = cellRule

### RE (Bazhenov et al.,2002)
cellRule = netParams.importCellParams(label='RErule', conds={'cellType': 'RE', 'cellModel': 'HH_RE'}, fileName='RE.tem', cellName='sRE')
cellRule['secs']['soma_0']['mechs']['hh2']={'gnabar': 0.1, 'gkbar': 0.01, 'vtraub': -55.0}
cellRule['secs']['soma_0']['mechs']['pas']={'g': 5e-5, 'e': -77}
cellRule['secs']['soma_0']['mechs']['it2']={'shift': 2.0, 'gcabar': 0.0023, 'qm': 2.5, 'qm': 2.5}
cellRule['secs']['soma_0']['mechs']['cad']={'taur': 5.0, 'depth': 1.0, 'kt': 0.0, 'cainf': 2.4e-4, 'kd': 0.0}
cellRule['secs']['soma_0']['ions']['ca']={'e': 120}
cellRule['secs']['soma_0']['pointps']['kleak_0']['gmax']= 0.005  # 0.005 mS/cm^2 for RE

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
#netParams.synMechParams['NMDA'] = {'mod': 'Exp2Syn', 'tau1': 0.15, 'tau2': 15, 'e': 0}  # NMDA
netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'Cmax': 1.0, 'Cdur': 1.0, 'Alpha': 0.072, 'Beta': 0.0066, 'Erev': 0} #}

# GABAa_S
#netParams.synMechParams['GABAA'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAA
netParams.synMechParams['GABAA'] = {'mod': 'GABAa_S', 'Cmax': 0.5, 'Cdur': 0.3, 'Alpha': 20, 'Beta': 0.162, 'Erev': -85} # }  # GABAA

# GABAb_S
#netParams.synMechParams['GABAB'] = {'mod': 'Exp2Syn', 'tau1': 0.07, 'tau2': 9.1, 'e': -80}  # GABAB
netParams.synMechParams['GABAB'] = {'mod': 'GABAb_S', 'Cmax': 0.5, 'Cdur': 0.3, 'K1': 0.09, 'K2': 0.0012, 'K3': 0.18, 'K4': 0.034, 'KD': 100, 'Erev': -95} # }  # GABAB

###############################################################################
# Stimulation parameters
###############################################################################
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 0.5}
netParams.stimTargetParams['bgCrx'] = {'source': 'bkg', 'conds': {'cellType': ['PY', 'IN']}, 
                                            'weight': 2*0.5, 'delay': 'uniform(1,5)', 'synMech': 'AMPA'}  
netParams.stimTargetParams['bgThl'] = {'source': 'bkg', 'conds': {'cellType': ['TC', 'RE']}, 
                                            'weight': 2*0.8, 'delay': 'uniform(1,5)', 'synMech': 'AMPA'}
#netParams.stimTargetParams['bg->sIN'] = {'source': 'bkg', 'conds': {'cellType': 'IN', 'cellModel': 'HH'}, 
#                                            'weight': 1, 'delay': 'uniform(1,5)', 'synMech': 'AMPA_S'}  

#netParams.stimTargetParams['bg->PYR_HH'] = {'source': 'bkg', 'conds': {'cellType': 'PYR', 'cellModel': 'HH'}, 
#                                            'weight': 1, 'synMech': 'AMPA', 'sec': 'dend', 'loc': 1.0, 'delay': 'uniform(1,5)'}

###############################################################################
# Connectivity parameters
###############################################################################
####################### intra cortikal projections ############################
netParams.connParams['PY->PY'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}   

netParams.connParams['PY->PY'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'NMDA',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}   

netParams.connParams['PY->IN'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'IN'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1} 

netParams.connParams['PY->IN'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'IN'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'NMDA',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1} 

netParams.connParams['IN->PY_GABAA'] = {
    'preConds': {'popLabel': 'IN'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'GABAA',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1} 

netParams.connParams['IN->PY_GABAB'] = {
    'preConds': {'popLabel': 'IN'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'GABAB',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}  

###################### intra thalamic projections #############################
netParams.connParams['TC->RE'] = {
    'preConds': {'popLabel': 'TC'}, 
    'postConds': {'popLabel': 'RE'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}  

netParams.connParams['RE->RE'] = {
    'preConds': {'popLabel': 'RE'}, 
    'postConds': {'popLabel': 'RE'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'GABAA',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}  

netParams.connParams['RE->TC_GABAA'] = {
    'preConds': {'popLabel': 'RE'}, 
    'postConds': {'popLabel': 'TC'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'GABAA',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}  

netParams.connParams['RE->TC_GABAB'] = {
    'preConds': {'popLabel': 'RE'}, 
    'postConds': {'popLabel': 'TC'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'GABAB',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}  

################# thalamo-cortical projections ################################
netParams.connParams['PY->RE'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'RE'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}   

netParams.connParams['PY->TC'] = {
    'preConds': {'popLabel': 'PY'}, 
    'postConds': {'popLabel': 'TC'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}  

netParams.connParams['TC->PY'] = {
    'preConds': {'popLabel': 'TC'}, 
    'postConds': {'popLabel': 'PY'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}  

netParams.connParams['TC->IN'] = {
    'preConds': {'popLabel': 'TC'}, 
    'postConds': {'popLabel': 'IN'},
    'weight': 0*0.002,                    
    'delay': netParams.axondelay, 
    'synMech': 'AMPA_S',
    #'probability': '1.0 if dist_x <= narrowdiam*xspacing else 0.0'}   
    'probability': 0*0.1}   



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

simConfig.duration = 1000 # simConfig.trans + simConfig.npoints * simConfig.Dt # Duration of the simulation, in ms
simConfig.dt = 0.1 # Internal integration timestep to use
simConfig.hParams['celsius'] = 36
simConfig.hParams['v_init'] = -70
simConfig.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
simConfig.verbose = False  # show detailed messages 

# Recording 
simConfig.recordCells = []  # which cells to record from
simConfig.recordTraces = {'V_soma':{'sec':'soma','loc':0.5,'var':'v'}}
                          # 'AMPA_i': {'sec':'soma', 'loc':'0.5', 'synMech':'AMPA', 'var':'i'}}
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
simConfig.analysis['plotTraces'] = {'include': [('PY',0),('IN',1),('TC',2),('RE',3)]} # plot recorded traces for this list of cells
#simConfig.analysis['plotRatePSD'] = {'include': ['allCells', 'PY', 'IN'], 'Fs': 200, 'smooth': 10} # plot recorded traces for this list of cells
simConfig.addAnalysis('plot2Dnet', {'include': ['PY', 'IN', 'TC', 'RE'], 'figSize': (8,10), 'showConns': True, 'saveFig': './images/plot2Dnet.png', 'showFig': False})
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


from netpyne import sim 
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)

