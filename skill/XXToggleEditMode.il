;##########################################################################################
;#
;# Function Name: XXToggleEditMode()
;# function will toggle schematic between edit/read and release license 
;#
;# created by Ali Hadiashar 08/19/2010
;#
;##########################################################################################

;;;;;;;;;;;;;
;
; Ali Hadiashar 20100819 verion 1.00: initial version
;
; load("/nfs/home/ahadiashar/scripts/skill/XXToggleEditMode.il")
;;;;;;;
;
;
;
;


procedure( SEToggleEditMode( wnd )
if( equal( wnd~>cellView~>mode "r" ) 
 then
  schHiChangeEditMode( "a" )
 else
  ;avMakeReadOnly()
  lmCheckIn("34500")
  schHiChangeEditMode( "r" )
  )
) ; end proc XXToggleEditMode

procedure( LEToggleEditMode( wnd )
if( equal( wnd~>cellView~>mode "r" ) 
 then
  geChangeEditMode( "a" )
 else
  lmCheckIn("300")
  lmCheckIn("3000")
  geChangeEditMode( "r" )
  )
) ; end proc LEToggleEditMode
