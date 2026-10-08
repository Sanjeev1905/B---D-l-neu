diamond_frame = r"""
    #include <cmath>

    using ROOT::Math::PxPyPzEVector;
    using ROOT::Math::XYZVector;

    PxPyPzEVector GetPBDiamond(
        double Ecms,

        double CMS_px,
        double CMS_py,
        double CMS_pz,
        double CMS_E,

        double DST_CMS_px,
        double DST_CMS_py,
        double DST_CMS_pz,
        double DST_CMS_E,

        double lep_CMS_px,
        double lep_CMS_py,
        double lep_CMS_pz,
        double lep_CMS_E,

        int n_points = 4,
        double phi_start = 0.,
        double Bmass = 5.27963,
        double neutrino_mass = 0.,
        bool clip_costhetaBY = true
    )
    {
        PxPyPzEVector PB(
            CMS_px,
            CMS_py,
            CMS_pz,
            CMS_E
        );

        PxPyPzEVector PDst(
            DST_CMS_px,
            DST_CMS_py,
            DST_CMS_pz,
            DST_CMS_E
        );

        PxPyPzEVector Plep(
            lep_CMS_px,
            lep_CMS_py,
            lep_CMS_pz,
            lep_CMS_E
        );

        PxPyPzEVector PY = PDst + Plep;

        //------------------------------------------
        // calculate_costhetaBY
        //------------------------------------------

        const double EY  = PY.E();
        const double mY2 = PY.M2();
        const double pY  = PY.P();

        const double EB = Ecms / 2.0;
        const double pB = std::sqrt(EB*EB - Bmass*Bmass);

        const double cost_num =
            2.0 * EB * EY
            - Bmass * Bmass
            - mY2
            + neutrino_mass * neutrino_mass;

        const double cost_den =
            2.0 * pB * pY;

        double costhetaBY = cost_num / cost_den;

        //------------------------------------------
        // clipping logic
        //------------------------------------------

        if (std::abs(costhetaBY) > 1.0)
        {
            if (clip_costhetaBY)
            {
                costhetaBY = costhetaBY/std::abs(costhetaBY);
            }
            else
            {
                return PB;
            }
        }

        const double thetaBY = std::acos(costhetaBY);

        //------------------------------------------
        // coordinate system
        //------------------------------------------

        XYZVector zHat = PY.Vect().Unit();
        XYZVector yHat = (PDst.Vect().Cross(zHat)).Unit();
        XYZVector xHat = yHat.Cross(zHat);

        //------------------------------------------
        // beam quantities
        //------------------------------------------

        const double EB_beam = Ecms / 2.0;
        const double pB_beam =
            std::sqrt(EB_beam*EB_beam - Bmass*Bmass);

        double w = 0.0;

        PxPyPzEVector PB_diamond(
            0.0,
            0.0,
            0.0,
            0.0
        );

        //------------------------------------------
        // diamond average
        //------------------------------------------

        for (int n = 0; n < n_points; ++n)
        {
            const double phi =
                phi_start +
                (2.0 * M_PI / n_points) * n;

            const double B0_px_Y =
                pB_beam *
                std::sin(thetaBY) *
                std::cos(phi);

            const double B0_py_Y =
                pB_beam *
                std::sin(thetaBY) *
                std::sin(phi);

            const double B0_pz_Y =
                pB_beam *
                std::cos(thetaBY);

            XYZVector pB_frame_n =
                xHat * B0_px_Y
                + yHat * B0_py_Y
                + zHat * B0_pz_Y;

            PxPyPzEVector vec(
                pB_frame_n.X(),
                pB_frame_n.Y(),
                pB_frame_n.Z(),
                EB_beam
            );

            const double cosTB =
                pB_frame_n.Z() /
                pB_frame_n.R();

            const double sin2 =
                1.0 - cosTB*cosTB;

            PB_diamond += vec * sin2;
            w += sin2;
        }

        return PB_diamond * (1.0 / w);
    }
    """


q2 = r"""
    #include <cmath>

    using ROOT::Math::PxPyPzEVector;
    using ROOT::Math::XYZVector;

    double GetQ2(
        double B_px,
        double B_py,
        double B_pz,
        double B_E,

        double DST_px,
        double DST_py,
        double DST_pz,
        double DST_E
    )
    {
        PxPyPzEVector PB(
            B_px,
            B_py,
            B_pz,
            B_E
        );

        PxPyPzEVector PDst(
            DST_px,
            DST_py,
            DST_pz,
            DST_E
        );

        PxPyPzEVector PTransfer = PB - PDst;
                            
        return PTransfer.M2();   
    }                       
    """


