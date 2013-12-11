/* ABlibManagerOpenFile.il
 
Library Manager Customization file. This adds the menus
into the Library Manager.
 
***************************************************
 
*/
 
;------------------------------------------------------------------------
; The callback for opening the file
;------------------------------------------------------------------------
procedure(ABlibManagerOpenFile(_menu lib cell view file _cat)
    let((fileName)
        fileName=ddGetObj(lib cell view file)~>writePath
        when(isFile(fileName)
            editFile(fileName)
        ) ; when
    ) ; let
) ; procedure
 
;------------------------------------------------------------------------
; The map callback. This takes care of greying out the menu (or not)
; if a file is not (or is) selected
;------------------------------------------------------------------------
procedure(ABlibManagerOpenFileMapCB(_menu _lib _cell _view file _cat)
    lmgrSensitizeMenuItems('("OpenFileMenuItem") file!="")
    )
