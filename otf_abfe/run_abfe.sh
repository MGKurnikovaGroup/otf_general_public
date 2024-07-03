#!/bin/bash
mywd=$(pwd)

#Loop to find otf_abfe absolute path
# current_dir=$(pwd)
# while [ "$current_dir" != "/" ]; do
#     if [ -d "$current_dir/otf_abfe" ]; then
#         mypcl="$current_dir/otf_abfe"
#         break
#     fi
#     parent_dir=$(dirname "$current_dir")
#     current_dir="$parent_dir"
# done

# if [ "$current_dir" == "/" ]; then
#     echo "Directory 'otf_abfe' not found."
# fi
mypcl=$(find ../ -type d -name "otf_abfe")

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
	echo "  -C, --custom-windows VALUE       Set custom windows"
	echo "  -m, --move-to VALUE              Set destination directory"
    echo "  -h, --help                       Show this help message and exit"

}

#Option Handling

#default values
convergence_cutoff=0.1
initial_time=2.5
additional_time=0.5
first_max=6.5
second_max=10.5
schedule='equal'
num_windows=10
move_to=.

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
		-m|--move-to)
			move_to="$2"
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

echo "convergence_cutoff = $convergence_cutoff"
echo "initial_time = $initial_time"
echo "additional_time = $additional_time"
echo "first_max = $first_max"
echo "second_max = $second_max"
echo "schedule = $schedule"
echo "num_windows = $num_windows"
echo "custom_windows = $custom_windows"
echo "type = $type"
echo "directories = $@"
echo "otf_abfe directory: $mypcl"
echo "moving to: $move_to"

for X in "$@"
do
	echo =====  $X  =======================
	cd $X
	cp $mypcl/*.py .
	python3 abfe_main.py "$mypcl" "$type" --convergence_cutoff "$convergence_cutoff" --initial_time "$initial_time" --additional_time "$additional_time" --first_max "$first_max" --second_max "$second_max" --schedule "$schedule" --num_windows "$num_windows" --custom_windows "$custom_windows"
	cd ..
	mv $X "$move_to"
done
