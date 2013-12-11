/*
Tested in    : IC5141
Lint score: 100    
Description: This code will display the Cell Name and Instance Name at the top banner.  Bindkeys are modified to run this function "CCSmySel". When you press the Left Mouse Button it will select an instance and display information at Banner.
 
***********************************************************************
* DISCLAIMER: This code is provided for Cadence customers to use      *
* with Cadence tools at their own risk. The code may require          *
* modification to satisfy the requirements of any user. The code and  *
* any modifications to the code may not be compatible with current or *
* future versions of Cadence products.                                *
* THE CODE IS PROVIDED "AS IS" AND WITH NO WARRANTIES, INCLUDING      *
* WITHOUT LIMITATION ANY EXPRESS OR IMPLIED WARRANTIES OF             *
* MERCHANTABILITY, FITNESS FOR A PARTICULAR USE OR NON-INFRINGEMENT.  *
* © 2006 Cadence Design Systems, Inc. All rights reserved.            *
***********************************************************************
*/
 
procedure(CCSmySel()
  let((ss cn in)
       mouseSingleSelectPt()
       ss=geGetSelSet()
         if(ss
            then
            case(car(ss)~>objType
             ("inst"
                cn=car(ss)~>cellName
                in=car(ss)~>name
                hiChangeBannerLabel(hiGetCurrentWindow() sprintf(nil "%s:%s" cn in) 0)
             )
             ("net"
                cn=car(ss)~>name      
                hiChangeBannerLabel(hiGetCurrentWindow() sprintf(nil "%s" cn) 0)
             )
             ("mosaic"
                hiDeleteBannerLabel(hiGetCurrentWindow() 0)
             )
             (t
                hiDeleteBannerLabel(hiGetCurrentWindow() 0)
             )
               );case
              else
                hiDeleteBannerLabel(hiGetCurrentWindow() 0)
            );if
      );let
);procedure
                                                                                                                                  
hiSetBindKeys( "Layout" list(list("None<Btn1Down>" "CCSmySel()" "mouseAddPt()")))
hiSetBindKeys( "Schematics" list(list("None<Btn1Down>" "CCSmySel()" "mouseAddPt()")))
