# check if socat is installed
if ! command -v socat &> /dev/null
then
    echo "socat could not be found"
    exit
fi

socat -d -d pty,raw,echo=0 pty,raw,echo=0