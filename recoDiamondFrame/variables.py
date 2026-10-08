import ROOT
import definitions_rdf

def apply_diamond_frame(rdf, bmass, numass, npoints=4, phi_start=0, clip_cost=True, name='diamond', truth=False, lepton='muon'):
    
    lep_name = 'mu' if lepton=='muon' else 'e'
    clip='true' if clip_cost else 'false'
    px, py, pz, E = 'px py pz E'.split()
    Ecms = 'Ecms'
    name4 = name
    full_name = f"B{name}_" if name else ''
    if name and not(name.startswith('_')):
            name = '_' + name
    if truth:
        name4 +='_mc'  # Needed to define the "internal" 4 momenta and not conflict with non truth name
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()
        #Ecms = 'EcmsMC'
    
    rdf_ =  rdf.Define(
        f"PB{name4}",
        f"""
        GetPBDiamond(
            {Ecms},
            CMS_{px}, CMS_{py}, CMS_{pz}, CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E},
            {lep_name}_CMS_{px}, {lep_name}_CMS_{py}, {lep_name}_CMS_{pz}, {lep_name}_CMS_{E},
            {npoints},     // n_points
            {phi_start},   // phi_start
            {bmass},       // Bmass
            {numass},      // neutrino_mass
            {clip}         // clip_costhetaBY
        )
        """)
    
    rdf_ = (
        rdf_ 
        .Define(f"{full_name}CMS_{px}", f"PB{name4}.Px()")
        .Define(f"{full_name}CMS_{py}", f"PB{name4}.Py()")
        .Define(f"{full_name}CMS_{pz}", f"PB{name4}.Pz()")
        .Define(f"{full_name}CMS_{E}",  f"PB{name4}.E()") )
    
    return rdf_


def apply_q2(rdf, name='diamond', truth=False):
    # In case we wan to calculate for GEN level, no name is passed
    full_name = f"B{name}_" if name else ''
    #if not name: name="MC"
    if name and not(name.startswith('_')):
        name = '_' + name
    px, py, pz, E = 'px py pz E'.split()
    if truth:
        name+='_mc'
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()

    var_name = f"q2{name}"
    function = f"""
        GetQ2(
            {full_name}CMS_{px}, {full_name}CMS_{py}, {full_name}CMS_{pz}, {full_name}CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E})
        """
    try:
        rdf_ =  rdf.Define(
            var_name,
            function)
        return rdf_
    
    except Exception as e:
        print(e)
        print(var_name)
        print(function)
    

def apply_costhetal(rdf, name='diamond', truth=False, lepton='muon'):
    lep_name = 'mu' if lepton=='muon' else 'e'
    # In case we wan to calculate for GEN level, no name is passed
    full_name = f"B{name}_" if name else ''
    # if not name:     name="MC"
    px, py, pz, E = 'px py pz E'.split()
    if name and not(name.startswith('_')):
            name = '_' + name
    if truth:
        name+='_mc'
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()
    rdf_ =  rdf.Define(
        f"costhetal{name}",
        f"""
        helicity_costheta_l(
            {lep_name}_CMS_{px}, {lep_name}_CMS_{py}, {lep_name}_CMS_{pz}, {lep_name}_CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E},
            {full_name}CMS_{px}, {full_name}CMS_{py}, {full_name}CMS_{pz}, {full_name}CMS_{E})
        """)
    return rdf_

def apply_costhetal_lucien(rdf, name='diamond', truth=False, lepton='muon'):
    lep_name = 'mu' if lepton=='muon' else 'e'
    # In case we wan to calculate for GEN level, no name is passed
    full_name = f"B{name}_" if name else ''
    if name and not(name.startswith('_')):
            name = '_' + name
    # if not name:         name="MC"
    px, py, pz, E = 'px py pz E'.split()
    if truth:
        name+='_mc'
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()
    rdf_ =  rdf.Define(
        f"costhetallucien{name}",
        f"""
        helicity_costheta_l_lucien(
            {lep_name}_CMS_{px}, {lep_name}_CMS_{py}, {lep_name}_CMS_{pz}, {lep_name}_CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E},
            {full_name}CMS_{px}, {full_name}CMS_{py}, {full_name}CMS_{pz}, {full_name}CMS_{E})
        """)
    return rdf_

def apply_costhetal_alexei(rdf, name='diamond', truth=False, lepton='muon'):
    lep_name = 'mu' if lepton=='muon' else 'e'
    # In case we wan to calculate for GEN level, no name is passed
    full_name = f"B{name}_" if name else ''
    if name and not(name.startswith('_')):
            name = '_' + name
    #if not name: name="MC"
    px, py, pz, E = 'px py pz E'.split()
    if truth:
        name+='_mc'
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()
    rdf_ =  rdf.Define(
        f"costhetalalexei{name}",
        f"""
        helicity_costheta_l_alexei(
            {lep_name}_CMS_{px}, {lep_name}_CMS_{py}, {lep_name}_CMS_{pz}, {lep_name}_CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E},
            {full_name}CMS_{px}, {full_name}CMS_{py}, {full_name}CMS_{pz}, {full_name}CMS_{E})
        """)
    return rdf_

