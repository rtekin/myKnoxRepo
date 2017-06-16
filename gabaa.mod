TITLE simple GABAa receptors

COMMENT
-----------------------------------------------------------------------------

	Simple model for GABAa receptors
	================================

  - FIRST-ORDER KINETICS, FIT TO WHOLE-CELL RECORDINGS

    Whole-cell recorded GABA-A postsynaptic currents (Otis et al, J. Physiol. 
    463: 391-407, 1993) were used to estimate the parameters of the present
    model; the fit was performed using a simplex algorithm (see Destexhe et
    al., J. Neurophysiol. 72: 803-818, 1994).

  - SHORT PULSES OF TRANSMITTER (0.3 ms, 0.5 mM)

    The simplified model was obtained from a detailed synaptic model that 
    included the release of transmitter in adjacent terminals, its lateral 
    diffusion and uptake, and its binding on postsynaptic receptors (Destexhe
    and Sejnowski, 1995).  Short pulses of transmitter with first-order
    kinetics were found to be the best fast alternative to represent the more
    detailed models.

  - ANALYTIC EXPRESSION

    The first-order model can be solved analytically, leading to a very fast
    mechanism for simulating synapses, since no differential equation must be
    solved (see references below).



References

   Destexhe, A., Mainen, Z.F. and Sejnowski, T.J.  An efficient method for
   computing synaptic conductances based on a kinetic model of receptor binding
   Neural Computation 6: 10-14, 1994.  

   Destexhe, A., Mainen, Z.F. and Sejnowski, T.J. Synthesis of models for
   excitable membranes, synaptic transmission and neuromodulation using a 
   common kinetic formalism, Journal of Computational Neuroscience 1: 
   195-230, 1994.

See also:

   http://cns.iaf.cnrs-gif.fr

Written by A. Destexhe, 1995
27-11-2002: the pulse is implemented using a counter, which is more
	stable numerically (thanks to Yann LeFranc)

-----------------------------------------------------------------------------
ENDCOMMENT



INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	POINT_PROCESS GABAa_S
	RANGE g, gmax, R
	NONSPECIFIC_CURRENT i
	:GLOBAL Cmax, Cdur, Alpha, Beta, Erev, Rinf, Rtau
	GLOBAL Rinf, Rtau
	RANGE Cmax, Cdur, Alpha, Beta, Erev
}
UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(umho) = (micromho)
	(mM) = (milli/liter)
}

PARAMETER {
	dt		(ms)
	deadtime = 1 (ms)
	Cmax	= 0.5	(mM)		: max transmitter concentration
	Cdur	= 0.3	(ms)		: transmitter duration (rising phase)
	Alpha	= 20	(/ms mM)	: forward (binding) rate
	Beta	= 0.162	(/ms)		: backward (unbinding) rate
	Erev	= -85	(mV)		: reversal potential
	gmax		(umho)		: maximum conductance
}


ASSIGNED {
	v		(mV)		: postsynaptic voltage
	i 		(nA)		: current = g*(v - Erev)
	g 		(umho)		: conductance
	Rinf				: steady state channels open
	Rtau		(ms)		: time constant of channel binding
	synon 			: sum of weights of all synapses in the "onset" state
}

STATE { Ron Roff }	: initialized to 0 by default
				: total conductances of all synapses
				: in the "pulse on" and "pulse off" states

INITIAL {
	synon = 0
	Rinf = Cmax*Alpha / (Cmax*Alpha + Beta)
	Rtau = 1 / ((Alpha * Cmax) + Beta)
}

BREAKPOINT {
	SOLVE release METHOD cnexp
	g = (Ron + Roff)
	i = g*(v - Erev)
}

DERIVATIVE release { 
	Ron' = (synon*Rinf - Ron)/Rtau
	Roff' = -Beta*Roff
}


NET_RECEIVE(weight, on, r0, t0 (ms), tmp)  {
	if (flag == 0) {
		:spike arrived, turn on
		if (!on) {
			: add to synapses in onset state
			synon = synon + weight
			tmp = r0*exp(-Beta*(t-dt-t0)) : matches old destexhe synapses better
			r0 = r0*exp(-Beta*(t-t0))
			Ron = Ron + tmp
			Roff = Roff - r0
			t0 = t 	
			on = 1
			net_send(Cdur,1)
		}
		:otherwise ignore new events 
	}
	if (flag == 1) {
		:turn off synapse
		synon = synon - weight
		: r0 at start of offset state
		tmp = weight*Rinf + (r0-weight*Rinf)*exp(-(t-dt-t0)/Rtau)	: matches old destexhe synapses better
		r0 = weight*Rinf + (r0-weight*Rinf)*exp(-(t-t0)/Rtau)
		Ron = Ron - r0
		Roff = Roff + tmp
		t0 = t		
		net_send(deadtime,2)	:flag = 2
	}
	if (flag == 2) {
		on = 0 :now that dead time is passed, allow activity
	}
}
