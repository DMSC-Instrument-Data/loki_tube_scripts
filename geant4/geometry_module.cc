/////////////////////////////////////////
// Declaration of our geometry module: //
/////////////////////////////////////////

#include "G4Interfaces/GeoConstructPyExport.hh"
#include "G4Tubs.hh"
#include "G4Box.hh"
#include "G4Transform3D.hh"
#include "G4Vector3D.hh"
//#include "G4LogicalVolume.hh"  ///might not be needed? 
//#include <fstream>
#include <cmath>

class GeoBCS : public G4Interfaces::GeoConstructBase
{
public:
  GeoBCS();
  virtual ~GeoBCS(){}
  virtual G4VPhysicalVolume* Construct();
protected:
  virtual bool validateParameters();
private:
  G4LogicalVolume * createStrawLV(); // create the logical volume of each straw for easy placement inside the tubebg
  G4LogicalVolume * createGasStrawLV(); // create the logical volume of the gas inside each straw 
  // G4LogicalVolume * createTubeLV();  // create the logical volume of a tube for easy placement in a panel
  //G4LogicalVolume * createPackLV();  // create the logical volume of a tube for easy placement in a panel
  G4LogicalVolume * createStrawWallLV();  // create the logical volume of a tube for easy placement in a panel
  G4LogicalVolume * createPackBoxLV();
  G4LogicalVolume * createRearPanelBoxLV();
  G4LogicalVolume * createVertMidPanelBoxLV();
  G4LogicalVolume * createHorMidPanelBoxLV();
  G4LogicalVolume * createVertFrontPanelBoxLV();
  G4LogicalVolume * createHorFrontPanelBoxLV();
  
  
  //G4LogicalVolume * createTubeLV();  // create the logical volume of a tube for easy placement in a panel
};

// this line is necessary to be able to declare the geometry in the python simulation script 
PYTHON_MODULE { GeoConstructPyExport::exportGeo<GeoBCS>("GeoBCSBanks"); } 

////////////////////////////////////////////
// Implementation of our geometry module: //
////////////////////////////////////////////

//#include "G4Box.hh"

GeoBCS::GeoBCS()
  : GeoConstructBase("G4GeoBCS/GeoBCSBanks")
{
  // declare all parameters that can be used from the command line,
  // define their type, pick a self-explanatory name and _unit
  // give the default value, the last 2 ones are optional (min, max)
  addParameterDouble("straw_length_cm", 100);
  addParameterDouble("straw_radius_mm", 3.75);
  addParameterDouble("straw_wall_mm", 0.025);

  addParameterDouble("mid_vert_straw_length_cm", 50);
  addParameterDouble("mid_hor_straw_length_cm", 100);

  addParameterDouble("front_straw_length_cm", 120);


  //addParameterDouble("gas_straw_length_cm", 100);
  addParameterDouble("gas_straw_radius_mm", 3.75-0.025);
  //addParameterDouble("gas_straw_wall_mm", 0.025);

  addParameterDouble("tube_radius_mm", 12.7); //1" diameter (this is outer radius)
  addParameterDouble("tube_wall_mm", 0.94);
  addParameterDouble("tube_tube_distance_mm", 27.62);  ///taken from most recent drawing (03.06.19)
  addParameterDouble("pack_pack_distance_mm", 2*28.40);  ///taken from most recent drawing (03.06.19)
  
  
  addParameterDouble("converter_thickness_front_um", 0.65);
  addParameterDouble("converter_thickness_back_um" , 1); 

  addParameterDouble("pack_box_width_mm", 200, 25.4,500); //default value=4*tube_outer_radius (for default tube paramaters)
  addParameterString("pack_box_fill_material", "G4_Vacuum");


  addParameterDouble("panel_box_width_mm", 250, 25.4,1500); //default need to select default parameters  (for default tube paramaters)

  addParameterDouble("B4C_panel_thickness_mm", 10, 0.1, 30);
  addParameterString("B4C_panel_material","ESS_B4C:b10_enrichment=0.95");

  
  addParameterString("converter_material","ESS_B4C:b10_enrichment=0.95");

  addParameterString("straw_wall_material", "NCrystal:cfg=Cu_sg225.ncmat");
  addParameterString("tube_wall_material", "NCrystal:cfg=Al_sg225.ncmat");
  addParameterString("tube_inner_gas","IdealGas:formula=0.8*Ar+0.2*CO2:pressure_atm=0.7");      /// corrected to 80:20 Ar:CO2 ratio (04/06/2019)


  addParameterString("counting_gas","IdealGas:formula=0.8*Ar+0.2*CO2:pressure_atm=0.7");
  addParameterString("world_material","G4_Vacuum");
  addParameterDouble("sample_detector_distance_m", 5.0127, 0, 10); //(5m + tube_radius) to position the front of the first panel to 5m
  addParameterDouble("generator_detector_distance_cm", 500, 0, 1000); //
  addParameterDouble("generator_mid_vert_detector_distance_cm", 330, 0, 1000); //
  addParameterDouble("generator_mid_hor_detector_distance_cm", 295, 0, 1000); //

  
  addParameterInt("number_of_pixels",256); 
  
  //addParameterInt("number_of_straws", 7, 1, 49);
  //addParameterInt("number_of_gas_straws", 128, 1, 128);
  addParameterInt("number_of_tubes", 2, 1, 40);
  addParameterInt("number_of_packs", 28, 1, 30);
  addParameterInt("number_of_panels", 1, 1, 5);

  addParameterInt("number_of_vert_mid_packs", 6,1,20);
  addParameterInt("number_of_hor_mid_packs", 8,1,20);

  addParameterInt("number_of_vert_front_packs", 16,1,20);
  addParameterInt("number_of_hor_front_packs", 10,1,20);

  addParameterDouble("tube_rotation_deg", 8.45-30,-360,360);   //the tubes are 30 degrees out of allignment  
  addParameterDouble("B4C_panel_rotation_deg", 0,-360,360);
  addParameterDouble("pack_rotation_deg", -13.45,-360,360);

  addParameterDouble("mid_vert_panel_rotation_deg", -6.3,-360,360);  
  addParameterDouble("mid_hor_panel_rotation_deg", -10,-360,360);  

  addParameterDouble("front_vert_panel_rotation_deg", -25.6,-360,360);  
  addParameterDouble("front_hor_panel_rotation_deg", -28,-360,360);  


  
  //addParameterDouble("panel_offset_mm", 10.16,0,100);
  
/*
  addParameterDouble("panel0_rotation_deg", 0,0,360);
  addParameterDouble("panel1_rotation_deg", 0,0,360);
  addParameterDouble("panel2_rotation_deg", 0,0,360);
  addParameterDouble("panel3_rotation_deg", 0,0,360);
  addParameterDouble("panel4_rotation_deg", 0,0,360);
  */
}


