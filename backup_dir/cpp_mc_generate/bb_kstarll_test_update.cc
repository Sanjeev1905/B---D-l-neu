# main executable which will take decfile of "new" parameters from 
/home/sanjeev/myAnalysis/btokstarll_resnet/src/python/mc_generator
to generate root file
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

void getpcth(double &p, double &cth, const EvtVector4R &l1){
  double lpx = l1.get(1), lpy = l1.get(2), lpz = l1.get(3), lp = sqrt(lpx*lpx+lpy*lpy+lpz*lpz);
  p = lp;
  cth = lpz/lp;
}

int main( int argc, char* argv[] ){
  program_name = argv[0];
  if(argc<2) usage(EXIT_FAILURE);
  const char *mnames[] = {"B0","anti-B0","B+","B-"};
  const char *mname="B0", *fname=NULL, *ufile = "/home/sanjeev/myAnalysis/evtgennp/test/exampleFiles/KSTARLL.DEC";
  char *endptr;
  long int nevent = 1000;
  int opt, seed = 1430957218, veto = 0;
  while ((opt = getopt(argc, argv, "n:b:o:u:s:v")) != -1) {
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
    case 'v':
      veto = 1;
      break;
    default: /* '?' */
      usage(EXIT_FAILURE);
    }
  }

  EvtRandomEngine *RandEng = new EvtMTRandomEngine(seed);
  //  EvtGen Generator( "simple_decay.dec", "evt.pdl", RandEng, NULL, NULL );
  EvtGen Generator(
    "/home/sanjeev/myAnalysis/btokstarll_resnet/src/python/mc_generator/np_mumu56/np_mumu_1p1/np_B2Kstarll_B0_mumu_1p1.dec",
    "/home/sanjeev/myAnalysis/evtgen/share/EvtGen/evt.pdl",
    RandEng, NULL, NULL
  );
  Generator.readUDecay(ufile);
  //  EvtId Mother = EvtPDL::getId(mname);
  //  EvtVector4R pB( EvtPDL::getMass( Mother ), 0.0, 0.0, 0.0 );
  EvtId Mother = EvtPDL::getId("Upsilon(4S)");
  double pe = 7, pp = 4, thetac = 0.083/2, px = sin(thetac)*(pe+pp), pz = cos(thetac)*(pe-pp), M = EvtPDL::getMass(Mother);
  EvtVector4R pY( sqrt(M*M + px*px + pz*pz), px, 0.0, pz );

  if(fname){
    TFile* file = new TFile( fname, "RECREATE" );
    TNtuple *ntp = new TNtuple("ntp","","mK:q2:ctk:ctl:chi:l1p:l1c:l2p:l2c:kp:kc:pp:pc");

    long int count = 1;
    do {
      EvtParticle* mY = EvtParticleFactory::particleFactory( Mother, pY );
      mY->setDiagonalSpinDensity();
      Generator.generateDecay( mY );

      EvtParticle* mp = mY->getDaug(1);
      
      EvtVector4R kstar = mp->getDaug( 0 )->getP4Lab();
      EvtVector4R l1 = mp->getDaug( 1 )->getP4Lab();
      EvtVector4R l2 = mp->getDaug( 2 )->getP4Lab();
      EvtVector4R q = l1 + l2;
      EvtVector4R b = mp->getP4Lab();
      EvtVector4R k = mp->getDaug( 0 )->getDaug( 0 )->getP4Lab();
      EvtVector4R pi = mp->getDaug( 0 )->getDaug( 1 )->getP4Lab();

      // Kinematic of the decay B -> K* l^+ l^- is fully described by 5 parameters:
      double q2 = q.mass2(); // q^2 -- hadronic recoil
      if(veto){
	if(fabs(q2-9.59079)<40*5.35732e-04){
	  mp->deleteTree();
	  continue;
	}
	if(fabs(q2-1.35872e+01)<10*2.00129e-03){
	  mp->deleteTree();
	  continue;
	}
      }
      double ctk = EvtDecayAngle(b, kstar, k); // cos(theta_K)
      double ctl = EvtDecayAngle(b, q, l1); // cos(theta_ell)
      double chi = EvtDecayAngleChi(b, k, pi, l1, l2); // -pi<chi<pi angle

      double mKpi = (k+pi).mass(); // for convenience -- invariant mass the kaon and pion system or K*
      double l1p,l1ct; getpcth(l1p, l1ct, l1);
      double l2p,l2ct; getpcth(l2p, l2ct, l2);
      double kp,kct; getpcth(kp, kct, k);
      double pip,pict; getpcth(pip, pict, pi);

      ntp->Fill(mKpi, q2, ctk, ctl, chi, l1p, l1ct, l2p, l2ct, kp, kct, pip, pict);
      mY->deleteTree();
      count++;
      if(count%10000==0) printf("nev = %d\n",count);
    } while ( count <= nevent );

    file->Write();
    file->Close();
  } else {
    long int count = 1;
    do {
      EvtParticle* mY = EvtParticleFactory::particleFactory( Mother, pY );
      mY->setDiagonalSpinDensity();
      Generator.generateDecay( mY );
      mY->deleteTree();
   } while ( count++ < nevent );
  }
  delete RandEng;
  return 0;
}