costhetal = r"""
    #include <Math/VectorUtil.h>
    #include <Math/Boost.h>
    #include <cmath>
    using namespace ROOT::Math;

    double helicity_costheta_l(double lpx, 
                    double lpy ,
                    double lpz, 
                    double le, 
                    double dstpx,
                    double dstpy,
                    double dstpz, 
                    double dste,
                    double bpx, 
                    double bpy, 
                    double bpz, 
                    double be)
    {
        PxPyPzEVector Bmeson4Vector(bpx, bpy, bpz, be);
        PxPyPzEVector lepton4Vector(lpx, lpy, lpz, le);
        PxPyPzEVector dst4Vector(dstpx, dstpy, dstpz, dste);

        PxPyPzEVector q4Vector = Bmeson4Vector - dst4Vector;

        XYZVector qBoost = q4Vector.BoostToCM();
        // We boost the momentum of the mother and of the granddaughter to the reference frame of the daughter.
        lepton4Vector = Boost(qBoost) * lepton4Vector;
        Bmeson4Vector = Boost(qBoost) * Bmeson4Vector;

        return - VectorUtil::CosTheta(lepton4Vector, Bmeson4Vector);  
    }"""

costhetal_lucien = r"""
    #include <Math/VectorUtil.h>
    #include <Math/Boost.h>
    #include <cmath>
    using namespace ROOT::Math;

    double helicity_costheta_l_lucien(double lpx, 
                    double lpy ,
                    double lpz, 
                    double le, 
                    double dstpx,
                    double dstpy,
                    double dstpz, 
                    double dste,
                    double bpx, 
                    double bpy, 
                    double bpz, 
                    double be)
    {
        PxPyPzEVector Bmeson4Vector(bpx, bpy, bpz, be);
        PxPyPzEVector lepton4Vector(lpx, lpy, lpz, le);
        PxPyPzEVector dst4Vector(dstpx, dstpy, dstpz, dste);

        PxPyPzEVector q4Vector = Bmeson4Vector - dst4Vector;

        XYZVector qBoost = q4Vector.BoostToCM();
        // We boost the momentum of the mother and of the granddaughter to the reference frame of the daughter.
        lepton4Vector = Boost(qBoost) * lepton4Vector;
        Bmeson4Vector = Boost(qBoost) * Bmeson4Vector;

        return - VectorUtil::CosTheta(lepton4Vector, q4Vector);  
    }"""


costhetal_alexei = """
    #include <Math/VectorUtil.h>
    #include <Math/Boost.h>
    #include <cmath>
    #include <math.h>
                            
    using namespace ROOT::Math;

    double helicity_costheta_l_alexei(double lpx, 
                    double lpy ,
                    double lpz, 
                    double le, 
                    double dstpx,
                    double dstpy,
                    double dstpz, 
                    double dste,
                    double bpx, 
                    double bpy, 
                    double bpz, 
                    double be)
    {
        PxPyPzEVector Bmeson4Vector(bpx, bpy, bpz, be);
        PxPyPzEVector lepton4Vector(lpx, lpy, lpz, le);
        PxPyPzEVector dst4Vector(dstpx, dstpy, dstpz, dste);
        PxPyPzEVector q24Vector = Bmeson4Vector - dst4Vector;

        double pd  = Bmeson4Vector.Dot(lepton4Vector);
        double pq  = Bmeson4Vector.Dot(q24Vector);
        double qd  = q24Vector.Dot(lepton4Vector);
        double mp2 = Bmeson4Vector.M2();
        double mq2 = q24Vector.M2();
        double md2 = lepton4Vector.M2();
                              
        double cost = (pd * mq2 - pq * qd )/
                            sqrt( (pq * pq - mq2 * mp2 ) * (qd * qd - mq2 * md2)  );

        return cost;
    }""" 


costhetadst = r"""
    #include <Math/VectorUtil.h>
    #include <Math/Boost.h>
    #include <cmath>
    using namespace ROOT::Math;

    double helicity_costheta_dst(double dpx, 
                    double dpy ,
                    double dpz, 
                    double de, 
                    double dstpx,
                    double dstpy,
                    double dstpz, 
                    double dste,
                    double bpx, 
                    double bpy, 
                    double bpz, 
                    double be)
    {
        PxPyPzEVector Bmeson4Vector(bpx, bpy, bpz, be);
        PxPyPzEVector dmeson4Vector(dpx, dpy, dpz, de);
        PxPyPzEVector dst4Vector(dstpx, dstpy, dstpz, dste);

        PxPyPzEVector daughter4Vector = dst4Vector;

        XYZVector daughterBoost = daughter4Vector.BoostToCM();
        // We boost the momentum of the mother and of the granddaughter to the reference frame of the daughter.
        dmeson4Vector = Boost(daughterBoost) * dmeson4Vector;
        Bmeson4Vector = Boost(daughterBoost) * Bmeson4Vector;

        return VectorUtil::CosTheta(dmeson4Vector, Bmeson4Vector);  
    }"""