//////////////////  Need to define the different panels separately due to different straw lengths ////////////////////

///////////  REAR DETECTOR PANEL   //////////////////////////

G4LogicalVolume *GeoBCS::createRearPanelBoxLV()
{
  const double straw_radius = getParameterDouble("straw_radius_mm")*Units::mm;
  const double straw_wall = getParameterDouble("straw_wall_mm")*Units::mm;
  const double straw_length = getParameterDouble("straw_length_cm")*Units::cm; 
  const double converter_thickness_front = getParameterDouble("converter_thickness_front_um")*Units::um;
  const double converter_thickness_back = getParameterDouble("converter_thickness_back_um")*Units::um;
  const double tube_outer_radius = getParameterDouble("tube_radius_mm")*Units::mm;
  const double tube_wall = getParameterDouble("tube_wall_mm")*Units::mm;
  const double pack_box = getParameterDouble("pack_box_width_mm")*Units::mm;
  const double panel_box = getParameterDouble("panel_box_width_mm")*Units::mm;
  const double tube_tube_distance = getParameterDouble("tube_tube_distance_mm")*Units::mm;
  const double pack_pack_distance = getParameterDouble("pack_pack_distance_mm")*Units::mm;
  const double B4C_panel_thickness = getParameterDouble("B4C_panel_thickness_mm")*Units::mm;

  
  auto pack_fill_material = getParameterMaterial("pack_box_fill_material");

  auto tube_wall_material = getParameterMaterial("tube_wall_material");
  auto tube_inner_gas = getParameterMaterial("tube_inner_gas");  
  auto straw_wall_material = getParameterMaterial("straw_wall_material");
  auto counting_gas = getParameterMaterial("counting_gas");
  auto converter_material = getParameterMaterial("converter_material");
  auto B4C_panel_material = getParameterMaterial("B4C_panel_material");


  
  const int number_of_tubes = getParameterInt("number_of_tubes");
  const int number_of_packs = getParameterInt("number_of_packs");
  //const int number_of_panels = getParameterInt("number_of_panels");

  const double tube_rotation = getParameterDouble("tube_rotation_deg")*Units::degree;
  const double B4C_rotation = getParameterDouble("B4C_panel_rotation_deg")*Units::degree;
  const double pack_rotation = getParameterDouble("pack_rotation_deg")*Units::degree;

  
  double tube_inner_radius = tube_outer_radius - tube_wall;  //3*straw_radius; // 3 times the outer radius of the straw
  //double tube_outer_radius = tube_inner_radius + tube_wall;


  auto lv_rear_panel_box = new G4LogicalVolume(new G4Box("EmptyPanelBox",0.5*panel_box,(2+number_of_packs/2)*pack_pack_distance, 0.5*straw_length),
                                          pack_fill_material, "EmptyPanelBox");
  
 
  auto lv_pack_box = new G4LogicalVolume(new G4Box("EmptyPackBox",0.5*pack_box, tube_tube_distance, 0.5*straw_length),
                                         pack_fill_material, "EmptyPackBox");  

  G4RotationMatrix* my_rotationMatrix=new G4RotationMatrix(0,0,pack_rotation);
  
  for(int l=0; l<number_of_packs; ++l) {      
    int copyNumber= 1000000*l+1000000;
    place(lv_pack_box, 0,l*pack_pack_distance-number_of_packs*pack_pack_distance/2, 0, lv_rear_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);
    //place(lv_pack_box, 0,-l/2*pack_pack_distance, 0, lv_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);

  }


 
  auto lv_tube = new G4LogicalVolume(new G4Tubs("TubeWall",0, tube_outer_radius, 0.5*straw_length, 0., 2*M_PI),
                                     tube_wall_material, "TubeWall");
  G4RotationMatrix* my_tuberotationMatrix=new G4RotationMatrix(0,0,tube_rotation);

  auto lv_B4C_panel = new G4LogicalVolume(new G4Box("B4CPanel", 0.5*B4C_panel_thickness,tube_tube_distance, 0.5*straw_length),
                                       B4C_panel_material, "B4CPanel");
  G4RotationMatrix* B4CRotationMatrix=new G4RotationMatrix(0,0,B4C_rotation);
  

  /////////////////////   BACK TUBES /////////////////////////////
  

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_B4C_panel, +1*tube_tube_distance,0,0, lv_pack_box, G4Colour(0,1,0), 00000,0, B4CRotationMatrix);   
    place(lv_tube, 0,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 100000,0, my_tuberotationMatrix);  // 1st trans is z, 2nd trans is y, 3rd trans is x 
    place(lv_tube, 6.6058,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 200000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 300000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 400000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  


  auto lv_empty_tube = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}



    const G4String name_db = "StrawWall";



  auto lv_straw_wall = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){


     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                converter_material, 0,0,0, lv_straw_wall, G4Colour(0,1,1),10,0,0).logvol;

     /// line above used to have cpNo/10 not just 10

     place(lv_converter, 0,0,0, lv_straw_wall, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels = getParameterInt("number_of_pixels");
     double pixel_length = (straw_length-straw_wall)/float(nPixels);
  
     for(int i=0; i<nPixels; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_front, 0.5*(straw_length-straw_wall)/float(nPixels), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter, G4Colour(0,0,1), i,0,0);}


