send_mail() {
    local text="$1"
    local object="$2"
    local sender="$3"
    local destination="$4"
    echo $text | mail -s $object -r "$sender" $destination
}