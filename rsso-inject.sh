for ipadd in {100..230} ; 
do
    echo  "Acct-Status-Type=1,Framed-IP-Address=192.168.1.$ipadd,Calling-Station-Id=JUL07-1125-$ipadd,Class=Any" | radclient 192.168.1.99 acct 12345
done

for ipadd in {100..230} ; 
do
    echo  "Acct-Status-Type=2,Framed-IP-Address=192.168.1.$ipadd,Calling-Station-Id=JUL07-1125-$ipadd,Class=Any" | radclient 192.168.1.99 acct 12345
done