/////////////////////   FRONT TUBES /////////////////////////////


  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_tube, -2*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 500000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-2*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 600000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -3*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 700000,0, my_rotationMatrix);
    place(lv_tube, 6.6058-3*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 800000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  


  auto lv_empty_tube_f = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube_f, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}



    const G4String name_db_f = "StrawWall";

  //   // define the shape inside the G4LogicalVolume constructor, saves a line of code from declaring the shape separately


  auto lv_straw_wall_f = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){


     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall_f, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall_f, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall_f, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter_f =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                converter_material, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),10,0,0).logvol;

     /// line above used to have cpNo/10 not just 10

     place(lv_converter_f, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels_f = getParameterInt("number_of_pixels");
     // double pixel_length_f = (straw_length-straw_wall)/float(nPixels_f);
  
     for(int i=0; i<nPixels_f; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_back, 0.5*(straw_length-straw_wall)/float(nPixels_f), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter_f, G4Colour(0,0,1), i,0,0);}


 return lv_rear_panel_box;
 }









///////////////////  RIGHT AND LEFT MID PANELS //////////////////////

G4LogicalVolume *GeoBCS::createVertMidPanelBoxLV()
{
  const double straw_radius = getParameterDouble("straw_radius_mm")*Units::mm;
  const double straw_wall = getParameterDouble("straw_wall_mm")*Units::mm;
  const double straw_length = getParameterDouble("mid_vert_straw_length_cm")*Units::cm; 
  const double converter_thickness_front = getParameterDouble("converter_thickness_front_um")*Units::um;
  const double converter_thickness_back = getParameterDouble("converter_thickness_back_um")*Units::um;
  const double tube_outer_radius = getParameterDouble("tube_radius_mm")*Units::mm;
  const double tube_wall = getParameterDouble("tube_wall_mm")*Units::mm;
  const double pack_box = getParameterDouble("pack_box_width_mm")*Units::mm;
  const double panel_box = getParameterDouble("panel_box_width_mm")*Units::mm;
  const double tube_tube_distance = getParameterDouble("tube_tube_distance_mm")*Units::mm;
  const double pack_pack_distance = getParameterDouble("pack_pack_distance_mm")*Units::mm;
  const double B4C_panel_thickness = getParameterDouble("B4C_panel_thickness_mm")*Units::mm;

  
  auto pack_fill_material = getParameterMaterial("pack_box_fill_material");

  auto tube_wall_material = getParameterMaterial("tube_wall_material");
  auto tube_inner_gas = getParameterMaterial("tube_inner_gas");  
  auto straw_wall_material = getParameterMaterial("straw_wall_material");
  auto counting_gas = getParameterMaterial("counting_gas");
  auto converter_material = getParameterMaterial("converter_material");
  auto B4C_panel_material = getParameterMaterial("B4C_panel_material");


  
  const int number_of_tubes = getParameterInt("number_of_tubes");
  const int number_of_packs = getParameterInt("number_of_vert_mid_packs");
  //const int number_of_panels = getParameterInt("number_of_panels");

  const double tube_rotation = getParameterDouble("tube_rotation_deg")*Units::degree;
  const double B4C_rotation = getParameterDouble("B4C_panel_rotation_deg")*Units::degree;
  const double pack_rotation = getParameterDouble("pack_rotation_deg")*Units::degree;

  
  double tube_inner_radius = tube_outer_radius - tube_wall;  //3*straw_radius; // 3 times the outer radius of the straw
  //double tube_outer_radius = tube_inner_radius + tube_wall;


  auto lv_vert_mid_panel_box = new G4LogicalVolume(new G4Box("EmptyPanelBox",0.5*panel_box,(2+number_of_packs/2)*pack_pack_distance, 0.5*straw_length),
                                          pack_fill_material, "EmptyPanelBox");
  
 
  auto lv_pack_box = new G4LogicalVolume(new G4Box("EmptyPackBox",0.5*pack_box, tube_tube_distance, 0.5*straw_length),
                                         pack_fill_material, "EmptyPackBox");  

  G4RotationMatrix* my_rotationMatrix=new G4RotationMatrix(0,0,pack_rotation);
  
  for(int l=0; l<number_of_packs; ++l) {      
    int copyNumber= 1000000*l+1000000;
    place(lv_pack_box, 0,l*pack_pack_distance-number_of_packs*pack_pack_distance/2, 0, lv_vert_mid_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);
    //place(lv_pack_box, 0,-l/2*pack_pack_distance, 0, lv_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);

  }


 
  auto lv_tube = new G4LogicalVolume(new G4Tubs("TubeWall",0, tube_outer_radius, 0.5*straw_length, 0., 2*M_PI),
                                     tube_wall_material, "TubeWall");
  G4RotationMatrix* my_tuberotationMatrix=new G4RotationMatrix(0,0,tube_rotation);

  auto lv_B4C_panel = new G4LogicalVolume(new G4Box("B4CPanel", 0.5*B4C_panel_thickness,tube_tube_distance, 0.5*straw_length),
                                       B4C_panel_material, "B4CPanel");
  G4RotationMatrix* B4CRotationMatrix=new G4RotationMatrix(0,0,B4C_rotation);
  

  /////////////////////   BACK TUBES /////////////////////////////
  

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_B4C_panel, +1*tube_tube_distance,0,0, lv_pack_box, G4Colour(0,1,0), 00000,0, B4CRotationMatrix);   
    place(lv_tube, 0,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 100000,0, my_tuberotationMatrix);  // first trans is z, second trans is y, third trans is x 
    place(lv_tube, 6.6058,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 200000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 300000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 400000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  

  auto lv_empty_tube = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}

    const G4String name_db = "StrawWall";


  auto lv_straw_wall = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){

     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                converter_material, 0,0,0, lv_straw_wall, G4Colour(0,1,1),10,0,0).logvol;

     /// line above used to have cpNo/10 not just 10

     place(lv_converter, 0,0,0, lv_straw_wall, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels = getParameterInt("number_of_pixels");
     double pixel_length = (straw_length-straw_wall)/float(nPixels);
  
     for(int i=0; i<nPixels; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_front, 0.5*(straw_length-straw_wall)/float(nPixels), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter, G4Colour(0,0,1), i,0,0);}


