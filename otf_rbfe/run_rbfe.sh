#!/bin/bash
_d="$(pwd)"
echo "$_d"
mypcl=$(realpath $(find ~/ -type d -name "otf_rbfe"))

show_help() {
    echo "Usage: $0 [OPTIONS] [type: dcrg, water, rtr, all] dir1 dir2 ... dirN"
    echo "Options:"
    echo "  -c, --convergence-cutoff VALUE   Set convergence cutoff"
    echo "  -i, --initial-time VALUE         Set initial time"
    echo "  -a, --additional-time VALUE      Set additional time"
    echo "  -f, --first-max VALUE            Set first max value"
    echo "  -s, --second-max VALUE           Set second max value"
    echo "  -S, --schedule VALUE             Set schedule"
	echo "  -n, --num-windows VALUE          Set number of windows"
	echo "  -C, --custom-windows x,y,z       Set custom windows"
	echo "  -o, --sssc VALUE                 Set sssc alpha and beta options (1, 2)"
	echo "  -m, --move-to VALUE              Set destination directory"
	echo "  -A, --equil_restr VALUE            Set additional restraints"
    	echo "  -F, --fpn VALUE        Set number of frames to save per ns"
     echo "  -h, --help                       Show this help message and exit"
	echo "  -R --reference_lam VALUE	 Special treatment for broken trajectories"
	echo "  -sp -special VALUE		 Use site or water"
	echo "  -T --target_lam	VALUE		 Special treatment for broken trajectory equil" 		
	echo "  -ctm1 --custom_ti_mask VALUE      Custom masks for protein-ligand complex TI for lig1"
	echo "  -ctm2 --custom_ti_mask VALUE      Custom masks for protein-ligand complex TI for lig2"
	echo "  -ctmw1 --custom_ti_mask VALUE      Custom masks for solvated ligand TI for lig1"
	echo "  -ctmw1 --custom_ti_mask VALUE      Custom masks for solvated ligand TI for lig2"
	echo "See README.md for default inputs."
}

#default values
convergence_cutoff=0.1
initial_time=2.5
additional_time=0.5
first_max=6.5
second_max=10.5
schedule='equal'
num_windows=9
sssc=2
move_to=.
equil_restr=''
frames_per_ns=0
reference_lam=-1
target_lam=-1
special='site'
custom_ti_mask1=''
custom_ti_mask2=''
custom_ti_mask_wat1=''
custom_ti_mask_wat2=''

#process parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c|--convergence-cutoff)
            convergence_cutoff="$2"
            shift 2
            ;;
        -i|--initial-time)
            initial_time="$2"
            shift 2
            ;;
		-a|--additional-time)
			additional_time="$2"
			shift 2
			;;
		-f|--first-max)
			first_max="$2"
			shift 2	
			;;
		-s|--second-max)
			second_max="$2"
			shift 2
			;;
		-S|--schedule)
			schedule="$2"
			shift 2
			;;
		-n|--num-windows)
			num_windows="$2"
			shift 2
			;;
		-C|--custom-windows)
			custom_windows="$2"
			shift 2
			;;
		-o|--sssc)
			sssc="$2"
			shift 2
			;;
		-m|--move-to)
			move_to="$2"
			shift 2
			;;
		-A|--equil_restr)
			equil_restr="$2"
			shift 2
			;;
		-F|--fpn)
                        frames_per_ns="$2"
                        shift 2
                        ;;
		-R|--reference_lam)
			reference_lam="$2"
			shift 2
			;;
		-T|--target_lam)
                        target_lam="$2"
                        shift 2
                        ;;
		-sp|--special)
			special="$2"
			shift 2
			;;
		-ctm1|--custom_ti_mask1)
			custom_ti_mask1="$2"
                        shift 2
                        ;;
		-ctm2|--custom_ti_mask2)
                        custom_ti_mask2="$2"
                        shift 2
                        ;;
		-ctmw1|--custom_ti_mask_wat1)
			custom_ti_mask_wat1="$2"
                        shift 2
                        ;;
                -ctmw2|--custom_ti_mask_wat2)
                        custom_ti_mask_wat2="$2"
                        shift 2
                        ;;
	

        -h|--help)
            show_help
            exit 0
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "Unknown option: $1" >&2
            show_help
            exit 1
            ;;
        *)
            break
            ;;
    esac
done

type=$1
shift 1
echo $type
echo $custom_ti_mask1 $custom_ti_mask2
FLAGS="--convergence_cutoff $convergence_cutoff --initial_time $initial_time --additional_time $additional_time\n--first_max $first_max --second_max $second_max\n--schedule $schedule --num_windows $num_windows --custom_windows $custom_windows\n--sssc $sssc --special $special --target_lam $target_lam --reference_lam $reference_lam --equil_restr $equil_restr --fpn $frames_per_ns --ctm1 $custom_ti_mask1 --ctm2 $custom_ti_mask2 --ctmw1 $custom_ti_mask_wat1 --ctmw2 $custom_ti_mask_wat2"
for X in "$@"
do
	cd $X
	cp $mypcl/*.py .
	cp $mypcl/../convergence_test.py .

	python3 rbfe_main.py "$mypcl" "$type" "$_d"/$X/scmask.txt --convergence_cutoff "$convergence_cutoff" --initial_time "$initial_time" --additional_time "$additional_time" --first_max "$first_max" --second_max "$second_max" --schedule "$schedule" --num_windows "$num_windows" --custom_windows "$custom_windows" --sssc "$sssc" --special "$special" --equil_restr "$equil_restr" --fpn "$frames_per_ns" --reference_lam "$reference_lam" --target_lam "$target_lam" --ctm1 "$custom_ti_mask1" --ctm2 "$custom_ti_mask2" --ctmw1 "$custom_ti_mask_wat1" --ctmw2 "$custom_ti_mask_wat2"

	echo -e $FLAGS >> otf_log.txt

	cd ..
	mv $X "$move_to"
done
