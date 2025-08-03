import os
import sys
import argparse
from pathlib import Path
import shutil
import subprocess

"""
Find directory that contains otf_abfe within the home directory,
and return the resolved path.

If the directory is not found, display an error.
"""
def find_dir_abfe():
    home = Path.home()
    for path in home.rglob('otf_abfe'):
        if path.is_dir():
            return path.resolve() # mypcl=$(realpath $(find ~/ -type d -name "otf_abfe"))
    sys.stderr.write("Error: Cannot find otf_abfe directory\n")
    sys.exit(1)

"""
Options for writing values of angle, distance, and dihedral to
samplep.cpp.get-vb.in file

Help messages are specified in the description and help variables
"""
def parse_args():
    parser = argparse.ArgumentParser(
        usage = "$0 [options] dir1 dir2 ... dirN" # echo "Usage: $0 [options] dir1 dir2 ... dirN"
    )

    parser.add_argument(
        '-d', '--distance', type = float, default = 2.0,
        help = "distance (default: 2.0)" # echo "  -d, --distance FLOAT     distance (default: 2.0)"
    )
    parser.add_argument(
        '-a', '--angle', type = float, default = 10.0,
        help = "angle (default: 10.0)" # echo "  -a, --angle FLOAT   angle (default: 10.0)"
    )
    parser.add_argument(
        '-D', '--dihedral', type = float, default = 20.0,
        help = "dihedral (default: 20.0)" # echo "  -D, --dihedral FLOAT   dihedral (default: 20.0)"
    )
    parser.add_argument(
        'dirs', nargs = '+',
        help = "Target directories to process" # Directory parameters stored in $@
    )
    return parser.parse_args() # Return parsed flags

"""
Open vbla.txt and vbla2.txt, splits each line on whitespace, and
returns a list of three strings
"""
def read_atoms(file_path):
    with open(file_path) as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                return parts[:3] # Values in myla1, myla2, and myla3
        sys.stderr.write(f"Error: {file_path} has less than 3 fields.\n")
        sys.exit(1)