/////////////////////   FRONT TUBES /////////////////////////////

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_tube, -2*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 500000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-2*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 600000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -3*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 700000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-3*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 800000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  


  auto lv_empty_tube_f = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube_f, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}



    const G4String name_db_f = "StrawWall";

  //   // define the shape inside the G4LogicalVolume constructor, saves a line of code from declaring the shape separately


  auto lv_straw_wall_f = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){


     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall_f, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall_f, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall_f, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter_f =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                  converter_material, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),10,0,0).logvol;         /////this is the mother of the gas pixel

     /// line above used to have cpNo/10 not just 10

     place(lv_converter_f, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels_f = getParameterInt("number_of_pixels");
     // double pixel_length_f = (straw_length-straw_wall)/float(nPixels_f);
  
     for(int i=0; i<nPixels_f; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_back, 0.5*(straw_length-straw_wall)/float(nPixels_f), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter_f, G4Colour(0,0,1), i,0,0);}


 return lv_vert_mid_panel_box;
 }










///////////////////  TOP and BOTTOM MID PANELS //////////////////////

G4LogicalVolume *GeoBCS::createHorMidPanelBoxLV()
{
  const double straw_radius = getParameterDouble("straw_radius_mm")*Units::mm;
  const double straw_wall = getParameterDouble("straw_wall_mm")*Units::mm;
  const double straw_length = getParameterDouble("mid_hor_straw_length_cm")*Units::cm; 
  const double converter_thickness_front = getParameterDouble("converter_thickness_front_um")*Units::um;
  const double converter_thickness_back = getParameterDouble("converter_thickness_back_um")*Units::um;
  const double tube_outer_radius = getParameterDouble("tube_radius_mm")*Units::mm;
  const double tube_wall = getParameterDouble("tube_wall_mm")*Units::mm;
  const double pack_box = getParameterDouble("pack_box_width_mm")*Units::mm;
  const double panel_box = getParameterDouble("panel_box_width_mm")*Units::mm;
  const double tube_tube_distance = getParameterDouble("tube_tube_distance_mm")*Units::mm;
  const double pack_pack_distance = getParameterDouble("pack_pack_distance_mm")*Units::mm;
  const double B4C_panel_thickness = getParameterDouble("B4C_panel_thickness_mm")*Units::mm;

  
  auto pack_fill_material = getParameterMaterial("pack_box_fill_material");

  auto tube_wall_material = getParameterMaterial("tube_wall_material");
  auto tube_inner_gas = getParameterMaterial("tube_inner_gas");  
  auto straw_wall_material = getParameterMaterial("straw_wall_material");
  auto counting_gas = getParameterMaterial("counting_gas");
  auto converter_material = getParameterMaterial("converter_material");
  auto B4C_panel_material = getParameterMaterial("B4C_panel_material");


  
  const int number_of_tubes = getParameterInt("number_of_tubes");
  const int number_of_packs = getParameterInt("number_of_hor_mid_packs");
  //const int number_of_panels = getParameterInt("number_of_panels");

  const double tube_rotation = getParameterDouble("tube_rotation_deg")*Units::degree;
  const double B4C_rotation = getParameterDouble("B4C_panel_rotation_deg")*Units::degree;
  const double pack_rotation = getParameterDouble("pack_rotation_deg")*Units::degree;

  
  double tube_inner_radius = tube_outer_radius - tube_wall;  //3*straw_radius; // 3 times the outer radius of the straw
  //double tube_outer_radius = tube_inner_radius + tube_wall;


  auto lv_hor_mid_panel_box = new G4LogicalVolume(new G4Box("EmptyPanelBox",0.5*panel_box,(number_of_packs/2+1)*pack_pack_distance, 0.5*straw_length),
                                          pack_fill_material, "EmptyPanelBox");
  
 
  auto lv_pack_box = new G4LogicalVolume(new G4Box("EmptyPackBox",0.5*pack_box, tube_tube_distance, 0.5*straw_length),
                                         pack_fill_material, "EmptyPackBox");  

  G4RotationMatrix* my_rotationMatrix=new G4RotationMatrix(0,0,pack_rotation);
  
  for(int l=0; l<number_of_packs; ++l) {      
    int copyNumber= 1000000*l+1000000;
    place(lv_pack_box, 0,l*pack_pack_distance-number_of_packs*pack_pack_distance/2, 0, lv_hor_mid_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);
    //place(lv_pack_box, 0,-l/2*pack_pack_distance, 0, lv_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);

  }


 
  auto lv_tube = new G4LogicalVolume(new G4Tubs("TubeWall",0, tube_outer_radius, 0.5*straw_length, 0., 2*M_PI),
                                     tube_wall_material, "TubeWall");
  G4RotationMatrix* my_tuberotationMatrix=new G4RotationMatrix(0,0,tube_rotation);

  auto lv_B4C_panel = new G4LogicalVolume(new G4Box("B4CPanel", 0.5*B4C_panel_thickness,tube_tube_distance, 0.5*straw_length),
                                       B4C_panel_material, "B4CPanel");
  G4RotationMatrix* B4CRotationMatrix=new G4RotationMatrix(0,0,B4C_rotation);
  

  /////////////////////   BACK TUBES /////////////////////////////
  

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_B4C_panel, +1*tube_tube_distance,0,0, lv_pack_box, G4Colour(0,1,0), 00000,0, B4CRotationMatrix);   
    place(lv_tube, 0,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 100000,0, my_tuberotationMatrix);  // first trans is z, second trans is y, third trans is x 
    place(lv_tube, 6.6058,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 200000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 300000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 400000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  

  auto lv_empty_tube = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}

    const G4String name_db = "StrawWall";


  auto lv_straw_wall = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){

     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                converter_material, 0,0,0, lv_straw_wall, G4Colour(0,1,1),10,0,0).logvol;

     /// line above used to have cpNo/10 not just 10

     place(lv_converter, 0,0,0, lv_straw_wall, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels = getParameterInt("number_of_pixels");
     double pixel_length = (straw_length-straw_wall)/float(nPixels);
  
     for(int i=0; i<nPixels; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_front, 0.5*(straw_length-straw_wall)/float(nPixels), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter, G4Colour(0,0,1), i,0,0);}


