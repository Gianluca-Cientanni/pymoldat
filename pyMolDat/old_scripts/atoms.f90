module atoms
use precision
use Types_Primary
implicit none
private
public :: AtomProp, iam_init_atoms, init_atoms, max_atoms
integer, parameter :: max_atoms = 83
type (element), save :: AtomProp(0:max_atoms)
logical, save :: iam_init_atoms = .false.
contains
  subroutine init_atoms
  use parameters, only : a_o, au2kJ
  implicit none
  real(dp), parameter :: vdwdef=2.5d0
  real(dp) :: conversion
  !
  !Fields
  !======
  !1) Symbol
  !2) Full Name
  !3) Weight: (amu) Kept same as Average Weight for now.
  !4) Average Weight: (amu) CRC Handbook of Chemistry and Physics Ed. D. R. Lide,
  !   72nd Ed. (Table obtained online).
  !5) van der Waals radii (Bondi): (Bohr) Bondi van der Waals radii, J Phys
  !   Chem (1964) 68, 441. No entry for Bismuth so I've used vdwdef.
  !6) Slater radius: (entered in Angstrom and converted to Bohr)
  !   Bragg-Slater radii from Slater, JCP (1964) 41, 3199.
  !   * Inert gases added with same radius as preceding halogen.
  !   * Hydrogen radius is twice the Slater value.
  !   * The dummy site (Z=0) is given a non-zero radius.
  !7) van der Waals radii (Grimme): (entered in Angstrom and converted to Bohr)
  !   J. Comput. Chem. (2006) 27, 1787-1799
  !8) Atomic C6 coefficient from Grimme: (entered in J nm^6/mol and converted to
  !   Hartree Bohr^6) J. Comput. Chem. (2006) 27, 1787-1799.
  !9) Covalent Radii from Data given here are taken from WebElements, copyright
  !   Mark Winter, University of Sheffield, UK. Data taken from
  !   http://www.crystalmaker.com/support/tutorials/crystalmaker/atomicradii/index.html
  !   Units: Entered in Angstrom and converted to Bohr
  AtomProp(0 ) = element('DU','Dummy       ', 0.0      , 0.0      ,0.0   ,0.65,0.000, 0.00, 0   )
  AtomProp(1 ) = element('H ','Hydrogen    ', 1.00794  , 1.00794  ,2.268 ,0.50,1.001, 0.14, 0.37)
  AtomProp(2 ) = element('He','Helium      ', 4.002602 , 4.002602 ,2.646 ,0.50,1.012, 0.08, 0.32)
  AtomProp(3 ) = element('Li','Lithium     ', 6.941    , 6.941    ,3.440 ,1.45,0.825, 1.61, 1.34)
  AtomProp(4 ) = element('Be','Beryllium   ', 9.012182 , 9.012182 ,vdwdef,1.05,1.408, 1.61, 0.90)
  AtomProp(5 ) = element('B ','Boron       ',10.811    ,10.811    ,vdwdef,0.85,1.485, 3.13, 0.82)
  AtomProp(6 ) = element('C ','Carbon      ',12.0107   ,12.0107   ,3.213 ,0.70,1.452, 1.75, 0.77)
  AtomProp(7 ) = element('N ','Nitrogen    ',14.0067   ,14.0067   ,2.929 ,0.65,1.397, 1.23, 0.75)
  AtomProp(8 ) = element('O ','Oxygen      ',15.9994   ,15.9994   ,2.872 ,0.60,1.342, 0.70, 0.73)
  AtomProp(9 ) = element('F ','Fluorine    ',18.9984032,18.9984032,2.778 ,0.50,1.287, 0.75, 0.71)
  AtomProp(10) = element('Ne','Neon        ',20.1797   ,20.1797   ,2.910 ,0.50,1.243, 0.63, 0.69)
  AtomProp(11) = element('Na','Sodium      ',22.989770 ,22.989770 ,4.290 ,1.80,1.144, 5.71, 1.54)
  AtomProp(12) = element('Mg','Magnesium   ',24.3050   ,24.3050   ,3.270 ,1.50,1.364, 5.71, 1.30)
  AtomProp(13) = element('Al','Aluminium   ',26.981538 ,26.981538 ,vdwdef,1.25,1.639, 10.7, 1.18)
  AtomProp(14) = element('Si','Silicon     ',28.0855   ,28.0855   ,3.968 ,1.10,1.716, 9.23, 1.11)
  AtomProp(15) = element('P ','Phosphorus  ',30.973761 ,30.973761 ,3.402 ,1.00,1.705, 7.84, 1.06)
  AtomProp(16) = element('S ','Sulfur      ',32.065    ,32.065    ,3.402 ,1.00,1.683, 5.57, 1.02)
  AtomProp(17) = element('Cl','Chlorine    ',35.453    ,35.453    ,3.307 ,1.00,1.639, 5.07, 0.99)
  AtomProp(18) = element('Ar','Argon       ',39.948    ,39.948    ,3.553 ,1.00,1.595, 4.61, 0.97)
  AtomProp(19) = element('K ','Potassium   ',39.0983   ,39.0983   ,5.197 ,2.20,1.485,10.80, 1.96)
  AtomProp(20) = element('Ca','Calcium     ',40.078    ,40.078    ,vdwdef,1.80,1.474,10.80, 1.74)
  AtomProp(21) = element('Sc','Scandium    ',44.955910 ,44.955910 ,vdwdef,1.60,1.562,10.80, 1.44)
  AtomProp(22) = element('Ti','Titanium    ',47.867    ,47.867    ,vdwdef,1.40,1.562,10.80, 1.36)
  AtomProp(23) = element('V ','Vanadium    ',50.9415   ,50.9415   ,vdwdef,1.35,1.562,10.80, 1.25)
  AtomProp(24) = element('Cr','Chromium    ',51.9961   ,51.9961   ,vdwdef,1.40,1.562,10.80, 1.27)
  AtomProp(25) = element('Mn','Manganese   ',54.938049 ,54.938049 ,vdwdef,1.40,1.562,10.80, 1.39)
  AtomProp(26) = element('Fe','Iron        ',55.845    ,55.845    ,vdwdef,1.40,1.562,10.80, 1.25)
  AtomProp(27) = element('Co','Cobalt      ',58.933200 ,58.933200 ,vdwdef,1.35,1.562,10.80, 1.26)
  AtomProp(28) = element('Ni','Nickel      ',58.6934   ,58.6934   ,3.080 ,1.35,1.562,10.80, 1.21)
  AtomProp(29) = element('Cu','Copper      ',63.546    ,63.546    ,2.646 ,1.35,1.562,10.80, 1.38)
  AtomProp(30) = element('Zn','Zinc        ',65.409    ,65.409    ,2.627 ,1.35,1.562,10.80, 1.31)
  AtomProp(31) = element('Ga','Gallium     ',69.723    ,69.723    ,3.534 ,1.30,1.650,16.99, 1.26)
  AtomProp(32) = element('Ge','Germanium   ',72.64     ,72.64     ,vdwdef,1.25,1.727,17.10, 1.22)
  AtomProp(33) = element('As','Arsenic     ',74.92160  ,74.92160  ,3.496 ,1.15,1.760,16.37, 1.19)
  AtomProp(34) = element('Se','Selenium    ',78.96     ,78.96     ,3.590 ,1.15,1.771,12.64, 1.16)
  AtomProp(35) = element('Br','Bromine     ',79.904    ,79.904    ,3.496 ,1.15,1.749,12.47, 1.14)
  AtomProp(36) = element('Kr','Krypton     ',83.798    ,83.798    ,3.817 ,1.15,1.727,12.01, 1.10)
  AtomProp(37) = element('Rb','Rubidium    ',85.4678   ,85.4678   ,vdwdef,2.35,1.628,24.67, 2.11)
  AtomProp(38) = element('Sr','Strontium   ',87.62     ,87.62     ,vdwdef,2.00,1.606,24.67, 1.92)
  AtomProp(39) = element('Y ','Yttrium     ',88.90585  ,88.90585  ,vdwdef,1.80,1.639,24.67, 1.62)
  AtomProp(40) = element('Zr','Zirconium   ',91.224    ,91.224    ,vdwdef,1.55,1.639,24.67, 1.48)
  AtomProp(41) = element('Nb','Niobium     ',92.90638  ,92.90638  ,vdwdef,1.45,1.639,24.67, 1.37)
  AtomProp(42) = element('Mo','Molybdenum  ',95.94     ,95.94     ,vdwdef,1.45,1.639,24.67, 1.45)
  AtomProp(43) = element('Tc','Technetium  ',98.       ,98.       ,vdwdef,1.35,1.639,24.67, 1.56)
  AtomProp(44) = element('Ru','Ruthenium   ',101.07    ,101.07    ,vdwdef,1.30,1.639,24.67, 1.26)
  AtomProp(45) = element('Rh','Rhodium     ',102.90550 ,102.90550 ,vdwdef,1.35,1.639,24.67, 1.35)
  AtomProp(46) = element('Pd','Palladium   ',106.42    ,106.42    ,3.080 ,1.40,1.639,24.67, 1.31)
  AtomProp(47) = element('Ag','Silver      ',107.8682  ,107.8682  ,3.250 ,1.60,1.639,24.67, 1.53)
  AtomProp(48) = element('Cd','Cadmium     ',112.411   ,112.411   ,2.986 ,1.55,1.639,24.67, 1.48)
  AtomProp(49) = element('In','Indium      ',114.818   ,114.818   ,3.647 ,1.55,1.672,37.32, 1.44)
  AtomProp(50) = element('Sn','Tin         ',118.710   ,118.710   ,4.100 ,1.45,1.804,38.71, 1.41)
  AtomProp(51) = element('Sb','Antimony    ',121.760   ,121.760   ,vdwdef,1.45,1.881,38.44, 1.38)
  AtomProp(52) = element('Te','Tellurium   ',127.60    ,127.60    ,3.893 ,1.40,1.892,31.74, 1.35)
  AtomProp(53) = element('I ','Iodine      ',126.90447 ,126.90447 ,3.742 ,1.40,1.892,31.50, 1.33)
  AtomProp(54) = element('Xe','Xenon       ',131.293   ,131.293   ,4.082 ,1.40,1.881,29.99, 1.30)
  AtomProp(55) = element('Cs','Caesium     ',132.90545 ,132.90545 ,vdwdef,0.00,0.000,00.00, 2.25)
  AtomProp(56) = element('Ba','Barium      ',137.327   ,137.327   ,vdwdef,0.00,0.000,00.00, 1.98)
  AtomProp(57) = element('La','Lanthanum   ',138.9055  ,138.9055  ,vdwdef,0.00,0.000,00.00, 1.69)
  AtomProp(58) = element('Ce','Cerium      ',140.116   ,140.116   ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(59) = element('Pr','Praseodymium',140.90765 ,140.90765 ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(60) = element('Nd','Neodymium   ',144.24    ,144.24    ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(61) = element('Pm','Promethium  ',145.      ,145.      ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(62) = element('Sm','Samarium    ',150.36    ,150.36    ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(63) = element('Eu','Europium    ',151.964   ,151.964   ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(64) = element('Gd','Gadolinium  ',157.25    ,157.25    ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(65) = element('Tb','Terbium     ',158.92534 ,158.92534 ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(66) = element('Dy','Dysprosium  ',162.500   ,162.500   ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(67) = element('Ho','Holmium     ',164.93032 ,164.93032 ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(68) = element('Er','Erbium      ',167.259   ,167.259   ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(69) = element('Tm','Thulium     ',168.93421 ,168.93421 ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(70) = element('Yb','Ytterbium   ',173.04    ,173.04    ,vdwdef,0.00,0.000,00.00, 0   )
  AtomProp(71) = element('Lu','Lutetium    ',174.967   ,174.967   ,vdwdef,0.00,0.000,00.00, 1.60)
  AtomProp(72) = element('Hf','Hafnium     ',178.49    ,178.49    ,vdwdef,0.00,0.000,00.00, 1.50)
  AtomProp(73) = element('Ta','Tantalum    ',180.9479  ,180.9479  ,vdwdef,0.00,0.000,00.00, 1.38)
  AtomProp(74) = element('W ','Tungsten    ',183.84    ,183.84    ,vdwdef,0.00,0.000,00.00, 1.46)
  AtomProp(75) = element('Re','Rhenium     ',186.207   ,186.207   ,vdwdef,0.00,0.000,00.00, 1.59)
  AtomProp(76) = element('Os','Osmium      ',190.23    ,190.23    ,vdwdef,0.00,0.000,00.00, 1.28)
  AtomProp(77) = element('Ir','Iridium     ',192.217   ,192.217   ,vdwdef,0.00,0.000,00.00, 1.37)
  AtomProp(78) = element('Pt','Platinum    ',195.078   ,195.078   ,3.250 ,0.00,0.000,00.00, 1.28)
  AtomProp(79) = element('Au','Gold        ',196.96655 ,196.96655 ,3.137 ,0.00,0.000,00.00, 1.44)
  AtomProp(80) = element('Hg','Mercury     ',200.59    ,200.59    ,2.929 ,0.00,0.000,00.00, 1.49)
  AtomProp(81) = element('Tl','Thallium    ',204.3833  ,204.3833  ,3.704 ,0.00,0.000,00.00, 1.48)
  AtomProp(82) = element('Pb','Lead        ',207.2     ,207.2     ,3.817 ,0.00,0.000,00.00, 1.47)
  AtomProp(83) = element('Bi','Bismuth     ',208.98038 ,208.98038 ,vdwdef,0.00,0.000,00.00, 1.46)
  !
  !A few conversions:
  AtomProp(:)%Rslater    = AtomProp(:)%Rslater/a_o
  AtomProp(:)%RvdwGrimme = AtomProp(:)%RvdwGrimme/a_o
  AtomProp(:)%Covalent   = AtomProp(:)%Covalent/a_o
  !Conversion from J nm^6/mol to Hartree Bohr^6:
  conversion = ((10.0_dp/a_o)**6)/(1000.0_dp*au2kJ)
  AtomProp(:)%C6Grimme = AtomProp(:)%C6Grimme*conversion
  !                                                                   
  iam_init_atoms = .true.
  return
  end subroutine init_atoms
end module atoms

MODULE radii
use precision
IMPLICIT NONE

INTEGER, PARAMETER :: numavw=38
real(dp), PARAMETER :: Agvwr=3.2503287d0
real(dp), PARAMETER :: Arvwr=3.5526849d0
real(dp), PARAMETER :: Asvwr=3.4959931d0
real(dp), PARAMETER :: Auvwr=3.1369451d0
real(dp), PARAMETER :: Brvwr=3.4959931d0
real(dp), PARAMETER :: Cvwr=3.2125342d0
real(dp), PARAMETER :: Cdvwr=2.9857671d0
real(dp), PARAMETER :: Clvwr=3.3070205d0
real(dp), PARAMETER :: Cuvwr=2.6456164d0
real(dp), PARAMETER :: Fvwr=2.7778972d0
real(dp), PARAMETER :: Gavwr=3.5337876d0
real(dp), PARAMETER :: Hvwr=2.2676712d0
real(dp), PARAMETER :: Hevwr=2.6456164d0
real(dp), PARAMETER :: Hgvwr=2.9290753d0
real(dp), PARAMETER :: Ivwr=3.7416575d0
real(dp), PARAMETER :: Invwr=3.6471712d0
real(dp), PARAMETER :: Kvwr=5.1967465d0
real(dp), PARAMETER :: Krvwr=3.8172465d0
real(dp), PARAMETER :: Livwr=3.4393013d0
real(dp), PARAMETER :: Mgvwr=3.2692260d0
real(dp), PARAMETER :: Nvwr=2.9290753d0
real(dp), PARAMETER :: Navwr=4.2896780d0
real(dp), PARAMETER :: Nevwr=2.9101780d0
real(dp), PARAMETER :: Nivwr=3.0802534d0
real(dp), PARAMETER :: Ovwr=2.8723835d0
real(dp), PARAMETER :: Pvwr=3.4015068d0
real(dp), PARAMETER :: Pbvwr=3.8172465d0
real(dp), PARAMETER :: Pdvwr=3.0802534d0
real(dp), PARAMETER :: Ptvwr=3.2503287d0
real(dp), PARAMETER :: Svwr=3.4015068d0
real(dp), PARAMETER :: Sevwr=3.5904794d0
real(dp), PARAMETER :: Sivwr=3.9684246d0
real(dp), PARAMETER :: Snvwr=4.1007054d0
real(dp), PARAMETER :: Tevwr=3.8928355d0
real(dp), PARAMETER :: Tlvwr=3.7038629d0
real(dp), PARAMETER :: Uvwr=3.5148903d0
real(dp), PARAMETER :: Xevwr=4.0818081d0
real(dp), PARAMETER :: Znvwr=2.6267191d0
real(dp), DIMENSION(2,38), PARAMETER :: avwrad=RESHAPE((/hvwr&
     &,1d0,hevwr,2d0,livwr,3d0,cvwr,6d0,nvwr,7d0,ovwr,8d0,fvwr,9d0&
     &,nevwr,10d0,navwr,11d0,mgvwr,12d0,sivwr,14d0,pvwr,15d0,svwr&
     &,16d0,clvwr,17d0,arvwr,18d0,kvwr,19d0,nivwr,29d0,cuvwr,29d0&
     &,znvwr,30d0,gavwr,32d0,asvwr,33d0,sevwr,34d0,brvwr,35d0,krvwr&
     &,36d0,pdvwr,46d0,agvwr,47d0,cdvwr,48d0,invwr,49d0,snvwr,50d0&
     &,tevwr,52d0,ivwr,53d0,xevwr,54d0,ptvwr,78d0,auvwr,79d0,hgvwr&
     &,80d0,tlvwr,81d0,pbvwr,82d00,uvwr,92d0/), (/2,38/))

INTEGER, PRIVATE :: i
real(dp), PARAMETER :: vdwdef=2.5d0
!  Bondi van der Waals radii, J Phys Chem (1964) 68, 441
!  UNITS: All radii in atomic units.
real(dp), PARAMETER :: vdw_radius(0:82) = (/   &
    0.0d0,                              & !  Dummy site
    2.268d0, 2.646d0,                   & !  H, He
    3.440d0, vdwdef,  vdwdef,  3.213d0, & !  Li, Be, B, C
    2.929d0, 2.872d0, 2.778d0, 2.910d0, & !  N, O, F, Ne
    4.290d0, 3.270d0, vdwdef,  3.968d0, & !  Na, Mg, Al, Si
    3.402d0, 3.402d0, 3.307d0, 3.553d0, & !  P, S, Cl, Ar
    5.197d0, vdwdef,  vdwdef,  vdwdef,  & !  K, Ca, Sc, Ti
    vdwdef,  vdwdef,  vdwdef,  vdwdef,  & !  V, Cr, Mn, Fe
    vdwdef,  3.080d0, 2.646d0, 2.627d0, & !  Co, Ni, Cu, Zn
    3.534d0, vdwdef,  3.496d0, 3.590d0, & !  Ga, Ge, As, Se
    3.496d0, 3.817d0, vdwdef,  vdwdef,  & !  Br, Kr, Rb, Sr
    vdwdef,  vdwdef,  vdwdef,  vdwdef,  & !  Y, Zr, Nb, Mo
    vdwdef,  vdwdef,  vdwdef,  3.080d0, & !  Tc, Ru, Rh, Pd
    3.250d0, 2.986d0, 3.647d0, 4.100d0, & !  Ag, Cd, In, Sn
    vdwdef,  3.893d0, 3.742d0, 4.082d0, & !  Sb, Te, I, Xe
    (vdwdef,i=55,72),                   & !  Cs, Ba, La-Hf
    vdwdef,  vdwdef,  vdwdef,  vdwdef,  & !  Ta, W, Re, Os
    vdwdef,  3.250d0, 3.137d0, 2.929d0, & !  Ir, Pt, Au, Hg
    3.704d0, 3.817d0 /)                   !  Tl, Pb

!  Bragg-Slater radii from Slater, JCP (1964) 41, 3199. Inert gases
!  added with same radius as preceding halogen. Hydrogen radius is
!  twice the Slater value. 
!  The dummy site (Z=0) is given a non-zero radius.
!  UNITS: These values are in Angstrom.
real(dp) :: slater_radius(0:54) = (/ 0.65d0, 0.50d0, 0.50d0,   &
    1.45d0, 1.05d0, 0.85d0, 0.70d0, 0.65d0, 0.60d0, 0.50d0, 0.50d0,    &
    1.80d0, 1.50d0, 1.25d0, 1.10d0, 1.00d0, 1.00d0, 1.00d0, 1.00d0,    &
    2.20d0, 1.80d0, 1.60d0, 1.40d0, 1.35d0, 1.40d0, 1.40d0, 1.40d0, 1.35d0, &
    1.35d0, 1.35d0, 1.35d0, 1.30d0, 1.25d0, 1.15d0, 1.15d0, 1.15d0, 1.15d0, &
    2.35d0, 2.00d0, 1.80d0, 1.55d0, 1.45d0, 1.45d0, 1.35d0, 1.30d0, 1.35d0, &
    1.40d0, 1.60d0, 1.55d0, 1.55d0, 1.45d0, 1.45d0, 1.40d0, 1.40d0, 1.40d0/)

END MODULE radii
