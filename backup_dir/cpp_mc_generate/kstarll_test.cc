#include "EvtGen/EvtGen.hh"

#include "EvtGenBase/EvtKine.hh"
#include "EvtGenBase/EvtMTRandomEngine.hh"
#include "EvtGenBase/EvtParticle.hh"
#include "EvtGenBase/EvtParticleFactory.hh"
#include "EvtGenBase/EvtVector3R.hh"

#include "TFile.h"
#include "TNtuple.h"

#include <getopt.h>

static const char *program_name = "";
void usage(int status){
  fprintf(stderr, "Usage: %s -n nevent -b B0|anti-B0|B+|B- [-u user_decay_file] [-o out_root_file] [-s seed]\n", program_name);
  exit(status);
}

bool allowed_arg(const char *arg, int n, const char* args[] ){
  bool match = false;
  for(int i=0;i<n;i++) if(strcmp(arg,args[i])==0) match = true;
  return match;
}

int main( int argc, char* argv[] ){
  program_name = argv[0];
  if(argc<2) usage(EXIT_FAILURE);
  const char *mnames[] = {"B0","anti-B0","B+","B-"};
  const char *mname="B0", *fname=NULL, *ufile = "kstarll.DEC";
  char *endptr;
  long int nevent = 1000;
  int opt, seed = 1430957218;
  while ((opt = getopt(argc, argv, "n:b:o:u:s:")) != -1) {
    switch (opt) {
    case 'n':
      nevent = strtoul(optarg, &endptr, 0);
      if(endptr!=NULL && *endptr!='\0') usage(EXIT_FAILURE);
      break;
    case 'b':
      if(!allowed_arg(optarg,4,mnames)) usage(EXIT_FAILURE);
      mname = optarg;
      break;
    case 'o':
      fname = optarg;
      break;
    case 'u':
      ufile = optarg;
      break;
    case 's':
      seed = atoi(optarg);
      break;
    default: /* '?' */
      usage(EXIT_FAILURE);
    }
  }

  EvtRandomEngine *RandEng = new EvtMTRandomEngine(seed);
  //  EvtGen Generator( "simple_decay.dec", "evt.pdl", RandEng, NULL, NULL );
  EvtGen Generator( "../myDECAY.DEC", "../evt.pdl", RandEng, NULL, NULL );
  Generator.readUDecay(ufile);
  EvtId Mother = EvtPDL::getId(mname);
  EvtVector4R pB( EvtPDL::getMass( Mother ), 0.0, 0.0, 0.0 );

  if(fname){
    TFile* file = new TFile( fname, "RECREATE" );
    TNtuple *ntp = new TNtuple("ntp","","mK:q2:ctk:ctl:chi");

    long int count = 1;
    do {
      EvtParticle* mp = EvtParticleFactory::particleFactory( Mother, pB );
      mp->setDiagonalSpinDensity();
      Generator.generateDecay( mp );
    
      EvtVector4R kstar = mp->getDaug( 0 )->getP4Lab();
      EvtVector4R l1 = mp->getDaug( 1 )->getP4Lab();
      EvtVector4R l2 = mp->getDaug( 2 )->getP4Lab();
      EvtVector4R q = l1 + l2;
      EvtVector4R b = mp->getP4();
      EvtVector4R k = mp->getDaug( 0 )->getDaug( 0 )->getP4Lab();
      EvtVector4R pi = mp->getDaug( 0 )->getDaug( 1 )->getP4Lab();

      // Kinematic of the decay B -> K* l^+ l^- is fully described by 4 parameters:
      double q2 = q.mass2(); // q^2 -- hadronic recoil
      double ctk = EvtDecayAngle(b, kstar, k); // cos(theta_K)
      double ctl = EvtDecayAngle(b, q, l1); // cos(theta_ell)
      double chi = EvtDecayAngleChi(b, k, pi, l1, l2); // -pi<chi<pi angle

      double mKpi = (k+pi).mass(); // for convenience -- invariant mass the kaon and pion system or K*
      ntp->Fill(mKpi, q2, ctk, ctl, chi);
      mp->deleteTree();
    } while ( count++ < nevent );

    file->Write();
    file->Close();
  } else {
    long int count = 1;
    do {
      EvtParticle* mp = EvtParticleFactory::particleFactory( Mother, pB );
      mp->setDiagonalSpinDensity();
      Generator.generateDecay( mp );
      mp->deleteTree();
   } while ( count++ < nevent );
  }
  delete RandEng;
  return 0;
}
