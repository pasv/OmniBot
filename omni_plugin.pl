#/usr/bin/perl
use Irssi;
use MIME:Base64;
use Crypt::CBC;

#
# omni.pl - Irssi plugin for OmniBot's encryption features
# Currently only supports AES-256-cbc. More to be added?
#

$key = undef;


sub cmd_omnikey {
      
    $key=Base64::decode_base64($msg); #it will be given originally in base64
}

# TODO: get IV out of $msg (first 16 bytes)
sub decrypt {
	$msg=MIME::Base64::decode_base64($msg)
	$cipher = Crypt::CBC->new(
	-key    => $key,
	-cipher => "Crypt::OpenSSL::AES"
	); 
	return $cipher->decrypt($msg);
}

# TODO: add random IV in front
sub encrypt {
    $cipher = Crypt::CBC->new(
    -key    => $key,
    -cipher => "Crypt::OpenSSL::AES"
    ); 
    return Base64::encode_base64($cipher->encrypt($msg));
}

sub event_privmsg {
    # $data = "nick/#channel :text"
    my ($server, $data, $nick, $address) = @_;
    my ($target, $text) = split(/ :/, $data, 2);
    
}

sub cmd_omnicrypt {
    my ($data, $server, $witem) = @_;
    if (!$server || !$server->{connected}) {
	Irssi::print("Not connected to server");
	return;
    }
    if ($witem && ($witem->{type} eq "CHANNEL" || $witem->{type} eq "QUERY") && not $data) {
	$msg=encrypt($data)
	$witem->command("MSG ".$witem->{name}." $msg");
    } else {
	Irssi::print("Invalid usage: use in active window!");
    }
}

Irssi::signal_add("event privmsg", "event_privmsg")
Irssi::command_bind('omnikey', 'cmd_omnikey');
Irssi::command_bind('omnicrypt', 'cmd_omnicrypt');
