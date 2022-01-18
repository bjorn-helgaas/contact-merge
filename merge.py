#!/usr/bin/perl

# read CSV file from STDIN, produce envelopes.tex
# ./merge.py < contacts.csv > envelopes.tex
# xelatex envelopes.tex
# okular envelopes.pdf, print with scale "none, print original size"

use Text::CSV_XS;
binmode(STDOUT, ":utf8");	# Google Contacts exports UTF-8

$from = "name\\\\street\\\\city, st  zip";

sub prefix {
    print("\\documentclass[12pt]{letter}\n");
    print("\\usepackage[noprintbarcodes,nocapaddress]{envlab}\n");
    print("\\SetEnvelope{7.25in}{5.25in}\n");
    print("\\makelabels\n");
    print("\\begin{document}\n");
    print("\\startlabels\n");
}

sub postfix {
    print("\\end{document}\n");
}

sub mklabel {
    my $addr = shift;

    $addr =~ s/ /~/g;		# prevent line breaks
    $addr =~ s/#/\\#/g;		# escape special character '#'
    $addr =~ s/&/\\&/g;		# escape special character '&'

    $addr =~ s/\n/\\\\/g;	# start new line ('\\') at \n

    print("\\mlabel{%\n");
    print("  $from}{%\n");
    print("  \\textrm{\\textit{\\large ");
    print("$addr");
    print("}}}\n");
}

prefix();

my $csv = Text::CSV_XS->new({binary => 1, auto_diag => 1});
$csv->header(STDIN);
while (my $contact = $csv->getline(STDIN)) {
    $addr = $contact->[42];	# Address 1 - Formatted
    $to = $contact->[72];	# Custom Field 1 - Value

    $addr =~ s/US$//;		# no need for "US" on domestic mail
    $addr =~ s/, USA$//;	# how does this happen?
    if ($addr =~ /,.*,/) {	# street, city, state sometimes on one line
	$addr =~ s/([^,]),/$1\n/;
    }
    chomp($addr);
    $addr =~ s/\n /\n/;
    mklabel("$to\n$addr");
}

postfix();
