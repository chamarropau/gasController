import subprocess as sb


print("See the global NIC name:")
n = ("netsh interface ipv4 show interface")
sb.run(n, shell=True)
n2 = ('netsh interface ipv4 show address Ethernet')
sb.run(n2, shell=True)