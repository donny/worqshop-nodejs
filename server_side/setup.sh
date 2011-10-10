# For OpenSolaris

dladm create-etherstub etherstub0
dladm create-vnic -l etherstub0 vnic0
dladm create-vnic -l etherstub0 vnic1
dladm create-vnic -l etherstub0 vnic2
dladm create-vnic -l etherstub0 vnic3
dladm create-vnic -l etherstub0 vnic4

ifconfig vnic0 plumb
ifconfig vnic0 inet 192.168.0.1 up

routeadm -u -e ipv4-forwarding

cat > /etc/ipf/ipnat.conf <<END
map xnf0 192.168.0.0/24 -> 0/32 portmap tcp/udp auto
map xnf0 192.168.0.0/24 -> 0/32

rdr xnf0 0.0.0.0/0 port 22101  -> 192.168.0.101 port 22
rdr xnf0 0.0.0.0/0 port 22102  -> 192.168.0.102 port 22
rdr xnf0 0.0.0.0/0 port 22103  -> 192.168.0.103 port 22
rdr xnf0 0.0.0.0/0 port 22104  -> 192.168.0.104 port 22
END

svcadm enable network/ipfilter

zonecfg -z zone1 <<END
create
set zonepath=/mnt/zone1
set ip-type=exclusive
add net
set physical=vnic1
end
add fs
set dir=/opt
set special=/opt
set type=lofs
add options ro
end
verify
commit
exit
END

zonecfg -z zone2 <<END
create
set zonepath=/mnt/zone2
set ip-type=exclusive
add net
set physical=vnic2
end
add fs
set dir=/opt
set special=/opt
set type=lofs
add options ro
end
verify
commit
exit
END

zonecfg -z zone3 <<END
create
set zonepath=/mnt/zone3
set ip-type=exclusive
add net
set physical=vnic3
end
add fs
set dir=/opt
set special=/opt
set type=lofs
add options ro
end
verify
commit
exit
END

zonecfg -z zone4 <<END
create
set zonepath=/mnt/zone4
set ip-type=exclusive
add net
set physical=vnic4
end
add fs
set dir=/opt
set special=/opt
set type=lofs
add options ro
end
verify
commit
exit
END

zoneadm -z zone1 install
zoneadm -z zone2 clone zone1
zoneadm -z zone3 clone zone1
zoneadm -z zone4 clone zone1

zoneadm -z zone1 ready
zoneadm -z zone2 ready
zoneadm -z zone3 ready
zoneadm -z zone4 ready

cat > /mnt/zone1/root/etc/sysidcfg <<END
system_locale=C
terminal=xterms
network_interface=primary {
	hostname=zone1
	ip_address=192.168.0.101
	netmask=255.255.255.0
	default_route=192.168.0.1
	protocol_ipv6=no
}
root_password=h87UkRudhD32k
timezone=US/Pacific
security_policy=none
nfs4_domain=dynamic
name_service=none
END

cat > /mnt/zone2/root/etc/sysidcfg <<END
system_locale=C
terminal=xterms
network_interface=primary {
	hostname=zone2
	ip_address=192.168.0.102
	netmask=255.255.255.0
	default_route=192.168.0.1
	protocol_ipv6=no
}
root_password=h87UkRudhD32k
timezone=US/Pacific
security_policy=none
nfs4_domain=dynamic
name_service=none
END

cat > /mnt/zone3/root/etc/sysidcfg <<END
system_locale=C
terminal=xterms
network_interface=primary {
	hostname=zone3
	ip_address=192.168.0.103
	netmask=255.255.255.0
	default_route=192.168.0.1
	protocol_ipv6=no
}
root_password=h87UkRudhD32k
timezone=US/Pacific
security_policy=none
nfs4_domain=dynamic
name_service=none
END

cat > /mnt/zone4/root/etc/sysidcfg <<END
system_locale=C
terminal=xterms
network_interface=primary {
	hostname=zone4
	ip_address=192.168.0.104
	netmask=255.255.255.0
	default_route=192.168.0.1
	protocol_ipv6=no
}
root_password=h87UkRudhD32k
timezone=US/Pacific
security_policy=none
nfs4_domain=dynamic
name_service=none
END

cat > /mnt/zone1/root/etc/resolv.conf <<END
domain compute-1.internal
nameserver 172.16.0.23
END

cp /mnt/zone1/root/etc/resolv.conf /mnt/zone2/root/etc/resolv.conf
cp /mnt/zone1/root/etc/resolv.conf /mnt/zone3/root/etc/resolv.conf
cp /mnt/zone1/root/etc/resolv.conf /mnt/zone4/root/etc/resolv.conf

zoneadm -z zone1 boot
zoneadm -z zone2 boot
zoneadm -z zone3 boot
zoneadm -z zone4 boot

sleep 600

cp /mnt/zone1/root/etc/nsswitch.dns /mnt/zone1/root/etc/nsswitch.conf
cp /mnt/zone2/root/etc/nsswitch.dns /mnt/zone2/root/etc/nsswitch.conf
cp /mnt/zone3/root/etc/nsswitch.dns /mnt/zone3/root/etc/nsswitch.conf
cp /mnt/zone4/root/etc/nsswitch.dns /mnt/zone4/root/etc/nsswitch.conf
