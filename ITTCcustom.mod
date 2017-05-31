TITLE Low threshold calcium current
:
:   Ca++ current responsible for low threshold spikes (LTS)
:   THALAMOCORTICAL CELLS
:   Differential equations
:
:   Model based on the data of Huguenard & McCormick, J Neurophysiol
:   68: 1373-1383, 1992 and Huguenard & Prince, J Neurosci.
:   12: 3804-3817, 1992.
:
:   Features:
:
:	- kinetics described by Nernst equations using a m2h format
:	- activation considered at steady-state
:	- inactivation fit to Huguenard's data using a bi-exp function
:	- shift for screening charge, q10 of inactivation of 3
:
:   Described in:
:    Destexhe, A., Bal, T., McCormick, D.A. and Sejnowski, T.J.  Ionic 
:    mechanisms underlying synchronized oscillations and propagating waves
:    in a model of ferret thalamic slices. Journal of Neurophysiology 76:
:    2049-2070, 1996.
:   See also http://www.cnl.salk.edu/~alain , http://cns.fmed.ulaval.ca
:   
:
:   Alain Destexhe, Salk Institute and Laval University, 1995
:

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX ittccustom
	USEION ca READ cai,cao WRITE ica
	GLOBAL q10
	RANGE gcabar, m_inf, tau_m, h_inf, tau_h, shift
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
	gcabar	= 0.002	(mho/cm2)
	q10	= 3			: Q10 of inactivation
	shift	= 2 	(mV)		: original 2  : corresponds to 2mM ext Ca++
	taubase (mV)
	cai	= 2.4e-4 (mM)		: adjusted for eca=120 mV
	cao	= 2	(mM)
}

STATE {
	h
}

ASSIGNED {
	ica	(mA/cm2)
	carev	(mV)
	m_inf
	tau_m	(ms)			: dummy variable for compatibility
	h_inf
	tau_h	(ms)
	phi_h
}

BREAKPOINT {
	SOLVE castate METHOD cnexp
	carev = (1e3) * (R*(celsius+273.15))/(2*FARADAY) * log (cao/cai)
	ica = gcabar * m_inf * m_inf * h * (v-carev)
}

DERIVATIVE castate {
	evaluate_fct(v)

	h' = (h_inf - h) / tau_h
}


UNITSOFF
INITIAL {
:
:   Transformation to 36 deg assuming Q10 of 3 for h
:   (as in Coulter et al., J Physiol 414: 587, 1989)
:
	phi_h = q10 ^ ((celsius-24 (degC) )/10 (degC) )

	h = 0
}

PROCEDURE evaluate_fct(v(mV)) { LOCAL Vm

	Vm = v + shift

: fooling around...
:	m_inf = 1.0 / ( 1 + exp(-(Vm+57)/6.2) )
:	h_inf = 1.0 / ( 1 + exp((Vm+81)/4.0) )
:	tau_h = 30.8 + (211.4 + exp((Vm+113.2)/5)) / (1 + exp((Vm+84)/3.2))

: Original steady state activation/inactivation
	m_inf = 1.0 / ( 1 + exp(-(Vm+57)/6.2) )
	h_inf = 1.0 / ( 1 + exp((Vm+81)/4.0) )

:Glauser
:WT no ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+42)/5.6) )
:	h_inf = 1.0 / ( 1 + exp((Vm+70.6)/6.5) )
:WT 3mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+52.6)/5.1) )
:	h_inf = 1.0 / ( 1 + exp((Vm+70.8)/6.4) )
:WT 10mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+56.6)/4.9) )
:	h_inf = 1.0 / ( 1 + exp((Vm+74.6)/6.5) )
:WT 30mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+54.7)/6.0) )
:	h_inf = 1.0 / ( 1 + exp((Vm+79)/7.0) )

:Mutant no ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+43.6)/4.5) )
:	h_inf = 1.0 / ( 1 + exp((Vm+65)/5.2) )
:Mutant 3mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+57.0)/4.3) )
:	h_inf = 1.0 / ( 1 + exp((Vm+72.9)/6.0) )
:Mutant 10mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+65.1)/4.8) )
:	h_inf = 1.0 / ( 1 + exp((Vm+78.7)/6.4) )
:Mutant 30mM ESM
:	m_inf = 1.0 / ( 1 + exp(-(Vm+66.5)/6.4) )
:	h_inf = 1.0 / ( 1 + exp((Vm+88.2)/7.8) )

:	if(Vm < -80) {
:		tau_h = exp((Vm+467)/66.6) / phi_h
:	} else {
:		tau_h = ( 28 + exp(-(Vm+22)/10.5) ) / phi_h
:	}

:original function
	tau_h = taubase + (211.4 + exp((Vm+113.2)/5)) / (1 + exp((Vm+84)/3.2))

:Glauser
:WT no ESM
:	tau_h = 17.19 + (211.4 + exp((Vm+113.2)/9.23)) / (1 + exp((Vm+64)/4.42))
:WT 3 ESM
:	tau_h = 12.69 + (211.4 + exp((Vm+113.2)/12.89)) / (1 + exp((Vm+64)/3.11))
:WT 10 ESM
:	tau_h = 11.56 + (211.4 + exp((Vm+113.2)/12.83)) / (1 + exp((Vm+64)/2.76))
:WT 30 ESM
:	tau_h = 10.65 + (211.4 + exp((Vm+113.2)/12.96)) / (1 + exp((Vm+64)/3.33))

:Mutant no ESM
:	tau_h = 15.77 + (211.4 + exp((Vm+113.2)/7.74)) / (1 + exp((Vm+64)/2.99))
:Mutant 3 ESM
:	tau_h = 15.24 + (211.4 + exp((Vm+113.2)/12.81)) / (1 + exp((Vm+64)/2.62))
:Mutant 10 ESM
:	tau_h = 12.95 + (211.4 + exp((Vm+113.2)/12.81)) / (1 + exp((Vm+64)/2.54))
:Mutant 30 ESM
:	tau_h = 11.40 + (211.4 + exp((Vm+113.2)/12.79)) / (1 + exp((Vm+64)/0.324))

	tau_h = tau_h / phi_h

}

UNITSON
