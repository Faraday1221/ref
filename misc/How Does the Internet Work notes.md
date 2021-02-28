# How does the Internet work?
[PDF here](https://web.stanford.edu/class/msande91si/www-spr04/readings/week1/InternetWhitepaper.htm)

## Where to Begin? Internet Addresses
[How do I find my ip address from the command line](http://apple.stackexchange.com/questions/20547/how-do-i-find-my-ip-address-from-the-command-line)
*several of the comments here are work checking out*
[ifconfig wiki](https://en.wikipedia.org/wiki/Ifconfig)
[How to use ping](http://osxdaily.com/2010/04/28/how-to-use-ping-on-a-mac-pinging-websites-domains-or-ip-addresses/)

Terms:
- DHCP: Dynamic Host Configuration Protocol
- ICMP: Internet Control Message Protocol
- IP Address: Internet Protocol Address

## Protocol Stacks and Packets

Terms:
- Protocol Stack: sequence of protocols required to accomplish some process
- TCP/IP: Transmission Control Protocol Layer / Internet Protocol Layer (internet protocol stack)
- packets: chunks of data, originating at the application layer. They store routing information from the TCP/IP

## Networking Infrastructure
We can trace the route of a packet using the **Traceroute** program
    traceroute www.yahoo.com

[A basic overview of traceroute](http://www.inmotionhosting.com/support/website/how-to/read-traceroute)

## Internet Infrastructure

Terms:
- NSP: Network Service Provider,  a large network part of the internet 'backbone'
- NAP: Network Access Point, a hub that connects NSPs such that a packet can travel over different paths
- MAE: Metropolitan Area Exchanges, essentially a privately owned NAPs
- IX: short for Internet Exchange Points, referring to NAPs and MAEs

## Internet Routing Hierarchy
The information required to get packets to their destinations are contained in
routing tables kept by each router connected to the internet. **Routers are packet switches**

Routers typically know about their sub-networks, not what is 'above' it

## Domain Name Service

DNS: Domain Name Service is a distributed database that tracks computer names
and corresponding IP addresses. Typically stored on a Primary and Secondary server
for any given computer.

[networksetup to find dns](http://osxdaily.com/2011/06/03/get-dns-server-ip-command-line-mac-os-x/)

## Internet Protocols

### Application Protocols: HTTP and the World Wide Web
HTTP is the protocol used by web browsers to communicate with web servers


Terms:
- HTTP: Hypertext Transfer Protocol - the application protocol that makes the web work
- RFC: Request for Comments - this is the document that describes Internet protocols e.g. RFC 1945 for HTTP

telnet
_Here is some coolness, telnet is a command line tool used to connect to various
websites, for instance freechess.org, it is like time traveling back to 1985
(or Russia 2010) to place chess from the command line. Amazing_

[telnet instructions](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/telnet.1.html)
[telnet geek suggestions](http://www.digitalcitizen.life/5-fun-geeky-things-you-can-do-telnet-client)
[a cool site about old school internet and telnet](http://cowbelljs.blogspot.com/2011/12/lost-art-of-telnet.html)

    telnet freechess.org
    telnet telehack.com _then_ starwars
