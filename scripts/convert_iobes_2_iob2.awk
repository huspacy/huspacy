BEGIN{ FS="\t"; OFS=FS }
length($0) > 0 {
    tag = $NF;
    if (substr(tag, 1,1) == "1"){
        print $1, "B" substr(tag, 2);
    } else if(substr(tag, 1,1) == "E") {
        print $1, "I" substr(tag, 2);
    } else {
        print $1, $NF;
    }
    prev = tag;
}
length($0) == 0 { print }