"""
Main procedure
"""
def main():
    args = parse_args() # Parse flags and store parameters
    mywd = Path.cwd().resolve() # mywd=$(pwd)
    mypcl = find_dir_abfe() # Directory of otf_abfe

    for X in args.dirs: # for X in "$@"
        print(f"=====  {X}  =======================")
        target = Path(X)
        if not target.is_absolute():
            target = mywd / target
        target = target.resolve()
        if not target.is_dir():
            sys.stderr.write(f"Warning: {target} is not a directory, skipping.\n")
            continue # Avoid undefined behaviors and raise error if directory is not found
        os.chdir(target) # cd $X/

        # Create directories
        # mkdir dcrg+vdw, water-dcrg+vdw, rtr
        for sub in ['dcrg+vdw', 'water-dcrg+vdw', 'rtr']:
            (target / sub).mkdir(parents = True, exist_ok = True)

        # Copy input coordinate files
        shutil.copy('complex-repres.rst7', 'complex.inpcrd') # cp complex-repres.rst7 ./complex.inpcrd
        shutil.copy('complex-repres.rst7', target / 'dcrg+vdw' / 'complex.inpcrd') # cp complex-repres.rst7 ./dcrg+vdw/complex.inpcrd
        shutil.copy('complex-repres.rst7', target / 'rtr' / 'complex_prod.inpcrd') # cp complex-repres.rst7 ./rtr/complex_prod.inpcrd

        # Copy topologies
        shutil.copy(target / 'md-complex' / 'complex.prmtop', 'complex.prmtop') # cp md-complex/complex.prmtop ./
        shutil.copy(target / 'md-complex' / 'complex.prmtop', target / 'dcrg+vdw' / 'complex.prmtop') # cp md-complex/complex.prmtop ./dcrg+vdw/
        shutil.copy(target / 'md-complex' / 'complex.prmtop', target / 'rtr' / 'complex.prmtop') # cp md-complex/complex.prmtop ./rtr/

        # Copy all executable files
        shutil.copy(mypcl / 'template.cpp.get-vb.in', target / 'template.cpp.get-vb.in') # cp $mypcl/template.cpp.get-vb.in ./
        for f in (mypcl / 'dcrg+vdw').glob('*.sh'):
            shutil.copy(f, target / 'dcrg+vdw') # cp $mypcl/dcrg+vdw/*sh dcrg+vdw/
        for f in (mypcl / 'rtr').glob('*.sh'):
            shutil.copy(f, target / 'rtr') # cp $mypcl/rtr/*sh rtr/
        for f in (mypcl / 'rtr').glob('*.py'):
            shutil.copy(f, target / 'rtr') # cp $mypcl/rtr/*py rtr/

        # Use names of selected ligand atoms to generate cpp.get-vb.in
        myla1, myla2, myla3 = read_atoms(target / 'vbla.txt') # myla1=$(awk '{print $1}' vbla.txt) ...
        mypa1, mypa2, mypa3 = read_atoms(target / 'vbla2.txt') # mypa1=$(awk '{print $1}' vbla2.txt) ...
        print("\nvbla.txt:") # echo; echo "vbla.txt:"
        print((target / 'vbla.txt').read_text()) # cat vbla.txt;

        # Edit template.cpp.get-vb.in to user inputted angle, distance, dihedral values
        templ_content = f"""parm complex.prmtop
reference complex.inpcrd

rst :MOL@LATOM1 :PROTATOM1 reference width 10.0 rk2 {args.distance} rk3 {args.distance} out k.RST
rst :MOL@LATOM1 :PROTATOM1 :PROTATOM2 reference width 90.0 rk2 {args.angle} rk3 {args.angle} out k.RST
rst :MOL@LATOM1 :PROTATOM1 :PROTATOM2 :PROTATOM3 reference width 90.0 rk2 {args.dihedral} rk3 {args.dihedral} out k.RST
rst :MOL@LATOM2 :MOL@LATOM1 :PROTATOM1 reference width 90.0 rk2 {args.angle} rk3 {args.angle} out k.RST
rst :MOL@LATOM2 :MOL@LATOM1 :PROTATOM1 :PROTATOM2 reference width 90.0 rk2 {args.dihedral} rk3 {args.dihedral} out k.RST
rst :MOL@LATOM3 :MOL@LATOM2 :MOL@LATOM1 :PROTATOM1 reference width 90.0 rk2 {args.dihedral} rk3 {args.dihedral} out k.RST

run
"""
        (target / 'template.cpp.get-vb.in').write_text(templ_content) # cat <<EOF > template.cpp.get-vb.in ... EOF
        
        # Write to cpp.get-vb.in
        cpp_content = templ_content.replace('LATOM1', myla1) # sed "s/LATOM1/$myla1/" template.cpp.get-vb.in > cpp.get-vb.in
        cpp_content = cpp_content.replace('LATOM2', myla2) # sed -i "s/LATOM2/$myla2/" cpp.get-vb.in
        cpp_content = cpp_content.replace('LATOM3', myla3) # sed -i "s/LATOM3/$myla3/" cpp.get-vb.in
        cpp_content = cpp_content.replace('PROTATOM1', mypa1) # sed -i "s/PROTATOM1/$mypa1/" cpp.get-vb.in
        cpp_content = cpp_content.replace('PROTATOM2', mypa2) # sed -i "s/PROTATOM2/$mypa2/" cpp.get-vb.in
        cpp_content = cpp_content.replace('PROTATOM3', mypa3) # sed -i "s/PROTATOM3/$mypa3/" cpp.get-vb.in
        (target / 'cpp.get-vb.in').write_text(cpp_content) # Write to cpp.get-vb.in

        print("\ncpp.get-vb.txt:") # echo; echo "cpp.get-vb.txt:"
        print(cpp_content) # cat cpp.get-vb.in;

        # Create protein-ligand restraints
        with open('std.get-vb.txt', 'w') as stdout_file:
            subprocess.run(['cpptraj', '-i', 'cpp.get-vb.in'], stdout=stdout_file) # cpptraj -i cpp.get-vb.in > std.get-vb.txt
        print("PROTEIN-LIGAND RESTRAINTS:") # cpptraj -i cpp.get-vb.in > std.get-vb.txt
        subprocess.run(['grep', 'rk2', 'k.RST']) # grep r2 k.RST
        shutil.copy('k.RST', target / 'dcrg+vdw') # cp k.RST dcrg+vdw/
        shutil.copy('k.RST', target / 'rtr') # cp k.RST rtr/

        # Copy water files
        shutil.copy(target / 'setup' / 'ligwat.inpcrd', target / 'water-dcrg+vdw' / 'ligwat.inpcrd') # cp setup/ligwat.inpcrd ./water-dcrg+vdw/
        # Copy all executable files
        for f in (mypcl / 'water-dcrg+vdw').glob('*.sh'):
            shutil.copy(f, target / 'water-dcrg+vdw') # cp $mypcl/water-dcrg+vdw/*sh water-dcrg+vdw/
        shutil.copy(target / 'setup' / 'ligwat.prmtop', target / 'water-dcrg+vdw' / 'ligwat.prmtop') # cp setup/ligwat.prmtop ./water-dcrg+vdw/

        os.chdir(mywd) # cd $mywd

if __name__ == '__main__':
    main()
