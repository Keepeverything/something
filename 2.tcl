#!/bin/tclsh
proc proverka {elemn} {
	set fp [open $elemn r]
	set how [read $fp]
	close $fp
    	set names []
	set lines [split $how "\n"]
	set v2 0
	set count1 0
	set count2 0
	foreach line $lines {
		regexp {module\s(\w+) } $line v1 v2
		if { [regexp {input} $line] == 1 } {
				set inline [split $line "\ "]
				foreach w $inline {
					if {[regexp {,} $w]==1} {
						incr count1
					}
				}
				if {$count1 == 0} {
					set count1 1
				}
		}
		if { [regexp {output} $line] == 1 } {
				set inline [split $line "\ "]
				foreach w $inline {
					if {[regexp {,} $w]==1} {
						incr count2
					}
				}
				if {[regexp {;} $line] == 1} {
					incr count2 
				}	
		}
		if {[regexp {endmodule} $line]==1} {
			if {[expr {$count1+$count2}]>3} {
				lappend names $v2
			}
			set count1 0
			set count2 0
		}
	}
	if {$names == []} {
		puts "NO"
	} else {
		puts "YES"
		foreach n $names {
		puts $n
		}
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
		if {$x == ".v"} {
			exist $elemn
		} else {
			puts "eto opredelenno ne verilog"
		}
	}

