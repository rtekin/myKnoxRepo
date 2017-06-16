
COMMENT
K passive leak channel

ENDCOMMENT


NEURON {
	SUFFIX kleak2
	USEION k READ ek WRITE ik
	RANGE g, ik, ek
}

PARAMETER {
	g = 0.004	(umho)		: maximum conductance (microSiemens)
	ek	= -100	(mV)		: reversal potential (potassium)

}


UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(umho) = (micromho)
} 

ASSIGNED {
	ik 		(nA)		: current = g*(v - Erev)
    :ek     	(mV)		: postsynaptic voltage
}
 

BREAKPOINT {

	ik = g * (v - ek)
} 