/////////////////////   FRONT TUBES /////////////////////////////

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_tube, -2*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 500000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-2*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 600000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -3*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 700000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-3*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 800000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  


  auto lv_empty_tube_f = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube_f, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}



    const G4String name_db_f = "StrawWall";

  //   // define the shape inside the G4LogicalVolume constructor, saves a line of code from declaring the shape separately


  auto lv_straw_wall_f = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){


     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall_f, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall_f, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall_f, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter_f =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                  converter_material, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),10,0,0).logvol;         /////this is the mother of the gas pixel

     /// line above used to have cpNo/10 not just 10

     place(lv_converter_f, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels_f = getParameterInt("number_of_pixels");
     // double pixel_length_f = (straw_length-straw_wall)/float(nPixels_f);
  
     for(int i=0; i<nPixels_f; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_back, 0.5*(straw_length-straw_wall)/float(nPixels_f), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter_f, G4Colour(0,0,1), i,0,0);}


 return lv_hor_mid_panel_box;
 }













///////////////////  LEFT AND RIGHT  FRONT PANELS //////////////////////

G4LogicalVolume *GeoBCS::createVertFrontPanelBoxLV()
{
  const double straw_radius = getParameterDouble("straw_radius_mm")*Units::mm;
  const double straw_wall = getParameterDouble("straw_wall_mm")*Units::mm;
  const double straw_length = getParameterDouble("front_straw_length_cm")*Units::cm; 
  const double converter_thickness_front = getParameterDouble("converter_thickness_front_um")*Units::um;
  const double converter_thickness_back = getParameterDouble("converter_thickness_back_um")*Units::um;
  const double tube_outer_radius = getParameterDouble("tube_radius_mm")*Units::mm;
  const double tube_wall = getParameterDouble("tube_wall_mm")*Units::mm;
  const double pack_box = getParameterDouble("pack_box_width_mm")*Units::mm;
  const double panel_box = getParameterDouble("panel_box_width_mm")*Units::mm;
  const double tube_tube_distance = getParameterDouble("tube_tube_distance_mm")*Units::mm;
  const double pack_pack_distance = getParameterDouble("pack_pack_distance_mm")*Units::mm;
  const double B4C_panel_thickness = getParameterDouble("B4C_panel_thickness_mm")*Units::mm;

  
  auto pack_fill_material = getParameterMaterial("pack_box_fill_material");

  auto tube_wall_material = getParameterMaterial("tube_wall_material");
  auto tube_inner_gas = getParameterMaterial("tube_inner_gas");  
  auto straw_wall_material = getParameterMaterial("straw_wall_material");
  auto counting_gas = getParameterMaterial("counting_gas");
  auto converter_material = getParameterMaterial("converter_material");
  auto B4C_panel_material = getParameterMaterial("B4C_panel_material");


  
  const int number_of_tubes = getParameterInt("number_of_tubes");
  const int number_of_packs = getParameterInt("number_of_vert_front_packs");
  //const int number_of_panels = getParameterInt("number_of_panels");

  const double tube_rotation = getParameterDouble("tube_rotation_deg")*Units::degree;
  const double B4C_rotation = getParameterDouble("B4C_panel_rotation_deg")*Units::degree;
  const double pack_rotation = getParameterDouble("pack_rotation_deg")*Units::degree;

  
  double tube_inner_radius = tube_outer_radius - tube_wall;  //3*straw_radius; // 3 times the outer radius of the straw
  //double tube_outer_radius = tube_inner_radius + tube_wall;


  auto lv_front_vert_panel_box = new G4LogicalVolume(new G4Box("EmptyPanelBox",0.5*panel_box,(number_of_packs/2+1)*pack_pack_distance, 0.5*straw_length),
                                          pack_fill_material, "EmptyPanelBox");
  
 
  auto lv_pack_box = new G4LogicalVolume(new G4Box("EmptyPackBox",0.5*pack_box, tube_tube_distance, 0.5*straw_length),
                                         pack_fill_material, "EmptyPackBox");  

  G4RotationMatrix* my_rotationMatrix=new G4RotationMatrix(0,0,pack_rotation);
  
  for(int l=0; l<number_of_packs; ++l) {      
    int copyNumber= 1000000*l+1000000;
    place(lv_pack_box, 0,l*pack_pack_distance-number_of_packs*pack_pack_distance/2, 0, lv_front_vert_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);
    //place(lv_pack_box, 0,-l/2*pack_pack_distance, 0, lv_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);

  }


 
  auto lv_tube = new G4LogicalVolume(new G4Tubs("TubeWall",0, tube_outer_radius, 0.5*straw_length, 0., 2*M_PI),
                                     tube_wall_material, "TubeWall");
  G4RotationMatrix* my_tuberotationMatrix=new G4RotationMatrix(0,0,tube_rotation);

  auto lv_B4C_panel = new G4LogicalVolume(new G4Box("B4CPanel", 0.5*B4C_panel_thickness,tube_tube_distance, 0.5*straw_length),
                                       B4C_panel_material, "B4CPanel");
  G4RotationMatrix* B4CRotationMatrix=new G4RotationMatrix(0,0,B4C_rotation);
  

  /////////////////////   BACK TUBES /////////////////////////////
  

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_B4C_panel, +1*tube_tube_distance,0,0, lv_pack_box, G4Colour(0,1,0), 00000,0, B4CRotationMatrix);   
    place(lv_tube, 0,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 100000,0, my_tuberotationMatrix);  // first trans is z, second trans is y, third trans is x 
    place(lv_tube, 6.6058,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 200000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 300000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 400000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  

  auto lv_empty_tube = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}

    const G4String name_db = "StrawWall";


  auto lv_straw_wall = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){

     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                converter_material, 0,0,0, lv_straw_wall, G4Colour(0,1,1),10,0,0).logvol;

     /// line above used to have cpNo/10 not just 10

     place(lv_converter, 0,0,0, lv_straw_wall, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels = getParameterInt("number_of_pixels");
     double pixel_length = (straw_length-straw_wall)/float(nPixels);
  
     for(int i=0; i<nPixels; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_front, 0.5*(straw_length-straw_wall)/float(nPixels), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter, G4Colour(0,0,1), i,0,0);}


