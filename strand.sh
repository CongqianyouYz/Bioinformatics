strand_file=$1
strand1=`sed -n '5p' $strand_file | sed 's/.*: //'`
strand2=`sed -n '6p' $strand_file | sed 's/.*: //'`
tag=$(echo "$strand1 - $strand2" | bc )
if [ $(echo "$tag < -.4"|bc) -eq 1 ]
then
	echo "0"
elif [ $(echo "$tag > .4"|bc) -eq 1 ]
then
	echo "1"
else
	echo "0.5"
fi
