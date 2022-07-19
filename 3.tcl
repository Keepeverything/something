#!/usr/bin/wish

proc makeTop { } {
	toplevel .about ;#Make the window
	label .about.lab -text "О программе"
	wm geometry .about =1200x810+600+100
	button .about.but -text "Закрыть" -command {destroy .about}
	set img [image create photo -file "ucheba.png"]
	label .about.img -image $img
	grid .about.lab -row 0 
	grid .about.img -row 1 
	grid .about.but -row 2 
}

set types {
	{"Verilog netlists" {.v} }
	{"All files" * }
}
proc doIt {label} {
	global types .t1 .t2
	set File ""
	set f 0
	set File [tk_getOpenFile -filetypes $types -parent .]
	regexp {\w+(.v)} $File f v2
	if {$File != ""} {
		set f "File: $f"
		$label configure -text $f
		set fp [open $File r]
		set how [read $fp]
		close $fp
		set names []
		set v3 0
		set count 0
		set numstr 0
		set lines [split $how "\n"]
		foreach line $lines {
			incr count
			regexp {module\s(\w+) } $line v1 v2
			if {$v3 != $v2} {
				set v3 $v2
				lappend names "$v3 : $count\n"
			}
		}
		.t1 insert 0.0 $how
		.t2 delete 0.0 end
		foreach n $names {
			incr numstr
			.t2 insert "$numstr.0" $n
		}
	}
	
	#set f "File: $f"
	#$label configure -text $f
	
}

wm title . "Имена модулей"
wm geometry . =490x810+100+100
wm resizable . 0 0

label .l1 -text "" ;#-font { -size 14 } 
grid .l1 -row 0 -column 3 

#######menubutton
menubutton .mb -text File -menu .mb.menu
grid .mb -row 0 -column 0
menu .mb.menu
.mb.menu add  check -label Open -command { doIt .l1}
.mb.menu add separator
.mb.menu add  check -label Exit -command exit

menubutton .mb1 -text Help -menu .mb1.menu
grid .mb1 -row 0  -column 1
menu .mb1.menu
.mb1.menu add  check -label About -command { makeTop }

#######text
text .t1 -width 60 -height 35 -wrap word
text .t2 -width 60 -height 10 -wrap word
grid .t1 -row 2 -column 0 -columnspan 30
grid .t2 -row 3 -column 0 -columnspan 30
#pack .l2 -side right -fill x




