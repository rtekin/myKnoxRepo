TITLE Low threshold calcium current
:
:   Ca++ current responsible for low threshold spikes (LTS)
:   RETICULAR THALAMUS - custom channel
:   Differential equations
:
:   Adapted from Model of Huguenard & McCormick, J Neurophysiol 68: 1373-1383, 1992.
:   The kinetics is described by standard equations (NOT GHK)
:   using a m2h format, according to the voltage-clamp data
:   (whole cell patch clamp) of Huguenard & Prince, J Neurosci.
:   12: 3804-3817, 1992.
:
:    - Kinetics adapted to fit the T-channel of reticular neuron
:    - Time constant tau_h refitted from experimental data
:    - shift parameter for screening charge
:
:   Model described in detail in:   
:     Destexhe, A., Contreras, D., Steriade, M., Sejnowski, T.J. and
:     Huguenard, J.R.  In vivo, in vitro and computational analysis of
:     dendritic calcium currents in thalamic reticular neurons.
:     Journal of Neuroscience 16: 169-185, 1996.
:   See also:
:     http://www.cnl.salk.edu/~alain
:     http://cns.fmed.ulaval.ca
:
:   Written by Alain Destexhe, Salk Institute, Sept 18, 1992
:

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX itrecustom
	USEION ca READ cai, cao WRITE ica
	RANGE gcabar, m_inf, tau_m, h_inf, tau_h, shift, qm, qh, taubase
}

UNITS {
	(molar) = (1/liter)
	(mV) =	(millivolt)
	(mA) =	(milliamp)
	(mM) =	(millimolar)

	FARADAY = (faraday) (coulomb)
	R = (k-mole) (joule/degC)
}

PARAMETER {
	v		(mV)
	celsius	= 36	(degC)
:	eca	= 120	(mV)
	gcabar	= .003	(mho/cm2)
	shift	= 0 	(mV)
	taubase (mV)
	cai	= 2.4e-4 (mM)		: adjusted for eca=120 mV
	cao	= 2	(mM)
	qm	= 2.5
	qh 	= 2.5
}

STATE {
	m h
}

ASSIGNED {
	ica	(mA/cm2)
	carev	(mV)
	m_inf
	tau_m	(ms)
	h_inf
	tau_h	(ms)
	phi_m
	phi_h
}

BREAKPOINT {
	SOLVE castate METHOD cnexp
	carev = (1e3) * (R*(celsius+273.15))/(2*FARADAY) * log (cao/cai)
	ica = gcabar * m*m*h * (v-carev)     : original function
:	ica = gcabar * m_inf * m_inf * h * (v-carev)
}

DERIVATIVE castate {
	evaluate_fct(v)

	m' = (m_inf - m) / tau_m
	h' = (h_inf - h) / tau_h
}

UNITSOFF
INITIAL {
:
:   Activation functions and kinetics were obtained from
:   Huguenard & Prince, and were at 23-25 deg.
:   Transformation to 36 deg using Q10
:
	phi_m = qm ^ ((celsius-24)/10)
	phi_h = qh ^ ((celsius-24)/10)

	evaluate_fct(v)
	m = m_inf
	h = h_inf
}

PROCEDURE evaluate_fct(v(mV)) { 
:
:   Time constants were obtained from J. Huguenard
:


: original steady state activation/inactivation
:	m_inf = 1.0 / ( 1 + exp(-(v+shift+50)/7.4) )
:	h_inf = 1.0 / ( 1 + exp((v+shift+78)/5.0) )

: original time constants
	tau_m = ( 3 + 1.0 / ( exp((v+shift+25)/10) + exp(-(v+shift+100)/15) ) )
	tau_h = ( taubase + 1.0 / ( exp((v+shift+46)/4) + exp(-(v+shift+405)/50) ))

:Glauser
:WT no ESM
:	m_inf = 1.0 / ( 1 + exp(-(v+42)/5.6) )
:	h_inf = 1.0 / ( 1 + exp((v+70.6)/6.5) )
:WT 3mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(v+52.6)/5.1) )
:	h_inf = 1.0 / ( 1 + exp((v+70.8)/6.4) )
:WT 10mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(v+56.6)/4.9) )
:	h_inf = 1.0 / ( 1 + exp((v+74.6)/6.5) )
:WT 30mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(v+54.7)/6.0) )
:	h_inf = 1.0 / ( 1 + exp((v+79)/7.0) )

:Mutant no ESM
:	m_inf = 1.0 / ( 1 + exp(-(v+43.6)/4.5) )
:	h_inf = 1.0 / ( 1 + exp((v+65)/5.2) )
:Mutant 3mM ESM
	m_inf = 1.0 / ( 1 + exp(-(v+57.0)/4.3) )
	h_inf = 1.0 / ( 1 + exp((v+72.9)/6.0) )
:Mutant 10mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(v+65.1)/4.8) )
:	h_inf = 1.0 / ( 1 + exp((v+78.7)/6.4) )
:Mutant 30mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(v+66.5)/6.4) )
:	h_inf = 1.0 / ( 1 + exp((v+88.2)/7.8) )

:Glauser
:WT no ESM
:	tau_h = 17.19 + (211.4 + exp((v+113.2)/9.23)) / (1 + exp((v+64)/4.42))
:WT 3 ESM
:	tau_h = 12.69 + (211.4 + exp((v+113.2)/12.89)) / (1 + exp((v+64)/3.11))
:WT 10 ESM
:	tau_h = 11.56 + (211.4 + exp((v+113.2)/12.83)) / (1 + exp((v+64)/2.76))
:WT 30 ESM
:	tau_h = 10.65 + (211.4 + exp((v+113.2)/12.96)) / (1 + exp((v+64)/3.33))

:Mutant no ESM
:	tau_h = 15.77 + (211.4 + exp((v+113.2)/7.74)) / (1 + exp((v+64)/2.99))
:Mutant 3 ESM
:	tau_h = 15.24 + (211.4 + exp((v+113.2)/12.81)) / (1 + exp((v+64)/2.62))
:Mutant 10 ESM
:	tau_h = 12.95 + (211.4 + exp((v+113.2)/12.81)) / (1 + exp((v+64)/2.54))
:Mutant 30 ESM
:	tau_h = 11.40 + (211.4 + exp((v+113.2)/12.79)) / (1 + exp((v+64)/0.324))

	tau_h = tau_h / phi_h
	tau_m = tau_m / phi_m
}
UNITSON