/////////////////////   FRONT TUBES /////////////////////////////

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_tube, -2*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 500000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-2*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 600000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -3*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 700000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-3*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 800000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  


  auto lv_empty_tube_f = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube_f, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}



    const G4String name_db_f = "StrawWall";

  //   // define the shape inside the G4LogicalVolume constructor, saves a line of code from declaring the shape separately


  auto lv_straw_wall_f = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){


     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall_f, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall_f, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall_f, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter_f =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                  converter_material, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),10,0,0).logvol;         /////this is the mother of the gas pixel

     /// line above used to have cpNo/10 not just 10

     place(lv_converter_f, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels_f = getParameterInt("number_of_pixels");
     // double pixel_length_f = (straw_length-straw_wall)/float(nPixels_f);
  
     for(int i=0; i<nPixels_f; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_back, 0.5*(straw_length-straw_wall)/float(nPixels_f), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter_f, G4Colour(0,0,1), i,0,0);}


 return lv_front_vert_panel_box;
 }















///////////////////  TOP and BOTTOM FRONT PANELS //////////////////////

G4LogicalVolume *GeoBCS::createHorFrontPanelBoxLV()
{
  const double straw_radius = getParameterDouble("straw_radius_mm")*Units::mm;
  const double straw_wall = getParameterDouble("straw_wall_mm")*Units::mm;
  const double straw_length = getParameterDouble("front_straw_length_cm")*Units::cm; 
  const double converter_thickness_front = getParameterDouble("converter_thickness_front_um")*Units::um;
  const double converter_thickness_back = getParameterDouble("converter_thickness_back_um")*Units::um;
  const double tube_outer_radius = getParameterDouble("tube_radius_mm")*Units::mm;
  const double tube_wall = getParameterDouble("tube_wall_mm")*Units::mm;
  const double pack_box = getParameterDouble("pack_box_width_mm")*Units::mm;
  const double panel_box = getParameterDouble("panel_box_width_mm")*Units::mm;
  const double tube_tube_distance = getParameterDouble("tube_tube_distance_mm")*Units::mm;
  const double pack_pack_distance = getParameterDouble("pack_pack_distance_mm")*Units::mm;
  const double B4C_panel_thickness = getParameterDouble("B4C_panel_thickness_mm")*Units::mm;

  
  auto pack_fill_material = getParameterMaterial("pack_box_fill_material");

  auto tube_wall_material = getParameterMaterial("tube_wall_material");
  auto tube_inner_gas = getParameterMaterial("tube_inner_gas");  
  auto straw_wall_material = getParameterMaterial("straw_wall_material");
  auto counting_gas = getParameterMaterial("counting_gas");
  auto converter_material = getParameterMaterial("converter_material");
  auto B4C_panel_material = getParameterMaterial("B4C_panel_material");


  
  const int number_of_tubes = getParameterInt("number_of_tubes");
  const int number_of_packs = getParameterInt("number_of_hor_front_packs");
  //const int number_of_panels = getParameterInt("number_of_panels");

  const double tube_rotation = getParameterDouble("tube_rotation_deg")*Units::degree;
  const double B4C_rotation = getParameterDouble("B4C_panel_rotation_deg")*Units::degree;
  const double pack_rotation = getParameterDouble("pack_rotation_deg")*Units::degree;

  
  double tube_inner_radius = tube_outer_radius - tube_wall;  //3*straw_radius; // 3 times the outer radius of the straw
  //double tube_outer_radius = tube_inner_radius + tube_wall;


  auto lv_front_hor_panel_box = new G4LogicalVolume(new G4Box("EmptyPanelBox",0.5*panel_box,(number_of_packs/2+1)*pack_pack_distance, 0.5*straw_length),
                                          pack_fill_material, "EmptyPanelBox");
  
 
  auto lv_pack_box = new G4LogicalVolume(new G4Box("EmptyPackBox",0.5*pack_box, tube_tube_distance, 0.5*straw_length),
                                         pack_fill_material, "EmptyPackBox");  

  G4RotationMatrix* my_rotationMatrix=new G4RotationMatrix(0,0,pack_rotation);
  
  for(int l=0; l<number_of_packs; ++l) {      
    int copyNumber= 1000000*l+1000000;
    place(lv_pack_box, 0,l*pack_pack_distance-number_of_packs*pack_pack_distance/2, 0, lv_front_hor_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);
    //place(lv_pack_box, 0,-l/2*pack_pack_distance, 0, lv_panel_box, G4Colour(0,1,1), copyNumber,0,my_rotationMatrix);

  }


 
  auto lv_tube = new G4LogicalVolume(new G4Tubs("TubeWall",0, tube_outer_radius, 0.5*straw_length, 0., 2*M_PI),
                                     tube_wall_material, "TubeWall");
  G4RotationMatrix* my_tuberotationMatrix=new G4RotationMatrix(0,0,tube_rotation);

  auto lv_B4C_panel = new G4LogicalVolume(new G4Box("B4CPanel", 0.5*B4C_panel_thickness,tube_tube_distance, 0.5*straw_length),
                                       B4C_panel_material, "B4CPanel");
  G4RotationMatrix* B4CRotationMatrix=new G4RotationMatrix(0,0,B4C_rotation);
  

  /////////////////////   BACK TUBES /////////////////////////////
  

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_B4C_panel, +1*tube_tube_distance,0,0, lv_pack_box, G4Colour(0,1,0), 00000,0, B4CRotationMatrix);   
    place(lv_tube, 0,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 100000,0, my_tuberotationMatrix);  // first trans is z, second trans is y, third trans is x 
    place(lv_tube, 6.6058,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 200000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 300000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 400000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  

  auto lv_empty_tube = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}

    const G4String name_db = "StrawWall";


  auto lv_straw_wall = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){

     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                converter_material, 0,0,0, lv_straw_wall, G4Colour(0,1,1),10,0,0).logvol;

     /// line above used to have cpNo/10 not just 10

     place(lv_converter, 0,0,0, lv_straw_wall, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels = getParameterInt("number_of_pixels");
     double pixel_length = (straw_length-straw_wall)/float(nPixels);
  
     for(int i=0; i<nPixels; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_front, 0.5*(straw_length-straw_wall)/float(nPixels), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter, G4Colour(0,0,1), i,0,0);}


