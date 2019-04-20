#------------------------------------------------------------------------------
# SIMULATION CONFIGURATION
#------------------------------------------------------------------------------

from netpyne import specs

simConfig = specs.SimConfig()   # object of class SimConfig to store the simulation configuration

# Simulation parameters
simConfig.checkErrors=False
simConfig.trans = 10000
simConfig.Dt = 0.1
simConfig.steps_per_ms = 1/simConfig.Dt
simConfig.npoints = 30000

simConfig.duration = 2*1000 # simConfig.trans + simConfig.npoints * simConfig.Dt # Duration of the simulation, in ms
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
#simConfig.saveJson = True

# Analysis and plotting 
simConfig.analysis['plotRaster'] = {'include': ['PY', 'IN', 'TC', 'RE'], 'timeRange': [1200,2000], 'orderInverse': True} #True # Whether or not to plot a raster
simConfig.analysis['plotTraces'] = {'include': [('PY',0),('IN',0),('TC',10),('RE',10)], 'timeRange': [1200,2000], 'oneFigPer': 'trace', 'overlay': True} # plot recorded traces for this list of cells
#simConfig.analysis['plot2Dnet'] = {'include': ['PY', 'IN', 'TC', 'RE'],  'showConns': True, 'saveFig': './images/plot2Dnet.png', 'showFig': False})
#simConfig.analysis.plotConn(include=['allCells'], feature='strength', groupBy='pop', figSize=(9,9), showFig=True)

# original parameters
simConfig.stimtime = 10050
simConfig.randomstim = 0

simConfig.field = 0
simConfig.fieldg = 0
simConfig.ampafield = 0
simConfig.gabaafield = 0
simConfig.gababfield = 0
simConfig.gababTCfield = 0

simConfig.runStopAt = simConfig.duration
