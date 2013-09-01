#!/bin/bash

declare -a field
declare sign
declare opSign
declare winner

PrintField()
{
	local index
	local i
	local j
	local s

	for ((i=0; i<3; i++)); do
		s=\|
		for ((j=0; j<3; j++)); do
			index=$((i*3 + j))
			s=$s${field[index]}
			s=$s\|
		done
		echo $s
	done
}

DoSet()
{
	local index
	local x=$1
	local y=$2

	if (( $x < 0 || $x > 3 || $y < 0 || $y > 3 )); then
		echo \($x $y\) is outside the field \(3x3\)
		return 1
	fi

	index=$((y*3 + x))

	if [[ ¨${field[index]}¨ != ¨\ ¨ ]]; then
		echo \($x $y\) already has a mark
		return 1
	fi

	field[index]=$sign
	
	return 0
}

PlayerGame()
{
	local x
	local y

	echo Your choice... \(x,y\)=1..3

	while true
	do
		read x
		read y

		x=$((x-1))
		y=$((y-1))

		if DoSet $x $y; then
			break
		fi
	done
}

OneStepToWin()
{
	local i
	local i1
	local i2
	local i3

	if [[ ¨${field[0]}¨ == ¨${field[4]}¨ && ¨${field[4]}¨ == ¨$opSign¨ && ¨${field[8]}¨ == ¨\ ¨ ]]; then
		field[8]=$opSign
		return 0
	fi

	if [[ ¨${field[0]}¨ == ¨${field[8]}¨ && ¨${field[8]}¨ == ¨$opSign¨ && ¨${field[4]}¨ == ¨\ ¨ ]]; then
		field[4]=$opSign
		return 0
	fi

	if [[ ¨${field[4]}¨ == ¨${field[8]}¨ && ¨${field[8]}¨ == ¨$opSign¨ && ¨${field[0]}¨ == ¨\ ¨ ]]; then
		field[0]=$opSign
		return 0
	fi

	#
	if [[ ¨${field[2]}¨ == ¨${field[4]}¨ && ¨${field[4]}¨ == ¨$opSign¨ && ¨${field[6]}¨ == ¨\ ¨ ]]; then
		field[6]=$opSign
		return 0
	fi

	if [[ ¨${field[4]}¨ == ¨${field[6]}¨ && ¨${field[6]}¨ == ¨$opSign¨ && ¨${field[2]}¨ == ¨\ ¨ ]]; then
		field[2]=$opSign
		return 0
	fi

	if [[ ¨${field[2]}¨ == ¨${field[6]}¨ && ¨${field[6]}¨ == ¨$opSign¨ && ¨${field[4]}¨ == ¨\ ¨ ]]; then
		field[4]=$opSign
		return 0
	fi

	for ((i=0; i<3; i++)); do
		i1=$((i*3))
		i2=$((i*3+1))
		i3=$((i*3+2))
		if [[ ¨${field[i1]}¨ == ¨${field[i2]}¨ && ¨${field[i2]}¨ == ¨$opSign¨ && ¨${field[i3]}¨ == ¨\ ¨ ]]; then
			field[i3]=$opSign
			return 0
		fi

		if [[ ¨${field[i1]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$opSign¨ && ¨${field[i2]}¨ == ¨\ ¨ ]]; then
			field[i2]=$opSign
			return 0
		fi

		if [[ ¨${field[i2]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$opSign¨ && ¨${field[i1]}¨ == ¨\ ¨ ]]; then
			field[i1]=$opSign
			return 0
		fi
	done

	for ((i=0; i<3; i++)); do
		i1=$((i))
		i2=$((i+3))
		i3=$((i+6))
		if [[ ¨${field[i1]}¨ == ¨${field[i2]}¨ && ¨${field[i2]}¨ == ¨$opSign¨ && ¨${field[i3]}¨ == ¨\ ¨ ]]; then
			field[i3]=$opSign
			return 0
		fi

		if [[ ¨${field[i1]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$opSign¨ && ¨${field[i2]}¨ == ¨\ ¨ ]]; then
			field[i2]=$opSign
			return 0
		fi

		if [[ ¨${field[i2]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$opSign¨ && ¨${field[i1]}¨ == ¨\ ¨ ]]; then
			field[i1]=$opSign
			return 0
		fi
	done

	return 1
}

PreventPlayerWin()
{
	local i
	local i1
	local i2
	local i3

	if [[ ¨${field[0]}¨ == ¨${field[4]}¨ && ¨${field[4]}¨ == ¨$sign¨ && ¨${field[8]}¨ == ¨\ ¨ ]]; then
		field[8]=$opSign
		return 0
	fi

	if [[ ¨${field[0]}¨ == ¨${field[8]}¨ && ¨${field[8]}¨ == ¨$sign¨ && ¨${field[4]}¨ == ¨\ ¨ ]]; then
		field[4]=$opSign
		return 0
	fi

	if [[ ¨${field[4]}¨ == ¨${field[8]}¨ && ¨${field[8]}¨ == ¨$sign¨ && ¨${field[0]}¨ == ¨\ ¨ ]]; then
		field[0]=$opSign
		return 0
	fi

	#
	if [[ ¨${field[2]}¨ == ¨${field[4]}¨ && ¨${field[4]}¨ == ¨$sign¨ && ¨${field[6]}¨ == ¨\ ¨ ]]; then
		field[6]=$opSign
		return 0
	fi

	if [[ ¨${field[4]}¨ == ¨${field[6]}¨ && ¨${field[6]}¨ == ¨$sign¨ && ¨${field[2]}¨ == ¨\ ¨ ]]; then
		field[2]=$opSign
		return 0
	fi

	if [[ ¨${field[2]}¨ == ¨${field[6]}¨ && ¨${field[6]}¨ == ¨$sign¨ && ¨${field[4]}¨ == ¨\ ¨ ]]; then
		field[4]=$opSign
		return 0
	fi

	for ((i=0; i<3; i++)); do
		i1=$((i*3))
		i2=$((i*3+1))
		i3=$((i*3+2))
		if [[ ¨${field[i1]}¨ == ¨${field[i2]}¨ && ¨${field[i2]}¨ == ¨$sign¨ && ¨${field[i3]}¨ == ¨\ ¨ ]]; then
			field[i3]=$opSign
			return 0
		fi

		if [[ ¨${field[i1]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$sign¨ && ¨${field[i2]}¨ == ¨\ ¨ ]]; then
			field[i2]=$opSign
			return 0
		fi

		if [[ ¨${field[i2]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$sign¨ && ¨${field[i1]}¨ == ¨\ ¨ ]]; then
			field[i1]=$opSign
			return 0
		fi
	done

	for ((i=0; i<3; i++)); do
		i1=$((i))
		i2=$((i+3))
		i3=$((i+6))
		if [[ ¨${field[i1]}¨ == ¨${field[i2]}¨ && ¨${field[i2]}¨ == ¨$sign¨ && ¨${field[i3]}¨ == ¨\ ¨ ]]; then
			field[i3]=$opSign
			return 0
		fi

		if [[ ¨${field[i1]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$sign¨ && ¨${field[i2]}¨ == ¨\ ¨ ]]; then
			field[i2]=$opSign
			return 0
		fi

		if [[ ¨${field[i2]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ == ¨$sign¨ && ¨${field[i1]}¨ == ¨\ ¨ ]]; then
			field[i1]=$opSign
			return 0
		fi
	done

	return 1
}

AiGame()
{
	local x
	local y
	local index

	echo Ai play...

	if OneStepToWin; then
		return
	fi

	if PreventPlayerWin; then
		return
	fi

	while true
	do
		x=$(($RANDOM%9))
		y=$(($RANDOM%9))
		
		index=$((y*3+x))
		if [[ ¨${field[index]}¨ == ¨\ ¨ ]]; then
			field[index]=$opSign
			break
		fi
	done
}

CheckWin()
{
	local i
	local j
	local found
	local i1
	local i2
	local i3

	if [[ ¨${field[0]}¨ == ¨${field[4]}¨ && ¨${field[4]}¨ == ¨${field[8]}¨ && ¨${field[0]}¨ != ¨\ ¨ ]]; then
		if [[ ¨${field[0]}¨ == ¨$sign¨ ]]; then
			winner=you
		else
			winner=ai
		fi
		return 0
	fi

	if [[ ¨${field[2]}¨ == ¨${field[4]}¨ && ¨${field[4]}¨ == ¨${field[6]}¨ && ¨${field[2]}¨ != ¨\ ¨ ]]; then
		if [[ ¨${field[2]}¨ == ¨$sign¨ ]]; then
			winner=you
		else
			winner=ai
		fi
		return 0
	fi

	for ((i=0; i<3; i++)); do
		i1=$((i*3))
		i2=$((i*3+1))
		i3=$((i*3+2))
		if [[ ¨${field[i1]}¨ == ¨${field[i2]}¨ && ¨${field[i2]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ != ¨\ ¨ ]]; then
			if [[ ¨${field[i1]}¨ == ¨$sign¨ ]]; then
				winner=you
			else
				winner=ai
			fi
			return 0
		fi
	done

	for ((i=0; i<3; i++)); do
		i1=$((i))
		i2=$((i+3))
		i3=$((i+6))
		if [[ ¨${field[i1]}¨ == ¨${field[i2]}¨ && ¨${field[i2]}¨ == ¨${field[i3]}¨ && ¨${field[i3]}¨ != ¨\ ¨ ]]; then
			if [[ ¨${field[i1]}¨ == ¨$sign¨ ]]; then
				winner=you
			else
				winner=ai
			fi
			return 0
		fi
	done

	found=false
	for ((i=0; i<3; i++)); do
		for ((j=0; j<3; j++)); do
			i1=$((i*3+j))
			if [[ ¨${field[i1]}¨ == ¨\ ¨ ]]; then
				found=true
				break
			fi
		done

		if [[ $found == true ]]; then
			break
		fi
	done

	if [[ $found == false ]]; then
		return 0
	fi

	return 1 
}

Play()
{
	local first=false

	if (( $(($RANDOM % 2)) == 0 )); then
		first=true
		echo Luck\! You play first...
	fi

	winner=\ 

	while true
	do
		if [[ $first == true ]]; then
			PlayerGame
			PrintField

			if CheckWin; then
				break;
			fi

			AiGame
			PrintField

			if CheckWin; then
				break;
			fi
		else
			AiGame
			PrintField

			if CheckWin; then
				break;
			fi

			PlayerGame
			PrintField

			if CheckWin; then
				break;
			fi
		fi
	done

	if [[ ¨$winner¨ == ¨\ ¨ ]]; then
		echo Standoff \;\)
	else
		echo $winner win\!
	fi
}

Main()
{
	local index
	local i
	local j

	echo =================
	echo Tic-Tac-Toe \;\)
	echo =================

	while true
	do
		echo Select you sign \(x/0\)

		read sign

		if [[ ¨$sign¨ == ¨[xX]¨ ]]; then
			sign=x
			opSign=\0
			break
		fi

		if [[ ¨$sign¨ == ¨0¨ ]]; then
			sign=\0
			opSign=x
			break
		fi
	done

	echo You have selected $sign

	for ((i=0; i<3; i++)); do
		for ((j=0; j<3; j++)); do
			index=$((i*3 + j))
			field[index]=\ 
		done
	done

	Play
}

Main


