import netParams  # import parameters file
import cfg
from netpyne import sim  # import netpyne init module

sim.createSimulateAnalyze(netParams = netParams.netParams, simConfig = cfg.simConfig)  # create and simulate network