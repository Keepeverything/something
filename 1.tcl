#!/bin/tclsh
proc proverka {elemn} {
	set a 0 ;#kolichestvo subckt
	set names [] ;#imena podshem
	set fp [open $elemn r]
	set how [read $fp]
	close $fp

	set lines [split $how "\n"]
	foreach line $lines {
		set inline [split $line "\ "]
		if {[lsearch -exact $inline ".subckt"] == 0} {
			incr a
			lappend names [lindex $inline 1]
		}
	}
	if {$a>0} {
		puts "yes $a $names"
	} else {
		puts "no"
	}
}
proc exist {elemn} {
	if {[file exists $elemn]} {
		proverka $elemn
	} else {
		puts "file not exist"
	}
}		
###################################
	foreach elemn $argv {
		set x [file extension $elemn]
		if {$x == ".sp"} {
			exist $elemn
		} else {
			puts "this is not hspice"
		}
	}

