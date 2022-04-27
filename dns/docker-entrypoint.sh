#! /bin/sh

GITLAB_SERVER=${GITLAB_SERVER}
WEB_SERVER=${WEB_SERVER}
DNS_SERVER=${DNS_SERVER}


if [ -z "$WEB_SERVER" ] || [ -z "$DNS_SERVER" ] || [ -z "$GITLAB_SERVER" ] ;
then
    echo "You need to specify the IP address for the DNS server and the employee web application IP address in .env file:
        
        $ cat .env
        IPV4_GITLAB=<GITLAB_SERVER_IP_ADDRESS>
        IPV4_DNS=<DNS_SERVER_IP_ADDRESS>
        IPV4_WORK=<EMPLOYEE_SERVER_IP_ADDRESS>"
    
    exit 1
else
    echo "Using the IP $DNS_SERVER for DNS server, IP $WEB_SERVER for the web application, and IP $GITLAB_SERVER for the gitlab server."
    sed -i "s/<GITLAB_SERVER>/$GITLAB_SERVER/g" /etc/bind/zones/db.ab-finance.no
    sed -i "s/<EMPLOYEE_SERVER>/$WEB_SERVER/g" /etc/bind/zones/db.ab-finance.no
    sed -i "s/<DNS_SERVER>/$DNS_SERVER/g" /etc/bind/zones/db.ab-finance.no
fi

/etc/init.d/bind9 start && while :; do sleep 10; done