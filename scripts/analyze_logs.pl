#!/usr/bin/env perl

use strict;
use warnings;

my $log_path = shift @ARGV;

if (!defined $log_path) {
    print "Usage: perl scripts/analyze_logs.pl <simulation.log>\n";
    exit 1;
}

if (!-f $log_path) {
    print "ERROR: Log file not found: $log_path\n";
    exit 1;
}

open my $fh, '<', $log_path
    or die "ERROR: Cannot open $log_path: $!\n";

my $content = do {
    local $/;
    <$fh>;
};

close $fh;

my ($status) = $content =~ /RESULT\s*:\s*(PASS|FAIL)/;
my ($checks) = $content =~ /Checks\s*:\s*(\d+)/;
my ($errors) = $content =~ /Errors\s*:\s*(\d+)/;

$status = defined $status ? $status : "UNKNOWN";
$checks = defined $checks ? $checks : 0;
$errors = defined $errors ? $errors : 0;

my $classification = "UNKNOWN";

if ($status eq "PASS" && $errors == 0) {
    $classification = "PASS";
}
elsif ($content =~ /SCOREBOARD ERROR/i) {
    $classification = "DUT_MISMATCH";
}
elsif ($content =~ /assertion|assert failed/i) {
    $classification = "SVA_FAILURE";
}
elsif ($content =~ /timeout/i) {
    $classification = "TIMEOUT";
}
elsif ($status eq "FAIL") {
    $classification = "VERIFICATION_FAILURE";
}

print "Log: $log_path\n";
print "\n";
print "Verification : $status\n";
print "Checks       : $checks\n";
print "Errors       : $errors\n";
print "Classification: $classification\n";

exit($status eq "PASS" ? 0 : 1);
