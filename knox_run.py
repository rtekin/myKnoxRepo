import knoxParams  # import parameters file
from netpyne import sim  # import netpyne init module

sim.createSimulateAnalyze(netParams = knoxParams.netParams, simConfig = knoxParams.simConfig)  # create and simulate network