/////////////////////   FRONT TUBES /////////////////////////////

  //for(int j=0; j<number_of_tubes; ++j) {
  //int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
  // place(lv_empty_tube, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);

  for(int k=0; k<number_of_packs; ++k) {
    // int copyNumber= 1000000*k+1000000;
    place(lv_tube, -2*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 500000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-2*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 600000,0, my_tuberotationMatrix);  /// offset by 28.4sin(13.45) 
    place(lv_tube, -3*tube_tube_distance,+0.5*tube_tube_distance,0, lv_pack_box, G4Colour(0,1,1), 700000,0, my_tuberotationMatrix);
    place(lv_tube, 6.6058-3*tube_tube_distance,-0.5*tube_tube_distance, 0, lv_pack_box, G4Colour(0,1,1), 800000,0, my_tuberotationMatrix); /// offset by 28.4sin(13.45) 
  }
  


  auto lv_empty_tube_f = new G4LogicalVolume(new G4Tubs("EmptyTube", 0., tube_inner_radius, 0.5*straw_length, 0., 2*M_PI),
                                         tube_inner_gas,"EmptyTube");


    for(int j=0; j<number_of_tubes; ++j) {
    int copyNumber= 100000*j+100000;
    // auto lv_straw_wall = createStrawLV();
    place(lv_empty_tube_f, 0,0,0, lv_tube, G4Colour(0,1,1), copyNumber);}



    const G4String name_db_f = "StrawWall";

  //   // define the shape inside the G4LogicalVolume constructor, saves a line of code from declaring the shape separately


  auto lv_straw_wall_f = new G4LogicalVolume(new G4Tubs(name_db, 0, straw_radius, 0.5*straw_length, 0., 2*M_PI),
                                              straw_wall_material, name_db);

  for(int cpNo=10000;cpNo<=70000;cpNo+=10000){


     // for(int j=1; j<=number_of_straws; ++j) {
       // int copyNumber= 100000*j+100000;
     
     place(lv_straw_wall_f, 0, 0, 0, lv_empty_tube, ORANGE, 10000,0,0);
     place(lv_straw_wall_f, 0, -2*straw_radius, 0, lv_empty_tube, ORANGE, 20000,0,0);
     place(lv_straw_wall_f, 0, 2*straw_radius, 0, lv_empty_tube, ORANGE, 30000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 40000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.),  straw_radius, 0, lv_empty_tube, ORANGE, 50000,0,0);
     place(lv_straw_wall_f,  straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 60000,0,0);
     place(lv_straw_wall_f, -straw_radius*tan(M_PI/3.), -straw_radius, 0, lv_empty_tube, ORANGE, 70000,0,0);
    
    }

    
     auto lv_converter_f =  place(new G4Tubs("Converter", 0., straw_radius-straw_wall, 0.5*(straw_length-straw_wall), 0., 2*M_PI),
                                  converter_material, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),10,0,0).logvol;         /////this is the mother of the gas pixel

     /// line above used to have cpNo/10 not just 10

     place(lv_converter_f, 0,0,0, lv_straw_wall_f, G4Colour(0,1,1),-3,0,0);
    ///used to be removed ^^
    
     
     int nPixels_f = getParameterInt("number_of_pixels");
     // double pixel_length_f = (straw_length-straw_wall)/float(nPixels_f);
  
     for(int i=0; i<nPixels_f; i++) {
       place(new G4Tubs("CountingGas", 0., straw_radius-straw_wall-converter_thickness_back, 0.5*(straw_length-straw_wall)/float(nPixels_f), 0., 2*M_PI),
             counting_gas, 0,0, i*pixel_length+0.5*pixel_length-0.5*straw_length+0.5*straw_wall, lv_converter_f, G4Colour(0,0,1), i,0,0);}


 return lv_front_hor_panel_box;
 }



