chi = r"""
    #include <Math/VectorUtil.h>
    #include <Math/Boost.h>
    #include <cmath>
    using namespace ROOT::Math;

    double helicity_chi2(double lpx, 
                    double lpy ,
                    double lpz, 
                    double le, 
                    double dpx, 
                    double dpy ,
                    double dpz, 
                    double de, 
                    double dstpx,
                    double dstpy,
                    double dstpz, 
                    double dste,
                    double bpx, 
                    double bpy, 
                    double bpz, 
                    double be)
    {
        PxPyPzEVector B04Vector(bpx, bpy, bpz, be);
        PxPyPzEVector lepton4Vector(lpx, lpy, lpz, le);
        PxPyPzEVector d04Vector(dpx, dpy, dpz, de);
        PxPyPzEVector dst4Vector(dstpx, dstpy, dstpz, dste);
        PxPyPzEVector dilepton4Vector = B04Vector-dst4Vector;

        XYZVector B0Boost        = B04Vector.BoostToCM();
        XYZVector dstBoost       = dst4Vector.BoostToCM();
        XYZVector dileptonBoost  = dilepton4Vector.BoostToCM();
                              
        // Boosting daughters to reference frame of the mother
        dst4Vector      = Boost(B0Boost) * dst4Vector;
        dilepton4Vector = Boost(B0Boost) * dilepton4Vector;
        
        // Boosting each granddaughter to reference frame of its mother
        d04Vector     = Boost(dstBoost) * d04Vector;
        lepton4Vector = Boost(dileptonBoost) * lepton4Vector;
                              
        // We calculate the normal vectors of the decay two planes
        XYZVector normalVectorDST   = dst4Vector.Vect().Cross(d04Vector.Vect());
        XYZVector normalVectordilpt = dilepton4Vector.Vect().Cross(lepton4Vector.Vect());
        
        return std::atan2((normalVectorDST.Unit().Cross(normalVectordilpt.Unit())).Dot(dst4Vector.Vect().Unit()), 
                            normalVectorDST.Unit().Dot(normalVectordilpt.Unit()));
    }"""



chi_alt = r"""
    #include <Math/VectorUtil.h>
    #include <Math/Boost.h>
    #include <cmath>
    using namespace ROOT::Math;

    double helicity_chi2_alt(double lpx, 
                    double lpy ,
                    double lpz, 
                    double le, 
                    double dpx, 
                    double dpy ,
                    double dpz, 
                    double de, 
                    double dstpx,
                    double dstpy,
                    double dstpz, 
                    double dste,
                    double bpx, 
                    double bpy, 
                    double bpz, 
                    double be)
    {
        PxPyPzEVector B04Vector(bpx, bpy, bpz, be);
        PxPyPzEVector lepton4Vector(lpx, lpy, lpz, le);
        PxPyPzEVector d04Vector(dpx, dpy, dpz, de);
        PxPyPzEVector dst4Vector(dstpx, dstpy, dstpz, dste);
        PxPyPzEVector dilepton4Vector = B04Vector-dst4Vector;

        XYZVector B0Boost        = B04Vector.BoostToCM();
        XYZVector dstBoost       = dst4Vector.BoostToCM();
        XYZVector dileptonBoost  = dilepton4Vector.BoostToCM();
                              
        // Boosting all particles to reference frame of the mother
        dst4Vector      = Boost(B0Boost) * dst4Vector;
        dilepton4Vector = Boost(B0Boost) * dilepton4Vector;
        d04Vector       = Boost(B0Boost) * d04Vector;
        lepton4Vector   = Boost(B0Boost) * lepton4Vector;
                              
        // We calculate the normal vectors of the decay two planes
        XYZVector n_D = dst4Vector.Vect().Cross(d04Vector.Vect());
        XYZVector n_L = dilepton4Vector.Vect().Cross(lepton4Vector.Vect());
        
        // Define the orientation to extract full angle
        XYZVector z = dst4Vector.Vect().Unit();

        double chi = std::atan2(
            (n_D.Unit().Cross(n_L.Unit())).Dot(z),
            n_D.Unit().Dot(n_L.Unit())
        );                  
        return chi;
    }"""