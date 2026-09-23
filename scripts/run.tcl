# Open EDA Verification - Tcl Flow Wrapper

puts "========================================"
puts "       TCL EDA VERIFICATION FLOW"
puts "========================================"

set simulator "icarus"
set seed 1

puts "Simulator : $simulator"
puts "Seed      : $seed"
puts "========================================"

set command "python run.py --simulator $simulator --seed $seed"

puts "Executing:"
puts "  $command"
puts ""

set result [catch {exec {*}$command} output]

puts $output

if {$result != 0} {
    puts "========================================"
    puts "TCL FLOW RESULT : FAIL"
    puts "========================================"
    exit 1
}

puts "========================================"
puts "TCL FLOW RESULT : PASS"
puts "========================================"

exit 0