def apply_costhetadst(rdf, name='diamond', truth=False):
    # In case we wan to calculate for GEN level, no name is passed
    full_name = f"B{name}_" if name else ''
    # if not name:         name="MC"
    px, py, pz, E = 'px py pz E'.split()
    if name and not(name.startswith('_')):
            name = '_' + name
    if truth:
        name+='_mc'
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()
    rdf_ =  rdf.Define(
        f"costhetadst{name}",
        f"""
        helicity_costheta_dst(
            DST_D0_CMS_{px}, DST_D0_CMS_{py}, DST_D0_CMS_{pz}, DST_D0_CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E},
            {full_name}CMS_{px}, {full_name}CMS_{py}, {full_name}CMS_{pz}, {full_name}CMS_{E})
        """)
    return rdf_

def apply_chi(rdf, name='diamond', truth=False, lepton='muon'):
    lep_name = 'mu' if lepton=='muon' else 'e'
    # In case we wan to calculate for GEN level, no name is passed
    full_name = f"B{name}_" if name else ''
    #if not name: name="MC"
    if name and not(name.startswith('_')):
            name = '_' + name
    px, py, pz, E = 'px py pz E'.split()
    if truth:
        name+='_mc'
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()
    rdf_ =  rdf.Define(
        f"helicitychi{name}",
        f"""
        helicity_chi2(
            {lep_name}_CMS_{px}, {lep_name}_CMS_{py}, {lep_name}_CMS_{pz}, {lep_name}_CMS_{E},
            DST_D0_CMS_{px}, DST_D0_CMS_{py}, DST_D0_CMS_{pz}, DST_D0_CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E},
            {full_name}CMS_{px}, {full_name}CMS_{py}, {full_name}CMS_{pz}, {full_name}CMS_{E})
        """)
    return rdf_


def apply_chi_alt(rdf, name='diamond', truth=False, lepton='muon'):
    lep_name = 'mu' if lepton=='muon' else 'e'
   # In case we wan to calculate for GEN level, no name is passed
    full_name = f"B{name}_" if name else ''
    #if not name: name="MC"
    px, py, pz, E = 'px py pz E'.split()
    if name and not(name.startswith('_')):
            name = '_' + name
    if truth:
        name+='_mc'
        px, py, pz, E = 'mcPX mcPY mcPZ mcE'.split()

    rdf_ =  rdf.Define(
        f"helicitychialt{name}",
        f"""
        helicity_chi2_alt(
            {lep_name}_CMS_{px}, {lep_name}_CMS_{py}, {lep_name}_CMS_{pz}, {lep_name}_CMS_{E},
            DST_D0_CMS_{px}, DST_D0_CMS_{py}, DST_D0_CMS_{pz}, DST_D0_CMS_{E},
            DST_CMS_{px}, DST_CMS_{py}, DST_CMS_{pz}, DST_CMS_{E},
            {full_name}CMS_{px}, {full_name}CMS_{py}, {full_name}CMS_{pz}, {full_name}CMS_{E})
        """)
    return rdf_






def define_all():
    ROOT.gInterpreter.Declare(definitions_rdf.diamond_frame)
    ROOT.gInterpreter.Declare(definitions_rdf.q2)
    ROOT.gInterpreter.Declare(definitions_rdf.costhetal )
    ROOT.gInterpreter.Declare(definitions_rdf.costhetal_lucien )
    ROOT.gInterpreter.Declare(definitions_rdf.costhetal_alexei)
    ROOT.gInterpreter.Declare(definitions_rdf.costhetadst )
    ROOT.gInterpreter.Declare(definitions_rdf.chi)
    ROOT.gInterpreter.Declare(definitions_rdf.chi_alt)

def apply_all(rdf, bmass, numass, npoints=4, phi_start=0, clip_cost=True, name='diamond', truth=False, lepton='muon'):
    rdf = apply_diamond_frame(rdf, bmass, numass, npoints, phi_start, clip_cost, name,truth, lepton=lepton)    
    rdf = apply_q2(rdf, name,truth)
    rdf = apply_costhetal(rdf, name,truth, lepton=lepton)
    rdf = apply_costhetal_lucien(rdf, name,truth, lepton=lepton)
    rdf = apply_costhetal_alexei(rdf, name,truth, lepton=lepton)
    rdf = apply_costhetadst(rdf, name,truth)
    rdf = apply_chi(rdf, name,truth, lepton=lepton)
    rdf = apply_chi_alt(rdf, name,truth, lepton=lepton)
    return rdf

def apply_all_gen(rdf, truth=False, lepton='muon'):
    rdf = apply_q2(rdf, name='', truth=truth)
    rdf = apply_costhetal(rdf, name='', truth=truth, lepton=lepton)
    rdf = apply_costhetal_lucien(rdf, name='', truth=truth, lepton=lepton)
    rdf = apply_costhetal_alexei(rdf, name='', truth=truth, lepton=lepton)
    rdf = apply_costhetadst(rdf, name='', truth=truth)
    rdf = apply_chi(rdf, name='', truth=truth, lepton=lepton)
    rdf = apply_chi_alt(rdf, name='', truth=truth, lepton=lepton)
    return rdf