# ******************************
from neuron import h
from math import pi

print "-------------------------------------------------------------------"
print "<< defining template for one-compartment sTC cell >>"
print " "

class sTC:
  def __init__ (self,ID=0,ty=0,col=0, v_potassium=-100.0,v_sodium =50.0):
    self.ID=ID
    self.ty=ty
    self.col=col
    self.soma = soma = h.Section(name='soma',cell=self)
    self.v_potassium = v_potassium # potassium reversal potential 
    self.v_sodium = v_sodium # sodium reversal potential 
    soma.diam = 96		# geometry 
    soma.L = 96			# so that area is about 29000 um2
    soma.nseg = 1
    soma.Ra = 100
	
    soma.insert('pas')		# leak current 
    soma.e_pas = -70		# from Rinzel
    soma.g_pas = 1e-5
    
    soma.insert('kleak2')
    soma.g_kleak2 = 0.004 # (uS) conversion: x(uS) = x(mS/cm2)*29000e-8*1e3
							#		     			 = x(mS/cm2) * 0.29
    #soma.ek_kleak2 = v_potassium

    soma.insert('hh2')		# Hodgin-Huxley INa and IK 
    #soma.insert('k_ion')
    soma.ek = v_potassium
    soma.ena = v_sodium
    soma.vtraub_hh2 = -25	# High threshold to simulated IA
    soma.gnabar_hh2 = 0.09
    soma.gkbar_hh2 = 0.01
    
    soma.insert('it')		# T-current 
    soma.cai = 2.4e-4 
    soma.cao = 2 
    soma.eca = 120 
    soma.gcabar_it = 0.002
    
    self.soma.insert('iar')		# h-current
    self.soma.eh = -40		# reversal
    #self.soma.nca_iar = 4		# nb of binding sites for Ca++ on protein
    #soma.k2_iar = 0.0004		# decay of Ca++ binding on protein
    #soma.cac_iar = 0.002		# half-activation of Ca++ binding
    #soma.nexp_iar = 1		# nb of binding sites on Ih channel
    #soma.k4_iar = 0.001		# decay of protein binding on Ih channel
    #soma.Pc_iar = 0.01		# half-activation of binding on Ih channel
    #soma.ginc_iar = 2		# augm of conductance of bound Ih
    self.soma.ghbar_iar = 2e-5	# low Ih for slow oscillations
    
    soma.insert('cad')		# calcium decay
    soma.depth_cad = 1
    soma.taur_cad = 5
    soma.cainf_cad = 2.4e-4
    soma.kt_cad = 0		# no pump
    	
  # resets cell to default values
  def todefault(self):
    self.v_potassium = -100
    self.v_sodium = 50
    self.soma.gnabar_hh2 = 0.09
    self.soma.gkbar_hh2 = 0.01
    self.soma.g_pas = 1e-5
    self.soma.gcabar_it = 0.002
    self.soma.ghbar_iar = 2e-5

print " "
print "<< sTC: passive, Kleak, INa, IK, IT, Ih-CAM and Ca++ decay inserted >>"
print "-------------------------------------------------------------------"