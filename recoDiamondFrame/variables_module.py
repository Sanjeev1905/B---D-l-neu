import basf2 as b2
import ROOT
import math
from ROOT import Belle2


class Variables(b2.Module):

    def initialize(self):

        self.B_list = Belle2.PyStoreObj("anti-B0:sl")


    def event(self):

        B_list = self.B_list.obj()

        for i in range(B_list.getListSize()):

            B = B_list.getParticle(i)

            if B.getNDaughters() < 2:
                continue

            Dstar = B.getDaughter(0)
            lepton = B.getDaughter(1)
            # neutrino = B.getDaughter(2)


            if Dstar.getNDaughters() < 2:
                continue

            D0 = Dstar.getDaughter(0)
            pion = Dstar.getDaughter(1)


            def p4(p):

                v = p.get4Vector()

                return ROOT.TLorentzVector(
                    v.Px(),
                    v.Py(),
                    v.Pz(),
                    v.E()
                )


            pB = p4(B)
            pDs = p4(Dstar)

            pl = p4(lepton)
            # pnu = p4(neutrino)
            pnu = p4(B) - p4(Dstar) - p4(lepton)

            pD = p4(D0)
            pPi = p4(pion)

            # print('pB: ', pB.M())
            # print('pDs: ', pDs.M())
            # print('pl: ', pl.M())
            # print('pnu: ', pnu.M())
            # print('pD: ', pD.M())
            # print('pPi: ', pPi.M())

            # ==================================================
            # mD
            # ==================================================

            mD = pD.M()
            # print('mD: ', mD)

            # ==================================================
            # q2
            # ==================================================

            q = pl + pnu
            # q = pB - pDs
            q2 = q.M2()
            # print('q2: ', q2)

            # ==================================================
            # cos(theta_D)
            # ==================================================

            pD_Ds = ROOT.TLorentzVector(pD)
            pB_Ds = ROOT.TLorentzVector(pB)

            beta = -pDs.BoostVector()

            pD_Ds.Boost(beta)
            pB_Ds.Boost(beta)

            denom_ctd = (
                pD_Ds.Vect().Mag()
                * pB_Ds.Vect().Mag()
            )

            if denom_ctd != 0:
                ctd = (
                    pD_Ds.Vect().Dot(-pB_Ds.Vect())
                    / denom_ctd
                )
            else:
                ctd = -999.0

            # print('ctd: ', ctd)
            # ==================================================
            # cos(theta_l)
            # ==================================================

            pl_W = ROOT.TLorentzVector(pl)
            pDs_W = ROOT.TLorentzVector(pDs)

            beta = -q.BoostVector()

            pl_W.Boost(beta)
            pDs_W.Boost(beta)

            denom_ctl = (
                pl_W.Vect().Mag()
                * pDs_W.Vect().Mag()
            )

            if denom_ctl != 0:
                ctl = (
                    pl_W.Vect().Dot(-pDs_W.Vect())
                    / denom_ctl
                )
            else:
                ctl = -999.0

            # print('ctl: ', ctl)
            # ==================================================
            # chi
            # ==================================================

            pl_B = ROOT.TLorentzVector(pl)
            pnu_B = ROOT.TLorentzVector(pnu)

            pD_B = ROOT.TLorentzVector(pD)
            pPi_B = ROOT.TLorentzVector(pPi)

            pDs_B = ROOT.TLorentzVector(pDs)

            beta = -pB.BoostVector()

            for v in [pl_B, pnu_B, pD_B, pPi_B, pDs_B]:
                v.Boost(beta)

            nD_vec = pD_B.Vect().Cross(pPi_B.Vect())
            nl_vec = pl_B.Vect().Cross(pnu_B.Vect())

            if nD_vec.Mag() != 0 and nl_vec.Mag() != 0:

                nD = nD_vec.Unit()
                nl = nl_vec.Unit()

                cosChi = nD.Dot(nl)

                if pDs_B.Vect().Mag() != 0:

                    sinChi = (
                        pDs_B.Vect().Unit()
                        .Dot(nD.Cross(nl))
                    )

                else:
                    sinChi = 0.0

                chi = math.atan2(sinChi, cosChi)

                if chi < 0:
                    chi += 2 * math.pi

            else:

                chi = -999.0

            # print('chi: ', chi)
            # ==================================================
            # Lab-frame variables
            # ==================================================

            lct = pl.CosTheta()
            lp = pl.P()

            nuct = pnu.CosTheta()
            nup = pnu.P()

            Dct = pD.CosTheta()
            Dp = pD.P()

            pict = pPi.CosTheta()
            pip = pPi.P()


            # ==================================================
            # Store ExtraInfo
            # ==================================================

            B.addExtraInfo("mD", mD)
            B.addExtraInfo("q2", q2)

            B.addExtraInfo("ctd", ctd)
            B.addExtraInfo("ctl", ctl)

            B.addExtraInfo("chi", chi)

            B.addExtraInfo("lct", lct)
            B.addExtraInfo("lp", lp)

            B.addExtraInfo("nuct", nuct)
            B.addExtraInfo("nup", nup)

            B.addExtraInfo("Dct", Dct)
            B.addExtraInfo("Dp", Dp)

            B.addExtraInfo("pict", pict)
            B.addExtraInfo("pip", pip)
            B.addExtraInfo("pl", lp)
            B.addExtraInfo("pnu", nup)
