# @kaptainzero

import serial, time

# settings
NL = '\r\n'
username = 'admin'
password = 'admin'
gatekeeper=''

def dbg():
    print('READING:%s BYTES' %(sp.inWaiting()))
    print(sp.read_all())

def rbc():
    _ = sp.read_all()
    time.sleep(1)
# configure the serial conection for tenor

try:
    sp = serial.Serial(
            port='COM1',
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits= serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            sp.timeout=1,
            sp.xonxoff=False,
            sp.rtscts=False,
            sp.dsrdtr=False,
            sp.writeTimeout=2)

    sp.isOpen()
    sp.flushInput()
    sp.flushOutput()
except serial.SerialException:
    print 'Another program is using serial port; or serial port is not ready'
    exit(1)

output=''
print 'PLUG IN TENOR WITHIN 5 SECONDS'
time.sleep(7)

print 'FACTORY DEFAULTS IN 30 SECONDS'

# reset using interrupt 'r'
sp.write('r'+NL)
time.sleep(1)
sp.write('y'+NL)

# uncomment for insystem reset
#sp.write('mc'+NL+'set factory'+NL+'yes'+NL)

dbg()
time.sleep(30)

print 'PROGRAMMING PROTOCOL INITIATED'
sp.write('%s\r%s'%(username,password))
#rbc()
dbg()

# CONFIG MODE
sp.write('conf'+NL)

#rbc()
dbg()

# ETHERNET AND IP ADDRESS
sp.write('eth'+NL)
ipaddress = raw_input('IP ADDRESS: ')
sp.write('set ipa '+ ipaddress + NL)
subnetmask = raw_input('SUBNET MASK: ')
sp.write('set sm ' + subnetmask + NL)
sp.write('siprd'+NL)
gateway = raw_input('GATEWAY: ')
sp.write('change 1 g '+gateway+NL)
sp.write('su'+NL)
#rbc()
dbg()


# DP
sp.write('dp'+NL)
sp.write('set max 8'+NL)
sp.write('set min 3'+NL)
sp.write('set ie 1'+NL)
sp.write('set cpp'+NL)
sp.write('set ldp'+NL)
sp.write('set pstn'+NL)
sp.write('set iprp'+NL)
sp.write('set intlp[1]'+NL)
sp.write('set mp'+NL)
sp.write('set dpc 0'+NL)
sp.write('set ptc 10'+NL)
sp.write('priv'+NL)
sp.write('set privdnl 5'+NL)
sp.write('su'+NL)
#rbc()
dbg()


# H323
gatekeeper = raw_input('GATEKEEPER: ')
sp.write('h323'+NL)
sp.write('set pgkipa '+gatekeeper+NL)
sp.write('su'+NL)
#rbc()
dbg()

# CASSG PHONE
sp.write('cassg phone'+NL)
sp.write('st 3'+NL)
sp.write('ds 1'+NL)
sp.write('cidg 1'+NL)
#rbc()
dbg()


# NUMBERING PLAN
numbers = []
n_numbers = int(raw_input('NUMBERS COUNT: '))
for i in range(n_numbers):
    numbers.append(raw_input('NUMBER #'+str(i+1)+': '))

for number in numbers:
    # HLDND
    sp.write('new hldnd pub'+number+NL)
    sp.write('add ' + number+NL)
    sp.write('new hldnd prv'+number+NL)
    sp.write('add ' + number+NL)
    sp.write('set ldnt 1'+NL)
    # LCRG
    sp.write('new lcrg '+number+NL)
    sp.write('set pubhlda[1] hldnd-pub'+number+NL)
    sp.write('set privhlda[1] hldnd-prv'+number+NL)
    # CG
    sp.write('new cg ' + number+NL)
    sp.write('set sga cassg-phone'+NL)
    sp.write('set rga lcrg-'+number+NL)
    sp.write('su'+NL)
    # sleep
    #rbc()
    dbg()
# MAPPING TO PHY PORTS
sp.write('ai phone'+NL)
for i in range(n_numbers):
    sp.write('map ' + str(i+1) + ' cg ' + numbers[i] + NL)
    sp.write('su'+NL)
    #rbc()
    dbg()

# SL 2
sp.write('sl 2'+NL)
sp.write('set on[1..'+str(n_numbers)+'] 1' + NL)
sp.write('su'+NL)
#rbc()
dbg()


# NEW PASSWORD
sp.write('main'+NL)
sp.write('password'+NL)
sp.write('admin'+NL)
new_password = raw_input('NEW PASSWORD: ')
sp.write(new_password+NL)
sp.write(new_password+NL)
sp.write('su'+NL)
dbg()
# finish
#sp.read(sp.inWaiting())
sp.close()