G4VPhysicalVolume* GeoBCS::Construct()
{
  // this is where we put the entire geometry together, the private functions creating the logical volumes are meant to facilitate the code below
  //Parameters:

  auto world_material = getParameterMaterial("world_material"); 
  //const double converter_thickness = getParameterDouble("converter_thickness_um")*Units::um;
  //const double straw_radius = getParameterDouble("straw_radius_mm")*Units::mm;

  const double generator_detector_distance = getParameterDouble("generator_detector_distance_cm")*Units::cm;


  const double mid_vert_panel_rotation = getParameterDouble("mid_vert_panel_rotation_deg")*Units::degree;
  const double mid_hor_panel_rotation = getParameterDouble("mid_hor_panel_rotation_deg")*Units::degree;

  const double front_vert_panel_rotation = getParameterDouble("front_vert_panel_rotation_deg")*Units::degree;
  const double front_hor_panel_rotation = getParameterDouble("front_hor_panel_rotation_deg")*Units::degree;

  
  //const double straw_wall = getParameterDouble("straw_wall_mm")*Units::mm;
  const double sdd = getParameterDouble("sample_detector_distance_m")*Units::m;
  const double straw_length = getParameterDouble("straw_length_cm")*Units::cm;
  // const double tube_wall = getParameterDouble("tube_wall_mm")*Units::mm;
  //double tube_inner_radius = 3 * straw_radius; // 3 times the outer radius of the straw
  //double tube_outer_radius = tube_inner_radius + tube_wall;
  //const double tube_box = getParameterDouble("tube_box_mm")*Units::mm;

  //const double pack_rotation = getParameterDouble("pack_rotation_deg")*Units::degree;


  
  // calculate a value that is big enough to fit your world volume, the "super mother"
  double epsilon = 1*Units::mm;


  ////////big dimension that has been used previously 
  //double big_dimension = 1.1*(straw_length + 2*tube_outer_radius + epsilon + sdd);
  double big_dimension = 1.1*(straw_length + generator_detector_distance + epsilon + sdd);


  
  //double big_dimension = 1.1*(straw_length + + epsilon + sdd);

  // const int number_of_straws = getParameterInt("number_of_straws");
  // const int number_of_gas_straws = getParameterInt("number_of_gas_straws");

  
  //World volume:
  auto worldvols = place(new G4Box("World", big_dimension, big_dimension, big_dimension),world_material,0,0,0,0,INVISIBLE);
  auto lvWorld = worldvols.logvol;
  auto pvWorld = worldvols.physvol;

  //auto lv_tube = createTubeLV();
  // auto lv_pack = createPackLV();
  auto rot = new G4RotationMatrix();
  rot->rotateY(M_PI/2); /// keep this or the tubes rotate around the y axis 


  
  auto rotvertmidleft = new G4RotationMatrix();
  rotvertmidleft->rotateY(M_PI/2);
  rotvertmidleft->rotateX(M_PI/2);   
  rotvertmidleft->rotateZ(mid_vert_panel_rotation);   //// needs to be 6.3 

  auto rotvertmidright = new G4RotationMatrix();
  rotvertmidright->rotateY(M_PI/2);
  rotvertmidright->rotateX(1.5*M_PI); /// for some unknown reason rotates around z....  5.5* definitely works 
  rotvertmidright->rotateZ(mid_vert_panel_rotation);   //// needs to be -6.3 
  

  
  auto rothormidtop = new G4RotationMatrix();
  rothormidtop->rotateY(M_PI/2);
  //rothormidtop->rotateX(mid_hor_panel_rotation); /// rotates around z   
  rothormidtop->rotateZ(mid_hor_panel_rotation);   //// needs to be 10 

  auto rothormidbottom = new G4RotationMatrix();
  rothormidbottom->rotateY(1.5*M_PI);
  //rothormidbottom->rotateX(M_PI/2); /// for some unknown reason rotates around y this time definitely dont need 
  rothormidbottom->rotateZ(M_PI+mid_hor_panel_rotation);   //// needs to be 10 
  


  auto rotvertfrontleft = new G4RotationMatrix();
  rotvertfrontleft->rotateY(M_PI/2);
  rotvertfrontleft->rotateX(M_PI/2);   
  rotvertfrontleft->rotateZ(front_vert_panel_rotation);   //// needs to be 

  auto rotvertfrontright = new G4RotationMatrix();
  rotvertfrontright->rotateY(M_PI/2);
  rotvertfrontright->rotateX(1.5*M_PI); /// for some unknown reason rotates around z....  5.5* definitely works 
  rotvertfrontright->rotateZ(front_vert_panel_rotation);   //// needs to be 




  auto rothorfronttop = new G4RotationMatrix();
  rothorfronttop->rotateY(M_PI/2);
  //rothormidtop->rotateX(mid_hor_panel_rotation); /// rotates around z   
  rothorfronttop->rotateZ(front_hor_panel_rotation);   //// needs to be 28

  auto rothorfrontbottom = new G4RotationMatrix();
  rothorfrontbottom->rotateY(1.5*M_PI);
  //rothormidbottom->rotateX(M_PI/2); /// for some unknown reason rotates around y this time definitely dont need 
  rothorfrontbottom->rotateZ(M_PI+front_hor_panel_rotation);   //// needs to be 28 
  







  
  
  
  // G4RotationMatrix* my_packRotationMatrix=new G4RotationMatrix(0,pack_rotation,rot);

  //const double tube_rotation = getParameterDouble("tube_rotation_deg")*Units::degree; //OFFforGeoShot// 
  //const double tube_box = getParameterDouble("tube_box_mm")*Units::mm;
  //auto tube_box_fill_material = getParameterMaterial("tube_box_fill_material"); //OFFforGeoShot//



 


 // const int number_of_tubes = getParameterInt("number_of_tubes");
  const int number_of_panels = getParameterInt("number_of_panels");
    //const int number_of_panels = getParameterInt("number_of_panels");
  //const double panel_offset= getParameterDouble("panel_offset_mm")*Units::mm;

  ////////////////////////////////////


  for(int m=0; m<number_of_panels; ++m) {
    // int copyNumber=10000000*m+10000000;
    auto lv_rear_panel_box = createRearPanelBoxLV();
    auto lv_vert_mid_panel_box = createVertMidPanelBoxLV();
    auto lv_hor_mid_panel_box = createHorMidPanelBoxLV();
    auto lv_vert_front_panel_box = createVertFrontPanelBoxLV();
    auto lv_hor_front_panel_box = createHorFrontPanelBoxLV();


    place(lv_rear_panel_box, 0,0, generator_detector_distance,lvWorld, ORANGE, 900000000,0,rot);
    
    place(lv_vert_mid_panel_box, 370,0,  3350,lvWorld, ORANGE, 700000000,0,rotvertmidleft);   // Mid left panel 
    place(lv_vert_mid_panel_box, -370,0,  3350,lvWorld, ORANGE, 800000000,0,rotvertmidright);  // Mid right panel   

    place(lv_hor_mid_panel_box,0,520,  2950,lvWorld, ORANGE, 500000000,0,rothormidtop);   // Mid top panel 
    place(lv_hor_mid_panel_box, 0,-520,  2950,lvWorld, ORANGE, 600000000,0,rothormidbottom);  // Mid bottom panel  

    place(lv_vert_front_panel_box, 835,0,  1750,lvWorld, ORANGE, 300000000,0,rotvertfrontleft);   // Front left panel 
    place(lv_vert_front_panel_box, -835,0,  1750,lvWorld, ORANGE, 400000000,0,rotvertfrontright);  // Front right panel   

    place(lv_hor_front_panel_box,0,702,  1320,lvWorld, ORANGE, 100000000,0,rothorfronttop);   // Front top panel 
    place(lv_hor_front_panel_box, 0,-702,  1320,lvWorld, ORANGE, 200000000,0,rothorfrontbottom);  // Front bottom panel  

  }



  
  
  return pvWorld;
}


  

bool GeoBCS::validateParameters() 
{


// you can apply conditions to control the sanity of the geometry parameters and warn the user of possible mistakes
  // a nice example: Projects/SingleCell/G4GeoSingleCell/libsrc/GeoB10SingleCell.cc

  //const double converter_thickness = getParameterDouble("converter_thickness_um")*Units::um;

  //if(converter_thickness>)
    return true;  
}

