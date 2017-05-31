#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _HH2_reg();
extern void _IM_reg();
extern void _IMZ_reg();
extern void _IT_reg();
extern void _IT2_reg();
extern void _ITREcustom_reg();
extern void _ITTCcustom_reg();
extern void _Ih_reg();
extern void _ampa_reg();
extern void _ca_reg();
extern void _cad2_reg();
extern void _cadecay_reg();
extern void _gabaa_reg();
extern void _gabab_reg();
extern void _gapJ_reg();
extern void _izhi2007b_reg();
extern void _kca_reg();
extern void _kleak_reg();
extern void _km_reg();
extern void _kv_reg();
extern void _na_reg();
extern void _nmda_reg();
extern void _vecevent_reg();

modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," HH2.mod");
fprintf(stderr," IM.mod");
fprintf(stderr," IMZ.mod");
fprintf(stderr," IT.mod");
fprintf(stderr," IT2.mod");
fprintf(stderr," ITREcustom.mod");
fprintf(stderr," ITTCcustom.mod");
fprintf(stderr," Ih.mod");
fprintf(stderr," ampa.mod");
fprintf(stderr," ca.mod");
fprintf(stderr," cad2.mod");
fprintf(stderr," cadecay.mod");
fprintf(stderr," gabaa.mod");
fprintf(stderr," gabab.mod");
fprintf(stderr," gapJ.mod");
fprintf(stderr," izhi2007b.mod");
fprintf(stderr," kca.mod");
fprintf(stderr," kleak.mod");
fprintf(stderr," km.mod");
fprintf(stderr," kv.mod");
fprintf(stderr," na.mod");
fprintf(stderr," nmda.mod");
fprintf(stderr," vecevent.mod");
fprintf(stderr, "\n");
    }
_HH2_reg();
_IM_reg();
_IMZ_reg();
_IT_reg();
_IT2_reg();
_ITREcustom_reg();
_ITTCcustom_reg();
_Ih_reg();
_ampa_reg();
_ca_reg();
_cad2_reg();
_cadecay_reg();
_gabaa_reg();
_gabab_reg();
_gapJ_reg();
_izhi2007b_reg();
_kca_reg();
_kleak_reg();
_km_reg();
_kv_reg();
_na_reg();
_nmda_reg();
_vecevent_reg();
}
